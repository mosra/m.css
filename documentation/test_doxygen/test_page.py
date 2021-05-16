#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020 Vladimír Vondruš <mosra@centrum.cz>
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
import unittest

from distutils.version import LooseVersion

from . import IntegrationTestCase, doxygen_version

class Order(IntegrationTestCase):
    def test(self):
        self.run_doxygen(index_pages=['pages'], wildcard='index.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class Brief(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/624")
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))
        self.assertEqual(*self.actual_expected_contents('page-a.html'))
        self.assertEqual(*self.actual_expected_contents('page-b.html'))

class Toc(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/625")
    def test(self):
        self.run_doxygen(wildcard='page-toc.xml')
        self.assertEqual(*self.actual_expected_contents('page-toc.html'))

class InNavbar(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='page*.xml')
        self.assertEqual(*self.actual_expected_contents('page-in-navbar.html'))
        self.assertEqual(*self.actual_expected_contents('page-b.html'))

class FooterNavigation(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='subpage*.xml')
        self.assertEqual(*self.actual_expected_contents('subpage1.html'))
        self.assertEqual(*self.actual_expected_contents('subpage2.html'))

class EmptyIndex(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class EmptyTitle(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='untitled.xml')
        self.assertEqual(*self.actual_expected_contents('untitled.html'))

class SubpageOfIndex(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class EmptyPage(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'group__bla_md_input.html')))
        self.assertFalse(os.path.exists(os.path.join(self.path, 'html', 'md_subdir_otherinput.html')))
        self.assertEqual(*self.actual_expected_contents('pages.html'))
