#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
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
import sys
import unittest

from . import BaseInspectTestCase

from _search import pretty_print, searchdata_filename
from python import EntryType

class CustomHeaderExtension(BaseInspectTestCase):
    def test(self):
        self.run_python_stubs({
            'STUB_HEADER': '#!/usr/bin/env python3\n\n# This is a custom header containing no trailing newline on its own.',
            'STUB_EXTENSION': '.custom.py'
        })

        # The stubs/ directory is implicitly prepended only for *.pyi files to
        # make testing against the input itself possible, so here I have to do
        # it manually.
        self.assertEqual(*self.actual_expected_contents('stubs_custom_header_extension/__init__.custom.py', 'stubs/stubs_custom_header_extension/__init__.custom.py'))
        self.assertEqual(*self.actual_expected_contents('stubs_custom_header_extension/sub.custom.py', 'stubs/stubs_custom_header_extension/__init__.custom.py'))

class ModuleDependencies(BaseInspectTestCase):
    def test(self):
        sys.path.append(self.path)
        self.run_python_stubs({
            # unparsed_module explicitly not included
            'INPUT_MODULES': ['stubs_module_dependencies', 'stubs_module_dependencies.sub', 'stubs_module_dependencies.sub.inner', 'another_module'],
            'PYBIND11_COMPATIBILITY': True,
            # So it looks like a regular Python file so I can verify the
            # imports (KDevelop doesn't look for .pyi for imports)
            'STUB_EXTENSION': '.py'
        })

        # The stubs/ directory is implicitly prepended only for *.pyi files to
        # make testing against the input itself possible, so here I have to do
        # it manually.
        self.assertEqual(*self.actual_expected_contents('stubs_module_dependencies/__init__.py', 'stubs/stubs_module_dependencies/__init__.py'))
        self.assertEqual(*self.actual_expected_contents('stubs_module_dependencies/sub/inner.py', 'stubs/stubs_module_dependencies/sub/inner.py'))

class NestedClasses(BaseInspectTestCase):
    def test(self):
        self.run_python_stubs({
            'STUB_EXTENSION': '.py'
        })

        # The output should be the same as the input, yes
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.py'))

    def test_html(self):
        self.run_python()

        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.Inner.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.InnerAnother.AndAnother.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.InnerAnother.AndAnother.YetAnother.html'))

    def test_both(self):
        self.run_python({
            'OUTPUT_STUBS': os.path.join(self.path, 'output'),
            'STUB_HEADER': '',
            'STUB_EXTENSION': '.py'
        })

        # There shouldn't be any difference compared to running these separately
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.py'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.Inner.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.InnerAnother.AndAnother.html'))
        self.assertEqual(*self.actual_expected_contents('stubs_nested_classes.Class.InnerAnother.AndAnother.YetAnother.html'))

class Spacing(BaseInspectTestCase):
    def test(self):
        self.run_python_stubs({
            'STUB_HEADER': '# This file is both an input and output, i.e. the generated stub should have\n# exactly the same spacing as the input.',
            'STUB_EXTENSION': '.py'
        })

        # The output should be the same as the input, yes
        # TODO make classmethod accept cls instead of *args once it's fixed
        self.assertEqual(*self.actual_expected_contents('stubs_spacing.py'))

    def test_empty_module(self):
        sys.path.append(self.path)
        self.run_python_stubs({
            'INPUT_MODULES': ['empty_module'],
            'STUB_EXTENSION': '.py'
        })

        # The output should be the same as the input, yes
        self.assertEqual(*self.actual_expected_contents('empty_module.py'))
