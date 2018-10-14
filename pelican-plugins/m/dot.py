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

import dot2svg

class Dot(rst.Directive):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {'class': directives.class_option,
                   'name': directives.unchanged}

    def run(self, source):
        set_classes(self.options)

        svg = dot2svg.dot2svg(source)

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
    dot2svg.configure(
        pelicanobj.settings.get('M_DOT_FONT', 'Source Sans Pro'),
        pelicanobj.settings.get('M_DOT_FONT_SIZE', 16.0))

def register():
    pelican.signals.initialized.connect(configure)
    rst.directives.register_directive('digraph', Digraph)
    rst.directives.register_directive('strict-digraph', StrictDigraph)
    rst.directives.register_directive('graph', Graph)
    rst.directives.register_directive('strict-graph', StrictGraph)
