import unittest

from distutils.version import LooseVersion

from test import IntegrationTestCase, doxygen_version

class Order(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'order', *args, **kwargs)

    def test(self):
        self.run_dox2html5(index_pages=['pages'], wildcard='index.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class Brief(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'brief', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/624")
    def test(self):
        self.run_dox2html5(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))
        self.assertEqual(*self.actual_expected_contents('page-a.html'))
        self.assertEqual(*self.actual_expected_contents('page-b.html'))

class Toc(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'toc', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/625")
    def test(self):
        self.run_dox2html5(wildcard='page-toc.xml')
        self.assertEqual(*self.actual_expected_contents('page-toc.html'))
