import unittest

from distutils.version import LooseVersion

from test import IntegrationTestCase, doxygen_version

class EnumClass(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'enum_class', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/627")
    def test(self):
        self.run_dox2html5(wildcard='File_8h.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))

class TemplateAlias(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'template_alias', *args, **kwargs)

    @unittest.skipUnless(LooseVersion(doxygen_version()) > LooseVersion("1.8.13"),
                         "https://github.com/doxygen/doxygen/pull/626")
    def test(self):
        self.run_dox2html5(wildcard='*.xml')
        self.assertEqual(*self.actual_expected_contents('File_8h.html'))
        self.assertEqual(*self.actual_expected_contents('structTemplate.html'))
