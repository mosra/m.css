#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
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

from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes
from docutils import nodes

class FancyLine(rst.Directive):
    final_argument_whitespace = True
    has_content = False
    required_arguments = 1

    def run(self):
        text = '~~~ {} ~~~'.format(self.arguments[0])
        title_nodes, _ = self.state.inline_text(text, self.lineno)
        node = nodes.paragraph('', '', *title_nodes)
        node['classes'] += ['m-transition']
        return [node]

pre_page_call_count = 0
post_run_call_count = 0

def _pre_page():
    global pre_page_call_count
    pre_page_call_count = pre_page_call_count + 1

def _post_run():
    global post_run_call_count
    post_run_call_count = post_run_call_count + 1

def register_mcss(hooks_pre_page, hooks_post_run, **kwargs):
    hooks_pre_page += [_pre_page]
    hooks_post_run += [_post_run]

    rst.directives.register_directive('fancy-line', FancyLine)
