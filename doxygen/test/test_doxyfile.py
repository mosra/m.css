import unittest

from dox2html5 import parse_doxyfile, State

class Doxyfile(unittest.TestCase):
    def test(self):
        state = State()
        parse_doxyfile(state, 'test/doxyfile/Doxyfile')
        self.assertEqual(state.doxyfile, {
            'HTML_EXTRA_FILES': ['css', 'another.png', 'hello'],
            'HTML_EXTRA_STYLESHEET': ['a.css', 'b.css'],
            'HTML_OUTPUT': 'html',
            'M_CLASS_TREE_EXPAND_LEVELS': 1,
            'M_EXPAND_INNER_TYPES': False,
            'M_FILE_TREE_EXPAND_LEVELS': 1,
            'M_SHOW_DOXYGEN_VERSION': True,
            'M_THEME_COLOR': '#22272e',
            'OUTPUT_DIRECTORY': '',
            'PROJECT_BRIEF': 'is cool',
            'PROJECT_NAME': 'My Pet Project',
            'XML_OUTPUT': 'xml'
        })
