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
import sys
import os
import inspect
import re
import shutil
import unittest

from python import run, default_templates, default_config

# https://stackoverflow.com/a/12867228
_camelcase_to_snakecase = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

# The test files are automatically detected from derived class name and
# filesystem location. For a `test_inspect.NameMapping` class, it will look
# for the `inspect_name_mapping` directory. If the class name is equivalent to
# the filename (e.g. `test_page.Page`), then it will be looking for just `page`
# instead of `page_page`. If needed, the directory name can be overridden by
# passing it via dir to __init__().
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
        if os.path.exists(os.path.join(self.path, 'output')): shutil.rmtree(os.path.join(self.path, 'output'))

    def run_python(self, config_overrides={}, templates=default_templates):
        # Defaults that make sense for the tests
        config = copy.deepcopy(default_config)
        config.update({
            'FINE_PRINT': None,
            'THEME_COLOR': None,
            'FAVICON': None,
            'LINKS_NAVBAR1': [],
            'LINKS_NAVBAR2': [],
            'SEARCH_DISABLED': True,
            'OUTPUT': os.path.join(self.path, 'output')
        })

        # Update it with config overrides
        config.update(config_overrides)

        run(self.path, config, templates=templates)

    def actual_expected_contents(self, actual, expected = None):
        if not expected: expected = actual

        with open(os.path.join(self.path, expected)) as f:
            expected_contents = f.read().strip()
        with open(os.path.join(self.path, 'output', actual)) as f:
            actual_contents = f.read().strip()
        return actual_contents, expected_contents

# On top of the automagic of BaseTestCase this automatically sets INPUT_MODULES
# to detected `dirname`, if not set already.
class BaseInspectTestCase(BaseTestCase):
    def run_python(self, config_overrides={}, templates=default_templates):
        if 'INPUT_MODULES' not in config_overrides:
            sys.path.append(self.path)

            # Have to do a deep copy to avoid overwriting the parameter default
            # value. UGH.
            config = copy.deepcopy(config_overrides)
            config['INPUT_MODULES'] = [self.dirname]
            config_overrides = config

        BaseTestCase.run_python(self, config_overrides, templates)
