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
import sys
import unittest

from . import PelicanPluginTestCase, parse_version

# Basically every matplotlib version causes the hashes to change, and 3.9.2 has
# them also different on different machines. Yay software developers. Replace
# them with a static string when comparing. The actual file is not changed in
# order to make it possible to actually view it, it's only for the comparison.
_normalize_hashes = re.compile('([mp])[0-9a-f]{10}')

class Plots(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.plots'],
            'M_PLOTS_FONT': 'DejaVu Sans'
        })

        # FUCK this is annoying
        if parse_version(matplotlib.__version__) >= parse_version('3.6'):
            # https://github.com/matplotlib/matplotlib/commit/1cf5a33b5b5fb07f8fd3956322b85efa0e307b18
            file = 'page.html'
        elif parse_version(matplotlib.__version__) >= parse_version('3.5'):
            file = 'page-35.html'
        elif parse_version(matplotlib.__version__) >= parse_version('3.2'):
            file = 'page-32.html'
        elif parse_version(matplotlib.__version__) >= parse_version('3.0'):
            file = 'page-30.html'
        else:
            file = 'page-22.html'

        # The element hashes change wildly between versions, replace them with
        # something stable before comparison
        actual_contents, expected_contents = self.actual_expected_contents('page.html', file)
        actual_contents = _normalize_hashes.sub(r'\1gggggggggg', actual_contents)
        expected_contents = _normalize_hashes.sub(r'\1gggggggggg', expected_contents)
        self.assertEqual(actual_contents, expected_contents)
