#!/usr/bin/env python3

#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
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

import argparse
import copy
import docutils
import enum
import urllib.parse
import hashlib
import html
import importlib
import inspect
import logging
import mimetypes
import os
import re
import sys
import shutil

from enum import Enum
from types import SimpleNamespace as Empty
from importlib.machinery import SourceFileLoader
from typing import Tuple, Dict, Set, Any, List, Callable
from urllib.parse import urljoin
from distutils.version import LooseVersion
from docutils.transforms import Transform

import jinja2

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plugins'))
import m.htmlsanity

default_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/python/')

special_pages = ['index', 'modules', 'classes', 'pages']

class EntryType(Enum):
    SPECIAL = 0 # one of files from special_pages
    PAGE = 1
    MODULE = 2
    CLASS = 3
    ENUM = 4
    ENUM_VALUE = 5
    FUNCTION = 6
    # Denotes a potentially overloaded pybind11 function. Has to be here to
    # be able to distinguish between zero-argument normal and pybind11
    # functions.
    OVERLOADED_FUNCTION = 7
    PROPERTY = 8
    DATA = 9

def default_url_formatter(type: EntryType, path: List[str]) -> Tuple[str, str]:
    # TODO: what about nested pages, how to format?
    url = '.'.join(path) + '.html'
    assert '/' not in url # TODO
    return url, url

def default_id_formatter(type: EntryType, path: List[str]) -> str:
    # Encode pybind11 function overloads into the anchor (hash them, like Rust
    # does)
    if type == EntryType.OVERLOADED_FUNCTION:
        return path[0] + '-' + hashlib.sha1(', '.join([str(i) for i in path[1:]]).encode('utf-8')).hexdigest()[:5]

    if type == EntryType.ENUM_VALUE:
        assert len(path) == 2
        return '-'.join(path)

    assert len(path) == 1
    return path[0]

default_config = {
    'PROJECT_TITLE': 'My Python Project',
    'PROJECT_SUBTITLE': None,
    'MAIN_PROJECT_URL': None,
    'INPUT': None,
    'OUTPUT': 'output',
    'INPUT_MODULES': [],
    'INPUT_PAGES': [],
    'INPUT_DOCS': [],
    'OUTPUT': 'output',
    'THEME_COLOR': '#22272e',
    'FAVICON': 'favicon-dark.png',
    'STYLESHEETS': [
        'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
        '../css/m-dark+documentation.compiled.css'],
    'EXTRA_FILES': [],
    'LINKS_NAVBAR1': [
        ('Pages', 'pages', []),
        ('Modules', 'modules', []),
        ('Classes', 'classes', [])],
    'LINKS_NAVBAR2': [],

    'PAGE_HEADER': None,
    'FINE_PRINT': '[default]',
    'FORMATTED_METADATA': ['summary'],

    'PLUGINS': [],
    'PLUGIN_PATHS': [],

    'CLASS_INDEX_EXPAND_LEVELS': 1,
    'CLASS_INDEX_EXPAND_INNER': False,

    'PYBIND11_COMPATIBILITY': False,

    'SEARCH_DISABLED': False,
    'SEARCH_DOWNLOAD_BINARY': False,
    'SEARCH_HELP': """.. raw:: html

    <p class="m-noindent">Search for modules, classes, functions and other
    symbols. You can omit any prefix from the symbol path; adding a <code>.</code>
    suffix lists all members of given symbol.</p>
    <p class="m-noindent">Use <span class="m-label m-dim">&darr;</span>
    / <span class="m-label m-dim">&uarr;</span> to navigate through the list,
    <span class="m-label m-dim">Enter</span> to go.
    <span class="m-label m-dim">Tab</span> autocompletes common prefix, you can
    copy a link to the result using <span class="m-label m-dim">⌘</span>
    <span class="m-label m-dim">L</span> while <span class="m-label m-dim">⌘</span>
    <span class="m-label m-dim">M</span> produces a Markdown link.</p>
""",
    'SEARCH_BASE_URL': None,
    'SEARCH_EXTERNAL_URL': None,

    'URL_FORMATTER': default_url_formatter,
    'ID_FORMATTER': default_id_formatter
}

class State:
    def __init__(self, config):
        self.config = config
        self.module_mapping: Dict[str, str] = {}
        self.module_docs: Dict[str, Dict[str, str]] = {}
        self.class_docs: Dict[str, Dict[str, str]] = {}
        self.data_docs: Dict[str, Dict[str, str]] = {}
        self.external_data: Set[str] = set()

        self.hooks_pre_page: List = []
        self.hooks_post_run: List = []

        self.name_map: Dict[str, Empty] = {}

def is_internal_function_name(name: str) -> bool:
    """If the function name is internal.

    Skips underscored functions but keeps special functions such as __init__.
    """
    return name.startswith('_') and not (name.startswith('__') and name.endswith('__'))

def map_name_prefix(state: State, type: str) -> str:
    for prefix, replace in state.module_mapping.items():
        if type == prefix or type.startswith(prefix + '.'):
            return replace + type[len(prefix):]

    # No mapping found, return the type as-is
    return type

def is_internal_or_imported_module_member(state: State, parent, path: str, name: str, object) -> bool:
    """If the module member is internal or imported."""

    if name.startswith('_'): return True

    # If this is not a module, check if the enclosing module of the object is
    # what expected. If not, it's a class/function/... imported from elsewhere
    # and we don't want those.
    # TODO: xml.dom.domreg says the things from it should be imported as
    #   xml.dom.foo() and this check discards them, can it be done without
    #   manually adding __all__?
    if not inspect.ismodule(object):
        # Variables don't have the __module__ attribute, so check for its
        # presence. Right now *any* variable will be present in the output, as
        # there is no way to check where it comes from.
        if hasattr(object, '__module__') and map_name_prefix(state, object.__module__) != '.'.join(path):
            return True

    # If this is a module, then things get complicated again and we need to
    # handle modules and packages differently. See also for more info:
    # https://stackoverflow.com/a/7948672
    else:
        # pybind11 submodules have __package__ set to None (instead of '') for
        # nested modules. Allow these. The parent's __package__ can be None (if
        # it's a nested submodule), '' (if it's a top-level module) or a string
        # (if the parent is a Python package), can't really check further.
        if state.config['PYBIND11_COMPATIBILITY'] and object.__package__ is None: return False

        # The parent is a single-file module (not a package), these don't have
        # submodules so this is most definitely an imported module. Source:
        # https://docs.python.org/3/reference/import.html#packages
        if not parent.__package__: return True

        # The parent is a package and this is either a submodule or a
        # subpackage. Check that the __package__ of parent and child is either
        # the same or it's parent + child name
        if object.__package__ not in [parent.__package__, parent.__package__ + '.' + name]: return True

    # If nothing of the above matched, then it's a thing we want to document
    return False

