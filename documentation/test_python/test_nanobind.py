#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
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
import sys
import unittest

from python import State, parse_pybind_signature, default_config

from . import BaseInspectTestCase

class Signatures(BaseInspectTestCase):
    def test(self):
        sys.path.append(self.path)
        import pybind_signatures
        self.run_python({
            # TODO false_positives ???
            'INPUT_MODULES': [pybind_signatures],
            'PYBIND11_COMPATIBILITY': True, # TODO don't rely on this
            'NANOBIND_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_signatures.html', '../pybind_signatures/pybind_signatures.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_signatures.MyClass.html', '../pybind_signatures/pybind_signatures.MyClass.html'))
        # TODO ??
        # self.assertEqual(*self.actual_expected_contents('false_positives.html'))
