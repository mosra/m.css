from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
    Literal, Number, Operator, Other, Punctuation, Text, Generic, \
    Whitespace

class DarkStyle(Style):

    background_color = None
    highlight_color = '#405363'
    default_style = ""

    styles = {
        # C++
        Comment:                '#a5c9ea',
        Comment.Preproc:        '#3bd267',
        Comment.PreprocFile:    '#c7cf2f',
        Keyword:                'bold #ffffff',
        Name:                   '#dcdcdc',
        String:                 '#e07f7c',
        String.Char:            '#e07cdc',
        Number:                 '#c7cf2f',
        Operator:               '#aaaaaa',
        Punctuation:            "#aaaaaa",

        # CMake
        Name.Builtin:           'bold #ffffff',
        Name.Variable:          '#c7cf2f',

        # reST, HTML
        Name.Tag:               'bold #dcdcdc',
        Name.Attribute:         'bold #dcdcdc',
        Name.Class:             'bold #dcdcdc',
        Operator.Word:          'bold #dcdcdc',
        Generic.Heading:        'bold #ffffff',
        Generic.Emph:           'italic #e6e6e6',
        Generic.Strong:         'bold #e6e6e6'
    }
