import docutils
from docutils.parsers import rst
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive, directives
from docutils import nodes, utils

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_by_name

class Code(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'hl_lines': directives.unchanged,
        'class': directives.class_option
    }
    has_content = True

    def run(self):
        self.assert_has_content()
        set_classes(self.options)

        classes = ['m-code']
        if 'classes' in self.options:
            classes += self.options['classes']
            del self.options['classes']

        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            lexer = TextLexer()
        formatter = HtmlFormatter(nowrap=True, **self.options)
        parsed = highlight('\n'.join(self.content), lexer, formatter)

        content = nodes.raw('', parsed, format='html')
        pre = nodes.literal_block('', classes=classes)
        pre.append(content)
        return [pre]

def code(role, rawtext, text, lineno, inliner, options={}, content=[]):
    set_classes(options)
    classes = ['m-code']
    if 'classes' in options:
        classes += options['classes']
        del options['classes']

    # Not sure why language is duplicated in classes?
    language = options.get('language', '')
    if language in classes: classes.remove(language)
    try:
        lexer = get_lexer_by_name(language)
    except ValueError:
        lexer = TextLexer()
    formatter = HtmlFormatter(nowrap=True)
    parsed = highlight(utils.unescape(text), lexer, formatter).strip()

    content = nodes.raw('', parsed, format='html')
    node = nodes.literal(rawtext, '', classes=classes, **options)
    node.append(content)
    return [node], []

code.options = {'class': directives.class_option,
                'language': directives.unchanged}

def register():
    rst.directives.register_directive('code', Code)
    rst.roles.register_canonical_role('code', code)
