#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
#   Copyright © 2020 Sergei Izmailov <sergei.a.izmailov@gmail.com>
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

from . import PelicanPluginTestCase


class PyExec(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # Need Source Code Pro for code
            'M_CSS_FILES': [
                'https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i',
                'static/m-dark.css'],
            'PAGE_EXCLUDES': ['errors'],
            'PLUGINS': ['m.htmlsanity', 'm.code', 'm.py_exec']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))

    def test_errors(self):
        from contextlib import redirect_stderr
        import io
        captured_stderr = io.StringIO()
        with redirect_stderr(captured_stderr):
            self.run_pelican({
                'PATH': os.path.join(self.path, 'errors'),
                'PLUGINS': ['m.htmlsanity', 'm.code', 'm.py_exec']
            })
        captured_stderr_value = captured_stderr.getvalue()
        self.assertIn("Expected exception type: IndexError", captured_stderr_value)
        self.assertIn("Snippet was expected to raise `Exception` exception but didn't", captured_stderr_value)
        self.assertIn("Snippet raised exception\n"
                      "Add `:raises: <exception-type>` to show exceptional snippet", captured_stderr_value)
