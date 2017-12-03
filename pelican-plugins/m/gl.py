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

from . import parse_link
from docutils import nodes, utils
from docutils.parsers import rst

def glext(name, rawtext, text, lineno, inliner, options={}, content=[]):
    title, extension = parse_link(text)
    if not title: title = extension
    prefix = extension.partition('_')[0]
    url = "https://www.khronos.org/registry/OpenGL/extensions/{}/{}.txt".format(prefix, extension)
    node = nodes.reference(rawtext, title, refuri=url, **options)
    return [node], []

def glfn(name, rawtext, text, lineno, inliner, options={}, content=[]):
    title, fn = parse_link(text)
    if not title: title = "gl{}()".format(fn)
    url = "https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/gl{}.xhtml".format(fn)
    node = nodes.reference(rawtext, title, refuri=url, **options)
    return [node], []

def glfnext(name, rawtext, text, lineno, inliner, options={}, content=[]):
    title, extension = parse_link(text)
    prefix = extension.partition('_')[0]
    url = "https://www.khronos.org/registry/OpenGL/extensions/{}/{}.txt".format(prefix, extension)
    node = nodes.reference(rawtext, "gl" + title + prefix + "()", refuri=url, **options)
    return [node], []

def register():
    rst.roles.register_local_role('glext', glext)
    rst.roles.register_local_role('glfn', glfn)
    rst.roles.register_local_role('glfnext', glfnext)
