from m.test import PluginTestCase

class Gh(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.gh']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
