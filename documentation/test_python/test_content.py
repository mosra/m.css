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
import unittest

from . import BaseInspectTestCase

from _search import pretty_print, searchdata_filename
from python import EntryType

class Content(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'INPUT_PAGES': ['page.rst']
        })
        self.assertEqual(*self.actual_expected_contents('classes.html'))
        self.assertEqual(*self.actual_expected_contents('content.html'))
        self.assertEqual(*self.actual_expected_contents('content.docstring_summary.html'))
        self.assertEqual(*self.actual_expected_contents('content.Class.html'))
        self.assertEqual(*self.actual_expected_contents('content.ClassDocumentingItsMembers.html'))
        self.assertEqual(*self.actual_expected_contents('content.ClassWithSlots.html'))
        self.assertEqual(*self.actual_expected_contents('content.ClassWithSummary.html'))

        self.assertEqual(*self.actual_expected_contents('page.html'))

class ParseDocstrings(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'M_SPHINX_PARSE_DOCSTRINGS': True
        })
        self.assertEqual(*self.actual_expected_contents('content_parse_docstrings.html'))
        self.assertEqual(*self.actual_expected_contents('content_parse_docstrings.Class.html'))

class HtmlEscape(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'INPUT_PAGES': ['page.rst'],
            'PYBIND11_COMPATIBILITY': True,
            'LINKS_NAVBAR1': [
                ('Pages', 'pages', []),
                ('Modules', 'modules', [])],
        })

        # Page title escaping
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))

        # Value escaping
        self.assertEqual(*self.actual_expected_contents('content_html_escape.html'))
        self.assertEqual(*self.actual_expected_contents('content_html_escape.Class.html'))
        self.assertEqual(*self.actual_expected_contents('content_html_escape.pybind.html'))

    def test_stubs(self):
        self.run_python_stubs({
            'PYBIND11_COMPATIBILITY': True,
        })

        # Compared to the HTML output, *none* of these should have any HTML
        # entities
        self.assertEqual(*self.actual_expected_contents('content_html_escape/__init__.pyi'))
        self.assertEqual(*self.actual_expected_contents('content_html_escape/pybind.pyi'))

    @unittest.skip("Page names are currently not exposed to search and there's nothing else that would require escaping, nothing to test")
    def test_search(self):
        # Re-run everything with search enabled, the search data shouldn't be
        # escaped. Not done as part of above as it'd unnecessarily inflate the
        # size of compared files with the search icon and popup.
        self.run_python({
            'INPUT_PAGES': ['page.rst'],
            'PYBIND11_COMPATIBILITY': True,
            'SEARCH_DISABLED': False,
            'SEARCH_DOWNLOAD_BINARY': True
        })

        with open(os.path.join(self.path, 'output', searchdata_filename.format(search_filename_prefix='searchdata')), 'rb') as f:
            serialized = f.read()
            search_data_pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        # print(search_data_pretty)
        self.assertEqual(search_data_pretty, """
TODO
""".strip())
