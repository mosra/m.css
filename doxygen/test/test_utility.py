import unittest

from dox2html5 import add_wbr

class Utility(unittest.TestCase):
    def test_add_wbr(self):
        self.assertEqual(add_wbr('Corrade::Containers'), 'Corrade::<wbr/>Containers')
        self.assertEqual(add_wbr('CORRADE_TEST_MAIN()'), 'CORRADE_<wbr/>TEST_<wbr/>MAIN()')
        self.assertEqual(add_wbr('http://magnum.graphics/showcase/'), 'http:/<wbr/>/<wbr/>magnum.graphics/<wbr/>showcase/<wbr/>')
        self.assertEqual(add_wbr('<strong>a</strong>'), '<strong>a</strong>')
