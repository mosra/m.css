from . import PelicanPluginTestCase


class MatplotlibFigure(PelicanPluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # Need Source Code Pro for code
            'M_CSS_FILES': [
                'https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i',
                'static/m-dark.css'],
            'PLUGINS': ['m.htmlsanity', 'm.code', 'm.py_exec', 'm.matplotlib_figure'],
            'STATIC_PATHS' : ['matplotlib-figures']
        })

        self.assertEqual(*self.actual_expected_contents('page.html'))