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

import copy
import math
import os
import sys
import unittest

from distutils.version import LooseVersion

from python import default_templates
from . import BaseInspectTestCase

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../plugins'))
import m.sphinx

class String(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'LINKS_NAVBAR1': [
                ('Modules', 'modules', []),
                ('Classes', 'classes', [])],
        })
        self.assertEqual(*self.actual_expected_contents('inspect_string.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.another_module.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.FooSlots.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.DerivedException.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.Specials.html'))

        self.assertEqual(*self.actual_expected_contents('classes.html'))
        self.assertEqual(*self.actual_expected_contents('modules.html'))

class Object(BaseInspectTestCase):
    def test(self):
        # Reuse the stuff from inspect_string, but this time reference it via
        # an object and not a string
        sys.path.append(os.path.join(os.path.dirname(self.path), 'inspect_string'))
        import inspect_string
        self.run_python({
            'LINKS_NAVBAR1': [
                ('Modules', 'modules', []),
                ('Classes', 'classes', [])],
            'INPUT_MODULES': [inspect_string]
        })

        # The output should be the same as when inspecting a string
        self.assertEqual(*self.actual_expected_contents('inspect_string.html', '../inspect_string/inspect_string.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.another_module.html', '../inspect_string/inspect_string.another_module.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.Foo.html', '../inspect_string/inspect_string.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.FooSlots.html', '../inspect_string/inspect_string.FooSlots.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.DerivedException.html', '../inspect_string/inspect_string.DerivedException.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_string.Specials.html', '../inspect_string/inspect_string.Specials.html'))

        self.assertEqual(*self.actual_expected_contents('classes.html', '../inspect_string/classes.html'))
        self.assertEqual(*self.actual_expected_contents('modules.html', '../inspect_string/modules.html'))

class AllProperty(BaseInspectTestCase):
    def test(self):
        self.run_python()
        self.assertEqual(*self.actual_expected_contents('inspect_all_property.html'))

