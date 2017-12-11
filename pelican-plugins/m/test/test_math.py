from m.test import PluginTestCase

class Math(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.math']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
