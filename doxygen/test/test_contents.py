import os

from test import IntegrationTestCase

class Typography(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'typography', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Blocks(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'blocks', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_xrefpages(self):
        self.run_dox2html5(wildcard='todo.xml')
        self.assertEqual(*self.actual_expected_contents('todo.html'))

class Code(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'code', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Image(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'image', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'html', 'tiny.png')))

    def test_warnings(self):
        self.run_dox2html5(wildcard='warnings.xml')
        self.assertEqual(*self.actual_expected_contents('warnings.html'))

class Math(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'math', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))

class Tagfile(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'tagfile', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='indexpage.xml')
        self.assertEqual(*self.actual_expected_contents('index.html'))