def is_enum(state: State, object) -> bool:
    return (inspect.isclass(object) and issubclass(object, enum.Enum)) or (state.config['PYBIND11_COMPATIBILITY'] and hasattr(object, '__members__'))

def object_type(state: State, object) -> EntryType:
    if inspect.ismodule(object): return EntryType.MODULE
    if inspect.isclass(object):
        if is_enum(state, object): return EntryType.ENUM
        else: return EntryType.CLASS
    if inspect.isfunction(object) or inspect.isbuiltin(object) or inspect.isroutine(object):
        return EntryType.FUNCTION
    if inspect.isdatadescriptor(object):
        return EntryType.PROPERTY
    # Assume everything else is data. The builtin help help() (from pydoc) does
    # the same: https://github.com/python/cpython/blob/d29b3dd9227cfc4a23f77e99d62e20e063272de1/Lib/pydoc.py#L113
    if not inspect.isframe(object) and not inspect.istraceback(object) and not inspect.iscode(object):
        return EntryType.DATA

    # caller should print a warning in this case
    return None # pragma: no cover

def crawl_class(state: State, path: List[str], class_):
    class_entry = Empty()
    class_entry.type = EntryType.CLASS
    class_entry.object = class_
    class_entry.path = path
    class_entry.members = []

    for name, object in inspect.getmembers(class_):
        type = object_type(state, object)
        subpath = path + [name]

        # Crawl the subclasses recursively (they also add itself to the
        # name_map)
        if type == EntryType.CLASS:
            if name in ['__base__', '__class__']: continue # TODO
            if name.startswith('_'): continue

            crawl_class(state, subpath, object)

        # Add other members directly
        else:
            # Filter out private / unwanted members
            if type == EntryType.ENUM:
                if name.startswith('_'): continue
            elif type == EntryType.FUNCTION:
                # Filter out underscored methods (but not dunder methods)
                if is_internal_function_name(name): continue
                # Filter out dunder methods that don't have their own docs
                if name.startswith('__') and (name, object.__doc__) in _filtered_builtin_functions: continue
            elif type == EntryType.PROPERTY:
                if (name, object.__doc__) in _filtered_builtin_properties: continue
                if name.startswith('_'): continue # TODO: are there any dunder props?
            elif type == EntryType.DATA:
                if name.startswith('_'): continue
            else: # pragma: no cover
                assert type is None; continue # ignore unknown object types

            entry = Empty()
            entry.type = type
            entry.object = object
            entry.path = subpath
            state.name_map['.'.join(subpath)] = entry

        class_entry.members += [name]

    # Add itself to the name map
    state.name_map['.'.join(path)] = class_entry

def crawl_module(state: State, path: List[str], module):
    module_entry = Empty()
    module_entry.type = EntryType.MODULE
    module_entry.object = module
    module_entry.path = path
    module_entry.members = []

    # This is actually complicated -- if the module defines __all__, use that.
    # The __all__ is meant to expose the public API, so we don't filter out
    # underscored things.
    if hasattr(module, '__all__'):
        # Names exposed in __all__ could be also imported from elsewhere, for
        # example this is a common pattern with native libraries and we want
        # Foo, Bar, submodule and *everything* in submodule to be referred to
        # as `library.RealName` (`library.submodule.func()`, etc.) instead of
        # `library._native.Foo`, `library._native.sub.func()` etc.
        #
        #   from ._native import Foo as PublicName
        #   from ._native import sub as submodule
        #   __all__ = ['PublicName', 'submodule']
        #
        # The name references can be cyclic so extract the mapping in a
        # separate pass before everything else.
        for name in module.__all__:
            # Everything available in __all__ is already imported, so get those
            # directly
            object = getattr(module, name)
            subpath = path + [name]

            # Modules have __name__ while other objects have __module__, need
            # to check both.
            if inspect.ismodule(object) and object.__name__ != '.'.join(subpath):
                assert object.__name__ not in state.module_mapping
                state.module_mapping[object.__name__] = '.'.join(subpath)
            elif hasattr(object, '__module__'):
                subname = object.__module__ + '.' + object.__name__
                if subname != '.'.join(subpath):
                    assert subname not in state.module_mapping
                    state.module_mapping[subname] = '.'.join(subpath)

        # Now extract the actual docs
        for name in module.__all__:
            object = getattr(module, name)
            subpath = path + [name]
            type = object_type(state, object)

            # Crawl the submodules and subclasses recursively (they also add
            # itself to the name_map), add other members directly.
            if not type: # pragma: no cover
                logging.warning("unknown symbol %s in %s", name, '.'.join(path))
                continue
            elif type == EntryType.MODULE:
                crawl_module(state, subpath, object)
            elif type == EntryType.CLASS:
                crawl_class(state, subpath, object)
            else:
                assert type in [EntryType.ENUM, EntryType.FUNCTION, EntryType.DATA]
                entry = Empty()
                entry.type = type
                entry.object = object
                entry.path = subpath
                state.name_map['.'.join(subpath)] = entry

            module_entry.members += [name]

    # Otherwise, enumerate the members using inspect. However, inspect lists
    # also imported modules, functions and classes, so take only those which
    # have __module__ equivalent to `path`.
    else:
        for name, object in inspect.getmembers(module):
            if is_internal_or_imported_module_member(state, module, path, name, object): continue

            type = object_type(state, object)
            subpath = path + [name]

            # Crawl the submodules and subclasses recursively (they also add
            # itself to the name_map), add other members directly.
            if not type: # pragma: no cover
                # Ignore unknown object types (with __all__ we warn instead)
                continue
            elif type == EntryType.MODULE:
                crawl_module(state, subpath, object)
            elif type == EntryType.CLASS:
                crawl_class(state, subpath, object)
            else:
                assert type in [EntryType.ENUM, EntryType.FUNCTION, EntryType.DATA]
                entry = Empty()
                entry.type = type
                entry.object = object
                entry.path = subpath
                state.name_map['.'.join(subpath)] = entry

            module_entry.members += [name]

    # Add itself to the name map
    state.name_map['.'.join(path)] = module_entry

