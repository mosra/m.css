#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes
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
    option_spec = {'class': directives.class_option}

    style_class = ''

    def run(self):
        set_classes(self.options)

        if len(self.arguments) == 1:
            title_text = self.arguments[0]
            title_nodes, _ = self.state.inline_text(title_text, self.lineno)
            title_node = nodes.title('', '', *title_nodes)

        text = '\n'.join(self.content)
        topic_node = nodes.topic(text, **self.options)
        topic_node['classes'] += ['m-note', self.style_class]

        if len(self.arguments) == 1:
            topic_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                topic_node)
        return [topic_node]

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
    option_spec = {'class': directives.class_option}

    style_class = ''

    def run(self):
        set_classes(self.options)

        title_text = self.arguments[0]
        title_elements, _ = self.state.inline_text(title_text, self.lineno)
        title_node = nodes.title('', '', *title_elements)

        text = '\n'.join(self.content)
        topic_node = nodes.topic(text, **self.options)
        topic_node['classes'] += ['m-block', self.style_class]
        topic_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                topic_node)

        return [topic_node]

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
    option_spec = {'class': directives.class_option}

    style_class = ''

    def run(self):
        set_classes(self.options)

        if len(self.arguments) == 1:
            title_text = self.arguments[0]
            title_nodes, _ = self.state.inline_text(title_text, self.lineno)
            title_node = nodes.title('', '', *title_nodes)

        text = '\n'.join(self.content)
        topic_node = nodes.topic(text, **self.options)
        topic_node['classes'] += ['m-frame', self.style_class]

        if len(self.arguments) == 1:
            topic_node.append(title_node)

        self.state.nested_parse(self.content, self.content_offset,
                                topic_node)
        return [topic_node]

class CodeFigure(rst.Directive):
    has_content = True
    option_spec = {'class': directives.class_option}

    style_class = 'm-code-figure'

    def run(self):
        set_classes(self.options)

        text = '\n'.join(self.content)
        figure_node = nodes.figure(text, **self.options)
        figure_node['classes'] += [self.style_class]

        self.state.nested_parse(self.content, self.content_offset,
                                figure_node)
        return [figure_node]

class ConsoleFigure(CodeFigure):
    style_class = 'm-console-figure'

class Text(rst.Directive):
    has_content = True
    option_spec = {'class': directives.class_option}

    style_class = ''

    def run(self):
        set_classes(self.options)

        text = '\n'.join(self.content)
        container_node = nodes.container(text, **self.options)
        container_node['classes'] += ['m-text', self.style_class]

        self.state.nested_parse(self.content, self.content_offset,
                                container_node)
        return [container_node]

class DefaultText(Text):
    style_class = 'm-default'

class PrimaryText(Text):
    style_class = 'm-primary'

class SuccessText(Text):
    style_class = 'm-success'

class WarningText(Text):
    style_class = 'm-warning'

class DangerText(Text):
    style_class = 'm-danger'

class InfoText(Text):
    style_class = 'm-info'

class DimText(Text):
    style_class = 'm-dim'

class Button(rst.Directive):
    has_content = True
    final_argument_whitespace = True
    required_arguments = 1
    option_spec = {'class': directives.class_option}

    style_class = ''

    def run(self):
        set_classes(self.options)

        text = '\n'.join(self.content)
        ref_node = nodes.reference(text, '', refuri=self.arguments[0], **self.options)
        ref_node['classes'] += ['m-button', self.style_class]

        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if not isinstance(first_node, nodes.paragraph):
                error = self.state_machine.reporter.error(
                      'Button must contain directly a caption and optional description',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [ref_node, error]

            if len(node) == 1:
                caption = nodes.inline(first_node.rawsource, '',
                                       *first_node.children)
            else:
                caption = nodes.container(first_node.rawsource,
                                          *first_node.children)
                caption['classes'] += ['m-big']

            caption.source = first_node.source
            caption.line = first_node.line
            ref_node += caption

            if len(node) > 1:
                second_node = node[1]
                description = nodes.container(second_node.rawsource,
                                              *second_node.children)
                description['classes'] += ['m-small']
                ref_node += description

        return [ref_node]

class DefaultButton(Button):
    style_class = 'm-default'

class PrimaryButton(Button):
    style_class = 'm-primary'

class SuccessButton(Button):
    style_class = 'm-success'

class WarningButton(Button):
    style_class = 'm-warning'

class DangerButton(Button):
    style_class = 'm-danger'

class InfoButton(Button):
    style_class = 'm-info'

class DimButton(Button):
    style_class = 'm-dim'

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
    rst.directives.register_directive('code-figure', CodeFigure)
    rst.directives.register_directive('console-figure', ConsoleFigure)

    rst.directives.register_directive('text-default', DefaultText)
    rst.directives.register_directive('text-primary', PrimaryText)
    rst.directives.register_directive('text-success', SuccessText)
    rst.directives.register_directive('text-warning', WarningText)
    rst.directives.register_directive('text-danger', DangerText)
    rst.directives.register_directive('text-info', InfoText)
    rst.directives.register_directive('text-dim', DimText)

    rst.directives.register_directive('button-default', DefaultButton)
    rst.directives.register_directive('button-primary', PrimaryButton)
    rst.directives.register_directive('button-success', SuccessButton)
    rst.directives.register_directive('button-warning', WarningButton)
    rst.directives.register_directive('button-danger', DangerButton)
    rst.directives.register_directive('button-info', InfoButton)
    rst.directives.register_directive('button-dim', DimButton)
