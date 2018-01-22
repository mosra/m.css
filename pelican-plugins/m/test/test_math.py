#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
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

import sys
import shutil
import unittest

from distutils.version import LooseVersion

from m.test import PluginTestCase

class Math(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(sys.version) >= LooseVersion("3.5") and shutil.which('latex'),
                         "The math plugin requires at least Python 3.5 and LaTeX installed")
    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.math']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))

    def test_code_fallback(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.math'],
            'M_MATH_RENDER_AS_CODE': True
        })

        self.assertEqual(*self.actual_expected_contents('page.html', 'page-code-fallback.html'))
