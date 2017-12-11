import sys
import unittest

from distutils.version import LooseVersion

from m.test import PluginTestCase

class Math(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(sys.version) >= LooseVersion("3.5"),
                         "The math plugin requires at least Python 3.5")
    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.math']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
