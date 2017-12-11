from m.test import PluginTestCase

class Dox(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity', 'm.dox'],
            'M_DOX_TAGFILES': [
                ('../doc/doxygen/corrade.tag', 'http://doc.magnum.graphics/corrade/', ['Corrade::'])]
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))