_pybind_name_rx = re.compile('[a-zA-Z0-9_]*')
_pybind_arg_name_rx = re.compile('[*a-zA-Z0-9_]+')
_pybind_type_rx = re.compile('[a-zA-Z0-9_.]+')
_pybind_default_value_rx = re.compile('[^,)]+')

def parse_pybind_type(state: State, signature: str) -> str:
    input_type = _pybind_type_rx.match(signature).group(0)
    signature = signature[len(input_type):]
    type = map_name_prefix(state, input_type)
    if signature and signature[0] == '[':
        type += '['
        signature = signature[1:]
        while signature[0] != ']':
            signature, inner_type = parse_pybind_type(state, signature)
            type += inner_type

            if signature[0] == ']': break
            assert signature.startswith(', ')
            signature = signature[2:]
            type += ', '

        assert signature[0] == ']'
        signature = signature[1:]
        type += ']'

    return signature, type

def parse_pybind_signature(state: State, signature: str) -> Tuple[str, str, List[Tuple[str, str, str]], str]:
    original_signature = signature # For error reporting
    name = _pybind_name_rx.match(signature).group(0)
    signature = signature[len(name):]
    args = []
    assert signature[0] == '('
    signature = signature[1:]

    # Arguments
    while signature[0] != ')':
        # Name
        arg_name = _pybind_arg_name_rx.match(signature).group(0)
        assert arg_name
        signature = signature[len(arg_name):]

        # Type (optional)
        if signature.startswith(': '):
            signature = signature[2:]
            signature, arg_type = parse_pybind_type(state, signature)
        else:
            arg_type = None

        # Default (optional) -- for now take everything until the next comma
        # TODO: ugh, do properly
        # The equals has spaces around since 2.3.0, preserve 2.2 compatibility.
        # https://github.com/pybind/pybind11/commit/0826b3c10607c8d96e1d89dc819c33af3799a7b8
        if signature.startswith(('=', ' = ')):
            signature = signature[1 if signature[0] == '=' else 3:]
            default = _pybind_default_value_rx.match(signature).group(0)
            signature = signature[len(default):]
        else:
            default = None

        args += [(arg_name, arg_type, default)]

        if signature[0] == ')': break

        # Failed to parse, return an ellipsis and docs
        if not signature.startswith(', '):
            end = original_signature.find('\n')
            logging.warning("cannot parse pybind11 function signature %s", original_signature[:end if end != -1 else None])
            if end != -1 and len(original_signature) > end + 1 and original_signature[end + 1] == '\n':
                summary = extract_summary(state, {}, [], original_signature[end + 1:])
            else:
                summary = ''
            return (name, summary, [('…', None, None)], None)

        signature = signature[2:]

    assert signature[0] == ')'
    signature = signature[1:]

    # Return type (optional)
    if signature.startswith(' -> '):
        signature = signature[4:]
        signature, return_type = parse_pybind_type(state, signature)
    else:
        return_type = None

    if signature and signature[0] != '\n':
        end = original_signature.find('\n')
        logging.warning("cannot parse pybind11 function signature %s", original_signature[:end if end != -1 else None])
        if end != -1 and len(original_signature) > end + 1 and original_signature[end + 1] == '\n':
            summary = extract_summary(state, {}, [], original_signature[end + 1:])
        else:
            summary = ''
        return (name, summary, [('…', None, None)], None)

    if len(signature) > 1 and signature[1] == '\n':
        summary = extract_summary(state, {}, [], signature[2:])
    else:
        summary = ''

    return (name, summary, args, return_type)

def parse_pybind_docstring(state: State, name: str, doc: str) -> List[Tuple[str, str, List[Tuple[str, str, str]], str]]:
    # Multiple overloads, parse each separately
    overload_header = "{}(*args, **kwargs)\nOverloaded function.\n\n".format(name);
    if doc.startswith(overload_header):
        doc = doc[len(overload_header):]
        overloads = []
        id = 1
        while True:
            assert doc.startswith('{}. {}('.format(id, name))
            id = id + 1
            next = doc.find('{}. {}('.format(id, name))

            # Parse the signature and docs from known slice
            overloads += [parse_pybind_signature(state, doc[len(str(id - 1)) + 2:next])]
            assert overloads[-1][0] == name
            if next == -1: break

            # Continue to the next signature
            doc = doc[next:]

        return overloads

    # Normal function, parse and return the first signature
    else:
        return [parse_pybind_signature(state, doc)]

def extract_summary(state: State, external_docs, path: List[str], doc: str) -> str:
    # Prefer external docs, if available
    path_str = '.'.join(path)
    if path_str in external_docs and external_docs[path_str]['summary']:
        return render_inline_rst(state, external_docs[path_str]['summary'])

    if not doc: return '' # some modules (xml.etree) have that :(
    doc = inspect.cleandoc(doc)
    end = doc.find('\n\n')
    return html.escape(doc if end == -1 else doc[:end])

def extract_type(type) -> str:
    # For types we concatenate the type name with its module unless it's
    # builtins (i.e., we want re.Match but not builtins.int).
    return (type.__module__ + '.' if type.__module__ != 'builtins' else '') + type.__name__

def extract_annotation(state: State, annotation) -> str:
    # TODO: why this is not None directly?
    if annotation is inspect.Signature.empty: return None

    # Annotations can be strings, also https://stackoverflow.com/a/33533514
    if type(annotation) == str: return map_name_prefix(state, annotation)

    # To avoid getting <class 'foo.bar'> for types (and getting foo.bar
    # instead) but getting the actual type for types annotated with e.g.
    # List[int], we need to check if the annotation is actually from the
    # typing module or it's directly a type. In Python 3.7 this worked with
    # inspect.isclass(annotation), but on 3.6 that gives True for annotations
    # as well and then we would get just List instead of List[int].
    if annotation.__module__ == 'typing': return map_name_prefix(state, str(annotation))
    return map_name_prefix(state, extract_type(annotation))

