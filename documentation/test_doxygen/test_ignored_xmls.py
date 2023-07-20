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

from . import BaseTestCase

class IgnoredXmls(BaseTestCase):
    def test(self):
        with self.assertLogs() as cm:
            self.run_doxygen(wildcard='*.xml')

        self.assertEqual(cm.output, [
            # The Doxyfile.xml should be completely ignored, producing just a
            # debug message and not even being opened, as that would spam the
            # output otherwise

            # This is like Doxyfile.xml, but with a different name, ensure it
            # gets properly skipped if the root element mismatches
            "WARNING:root:Foxydile.xml: root element expected to be <doxygen> but is <doxyfile>, skipping whole file",

            # A file that has a XML parse error should get skipped
            "ERROR:root:broken.xml: XML parse error, skipping whole file: not well-formed (invalid token): line 1, column 1",

            # The index.xml should be parsed and not produce any warning

            # A file that has <doxygen> but something weird inside, skipped
            # also
            "WARNING:root:thingsgotcrazy.xml: first child element expected to be <compounddef> but is <crazyisay>, skipping whole file"
        ])

        # Some index page should be generated, with version 1.0.666 extracted
        # from index.xml
        self.assertEqual(*self.actual_expected_contents('pages.html'))
