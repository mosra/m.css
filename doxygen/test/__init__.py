import os
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET

from dox2html5 import run, default_templates, default_wildcard, default_index_pages

class IntegrationTestCase(unittest.TestCase):
    def __init__(self, path, dir, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        # Source files for test_something.py are in something_{dir}/ subdirectory
        self.path = os.path.join(os.path.dirname(os.path.realpath(path)), os.path.splitext(os.path.basename(path))[0][5:] + ('_' + dir if dir else ''))

        # Display ALL THE DIFFS
        self.maxDiff = None

    def setUp(self):
        if os.path.exists(os.path.join(self.path, 'xml')): shutil.rmtree(os.path.join(self.path, 'xml'))
        subprocess.run(["doxygen"], cwd=self.path)

        if os.path.exists(os.path.join(self.path, 'html')): shutil.rmtree(os.path.join(self.path, 'html'))

    def run_dox2html5(self, templates=default_templates, wildcard=default_wildcard, index_pages=default_index_pages):
        run(os.path.join(self.path, 'Doxyfile'), templates=templates, wildcard=wildcard, index_pages=index_pages)

    def expected_actual_contents(self, file):
        with open(os.path.join(self.path, file)) as f:
            expected = f.read().strip()
        with open(os.path.join(self.path, 'html', file)) as f:
            actual = f.read().strip()
        return expected, actual
