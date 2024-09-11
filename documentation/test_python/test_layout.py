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

from _search import searchdata_format_version, searchdata_filename, searchdata_filename_b85
from . import BaseTestCase

class Layout(BaseTestCase):
    def test(self):
        self.run_python({
            'PROJECT_TITLE': "A project",
            'PROJECT_SUBTITLE': "is cool",

            'THEME_COLOR': '#00ffff',
            'FAVICON': 'favicon-light.png',
            'PAGE_HEADER': "`A self link <{url}>`_",
            'FINE_PRINT': "This beautiful thing is done thanks to\n`m.css <https://mcss.mosra.cz>`_.",
            'INPUT_PAGES': ['getting-started.rst', 'troubleshooting.rst', 'about.rst'],
            'LINKS_NAVBAR1': [
                ('Pages', 'pages', [
                    ('Getting started', 'getting-started'),
                    ('Troubleshooting', 'troubleshooting')]),
                ('Modules', 'modules', [])],
            'LINKS_NAVBAR2': [
                ('Classes', 'classes', []),
                ('GitHub', 'https://github.com/mosra/m.css', [
                    ('About', 'about')])],
            'SEARCH_DISABLED': False,
            'SEARCH_EXTERNAL_URL': 'https://google.com/search?q=site:mcss.mosra.cz+{}',
            'SEARCH_HELP': "Some *help*.\nOn multiple lines.",
            'HTML_HEADER':
"""<!-- this is extra in the header -->
  <!-- and more, indented -->
<!-- yes. -->""",
            'EXTRA_FILES': ['sitemap.xml']
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/m-dark+documentation.compiled.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/favicon-light.png')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/search-v{}.js'.format(searchdata_format_version))))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output', searchdata_filename_b85.format(search_filename_prefix='searchdata'))))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/sitemap.xml')))

class SearchBinary(BaseTestCase):
    def test(self):
        self.run_python({
            'SEARCH_DISABLED': False,
            'SEARCH_DOWNLOAD_BINARY': True
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output', 'search-v{}.js'.format(searchdata_format_version))))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output', searchdata_filename.format(search_filename_prefix='searchdata'))))

class SearchOpenSearch(BaseTestCase):
    def test(self):
        self.run_python({
            'FAVICON': 'favicon-dark.png',
            'SEARCH_DISABLED': False,
            'SEARCH_BASE_URL': 'http://localhost:8000',
            'SEARCH_HELP': "Right-click to add a search engine."
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output', 'search-v{}.js'.format(searchdata_format_version))))
        self.assertEqual(*self.actual_expected_contents('opensearch.xml'))

class ProjectLogo(BaseTestCase):
    def test(self):
        self.run_python({
            'PROJECT_LOGO': 'mosra.jpg',
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))

class ProjectLogoMainProjectUrl(BaseTestCase):
    def test(self):
        self.run_python({
            'PROJECT_LOGO': 'mosra.jpg',
            'PROJECT_SUBTITLE': 'docs',
            'MAIN_PROJECT_URL': 'http://your.brand'
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))
