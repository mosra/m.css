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

import matplotlib
import os
import re
import subprocess

from . import BaseTestCase, parse_version

# Same as in the m.plots test case, see there for details
_normalize_matplotlib_hashes = re.compile('([mp])[0-9a-f]{10}')

def dot_version():
    return re.match(r'.*version (?P<version>\d+\.\d+\.\d+).*', subprocess.check_output(['dot', '-V'], stderr=subprocess.STDOUT).decode('utf-8').strip()).group('version')

class Page(BaseTestCase):
    def test(self):
        self.run_python({
            'INPUT_PAGES': ['index.rst', 'another.rst', 'error.rst']
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertEqual(*self.actual_expected_contents('another.html'))
        self.assertEqual(*self.actual_expected_contents('error.html'))
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class InputSubdir(BaseTestCase):
    def test(self):
        self.run_python({
            'INPUT': 'sub',
            'INPUT_PAGES': ['index.rst']
        })
        # The same output as Page, just the file is taken from elsewhere
        self.assertEqual(*self.actual_expected_contents('index.html', '../page/index.html'))

class Plugins(BaseTestCase):
    def test(self):
        self.run_python({
            # Test all of them to check the registration works well
            'PLUGINS': [
                'm.abbr',
                'm.code',
                'm.components',
                'm.dot',
                'm.dox',
                'm.gh',
                'm.gl',
                'm.images',
                'm.link',
                'm.plots',
                'm.vk',
                'fancyline'
            ],
            'PLUGIN_PATHS': ['plugins'],
            'INPUT_PAGES': ['index.rst', 'dot.rst', 'plots.rst'],
            'M_HTMLSANITY_SMART_QUOTES': True,
            'M_DOT_FONT': 'DejaVu Sans',
            'M_PLOTS_FONT': 'DejaVu Sans',
            'M_DOX_TAGFILES': [
                (os.path.join(self.path, '../../../doc/documentation/corrade.tag'), 'https://doc.magnum.graphics/corrade/')
            ]
        })
        self.assertEqual(*self.actual_expected_contents('index.html'))

        # The damn thing adopted Chrome versioning apparently. No idea if the
        # output changed in version 7, 8 or 9 already.
        if parse_version(dot_version()) >= parse_version("10.0"):
            file = 'dot.html'
        # Used to be >= 2.44.0, but 2.42.2 appears to have the same output
        elif parse_version(dot_version()) >= parse_version("2.42.2"):
            file = 'dot-2.html'
        else:
            file = 'dot-240.html'
        self.assertEqual(*self.actual_expected_contents('dot.html', file))

        # I assume this will be a MASSIVE ANNOYANCE at some point as well so
        # keeping it separate. (Yes, thank you past mosra. Very helpful.)
        if parse_version(matplotlib.__version__) >= parse_version('3.6'):
            # https://github.com/matplotlib/matplotlib/commit/1cf5a33b5b5fb07f8fd3956322b85efa0e307b18
            file = 'plots.html'
        elif parse_version(matplotlib.__version__) >= parse_version('3.5'):
            file = 'plots-35.html'
        else:
            file = 'plots-32.html'

        # The element hashes change wildly between versions, replace them with
        # something stable before comparison
        plots_actual_contents, plots_expected_contents = self.actual_expected_contents('plots.html', file)
        plots_actual_contents = _normalize_matplotlib_hashes.sub(r'\1gggggggggg', plots_actual_contents)
        plots_expected_contents = _normalize_matplotlib_hashes.sub(r'\1gggggggggg', plots_expected_contents)
        self.assertEqual(plots_actual_contents, plots_expected_contents)
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/tiny.png')))

        import fancyline
        self.assertEqual(fancyline.post_crawl_call_count, 1)

        self.assertEqual(fancyline.scope_stack, [])

        # No code, thus no docstrings processed
        self.assertEqual(fancyline.docstring_call_count, 0)

        # Once for each page, but nonce for render_docs() as that shouldn't
        # generate any output anyway
        self.assertEqual(fancyline.pre_page_call_count, 3)
        self.assertEqual(fancyline.post_run_call_count, 1)
