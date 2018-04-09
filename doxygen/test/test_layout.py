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

import os
import subprocess

from test import BaseTestCase

class Layout(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='index.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'm-dark+doxygen.compiled.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'search.js')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'searchdata.js')))

class LayoutGeneratedDoxyfile(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'generated_doxyfile', *args, **kwargs)

    def test(self):
        if os.path.exists(os.path.join(self.path, 'Doxyfile')):
            os.remove(os.path.join(self.path, 'Doxyfile'))

        subprocess.run(['doxygen', '-g'], cwd=self.path)
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class LayoutMinimal(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'minimal', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class LayoutNavbarSingleColumn(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'navbar_single_column', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class LayoutSearchBinary(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'search_binary', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'searchdata.bin')))
