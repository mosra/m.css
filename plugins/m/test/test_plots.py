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

import matplotlib
import os
import sys
import unittest

from distutils.version import LooseVersion

from . import PelicanPluginTestCase

class Plots(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.plots'],
            'M_PLOTS_FONT': 'DejaVu Sans'
        })

        # FUCK this is annoying
        if LooseVersion(matplotlib.__version__) >= LooseVersion('3.5'):
            self.assertEqual(*self.actual_expected_contents('page.html'))
        elif LooseVersion(matplotlib.__version__) >= LooseVersion('3.4'):
            self.assertEqual(*self.actual_expected_contents('page.html', 'page-34.html'))
        elif LooseVersion(matplotlib.__version__) >= LooseVersion('3.2'):
            self.assertEqual(*self.actual_expected_contents('page.html', 'page-32.html'))
        elif LooseVersion(matplotlib.__version__) >= LooseVersion('3.0'):
            self.assertEqual(*self.actual_expected_contents('page.html', 'page-30.html'))
        else:
            self.assertEqual(*self.actual_expected_contents('page.html', 'page-22.html'))