def render(config, template: str, page, env: jinja2.Environment):
    template = env.get_template(template)
    rendered = template.render(page=page, URL=page.url, **config)
    with open(os.path.join(config['OUTPUT'], page.filename), 'wb') as f:
        f.write(rendered.encode('utf-8'))
        # Add back a trailing newline so we don't need to bother with
        # patching test files to include a trailing newline to make Git
        # happy. Can't use keep_trailing_newline because that'd add it
        # also for nested templates :(
        f.write(b'\n')

def extract_module_doc(state: State, path: List[str], module):
    assert inspect.ismodule(module)

    out = Empty()
    out.url = state.config['URL_FORMATTER'](EntryType.MODULE, path)[1]
    out.name = path[-1]
    out.summary = extract_summary(state, state.class_docs, path, module.__doc__)
    return out

def extract_class_doc(state: State, path: List[str], class_):
    assert inspect.isclass(class_)

    out = Empty()
    out.url = state.config['URL_FORMATTER'](EntryType.CLASS, path)[1]
    out.name = path[-1]
    out.summary = extract_summary(state, state.class_docs, path, class_.__doc__)
    return out

def extract_enum_doc(state: State, path: List[str], enum_):
    out = Empty()
    out.name = path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.ENUM, path[-1:])
    out.values = []
    out.has_details = False
    out.has_value_details = False

    # The happy case
    if issubclass(enum_, enum.Enum):
        # Enum doc is by default set to a generic value. That's useless as well.
        if enum_.__doc__ == 'An enumeration.':
            out.summary = ''
        else:
            # TODO: external summary for enums
            out.summary = extract_summary(state, {}, [], enum_.__doc__)

        out.base = extract_type(enum_.__base__)

        for i in enum_:
            value = Empty()
            value.name = i.name
            value.id = state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, path[-1:] + [i.name])
            value.value = html.escape(repr(i.value))

            # Value doc gets by default inherited from the enum, that's useless
            if i.__doc__ == enum_.__doc__:
                value.summary = ''
            else:
                # TODO: external summary for enum values
                value.summary = extract_summary(state, {}, [], i.__doc__)

            if value.summary:
                out.has_details = True
                out.has_value_details = True
            out.values += [value]

    # Pybind11 enums are ... different
    elif state.config['PYBIND11_COMPATIBILITY']:
        assert hasattr(enum_, '__members__')

        # TODO: external summary for enums
        out.summary = extract_summary(state, {}, [], enum_.__doc__)
        out.base = None

        for name, v in enum_.__members__.items():
            value = Empty()
            value. name = name
            value.id = state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, path[-1:] + [name])
            value.value = int(v)
            # TODO: once https://github.com/pybind/pybind11/pull/1160 is
            #       released, extract from class docs (until then the class
            #       docstring is duplicated here, which is useless)
            value.summary = ''
            out.values += [value]

    return out

def extract_function_doc(state: State, parent, path: List[str], function) -> List[Any]:
    assert inspect.isfunction(function) or inspect.ismethod(function) or inspect.isroutine(function)

    # Extract the signature from the docstring for pybind11, since it can't
    # expose it to the metadata: https://github.com/pybind/pybind11/issues/990
    # What's not solvable with metadata, however, are function overloads ---
    # one function in Python may equal more than one function on the C++ side.
    # To make the docs usable, list all overloads separately.
    if state.config['PYBIND11_COMPATIBILITY'] and function.__doc__.startswith(path[-1]):
        funcs = parse_pybind_docstring(state, path[-1], function.__doc__)
        overloads = []
        for name, summary, args, type in funcs:
            out = Empty()
            out.name = path[-1]
            out.params = []
            out.has_complex_params = False
            out.has_details = False
            # TODO: external summary for functions
            out.summary = summary

            # Don't show None return type for void functions
            out.type = None if type == 'None' else type

            # There's no other way to check staticmethods than to check for
            # self being the name of first parameter :( No support for
            # classmethods, as C++11 doesn't have that
            out.is_classmethod = False
            if inspect.isclass(parent) and args and args[0][0] == 'self':
                out.is_staticmethod = False
            else:
                out.is_staticmethod = True

            # Guesstimate whether the arguments are positional-only or
            # position-or-keyword. It's either all or none. This is a brown
            # magic, sorry.

            # For instance methods positional-only argument names are either
            # self (for the first argument) or arg(I-1) (for second
            # argument and further). Also, the `self` argument is
            # positional-or-keyword only if there are positional-or-keyword
            # arguments afgter it, otherwise it's positional-only.
            if inspect.isclass(parent) and not out.is_staticmethod:
                assert args and args[0][0] == 'self'

                positional_only = True
                for i, arg in enumerate(args[1:]):
                    name, type, default = arg
                    if name != 'arg{}'.format(i):
                        positional_only = False
                        break

            # For static methods or free functions positional-only arguments
            # are argI.
            else:
                positional_only = True
                for i, arg in enumerate(args):
                    name, type, default = arg
                    if name != 'arg{}'.format(i):
                        positional_only = False
                        break

            for i, arg in enumerate(args):
                name, type, default = arg
                param = Empty()
                param.name = name
                # Don't include redundant type for the self argument
                if name == 'self': param.type = None
                else: param.type = type
                param.default = html.escape(default or '')
                if type or default: out.has_complex_params = True

                # *args / **kwargs can still appear in the parsed signatures if
                # the function accepts py::args / py::kwargs directly
                if name == '*args':
                    param.name = 'args'
                    param.kind = 'VAR_POSITIONAL'
                elif name == '**kwargs':
                    param.name = 'kwargs'
                    param.kind = 'VAR_KEYWORD'
                else:
                    param.kind = 'POSITIONAL_ONLY' if positional_only else 'POSITIONAL_OR_KEYWORD'

                out.params += [param]

            # Format the anchor. Pybind11 functions are sometimes overloaded,
            # thus name alone is not enough.
            out.id = state.config['ID_FORMATTER'](EntryType.OVERLOADED_FUNCTION, path[-1:] + [param.type for param in out.params])

            overloads += [out]

        return overloads

    # Sane introspection path for non-pybind11 code
    else:
        out = Empty()
        out.name = path[-1]
        out.id = state.config['ID_FORMATTER'](EntryType.FUNCTION, path[-1:])
        out.params = []
        out.has_complex_params = False
        out.has_details = False
        # TODO: external summary for functions
        out.summary = extract_summary(state, {}, [], function.__doc__)

        # Decide if classmethod or staticmethod in case this is a method
        if inspect.isclass(parent):
            out.is_classmethod = inspect.ismethod(function)
            out.is_staticmethod = out.name in parent.__dict__ and isinstance(parent.__dict__[out.name], staticmethod)

        try:
            signature = inspect.signature(function)
            out.type = extract_annotation(state, signature.return_annotation)
            for i in signature.parameters.values():
                param = Empty()
                param.name = i.name
                param.type = extract_annotation(state, i.annotation)
                if param.type:
                    out.has_complex_params = True
                if i.default is inspect.Signature.empty:
                    param.default = None
                else:
                    param.default = repr(i.default)
                    out.has_complex_params = True
                param.kind = str(i.kind)
                out.params += [param]

        # In CPython, some builtin functions (such as math.log) do not provide
        # metadata about their arguments. Source:
        # https://docs.python.org/3/library/inspect.html#inspect.signature
        except ValueError:
            param = Empty()
            param.name = '...'
            param.name_type = param.name
            out.params = [param]
            out.type = None

        return [out]

