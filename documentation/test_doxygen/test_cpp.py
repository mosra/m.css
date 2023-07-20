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

import unittest

from distutils.version import LooseVersion

from . import IntegrationTestCase, doxygen_version

class EnumClass(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/627")
    def test(self):
        self.run_doxygen(wildcard='File_8h.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class TemplateAlias(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/626")
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(*self.actual_expected_contents('structTemplate.html'))

class Derived(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('classNamespace_1_1A.html'))
        self.assertEqual(*self.actual_expected_contents('classNamespace_1_1PrivateBase.html'))
        self.assertEqual(*self.actual_expected_contents('classAnother_1_1ProtectedBase.html'))
        self.assertEqual(*self.actual_expected_contents('classNamespace_1_1VirtualBase.html'))
        self.assertEqual(*self.actual_expected_contents('classBaseOutsideANamespace.html'))
        self.assertEqual(*self.actual_expected_contents('classDerivedOutsideANamespace.html'))
        self.assertEqual(*self.actual_expected_contents('structAnother_1_1Final.html'))
        # For the final label in the tree
        self.assertEqual(*self.actual_expected_contents('annotated.html'))

class Friends(IntegrationTestCase):
    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "1.8.13 produces invalid XML for friend declarations")
    def test(self):
        self.run_doxygen(wildcard='class*.xml')
        self.assertEqual(*self.actual_expected_contents('classClass.html'))
        self.assertEqual(*self.actual_expected_contents('classTemplate.html'))

    def test_warnings(self):
        with self.assertLogs() as cm:
            self.run_doxygen(wildcard='structWarning.xml')
        self.assertEqual(*self.actual_expected_contents('structWarning.html'))
        self.assertEqual(cm.output, [
            "WARNING:root:structWarning.xml: doxygen is unable to cross-link friend class GroupedFriendClassWarning, ignoring, sorry",
            "WARNING:root:structWarning.xml: doxygen is unable to cross-link friend class FriendClassWarning, ignoring, sorry"
        ])

class SignalsSlots(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='classClass.xml')
        self.assertEqual(*self.actual_expected_contents('classClass.html'))

class VariableTemplate(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('structFoo.html'))
        self.assertEqual(*self.actual_expected_contents('structBar.html'))

class FunctionAttributes(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('structFoo.html'))
        self.assertEqual(*self.actual_expected_contents('classBase.html'))
        self.assertEqual(*self.actual_expected_contents('classDerived.html'))
        self.assertEqual(*self.actual_expected_contents('structFinal.html'))

class FunctionAttributesNospace(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='structFoo.xml')
        self.assertEqual(*self.actual_expected_contents('structFoo.html'))

class MishandledMacroCall(IntegrationTestCase):
    def test(self):
        with self.assertLogs() as cm:
            self.run_doxygen(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(cm.output, [
            "WARNING:root:File_8h.xml: parameter $ of function DEFINE_FUNCTION has no type, ignoring the whole function as it's suspected to be a mishandled macro call"
        ])
