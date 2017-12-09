from test import IntegrationTestCase

class Order(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'order', *args, **kwargs)

    def test(self):
        self.run_dox2html5(index_pages=['pages'], wildcard='index.xml')
        self.assertEqual(*self.actual_expected_contents('pages.html'))

class DuplicatedBrief(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'duplicated_brief', *args, **kwargs)

    def test(self):
        self.run_dox2html5(wildcard='page-*.xml')
        self.assertEqual(*self.actual_expected_contents('page-a.html'))
        self.assertEqual(*self.actual_expected_contents('page-b.html'))
