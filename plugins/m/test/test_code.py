#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022
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

from . import PelicanPluginTestCase

_css_colors_src = re.compile(r"""<span class="mh">#(?P<hex>[0-9a-f]{6})</span>""")
_css_colors_dst = r"""<span class="mh">#\g<hex><span class="m-code-color" style="background-color: #\g<hex>;"></span></span>"""

def _add_color_swatch(str):
    return _css_colors_src.sub(_css_colors_dst, str)

class Code(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # Need Source Code Pro for code
            'M_CSS_FILES': ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i',
                            'static/m-dark.css'],
            'PLUGINS': ['m.htmlsanity', 'm.code'],
            'M_CODE_FILTERS_PRE': {
                'CSS': lambda str: str.replace(':', ': ').replace('{', ' {'),
                ('CSS', 'lowercase'): lambda str: str.lower(),
                ('CSS', 'uppercase'): lambda str: str.upper(), # not used
            },
            'M_CODE_FILTERS_POST': {
                'CSS': _add_color_swatch,
                ('CSS', 'replace_colors'): lambda str: str.replace('#c0ffee', '#3bd267')
            },
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
