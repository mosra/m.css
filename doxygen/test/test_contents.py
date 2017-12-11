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

import os
import shutil
import unittest

from distutils.version import LooseVersion

from test import IntegrationTestCase, doxygen_version

class Typography(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'typography', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Blocks(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'blocks', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_xrefpages(self):
        self.run_dox2html5(wildcard='todo.xml')
        self.assertEqual(*self.actual_expected_contents('todo.html'))

class Code(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'code', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class CodeLanguage(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'code_language', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/621")
    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/623")
    def test_ansi(self):
        self.run_dox2html5(wildcard='ansi.xml')
        self.assertEqual(*self.actual_expected_contents('ansi.html'))

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/621")
    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Image(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'image', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'tiny.png')))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Math(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'math', *args, **kwargs)

    @unittest.skipUnless(shutil.which('latex'),
                         "Math rendering requires LaTeX installed")
    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class Tagfile(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'tagfile', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
