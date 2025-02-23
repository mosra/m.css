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

import re
import subprocess
import unittest

from . import PelicanPluginTestCase, parse_version

def dot_version():
    return re.match(r'.*version (?P<version>\d+\.\d+\.\d+).*', subprocess.check_output(['dot', '-V'], stderr=subprocess.STDOUT).decode('utf-8').strip()).group('version')

class Dot(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.components', 'm.dot'],
            'M_DOT_FONT': 'DejaVu Sans'
        })

        # The damn thing adopted Chrome versioning apparently. No idea if the
        # output changed in version 7, 8 or 9 already.
        if parse_version(dot_version()) >= parse_version("10.0"):
            file = 'page.html'
        # Used to be >= 2.44.0, but 2.42.2 appears to have the same output
        elif parse_version(dot_version()) >= parse_version("2.42.2"):
            file = 'page-2.html'
        else:
            file = 'page-240.html'

        self.assertEqual(*self.actual_expected_contents('page.html', file))
