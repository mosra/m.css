#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
#   Copyright © 2020 Sergei Izmailov <sergei.a.izmailov@gmail.com>
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

import io
import traceback

from contextlib import redirect_stdout, redirect_stderr
from docutils.parsers import rst
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive, directives
from docutils import nodes
from typing import List, Dict

from m.code import _highlight


def strip_second_line(text):
    l1_pos = text.find('\n') + 1
    l2_pos = text.find('\n', l1_pos) + 1
    l3_pos = text.find('\n', l2_pos) + 1
    return text[:l1_pos] + text[l3_pos:]


_exec_contexts = {}  # global storage of snippet contexts


class StreamWrapper:
    def __init__(self, terminal: "ConsoleLikeTerminal", kind):
        self.terminal = terminal
        self.kind = kind  # "o" stands for stdout and "e" for stderr

    def write(self, data):
        self.terminal.render(self.kind, data)


class ConsoleLikeTerminal:

    def __init__(self, recolor_stderr=True):
        self._output = []
        self.recolor_stderr = recolor_stderr
        self.stdout = StreamWrapper(self, "o")
        self.stderr = StreamWrapper(self, "e")

    def render(self, kind, data):
        self._output.append((kind, data))

    def getvalue(self):
        return "".join(
            self.format(kind, data) for kind, data in self._output
        )

    def format(self, kind, data):
        if not self.recolor_stderr or kind == "o":
            return data
        else:
            # not perfect, might interfere with stdout,
            # but it's what most of terminals do
            return "\033[31m" + data + "\033[0m"


class PyCodeExec(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'hl_lines': directives.unchanged,  # same as in m.code.Code
        'class': directives.class_option,  # same as in m.code.Code
        'filters': directives.unchanged,  # same as in m.code.Code
        'context-id': directives.unchanged,  # serves to share state between snippets
        'raises': directives.unchanged,  # expected exception of the snippet (just class name)
        'hide-code': directives.flag,  # suppress snippet code
        'hide-stdout': directives.flag,  # suppress snippet stdout
        'hide-stderr': directives.flag,  # suppress snippet stderr
        'discard-context': directives.flag,  # don't forget to clean-up named contexts
        'no-red-stderr': directives.flag,  # don't make stderr red
    }
    has_content = True

    def run(self):
        self.assert_has_content()

        set_classes(self.options)
        classes = []
        if 'classes' in self.options:
            classes += self.options['classes']
            del self.options['classes']

        filters = self.options.pop('filters', '').split()

        gl = {}

        if 'context-id' in self.options:
            ctx_id = self.options['context-id']
            if ctx_id in _exec_contexts:
                gl = _exec_contexts[ctx_id]
            else:
                _exec_contexts[ctx_id] = gl

            if 'discard-context' in self.options:
                del _exec_contexts[ctx_id]

        terminal = ConsoleLikeTerminal(recolor_stderr='no-red-stderr' not in self.options)
        devnull = io.StringIO()  # replace with portable /dev/null ?
        stdout = terminal.stdout if 'hide-stdout' not in self.options else devnull
        stderr = terminal.stderr if 'hide-stderr' not in self.options else devnull

        expected_raise = self.options.get('raises', False)

        try:
            with redirect_stdout(stdout):
                with redirect_stderr(stderr):
                    exec("\n".join(self.content), gl)
        except Exception as exc:
            exc_class_name = exc.__class__.__name__
            if not expected_raise:
                raise self.severe('Snippet raised exception\n'
                                  'Add `:raises: <exception-type>` to show exceptional snippet\n'.format(self.name) +
                                  strip_second_line(traceback.format_exc()))
            if exc_class_name != expected_raise:
                raise self.severe('Snippet raised unexpected exception {}, \n'.format(exc_class_name) +
                                  'Expected exception type: {}\n'.format(expected_raise) +
                                  strip_second_line(traceback.format_exc())
                                  )
            stderr.write(strip_second_line(traceback.format_exc()))
        else:
            if expected_raise:
                raise self.severe('Snippet was expected to raise {} exception '.format(expected_raise) +
                                  'but it didn\'t')
        finally:
            output = terminal.getvalue()

        pipe_options = self.options.copy()
        output_extra_classes = ['m-nopad']

        result = []

        if 'hl_lines' in pipe_options:
            del pipe_options['hl_lines']

        if 'hide-code' not in self.options:
            result.append(self._run("\n".join(self.content), 'py', self.options, filters, classes))
        if output:
            result.append(self._run(output, 'ansi', pipe_options, filters, classes + output_extra_classes))
        if result:
            fig = nodes.container('', classes=['m-code-figure'])
            for el in result:
                fig.append(el)
            return [fig]
        else:
            return []

    @classmethod
    def _run(cls, content: str, lang: str, options: Dict, filters: List[str], classes: List[str]):

        class_, highlighted = _highlight(content, lang, options, is_block=True, filters=filters)
        classes += [class_]

        pre = nodes.literal_block('', classes=classes)

        content = nodes.raw('', highlighted, format='html')
        pre.append(content)
        div = nodes.container('', classes=['m-py-exec'])
        div.append(pre)

        return div


def register_mcss(**kwargs):
    rst.directives.register_directive('py-exec', PyCodeExec)


# Below is only Pelican-specific functionality. If Pelican is not found, these
# do nothing.

register = register_mcss
