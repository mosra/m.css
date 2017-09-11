from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils import nodes

class Transition(rst.Directive):
    final_argument_whitespace = True
    has_content = False
    required_arguments = 1

    def run(self):
        text = ' '.join(self.arguments)
        title_nodes, _ = self.state.inline_text(text, self.lineno)
        transition_node = nodes.paragraph('', '', *title_nodes)
        transition_node['classes'] += ['m-transition']
        return [transition_node]

class Note(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    optional_arguments = 1

    style_class = ''

    def run(self):
        if len(self.arguments) == 1:
            title_text = self.arguments[0]
            title_nodes, _ = self.state.inline_text(title_text, self.lineno)
            title_node = nodes.title('', '', *title_nodes)

        text = '\n'.join(self.content)
        note_node = nodes.topic(text)
        note_node['classes'] += ['m-note', self.style_class]

        if len(self.arguments) == 1:
            note_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                note_node)
        return [note_node]

class DefaultNote(Note):
    style_class = 'm-default'

class PrimaryNote(Note):
    style_class = 'm-primary'

class SuccessNote(Note):
    style_class = 'm-success'

class WarningNote(Note):
    style_class = 'm-warning'

class DangerNote(Note):
    style_class = 'm-danger'

class InfoNote(Note):
    style_class = 'm-info'

class DimNote(Note):
    style_class = 'm-dim'

class Block(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    required_arguments = 1

    style_class = ''

    def run(self):
        title_text = self.arguments[0]
        title_elements, _ = self.state.inline_text(title_text, self.lineno)
        title_node = nodes.title('', '', *title_elements)

        text = '\n'.join(self.content)
        note_node = nodes.topic(text)
        note_node['classes'] += ['m-block', self.style_class]
        note_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                note_node)

        return [note_node]

class DefaultBlock(Block):
    style_class = 'm-default'

class PrimaryBlock(Block):
    style_class = 'm-primary'

class SuccessBlock(Block):
    style_class = 'm-success'

class WarningBlock(Block):
    style_class = 'm-warning'

class DangerBlock(Block):
    style_class = 'm-danger'

class InfoBlock(Block):
    style_class = 'm-info'

class DimBlock(Block):
    style_class = 'm-dim'

class FlatBlock(Block):
    style_class = 'm-flat'

class Frame(rst.Directive):
    final_argument_whitespace = True
    has_content = True
    optional_arguments = 1

    style_class = ''

    def run(self):
        if len(self.arguments) == 1:
            title_text = self.arguments[0]
            title_nodes, _ = self.state.inline_text(title_text, self.lineno)
            title_node = nodes.title('', '', *title_nodes)

        text = '\n'.join(self.content)
        note_node = nodes.topic(text)
        note_node['classes'] += ['m-frame', self.style_class]

        if len(self.arguments) == 1:
            note_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                note_node)
        return [note_node]

def register():
    rst.directives.register_directive('transition', Transition)

    rst.directives.register_directive('note-default', DefaultNote)
    rst.directives.register_directive('note-primary', PrimaryNote)
    rst.directives.register_directive('note-success', SuccessNote)
    rst.directives.register_directive('note-warning', WarningNote)
    rst.directives.register_directive('note-danger', DangerNote)
    rst.directives.register_directive('note-info', InfoNote)
    rst.directives.register_directive('note-dim', DimNote)

    rst.directives.register_directive('block-default', DefaultBlock)
    rst.directives.register_directive('block-primary', PrimaryBlock)
    rst.directives.register_directive('block-success', SuccessBlock)
    rst.directives.register_directive('block-warning', WarningBlock)
    rst.directives.register_directive('block-danger', DangerBlock)
    rst.directives.register_directive('block-info', InfoBlock)
    rst.directives.register_directive('block-dim', DimBlock)
    rst.directives.register_directive('block-flat', FlatBlock)

    rst.directives.register_directive('frame', Frame)