def extract_property_doc(state: State, path: List[str], property):
    assert inspect.isdatadescriptor(property)

    out = Empty()
    out.name = path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.PROPERTY, path[-1:])
    # TODO: external summary for properties
    out.summary = extract_summary(state, {}, [], property.__doc__)
    out.is_settable = property.fset is not None
    out.is_deletable = property.fdel is not None
    out.has_details = False

    try:
        signature = inspect.signature(property.fget)
        out.type = extract_annotation(state, signature.return_annotation)
    except ValueError:
        # pybind11 properties have the type in the docstring
        if state.config['PYBIND11_COMPATIBILITY']:
            out.type = parse_pybind_signature(state, property.fget.__doc__)[3]
        else:
            out.type = None

    return out

def extract_data_doc(state: State, parent, path: List[str], data):
    assert not inspect.ismodule(data) and not inspect.isclass(data) and not inspect.isroutine(data) and not inspect.isframe(data) and not inspect.istraceback(data) and not inspect.iscode(data)

    out = Empty()
    out.name = path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.DATA, path[-1:])
    # Welp. https://stackoverflow.com/questions/8820276/docstring-for-variable
    out.summary = ''
    out.has_details = False
    if hasattr(parent, '__annotations__') and out.name in parent.__annotations__:
        out.type = extract_annotation(state, parent.__annotations__[out.name])
    else:
        out.type = None
    # The autogenerated <foo.bar at 0xbadbeef> is useless, so provide the value
    # only if __repr__ is implemented for given type
    if '__repr__' in type(data).__dict__:
        out.value = html.escape(repr(data))
    else:
        out.value = None

    # External data summary, if provided
    path_str = '.'.join(path)
    if path_str in state.data_docs:
        # TODO: use also the contents
        out.summary = render_inline_rst(state, state.data_docs[path_str]['summary'])
        del state.data_docs[path_str]

    return out

def render_module(state: State, path, module, env):
    # Generate breadcrumb as the first thing as it generates the output
    # filename as a side effect
    breadcrumb = []
    filename: str
    url: str
    for i in range(len(path)):
        filename, url = state.config['URL_FORMATTER'](EntryType.MODULE, path[:i + 1])
        breadcrumb += [(path[i], url)]

    logging.debug("generating %s", filename)

    # Call all registered page begin hooks
    for hook in state.hooks_pre_page: hook()

    page = Empty()
    page.summary = extract_summary(state, state.module_docs, path, module.__doc__)
    page.filename = filename
    page.url = url
    page.breadcrumb = breadcrumb
    page.prefix_wbr = '.<wbr />'.join(path + [''])
    page.modules = []
    page.classes = []
    page.enums = []
    page.functions = []
    page.data = []
    page.has_enum_details = False

    # External page content, if provided
    path_str = '.'.join(path)
    if path_str in state.module_docs:
        page.content = render_rst(state, state.module_docs[path_str]['content'])
        state.module_docs[path_str]['used'] = True

    # Find itself in the global map, save the summary back there for index
    module_entry = state.name_map[path_str]
    module_entry.summary = page.summary

    # Extract docs for all members
    for name in module_entry.members:
        subpath = path + [name]
        subpath_str = '.'.join(subpath)
        member_entry = state.name_map[subpath_str]

        if member_entry.type != EntryType.DATA and not object.__doc__: # pragma: no cover
            logging.warning("%s is undocumented", subpath_str)

        if member_entry.type == EntryType.MODULE:
            page.modules += [extract_module_doc(state, subpath, member_entry.object)]
        elif member_entry.type == EntryType.CLASS:
            page.classes += [extract_class_doc(state, subpath, member_entry.object)]
        elif member_entry.type == EntryType.ENUM:
            enum_ = extract_enum_doc(state, subpath, member_entry.object)
            page.enums += [enum_]
            if enum_.has_details: page.has_enum_details = True
        elif member_entry.type == EntryType.FUNCTION:
            page.functions += extract_function_doc(state, module, subpath, member_entry.object)
        elif member_entry.type == EntryType.DATA:
            page.data += [extract_data_doc(state, module, subpath, member_entry.object)]
        else: # pragma: no cover
            assert False

    render(state.config, 'module.html', page, env)

