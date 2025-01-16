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

import pygments
import unittest

from . import IntegrationTestCase, doxygen_version, parse_version

class Example(IntegrationTestCase):
    def test_cpp(self):
        self.run_doxygen(index_pages=[], wildcard='*.xml')

        self.assertEqual(*self.actual_expected_contents('path-prefix_2configure_8h_8cmake-example.html'))
        # Pygments 2.10+ properly highlight Whitespace as such, and not as
        # Text
        if parse_version(pygments.__version__) >= parse_version("2.10"):
            self.assertEqual(*self.actual_expected_contents('path-prefix_2main_8cpp-example.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('path-prefix_2main_8cpp-example.html', 'path-prefix_2main_8cpp-example-pygments29.html'))

    @unittest.skipUnless(parse_version(doxygen_version()) > parse_version("1.8.13"),
                         "needs to have file extension exposed in the XML")
    def test_other(self):
        self.run_doxygen(index_pages=[], wildcard='*.xml')

        # Pygments 2.10+ properly highlight Whitespace as such, and not as
        # Text. Compared to elsewhere, in this case the difference is only with
        # 2.11+.
        if parse_version(pygments.__version__) >= parse_version("2.11"):
            self.assertEqual(*self.actual_expected_contents('path-prefix_2CMakeLists_8txt-example.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('path-prefix_2CMakeLists_8txt-example.html', 'path-prefix_2CMakeLists_8txt-example-pygments210.html'))
        self.assertEqual(*self.actual_expected_contents('a_8txt-example.html'))
