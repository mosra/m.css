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

import unittest

from dox2html5 import parse_doxyfile, State

class Doxyfile(unittest.TestCase):
    def test(self):
        state = State()
        parse_doxyfile(state, 'test/doxyfile/Doxyfile')
        self.assertEqual(state.doxyfile, {
            'HTML_EXTRA_FILES': ['css', 'another.png', 'hello'],
            'HTML_EXTRA_STYLESHEET': ['a.css', 'b.css'],
            'HTML_OUTPUT': 'html',
            'M_CLASS_TREE_EXPAND_LEVELS': 1,
            'M_EXPAND_INNER_TYPES': False,
            'M_FILE_TREE_EXPAND_LEVELS': 1,
            'M_PAGE_FINE_PRINT': 'this is "quotes"',
            'M_PAGE_HEADER': 'this is "quotes" \'apostrophes\'',
            'M_SHOW_DOXYGEN_VERSION': True,
            'M_THEME_COLOR': '#22272e',
            'OUTPUT_DIRECTORY': '',
            'PROJECT_BRIEF': 'is cool',
            'PROJECT_NAME': 'My Pet Project',
            'XML_OUTPUT': 'xml'
        })
