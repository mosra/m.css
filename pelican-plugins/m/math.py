# -*- coding: utf-8 -*-
#
#   This file is part of m.css.
#
#   Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

import re

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes

import pelican.signals

from . import latex2svg

latex2svg_params = latex2svg.default_params.copy()
latex2svg_params.update({
    # Don't use libertine fonts as they mess up things
    'preamble': r"""
\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{newtxtext}
""",
    # Zoom the letters a bit to match page font size
    'dvisvgm_cmd': 'dvisvgm --no-fonts -Z 1.25',
    })

patch_src = re.compile(r"""<\?xml version='1.0' encoding='UTF-8'\?>
<!-- This file was generated by dvisvgm \d+\.\d+\.\d+ -->
<svg (?P<attribs>.+) xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>
""")

patch_dst = r"""<svg{attribs} \g<attribs>>
<title>LaTeX Math</title>
<desc>
{formula}
</desc>
"""

unique_src = re.compile(r"""(?P<name> id|xlink:href)='(?P<ref>#?)(?P<id>g\d+-\d+|page\d+)'""")
unique_dst = r"""\g<name>='\g<ref>eq{counter}-\g<id>'"""

counter = 0

def _patch(formula, out, attribs):
    global counter
    counter += 1
    return unique_src.sub(unique_dst.format(counter=counter), patch_src.sub(patch_dst.format(attribs=attribs, formula=formula.replace('\\', '\\\\')), out['svg']))

class Math(rst.Directive):
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}
    has_content = True

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        # join lines, separate blocks
        content = '\n'.join(self.content).split('\n\n')
        _nodes = []
        for block in content:
            if not block:
                continue

            out = latex2svg.latex2svg("$$" + block + "$$", params=latex2svg_params)

            container = nodes.container(**self.options)
            container['classes'] += ['m-math']
            node = nodes.raw(self.block_text, _patch(block, out, ''), format='html')
            node.line = self.content_offset + 1
            self.add_name(node)
            container.append(node)
            _nodes.append(container)
        return _nodes

def new_page(content):
    global counter
    counter = 0

def math(role, rawtext, text, lineno, inliner, options={}, content=[]):
    # Otherwise the backslashes do quite a mess there
    i = rawtext.find('`')
    text = rawtext.split('`')[1]

    # Apply classes to the <svg> element instead of some outer <span>
    set_classes(options)
    classes = 'm-math'
    if 'classes' in options:
        classes += ' ' + ' '.join(options['classes'])
        del options['classes']

    out = latex2svg.latex2svg("$" + text + "$", params=latex2svg_params)

    # CSS classes and styling for proper vertical alignment. Depth is relative
    # to font size, describes how below the line the text is. Scaling it back
    # to 12pt font, scaled by 125% as set above in the config.
    attribs = ' class="{}" style="vertical-align: -{:.1f}pt;"'.format(classes, out['depth']*12*1.25)

    node = nodes.raw(rawtext, _patch(text, out, attribs), format='html', **options)
    return [node], []

def register():
    pelican.signals.content_object_init.connect(new_page)
    rst.directives.register_directive('math', Math)
    rst.roles.register_canonical_role('math', math)
