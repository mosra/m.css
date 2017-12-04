# -*- coding: utf-8 -*-
#
#   This file is part of m.css.
#
#   Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>
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

from pygments.lexer import RegexLexer
from pygments.token import *

class AnsiLexer(RegexLexer):
    name = 'Ansi escape lexer'

    def callback(lexer, match):
        bright = match.group(1)
        color = match.group(2)
        text = match.group(3)

        if int(bright) == 0:
            token = 'Generic.Ansi'
        elif int(bright) == 1:
            token = 'Generic.AnsiBright'
        else:
            yield (match.start(), Text, text)
            return

        if color == ';30':
            token += 'Black'
        elif color == ';31':
            token += 'Red'
        elif color == ';32':
            token += 'Green'
        elif color == ';33':
            token += 'Yellow'
        elif color == ';34':
            token += 'Blue'
        elif color == ';35':
            token += 'Magenta'
        elif color == ';36':
            token += 'Cyan'
        elif color == ';37':
            token += 'White'
        elif color == ';39':
            token += 'Default'
        else:
            yield (match.start(), Text, text)
            return

        yield (match.start(), string_to_tokentype(token), text)

    tokens = {
        'root': [
            ('[^\x1b]+', Text),
            ('\x1b\\[(\\d+)(;\\d+)?m([^\x1b]*)', callback)]
    }
