from m.test import PluginTestCase

class Gl(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.gl']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
