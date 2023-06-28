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
import re
import shutil
import subprocess
import sys
import unittest

from doxygen import State, parse_doxyfile, run, default_templates, default_wildcard, default_index_pages, default_config

# https://stackoverflow.com/a/12867228
_camelcase_to_snakecase = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

def doxygen_version():
    return subprocess.check_output(['doxygen', '-v']).decode('utf-8').strip()

class BaseTestCase(unittest.TestCase):
    def __init__(self, *args, dir=None, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        # Get the test filename from the derived class module file. If path is
        # not supplied, get it from derived class name converted to snake_case
        path = sys.modules[self.__class__.__module__].__file__
        if not dir: dir = _camelcase_to_snakecase.sub('_\\1', self.__class__.__name__).lower()

        # Full directory name (for test_something.py the directory is
        # something_{dir}
        dir_prefix = os.path.splitext(os.path.basename(path))[0][5:]
        if dir and dir_prefix != dir:
            self.dirname = dir_prefix + '_' + dir
        else:
            self.dirname = dir_prefix
        # Absolute path to this directory
        self.path = os.path.join(os.path.dirname(os.path.realpath(path)), self.dirname)

        if not os.path.exists(self.path):
            raise AssertionError("autodetected path {} doesn't exist".format(self.path))

        # Display ALL THE DIFFS
        self.maxDiff = None

    def setUp(self):
        if os.path.exists(os.path.join(self.path, 'html')): shutil.rmtree(os.path.join(self.path, 'html'))

    def run_doxygen(self, templates=default_templates, wildcard=default_wildcard, index_pages=default_index_pages, config={}):
        state = State({**copy.deepcopy(default_config), **config})
        parse_doxyfile(state, os.path.join(self.path, 'Doxyfile'))
        run(state, templates=templates, wildcard=wildcard, index_pages=index_pages, sort_globbed_files=True)

    def actual_expected_contents(self, actual, expected = None):
        if not expected: expected = actual

        with open(os.path.join(self.path, expected)) as f:
            expected_contents = f.read().strip()
        with open(os.path.join(self.path, 'html', actual)) as f:
            actual_contents = f.read().strip()
        return actual_contents, expected_contents

class IntegrationTestCase(BaseTestCase):
    def setUp(self):
        if os.path.exists(os.path.join(self.path, 'xml')): shutil.rmtree(os.path.join(self.path, 'xml'))
        subprocess.run(['doxygen'], cwd=self.path, check=True)

        if os.path.exists(os.path.join(self.path, 'html')): shutil.rmtree(os.path.join(self.path, 'html'))