class Annotations(BaseInspectTestCase):
    def test(self):
        self.run_python()
        if LooseVersion(sys.version) >= LooseVersion('3.7.0') and LooseVersion(sys.version) < LooseVersion('3.9.0'):
            self.assertEqual(*self.actual_expected_contents('inspect_annotations.html', 'inspect_annotations-py37+38.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('inspect_annotations.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_annotations.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_annotations.FooSlots.html'))

        # This should not list any internal stuff from the typing module. The
        # Generic.__new__() is gone in 3.9: https://bugs.python.org/issue39168
        if LooseVersion(sys.version) >= LooseVersion('3.9.0'):
            self.assertEqual(*self.actual_expected_contents('inspect_annotations.AContainer.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('inspect_annotations.AContainer.html', 'inspect_annotations.AContainer-py36-38.html'))

    # https://github.com/python/cpython/pull/13394
    @unittest.skipUnless(LooseVersion(sys.version) >= LooseVersion('3.7.4'),
        "signature with / for pow() is not present in 3.6, "
        "3.7.3 and below has a different docstring")
    def test_math(self):
        # From math export only pow() so we have the verification easier, and
        # in addition log() because it doesn't provide any signature metadata
        assert not hasattr(math, '__all__')
        math.__all__ = ['pow', 'log']

        self.run_python({
            'INPUT_MODULES': [math]
        })

        del math.__all__
        assert not hasattr(math, '__all__')

        self.assertEqual(*self.actual_expected_contents('math.html'))

    # https://github.com/python/cpython/pull/13394
    @unittest.skipUnless(LooseVersion(sys.version) < LooseVersion('3.7.4') and LooseVersion(sys.version) >= LooseVersion('3.7'),
        "signature with / for pow() is not present in 3.6, "
        "3.7.3 and below has a different docstring")
    def test_math373(self):
        # From math export only pow() so we have the verification easier, and
        # in addition log() because it doesn't provide any signature metadata
        assert not hasattr(math, '__all__')
        math.__all__ = ['pow', 'log']

        self.run_python({
            'INPUT_MODULES': [math]
        })

        del math.__all__
        assert not hasattr(math, '__all__')

        self.assertEqual(*self.actual_expected_contents('math.html', 'math373.html'))

    @unittest.skipUnless(LooseVersion(sys.version) < LooseVersion('3.7'),
        "docstring for log() is different in 3.7")
    def test_math36(self):
        # From math export only pow() so we have the verification easier, and
        # in addition log() because it doesn't provide any signature metadata
        assert not hasattr(math, '__all__')
        math.__all__ = ['log']

        self.run_python({
            'INPUT_MODULES': [math]
        })

        del math.__all__
        assert not hasattr(math, '__all__')

        self.assertEqual(*self.actual_expected_contents('math.html', 'math36.html'))

class NameMapping(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'NAME_MAPPING': {
                'inspect_name_mapping._sub.bar._NameThatGetsOverridenExternally': 'yay.ThisGotOverridenExternally'
            }
        })
        self.assertEqual(*self.actual_expected_contents('inspect_name_mapping.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_name_mapping.Class.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_name_mapping.submodule.html'))

class Recursive(BaseInspectTestCase):
    def test(self):
        self.run_python()
        self.assertEqual(*self.actual_expected_contents('inspect_recursive.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_recursive.first.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_recursive.a.html'))

class TypeLinks(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'INPUT_PAGES': ['index.rst'],
            'M_SPHINX_INVENTORIES': [
                ('../../../doc/documentation/python.inv', 'https://docs.python.org/3/', [], ['m-doc-external'])]
        })

        self.assertEqual(*self.actual_expected_contents('index.html'))

        self.assertEqual(*self.actual_expected_contents('inspect_type_links.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.first.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.first.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.first.Foo.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.first.sub.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.first.sub.Foo.html'))

        self.assertEqual(*self.actual_expected_contents('inspect_type_links.second.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.second.Foo.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.second.FooSlots.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_type_links.second.FooSlotsInvalid.html'))

class CreateIntersphinx(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_PAGES': ['page.rst'],
            'M_SPHINX_INVENTORIES': [
                # Nothing from here should be added to the output
                ('../../../doc/documentation/python.inv', 'https://docs.python.org/3/', [], ['m-doc-external'])],
            'M_SPHINX_INVENTORY_OUTPUT': 'things.inv',
            'PYBIND11_COMPATIBILITY': True
        })

        with open(os.path.join(self.path, 'output/things.inv'), 'rb') as f:
            self.assertEqual(m.sphinx.pretty_print_intersphinx_inventory(f), """
# Sphinx inventory version 2
# Project: X
# Version: 0
# The remainder of this file is compressed using zlib.
inspect_create_intersphinx.Class.a_property py:attribute 2 inspect_create_intersphinx.Class.html#a_property -
inspect_create_intersphinx.Class py:class 2 inspect_create_intersphinx.Class.html -
inspect_create_intersphinx.Class.CLASS_DATA py:data 2 inspect_create_intersphinx.Class.html#CLASS_DATA -
inspect_create_intersphinx.MODULE_DATA py:data 2 inspect_create_intersphinx.html#MODULE_DATA -
inspect_create_intersphinx.Enum py:enum 2 inspect_create_intersphinx.html#Enum -
inspect_create_intersphinx.Enum.ENUM_VALUE py:enumvalue 2 inspect_create_intersphinx.html#Enum-ENUM_VALUE -
inspect_create_intersphinx.Class.class_method py:function 2 inspect_create_intersphinx.Class.html#class_method -
inspect_create_intersphinx.Class.method py:function 2 inspect_create_intersphinx.Class.html#method -
inspect_create_intersphinx.Class.static_method py:function 2 inspect_create_intersphinx.Class.html#static_method -
inspect_create_intersphinx.function py:function 2 inspect_create_intersphinx.html#function -
inspect_create_intersphinx.pybind.overloaded_function py:function 2 inspect_create_intersphinx.pybind.html#overloaded_function -
inspect_create_intersphinx py:module 2 inspect_create_intersphinx.html -
inspect_create_intersphinx.pybind py:module 2 inspect_create_intersphinx.pybind.html -
page std:doc 2 page.html -
index std:special 2 index.html -
modules std:special 2 modules.html -
classes std:special 2 classes.html -
pages std:special 2 pages.html -
""".lstrip())
        # Yes, above it should say A documentation page, but it doesn't

try:
    import attr
except ImportError:
    attr = None
class Attrs(BaseInspectTestCase):
    @unittest.skipUnless(attr, "the attr package was not found")
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'ATTRS_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('inspect_attrs.MyClass.html'))
        if attr.__version_info__ >= (20, 1):
            self.assertEqual(*self.actual_expected_contents('inspect_attrs.MyClassAutoAttribs.html'))
            self.assertEqual(*self.actual_expected_contents('inspect_attrs.MySlotClass.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('inspect_attrs.MyClassAutoAttribs.html', 'inspect_attrs.MyClassAutoAttribs-attrs193.html'))
            self.assertEqual(*self.actual_expected_contents('inspect_attrs.MySlotClass.html', 'inspect_attrs.MySlotClass-attrs193.html'))

class Underscored(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'M_SPHINX_PARSE_DOCSTRINGS': True
        })

        self.assertEqual(*self.actual_expected_contents('inspect_underscored.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_underscored.Class.html'))

class ValueFormatting(BaseInspectTestCase):
    def test(self):
        self.run_python({})
        self.assertEqual(*self.actual_expected_contents('inspect_value_formatting.html'))

class DuplicateClass(BaseInspectTestCase):
    def test(self):
        self.run_python({})
        self.assertEqual(*self.actual_expected_contents('inspect_duplicate_class.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_duplicate_class.sub.html'))
        self.assertEqual(*self.actual_expected_contents('inspect_duplicate_class.Bar.html'))
