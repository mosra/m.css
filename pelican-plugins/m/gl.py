#!/usr/bin/env python

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
    url = "https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/gl{}.xhtml".format(name)
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