# Builtin dunder functions have hardcoded docstrings. This is totally useless
# to have in the docs, so filter them out. Uh... kinda ugly.
_filtered_builtin_functions = set([
    ('__delattr__', "Implement delattr(self, name)."),
    ('__eq__', "Return self==value."),
    ('__ge__', "Return self>=value."),
    ('__getattribute__', "Return getattr(self, name)."),
    ('__gt__', "Return self>value."),
    ('__hash__', "Return hash(self)."),
    ('__init__', "Initialize self.  See help(type(self)) for accurate signature."),
    ('__init_subclass__',
        "This method is called when a class is subclassed.\n\n"
        "The default implementation does nothing. It may be\n"
        "overridden to extend subclasses.\n"),
    ('__le__', "Return self<=value."),
    ('__lt__', "Return self<value."),
    ('__ne__', "Return self!=value."),
    ('__new__',
        "Create and return a new object.  See help(type) for accurate signature."),
    ('__repr__', "Return repr(self)."),
    ('__setattr__', "Implement setattr(self, name, value)."),
    ('__str__', "Return str(self)."),
    ('__subclasshook__',
        "Abstract classes can override this to customize issubclass().\n\n"
        "This is invoked early on by abc.ABCMeta.__subclasscheck__().\n"
        "It should return True, False or NotImplemented.  If it returns\n"
        "NotImplemented, the normal algorithm is used.  Otherwise, it\n"
        "overrides the normal algorithm (and the outcome is cached).\n")
])

# Python 3.6 has slightly different docstrings than 3.7
if LooseVersion(sys.version) >= LooseVersion("3.7"):
    _filtered_builtin_functions.update({
        ('__dir__', "Default dir() implementation."),
        ('__format__', "Default object formatter."),
        ('__reduce__', "Helper for pickle."),
        ('__reduce_ex__', "Helper for pickle."),
        ('__sizeof__', "Size of object in memory, in bytes."),
    })
else:
    _filtered_builtin_functions.update({
        ('__dir__', "__dir__() -> list\ndefault dir() implementation"),
        ('__format__', "default object formatter"),
        ('__reduce__', "helper for pickle"),
        ('__reduce_ex__', "helper for pickle"),
        ('__sizeof__', "__sizeof__() -> int\nsize of object in memory, in bytes")
    })

_filtered_builtin_properties = set([
    ('__weakref__', "list of weak references to the object (if defined)")
])

def render_class(state: State, path, class_, env):
    # Generate breadcrumb as the first thing as it generates the output
    # filename as a side effect. It's a bit hairy because we need to figure out
    # proper entry type for the URL formatter for each part of the breadcrumb.
    breadcrumb = []
    filename: str
    url: str
    for i in range(len(path)):
        type = state.name_map['.'.join(path[:i + 1])].type
        filename, url = state.config['URL_FORMATTER'](type, path[:i + 1])
        breadcrumb += [(path[i], url)]

    logging.debug("generating %s", filename)

    # Call all registered page begin hooks
    for hook in state.hooks_pre_page: hook()

    page = Empty()
    page.summary = extract_summary(state, state.class_docs, path, class_.__doc__)
    page.filename = filename
    page.url = url
    page.breadcrumb = breadcrumb
    page.prefix_wbr = '.<wbr />'.join(path + [''])
    page.classes = []
    page.enums = []
    page.classmethods = []
    page.staticmethods = []
    page.dunder_methods = []
    page.methods = []
    page.properties = []
    page.data = []
    page.has_enum_details = False

    # External page content, if provided
    path_str = '.'.join(path)
    if path_str in state.class_docs:
        page.content = render_rst(state, state.class_docs[path_str]['content'])
        state.class_docs[path_str]['used'] = True

    # Find itself in the global map, save the summary back there for index
    module_entry = state.name_map[path_str]
    module_entry.summary = page.summary

    # Extract docs for all members
    for name in module_entry.members:
        subpath = path + [name]
        subpath_str = '.'.join(subpath)
        member_entry = state.name_map[subpath_str]

        # TODO: yell only if there's also no external doc content
        if member_entry.type != EntryType.DATA and not object.__doc__: # pragma: no cover
            logging.warning("%s is undocumented", subpath_str)

        if member_entry.type == EntryType.CLASS:
            page.classes += [extract_class_doc(state, subpath, member_entry.object)]
        elif member_entry.type == EntryType.ENUM:
            enum_ = extract_enum_doc(state, subpath, member_entry.object)
            page.enums += [enum_]
            if enum_.has_details: page.has_enum_details = True
        elif member_entry.type == EntryType.FUNCTION:
            for function in extract_function_doc(state, class_, subpath, member_entry.object):
                if name.startswith('__'):
                    page.dunder_methods += [function]
                elif function.is_classmethod:
                    page.classmethods += [function]
                elif function.is_staticmethod:
                    page.staticmethods += [function]
                else:
                    page.methods += [function]
        elif member_entry.type == EntryType.PROPERTY:
            page.properties += [extract_property_doc(state, subpath, member_entry.object)]
        elif member_entry.type == EntryType.DATA:
            page.data += [extract_data_doc(state, class_, subpath, member_entry.object)]
        else: # pragma: no cover
            assert False

    render(state.config, 'class.html', page, env)

# Extracts image paths and transforms them to just the filenames
class ExtractImages(Transform):
    # Max Docutils priority is 990, be sure that this is applied at the very
    # last
    default_priority = 991

    # There is no simple way to have stateful transforms (the publisher always
    # gets just the class, not the instance) so we have to use this
    # TODO: maybe the pending nodes could solve this?
    external_data = set()

    def __init__(self, document, startnode):
        Transform.__init__(self, document, startnode=startnode)

    def apply(self):
        ExtractImages._external_data = set()
        for image in self.document.traverse(docutils.nodes.image):
            # Skip absolute URLs
            if urllib.parse.urlparse(image['uri']).netloc: continue

            # TODO: is there a non-private access to current document source
            # path?
            ExtractImages._external_data.add(os.path.join(os.path.dirname(self.document.settings._source), image['uri']) if isinstance(self.document.settings._source, str) else image['uri'])

            # Patch the URL to be just the filename
            image['uri'] = os.path.basename(image['uri'])

class DocumentationWriter(m.htmlsanity.SaneHtmlWriter):
    def get_transforms(self):
        return m.htmlsanity.SaneHtmlWriter.get_transforms(self) + [ExtractImages]

