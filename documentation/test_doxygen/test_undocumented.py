#!/usr/bin/env python3

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

from _search import Serializer, searchdata_filename

from . import IntegrationTestCase

class Undocumented(IntegrationTestCase):
    def test(self):
        self.run_doxygen(wildcard='*.xml')

        # The index pages should be full
        self.assertEqual(*self.actual_expected_contents('annotated.html'))
        self.assertEqual(*self.actual_expected_contents('files.html'))

        # The empty class pages should be present
        self.assertEqual(*self.actual_expected_contents('classClass.html'))

        # Namespace, dir, file, group and class member listing
        self.assertEqual(*self.actual_expected_contents('namespaceNamespace.html'))
        self.assertEqual(*self.actual_expected_contents('dir_4b0d5f8864bf89936129251a2d32609b.html'))
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(*self.actual_expected_contents('group__group.html'))
        self.assertEqual(*self.actual_expected_contents('structNamespace_1_1ClassInANamespace.html'))

        # Test we have all symbols in search data. It's enough to assert the
        # count, it equal to symbol count in the header file
        # TODO: reuse the search data deserialization API once done
        with open(os.path.join(self.path, 'html', searchdata_filename.format(search_filename_prefix='searchdata')), 'rb') as f:
            serialized = f.read()
            magic, version, type_data, symbol_count, map_offset, type_map_offset = Serializer.header_struct.unpack_from(serialized)
            self.assertEqual(symbol_count, 44)
