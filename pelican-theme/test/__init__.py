import os
import shutil
import unittest

from pelican import read_settings, Pelican

class MinimalTestCase(unittest.TestCase):
    def __init__(self, path, dir, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        # Source files for test_something.py are in something_{dir}/ subdirectory
        self.path = os.path.join(os.path.dirname(os.path.realpath(path)), os.path.splitext(os.path.basename(path))[0][5:] + ('_' + dir if dir else ''))

        # Display ALL THE DIFFS
        self.maxDiff = None

    def setUp(self):
        if os.path.exists(os.path.join(self.path, 'output')): shutil.rmtree(os.path.join(self.path, 'output'))

    def run_pelican(self, settings):
        implicit_settings = {
            # Contains just stuff that isn't required by the m.css theme itself,
            # but is needed to have the test setup working correctly
            'RELATIVE_URLS': True,
            'TIMEZONE': 'UTC',
            'READERS': {'html': None},
            'SITEURL': '.',
            'PATH': os.path.join(self.path),
            'OUTPUT_PATH': os.path.join(self.path, 'output'),
            'PAGE_EXCLUDES': [os.path.join(self.path, 'output')],
            'ARTICLE_EXCLUDES': [os.path.join(self.path, 'output')],
            'FEED_ALL_ATOM': None, # Don't render feeds, we're not testing them *ever*
        }
        settings = read_settings(path=None, override={**implicit_settings, **settings})
        pelican = Pelican(settings=settings)
        pelican.run()

    def actual_expected_contents(self, actual, expected = None):
        if not expected: expected = actual

        with open(os.path.join(self.path, expected)) as f:
            expected_contents = f.read().strip()
        with open(os.path.join(self.path, 'output', actual)) as f:
            actual_contents = f.read().strip()
        return actual_contents, expected_contents

class BaseTestCase(MinimalTestCase):
    def run_pelican(self, settings):
        implicit_settings = {
            'THEME': '.',
            'PLUGIN_PATHS': ['../pelican-plugins'],
            'PLUGINS': ['m.htmlsanity'],
            'THEME_STATIC_DIR': 'static',
            'M_CSS_FILES': ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i',
               'static/m-dark.css'],
            # i.e., not rendering the category, tag and author lists as they
            # are not supported anyway
            'DIRECT_TEMPLATES': ['index', 'archives'],
            'SLUGIFY_SOURCE': 'basename'
        }
        MinimalTestCase.run_pelican(self, {**implicit_settings, **settings})
