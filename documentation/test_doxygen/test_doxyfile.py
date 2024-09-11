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
import os
import shutil
import subprocess
import unittest

from doxygen import parse_doxyfile, State, default_config

from . import BaseTestCase

class Doxyfile(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        # Display ALL THE DIFFS
        self.maxDiff = None

    expected_doxyfile = {
        'DOT_FONTNAME': 'Helvetica',
        'DOT_FONTSIZE': 10,
        'HTML_OUTPUT': 'html',
        'OUTPUT_DIRECTORY': '',
        'PROJECT_BRIEF': 'is cool',
        'PROJECT_LOGO': '',
        'PROJECT_NAME': 'My Pet Project',
        'SHOW_INCLUDE_FILES': True,
        'XML_OUTPUT': 'xml'
    }
    expected_config = {
        'DOXYFILE': 'Doxyfile',

        'FAVICON': ('favicon-dark.png', 'image/png'),
        'LINKS_NAVBAR1': [(None, 'Pages', 'pages.html', 'pages', []),
                          (None, 'Modules', 'modules.html', 'modules', [])],
        # different order
        'LINKS_NAVBAR2': [(None, 'Files', 'files.html', 'files', []),
                          (None, 'Classes', 'annotated.html', 'annotated', [])],
        'FINE_PRINT': 'this is "quotes"',
        'THEME_COLOR': '#22272e',
        'STYLESHEETS': ['a.css', 'b.css'],
        'HTML_HEADER': None,
        'EXTRA_FILES': ['css', 'another.png', 'hello'],
        'PAGE_HEADER': 'this is "quotes" \'apostrophes\'',

        'CLASS_INDEX_EXPAND_LEVELS': 1,
        'CLASS_INDEX_EXPAND_INNER': False,
        'FILE_INDEX_EXPAND_LEVELS': 1,

        'M_CODE_FILTERS_PRE': {},
        'M_CODE_FILTERS_POST': {},
        'M_MATH_CACHE_FILE': 'm.math.cache',

        'SEARCH_DISABLED': False,
        'SEARCH_DOWNLOAD_BINARY': False,
        'SEARCH_FILENAME_PREFIX': 'searchdata',
        'SEARCH_RESULT_ID_BYTES': 2,
        'SEARCH_FILE_OFFSET_BYTES': 3,
        'SEARCH_NAME_SIZE_BYTES': 1,
        'SEARCH_BASE_URL': None,
        'SEARCH_EXTERNAL_URL': None,
        'SEARCH_HELP':
"""<p class="m-noindent">Search for symbols, directories, files, pages or
modules. You can omit any prefix from the symbol or file path; adding a
<code>:</code> or <code>/</code> suffix lists all members of given symbol or
directory.</p>
<p class="m-noindent">Use <span class="m-label m-dim">&darr;</span>
/ <span class="m-label m-dim">&uarr;</span> to navigate through the list,
<span class="m-label m-dim">Enter</span> to go.
<span class="m-label m-dim">Tab</span> autocompletes common prefix, you can
copy a link to the result using <span class="m-label m-dim">⌘</span>
<span class="m-label m-dim">L</span> while <span class="m-label m-dim">⌘</span>
<span class="m-label m-dim">M</span> produces a Markdown link.</p>
""",

        'SHOW_UNDOCUMENTED': False,
        'VERSION_LABELS': False,
    }

    def test(self):
        # Basically mirroring what's in the Doxyfile-legacy. It's silly because
        # we don't need to check most of these here anyway but whatever. To
        # make this a bit saner, all existing tests are using the
        # "legacy Doxyfile" config anyway, so it should be tested more than
        # enough... until we port away from that. This should get then further
        # extended to cover the cases that are no longer tested by other code.
        state = State({**copy.deepcopy(default_config), **{
            'EXTRA_FILES': ['css', 'another.png', 'hello'],
            'STYLESHEETS': ['a.css', 'b.css'],
            'PAGE_HEADER': 'this is "quotes" \'apostrophes\'',
            'FINE_PRINT': 'this is "quotes"',
            'LINKS_NAVBAR1': [(None, 'pages', []),
                              (None, 'modules', [])],
            'LINKS_NAVBAR2': [(None, 'files', []),
                              (None, 'annotated', [])]
        }})

        parse_doxyfile(state, 'test_doxygen/doxyfile/Doxyfile')
        self.assertEqual(state.doxyfile, self.expected_doxyfile)
        self.assertEqual(state.config, self.expected_config)

    def test_legacy(self):
        state = State(copy.deepcopy(default_config))

        parse_doxyfile(state, 'test_doxygen/doxyfile/Doxyfile-legacy')
        self.assertEqual(state.doxyfile, self.expected_doxyfile)
        self.assertEqual(state.config, self.expected_config)

    def test_subdirs(self):
        state = State(copy.deepcopy(default_config))
        with self.assertLogs() as cm:
            with self.assertRaises(NotImplementedError):
                parse_doxyfile(state, 'test_doxygen/doxyfile/Doxyfile-subdirs')
        self.assertEqual(cm.output, [
            "CRITICAL:root:test_doxygen/doxyfile/Doxyfile-subdirs: CREATE_SUBDIRS is not supported, sorry. Disable it and try again."
        ])

class UpgradeCustomVariables(BaseTestCase):
    def test(self):
        # Copy the Doxyfile to a new location because it gets overwritten
        shutil.copyfile(os.path.join(self.path, 'Doxyfile'),
                        os.path.join(self.path, 'Doxyfile-upgrade'))

        subprocess.run(['doxygen', '-u', 'Doxyfile-upgrade'], cwd=self.path, check=True)
        with open(os.path.join(self.path, 'Doxyfile-upgrade'), 'r') as f:
            contents = f.read()

        self.assertFalse('UNKNOWN_VARIABLE' in contents)
        self.assertFalse('COMMENTED_OUT_VARIABLE' in contents)
        self.assertTrue('## HASHED_COMMENTED_VARIABLE = 2' in contents)
        self.assertTrue('##! HASHED_BANG_COMMENTED_VARIABLE = 3 \\' in contents)
        self.assertTrue('##!   HASHED_BANG_COMMENTED_VARIABLE_CONT' in contents)
        self.assertTrue('##!HASHED_BANG_COMMENTED_VARIABLE_NOSPACE = 4' in contents)
        self.assertTrue('INPUT                  = 5' in contents)
        self.assertTrue('##! HASHED_BANG_COMMENTED_VARIABLE_END = 6' in contents)
