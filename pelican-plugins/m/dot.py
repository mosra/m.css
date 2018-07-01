#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
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

import pelican
import re
import subprocess

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes

_patch_src = re.compile(r"""<\?xml version="1\.0" encoding="UTF-8" standalone="no"\?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1\.1//EN"
 "http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd">
<svg width="(?P<width>\d+)pt" height="(?P<height>\d+)pt"
 viewBox="(?P<viewBox>[^"]+)" xmlns="http://www\.w3\.org/2000/svg" xmlns:xlink="http://www\.w3\.org/1999/xlink">
<g id="graph0" class="graph" """)

_patch_dst = r"""<svg style="width: {width:.3f}rem; height: {height:.3f}rem;" viewBox="{viewBox}">
<g """

_comment_src = re.compile(r"""<!--[^-]+-->\n""")

_class_src = re.compile(r"""<g id="(edge|node)\d+" class="(?P<type>edge|node)(?P<classes>[^"]*)">
<title>(?P<title>[^<]*)</title>
<(?P<element>ellipse|polygon|path) fill="(?P<fill>[^"]+)" stroke="[^"]+" """)

_class_dst = r"""<g class="{classes}">
<title>{title}</title>
<{element} """

_attributes_src = re.compile(r"""<(?P<element>ellipse|polygon) fill="[^"]+" stroke="[^"]+" """)

_attributes_dst = r"""<\g<element> """

# re.compile() is called after replacing {font} in configure()
_text_src_src = ' font-family="{font}" font-size="(?P<size>[^"]+)" fill="[^"]+"'

_text_dst = ' style="font-size: {size}px;"'

_font = ''
_font_size = 0.0

# The pt are actually px (16pt font is the same size as 16px), so just
# converting to rem here
def _pt2em(pt): return pt/_font_size

class Dot(rst.Directive):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}

    def run(self, source):
        set_classes(self.options)

        title_text = self.arguments[0]

        try:
            ret = subprocess.run(['dot', '-Tsvg',
                '-Gfontname={}'.format(_font),
                '-Nfontname={}'.format(_font),
                '-Efontname={}'.format(_font),
                '-Gfontsize={}'.format(_font_size),
                '-Nfontsize={}'.format(_font_size),
                '-Efontsize={}'.format(_font_size),
                '-Gbgcolor=transparent',
                ], input=source.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if ret.returncode: print(ret.stderr.decode('utf-8'))
            ret.check_returncode()
        except FileNotFoundError: # pragma: no cover
            raise RuntimeError("dot not found")

        # First Remove comments
        svg = _comment_src.sub('', ret.stdout.decode('utf-8'))

        # Remove preamble and fixed size
        def patch_repl(match): return _patch_dst.format(
            width=_pt2em(float(match.group('width'))),
            height=_pt2em(float(match.group('height'))),
            viewBox=match.group('viewBox'))
        svg = _patch_src.sub(patch_repl, svg)

        # Remove unnecessary IDs and attributes, replace classes for elements
        def element_repl(match):
            classes = ['m-' + match.group('type')] + match.group('classes').replace('&#45;', '-').split()
            # distinguish between solid and filled nodes
            if match.group('type') == 'node' and match.group('fill') == 'none':
                classes += ['m-flat']

            return _class_dst.format(
                classes=' '.join(classes),
                title=match.group('title'),
                element=match.group('element'))
        svg = _class_src.sub(element_repl, svg)

        # Remove unnecessary fill and stroke attributes
        svg = _attributes_src.sub(_attributes_dst, svg)

        # Remove unnecessary text attributes. Keep font size only if nondefault
        def text_repl(match):
            if float(match.group('size')) != _font_size:
                return _text_dst.format(size=float(match.group('size')))
            return ''
        svg = _text_src.sub(text_repl, svg)

        container = nodes.container(**self.options)
        container['classes'] = ['m-graph'] + container['classes']
        node = nodes.raw('', svg, format='html')
        container.append(node)
        return [container]

class Digraph(Dot):
    def run(self):
        return Dot.run(self, 'digraph "{}" {{\n{}}}'.format(self.arguments[0], '\n'.join(self.content)))

class StrictDigraph(Dot):
    def run(self):
        return Dot.run(self, 'strict digraph "{}" {{\n{}}}'.format(self.arguments[0], '\n'.join(self.content)))

class Graph(Dot):
    def run(self):
        return Dot.run(self, 'graph "{}" {{\n{}}}'.format(self.arguments[0], '\n'.join(self.content)))

class StrictGraph(Dot):
    def run(self):
        return Dot.run(self, 'strict graph "{}" {{\n{}}}'.format(self.arguments[0], '\n'.join(self.content)))

def configure(pelicanobj):
    global _font, _font_size, _text_src
    _font = pelicanobj.settings.get('M_DOT_FONT', 'Source Sans Pro')
    _font_size = pelicanobj.settings.get('M_DOT_FONT_SIZE', 16.0)
    _text_src = re.compile(_text_src_src.format(font=_font))

def register():
    pelican.signals.initialized.connect(configure)
    rst.directives.register_directive('digraph', Digraph)
    rst.directives.register_directive('strict-digraph', StrictDigraph)
    rst.directives.register_directive('graph', Graph)
    rst.directives.register_directive('strict-graph', StrictGraph)