def publish_rst(state: State, source, *, source_path=None, translator_class=m.htmlsanity.SaneHtmlTranslator):
    pub = docutils.core.Publisher(
        writer=DocumentationWriter(),
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.writer.translator_class = translator_class
    pub.process_programmatic_settings(None, m.htmlsanity.docutils_settings, None)
    # Docutils uses a deprecated U mode for opening files, so instead of
    # monkey-patching docutils.io.FileInput to not do that (like Pelican does),
    # I just read the thing myself.
    # TODO for external docs it *somehow* needs to supply the filename and line
    # range to it for better error reporting, this is too awful
    pub.set_source(source=source, source_path=source_path)
    pub.publish()

    # External images to pull later
    state.external_data = state.external_data.union(ExtractImages._external_data)

    return pub

def render_rst(state: State, source):
    return publish_rst(state, source, source_path=None).writer.parts.get('body').rstrip()

class _SaneInlineHtmlTranslator(m.htmlsanity.SaneHtmlTranslator):
    # Unconditionally force compact paragraphs. This means the inline HTML
    # won't be wrapped in a <p> which is exactly what we want.
    def should_be_compact_paragraph(self, node):
        return True

def render_inline_rst(state: State, source):
    return publish_rst(state, source, translator_class=_SaneInlineHtmlTranslator).writer.parts.get('body').rstrip()

def render_doc(state: State, filename):
    logging.debug("parsing docs from %s", filename)

    # Page begin hooks are called before this in run(), once for all docs since
    # these functions are not generating any pages

    # Render the file. The directives should take care of everything, so just
    # discard the output afterwards.
    with open(filename, 'r') as f: publish_rst(state, f.read())

def render_page(state: State, path, input_filename, env):
    filename, url = state.config['URL_FORMATTER'](EntryType.PAGE, path)

    logging.debug("generating %s", filename)

    # Call all registered page begin hooks
    for hook in state.hooks_pre_page: hook()

    # Render the file
    with open(input_filename, 'r') as f: pub = publish_rst(state, f.read(), source_path=input_filename)

    # Extract metadata from the page
    metadata = {}
    for docinfo in pub.document.traverse(docutils.nodes.docinfo):
        for element in docinfo.children:
            if element.tagname == 'field':
                name_elem, body_elem = element.children
                name = name_elem.astext()
                if name in state.config['FORMATTED_METADATA']:
                    # If the metadata are formatted, format them. Use a special
                    # translator that doesn't add <dd> tags around the content,
                    # also explicitly disable the <p> around as we not need it
                    # always.
                    # TODO: uncrapify this a bit
                    visitor = m.htmlsanity._SaneFieldBodyTranslator(pub.document)
                    visitor.compact_field_list = True
                    body_elem.walkabout(visitor)
                    value = visitor.astext()
                else:
                    value = body_elem.astext()
                metadata[name.lower()] = value

    # Breadcrumb, we don't do page hierarchy yet
    assert len(path) == 1
    breadcrumb = [(pub.writer.parts.get('title'), url)]

    page = Empty()
    page.filename = filename
    page.url = url
    page.breadcrumb = breadcrumb
    page.prefix_wbr = path[0]

    # Set page content and add extra metadata from there
    page.content = pub.writer.parts.get('body').rstrip()
    for key, value in metadata.items(): setattr(page, key, value)
    if not hasattr(page, 'summary'): page.summary = ''

    # Find itself in the global map, save the page title and summary back there
    # for index
    module_entry = state.name_map['.'.join(path)]
    module_entry.summary = page.summary
    module_entry.name = breadcrumb[-1][0]

    # Render the output file
    render(state.config, 'page.html', page, env)

def run(basedir, config, templates):
    # Populate the INPUT, if not specified, make it absolute
    if config['INPUT'] is None: config['INPUT'] = basedir
    else: config['INPUT'] = os.path.join(basedir, config['INPUT'])

    # Make the output dir absolute
    config['OUTPUT'] = os.path.join(config['INPUT'], config['OUTPUT'])
    if not os.path.exists(config['OUTPUT']): os.makedirs(config['OUTPUT'])

    # Guess MIME type of the favicon
    if config['FAVICON']:
        config['FAVICON'] = (config['FAVICON'], mimetypes.guess_type(config['FAVICON'])[0])

    state = State(config)

    # Prepare Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates), trim_blocks=True,
        lstrip_blocks=True, enable_async=True)
    # Filter to return file basename or the full URL, if absolute
    def basename_or_url(path):
        if urllib.parse.urlparse(path).netloc: return path
        return os.path.basename(path)
    # Filter to return URL for given symbol. If the path is a string, first try
    # to treat it as an URL. If that fails, turn it into a list and try to look
    # it up in various dicts.
    def path_to_url(path):
        if isinstance(path, str):
            if urllib.parse.urlparse(path).netloc: return path
            path = [path]
        entry = state.name_map['.'.join(path)]
        return state.config['URL_FORMATTER'](entry.type, entry.path)[1]

    env.filters['basename_or_url'] = basename_or_url
    env.filters['path_to_url'] = path_to_url
    env.filters['urljoin'] = urljoin

    # Set up extra plugin paths. The one for m.css plugins was added above.
    for path in config['PLUGIN_PATHS']:
        if path not in sys.path: sys.path.append(os.path.join(config['INPUT'], path))

    # Import plugins
    for plugin in ['m.htmlsanity'] + config['PLUGINS']:
        module = importlib.import_module(plugin)
        module.register_mcss(
            mcss_settings=config,
            jinja_environment=env,
            module_doc_contents=state.module_docs,
            class_doc_contents=state.class_docs,
            data_doc_contents=state.data_docs,
            hooks_pre_page=state.hooks_pre_page,
            hooks_post_run=state.hooks_post_run)

    # Call all registered page begin hooks for the first time
    for hook in state.hooks_pre_page: hook()

    # Crawl all input modules to gather the name tree, put their names into a
    # list for the index
    class_index = []
    for module in config['INPUT_MODULES']:
        if isinstance(module, str):
            module_name = module
            module = importlib.import_module(module)
        else:
            module_name = module.__name__

        crawl_module(state, [module_name], module)
        class_index += [module_name]

    # Add special pages to the name map. The pages are done after so they can
    # override these.
    for page in special_pages:
        entry = Empty()
        entry.type = EntryType.SPECIAL
        entry.path = [page]
        state.name_map[page] = entry

    # Do the same for pages
    # TODO: turn also into some crawl_page() function? once we have subpages?
    page_index = []
    for page in config['INPUT_PAGES']:
        page_name = os.path.splitext(os.path.basename(page))[0]

        entry = Empty()
        entry.type = EntryType.PAGE
        entry.path = [page_name]
        entry.filename = os.path.join(config['INPUT'], page)
        state.name_map[page_name] = entry

        # The index page doesn't go to the index
        if page_name != 'index': page_index += [page_name]

    # Then process the doc input files so we have all data for rendering
    # module pages. This needs to be done *after* the initial crawl so
    # cross-linking works as expected.
    for file in config['INPUT_DOCS']:
        render_doc(state, os.path.join(basedir, file))

    # Go through all crawled names and render modules, classes and pages. A
    # side effect of the render is entry.summary (and entry.name for pages)
    # being filled.
    for entry in state.name_map.values():
        if entry.type == EntryType.MODULE:
            render_module(state, entry.path, entry.object, env)
        elif entry.type == EntryType.CLASS:
            render_class(state, entry.path, entry.object, env)
        elif entry.type == EntryType.PAGE:
            render_page(state, entry.path, entry.filename, env)

    # Warn if there are any unused contents left after processing everything
    unused_module_docs = [key for key, value in state.module_docs.items() if not 'used' in value]
    unused_class_docs = [key for key, value in state.class_docs.items() if not 'used' in value]
    unused_data_docs = [key for key, value in state.data_docs.items() if not 'used' in value]
    if unused_module_docs:
        logging.warning("The following module doc contents were unused: %s", unused_module_docs)
    if unused_class_docs:
        logging.warning("The following class doc contents were unused: %s", unused_class_docs)
    if unused_data_docs:
        logging.warning("The following data doc contents were unused: %s", unused_data_docs)

    # Create module and class index from the toplevel name list. Recursively go
    # from the top-level index list and gather all class/module children.
    def fetch_class_index(entry):
        index_entry = Empty()
        index_entry.kind = 'module' if entry.type == EntryType.MODULE else 'class'
        index_entry.name = entry.path[-1]
        index_entry.url = state.config['URL_FORMATTER'](entry.type, entry.path)[1]
        index_entry.summary = entry.summary
        index_entry.has_nestable_children = False
        index_entry.children = []

        # Module children should go before class children, put them in a
        # separate list and then concatenate at the end
        class_children = []
        for member in entry.members:
            member_entry = state.name_map['.'.join(entry.path + [member])]
            if member_entry.type == EntryType.MODULE:
                index_entry.has_nestable_children = True
                index_entry.children += [fetch_class_index(state.name_map['.'.join(member_entry.path)])]
            elif member_entry.type == EntryType.CLASS:
                class_children += [fetch_class_index(state.name_map['.'.join(member_entry.path)])]
        index_entry.children += class_children

        return index_entry

    for i in range(len(class_index)):
        class_index[i] = fetch_class_index(state.name_map[class_index[i]])

    # Create page index from the toplevel name list
    # TODO: rework when we have nested page support
    for i in range(len(page_index)):
        entry = state.name_map[page_index[i]]
        assert entry.type == EntryType.PAGE

        index_entry = Empty()
        index_entry.kind = 'page'
        index_entry.name = entry.name
        index_entry.url = state.config['URL_FORMATTER'](entry.type, entry.path)[1]
        index_entry.summary = entry.summary
        index_entry.has_nestable_children = False
        index_entry.children = []

        page_index[i] = index_entry

    index = Empty()
    index.classes = class_index
    index.pages = page_index
    for file in special_pages[1:]: # exclude index
        template = env.get_template(file + '.html')
        filename, url = state.config['URL_FORMATTER'](EntryType.SPECIAL, [file])
        rendered = template.render(index=index, URL=url, **config)
        with open(os.path.join(config['OUTPUT'], filename), 'wb') as f:
            f.write(rendered.encode('utf-8'))
            # Add back a trailing newline so we don't need to bother with
            # patching test files to include a trailing newline to make Git
            # happy. Can't use keep_trailing_newline because that'd add it
            # also for nested templates :(
            f.write(b'\n')

    # Create index.html if it was not provided by the user
    if 'index.rst' not in [os.path.basename(i) for i in config['INPUT_PAGES']]:
        logging.debug("writing index.html for an empty main page")

        filename, url = state.config['URL_FORMATTER'](EntryType.SPECIAL, ['index'])

        page = Empty()
        page.filename = filename
        page.url = url
        page.breadcrumb = [(config['PROJECT_TITLE'], url)]
        render(config, 'page.html', page, env)

    # Copy referenced files
    for i in config['STYLESHEETS'] + config['EXTRA_FILES'] + ([config['FAVICON'][0]] if config['FAVICON'] else []) + list(state.external_data) + ([] if config['SEARCH_DISABLED'] else ['search.js']):
        # Skip absolute URLs
        if urllib.parse.urlparse(i).netloc: continue

        # If file is found relative to the conf file, use that
        if os.path.exists(os.path.join(config['INPUT'], i)):
            i = os.path.join(config['INPUT'], i)

        # Otherwise use path relative to script directory
        else:
            i = os.path.join(os.path.dirname(os.path.realpath(__file__)), i)

        logging.debug("copying %s to output", i)
        shutil.copy(i, os.path.join(config['OUTPUT'], os.path.basename(i)))

    # Call all registered finalization hooks for the first time
    for hook in state.hooks_post_run: hook()

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', help="configuration file")
    parser.add_argument('--templates', help="template directory", default=default_templates)
    parser.add_argument('--debug', help="verbose debug output", action='store_true')
    args = parser.parse_args()

    # Load configuration from a file, update the defaults with it
    config = copy.deepcopy(default_config)
    name, _ = os.path.splitext(os.path.basename(args.conf))
    module = SourceFileLoader(name, args.conf).load_module()
    if module is not None:
        config.update((k, v) for k, v in inspect.getmembers(module) if k.isupper())

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    run(os.path.dirname(os.path.abspath(args.conf)), config, os.path.abspath(args.templates))
