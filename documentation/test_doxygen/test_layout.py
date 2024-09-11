#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023
#             Vladimír Vondruš <mosra@centrum.cz>
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

from _search import search_filename, searchdata_filename, searchdata_filename_b85
from . import BaseTestCase

class Layout(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='index.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'm-dark+documentation.compiled.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', search_filename)))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', searchdata_filename_b85.format(search_filename_prefix='searchdata'))))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'favicon-light.png')))

class GeneratedDoxyfile(BaseTestCase):
    def test(self):
        if os.path.exists(os.path.join(self.path, 'Doxyfile')):
            os.remove(os.path.join(self.path, 'Doxyfile'))

        subprocess.run(['doxygen', '-g'], cwd=self.path)
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class Minimal(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class TemplateFallback(BaseTestCase):
    def test(self):
        self.run_doxygen(templates=self.path, wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NavbarSingleColumn(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NavbarHtml(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NavbarMainProjectUrl(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NavbarProjectLogo(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NavbarProjectLogoMainProjectUrl(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class SearchBinary(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', searchdata_filename.format(search_filename_prefix='searchdata'))))

class SearchOpensearch(BaseTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        # Renamed with a HTML extension so doxygen.py's metadata parser doesn't
        # pick it up
        self.assertEqual(*self.actual_expected_contents('opensearch.xml', 'opensearch.xml.html'))
