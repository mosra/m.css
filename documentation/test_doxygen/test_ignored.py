#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025
#             Vladimír Vondruš <mosra@centrum.cz>
#   Copyright © 2022 crf8472 <crf8472@web.de>
#   Copyright © 2022 SRGDamia1 <sdamiano@stroudcenter.org>
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

from . import BaseTestCase, IntegrationTestCase, doxygen_version, parse_version

class Xmls(BaseTestCase):
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

class Languages(IntegrationTestCase):
    def test(self):
        with self.assertLogs() as cm:
            self.run_doxygen(index_pages=[], wildcard='*.xml')

        expected = [
            'WARNING:root:file_8cs.xml: unsupported language C#, skipping whole file',
            'WARNING:root:file_8java.xml: unsupported language Java, skipping whole file',
            'WARNING:root:file_8py.xml: unsupported language Python, skipping whole file',
            'WARNING:root:namespacefile.xml: unsupported language Python, skipping whole file'
        ]
        # Doxygen 1.9.3 (?) generates one more strange file for Java
        if parse_version(doxygen_version()) >= parse_version("1.9.3"):
            expected += ['WARNING:root:namespacejava_1_1lang.xml: unsupported language Java, skipping whole file']
        self.assertEqual(cm.output, expected)

        # C files shouldn't be ignored. Testing explicitly as the rest of the
        # tests is all C++ files. Right now, Doxygen says the language is C++
        # as well, but that might change in the future, so have that verified.
        self.assertEqual(*self.actual_expected_contents('file_8c.html'))
