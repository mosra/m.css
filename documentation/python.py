#!/usr/bin/env python3

#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024
#             Vladimír Vondruš <mosra@centrum.cz>
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

import argparse
import copy
import docutils
import docutils.core
import docutils.utils
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
import typing

from enum import Enum
from types import SimpleNamespace as Empty
from importlib.machinery import SourceFileLoader
from typing import Tuple, Dict, Set, Any, List, Callable, Optional, Union
from urllib.parse import urljoin
from docutils.transforms import Transform

import jinja2

from _search import CssClass, ResultFlag, ResultMap, Trie, Serializer, serialize_search_data, base85encode_search_data, searchdata_format_version, search_filename, searchdata_filename, searchdata_filename_b85

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plugins'))
import m.htmlsanity

default_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/python/')

special_pages = ['index', 'modules', 'classes', 'pages']

class EntryType(Enum):
    # Order must match the search_type_map below; first value is reserved for
    # ResultFlag.ALIAS
    PAGE = 1
    MODULE = 2
    CLASS = 3
    FUNCTION = 4
    PROPERTY = 5
    ENUM = 6
    ENUM_VALUE = 7
    DATA = 8

    # Types not exposed to search are below. Deliberately set to large values
    # so their accidental use triggers assertions when building search data.

    # Statically linked data, such as images. Passed only to the URL_FORMATTER.
    STATIC = 98
    # One of files from special_pages. Doesn't make sense to include in the
    # search.
    SPECIAL = 99
    # Denotes a potentially overloaded pybind11 function. Has to be here to
    # be able to distinguish between zero-argument normal and pybind11
    # functions. To search it's exposed as FUNCTION.
    OVERLOADED_FUNCTION = 100

# Order must match the EntryType above
search_type_map = [
    (CssClass.SUCCESS, "page"),
    (CssClass.PRIMARY, "module"),
    (CssClass.PRIMARY, "class"),
    (CssClass.INFO, "func"),
    (CssClass.WARNING, "property"),
    (CssClass.PRIMARY, "enum"),
    (CssClass.DEFAULT, "enum val"),
    (CssClass.DEFAULT, "data")
]

# TODO: what about nested pages, how to format?
# [default-url-formatter]
def default_url_formatter(type: EntryType, path: List[str]) -> Tuple[str, str]:
    if type == EntryType.STATIC:
        url = os.path.basename(path[0])

        # Encode version information into the search driver
        if url == 'search.js':
            url = 'search-v{}.js'.format(searchdata_format_version)

        return url, url

    url = '.'.join(path) + '.html'
    assert '/' not in url
    return url, url
# [/default-url-formatter]

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
    'PROJECT_LOGO': None,
    'MAIN_PROJECT_URL': None,

    'INPUT': None,
    'OUTPUT': 'output',
    'OUTPUT_STUBS': None,
    'INPUT_MODULES': [],
    'INPUT_PAGES': [],
    'INPUT_DOCS': [],

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

    'HTML_HEADER': None,
    'PAGE_HEADER': None,
    'FINE_PRINT': '[default]',
    'FORMATTED_METADATA': ['summary'],

    'PLUGINS': [],
    'PLUGIN_PATHS': [],

    'CLASS_INDEX_EXPAND_LEVELS': 1,
    'CLASS_INDEX_EXPAND_INNER': False,

    'NAME_MAPPING': {},
    'PYBIND11_COMPATIBILITY': False,
    'ATTRS_COMPATIBILITY': False,

    'SEARCH_DISABLED': False,
    'SEARCH_DOWNLOAD_BINARY': False,
    'SEARCH_FILENAME_PREFIX': 'searchdata',
    'SEARCH_RESULT_ID_BYTES': 2,
    'SEARCH_FILE_OFFSET_BYTES': 3,
    'SEARCH_NAME_SIZE_BYTES': 1,
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
    'ID_FORMATTER': default_id_formatter,

    'STUB_EXTENSION': '.pyi',
    'STUB_HEADER': "# This file is a stub generated by m.css out of actual Python code. Don't edit\n# directly, modify the original code and regenerate.",
}

class State:
    def __init__(self, config):
        self.config = config
        self.name_mapping: Dict[str, str] = copy.deepcopy(config['NAME_MAPPING'])
        self.module_docs: Dict[str, Dict[str, str]] = {}
        self.class_docs: Dict[str, Dict[str, str]] = {}
        self.enum_docs: Dict[str, Dict[str, str]] = {}
        self.enum_value_docs: Dict[str, Dict[str, str]] = {}
        self.function_docs: Dict[str, Dict[str, str]] = {}
        self.property_docs: Dict[str, Dict[str, str]] = {}
        self.data_docs: Dict[str, Dict[str, str]] = {}
        self.external_data: Set[str] = set()

        self.hooks_post_crawl: List = []
        self.hooks_docstring: List = []
        self.hooks_pre_scope: List = []
        self.hooks_post_scope: List = []
        self.hooks_pre_page: List = []
        self.hooks_post_run: List = []

        self.name_map: Dict[str, Empty] = {}
        self.search: List[Any] = []

        self.crawled: Set[object] = set()

        # For collecting module dependencies (i.e., what to import to have all
        # used types known). The `current_module` gets set to the module name
        # at start of render_module() and render_class(), is cleared again when
        # the functions exit.
        #
        # Cannot be just `current_module_dependencies`, because
        self.current_module: Optional[str] = None
        # Should be filled only through add_module_dependency_for()
        self.module_dependencies: Dict[str, Set[str]] = {}

        # If we're generating stubs, parsed classes have to be saved and then
        # rendered together with the rest of the module.
        if self.config['OUTPUT_STUBS']:
            # Key is path including the class name, value is a parsed class
            self.parsed_classes: Dict[List[str], Empty] = {}
        else:
            self.parsed_classes = None

def map_name_prefix(state: State, type: str) -> str:
    for prefix, replace in state.name_mapping.items():
        if type == prefix or type.startswith(prefix + '.'):
            return replace + type[len(prefix):]

    # No mapping found, return the type as-is
    return type

def object_type(state: State, object, name) -> EntryType:
    if inspect.ismodule(object): return EntryType.MODULE
    if inspect.isclass(object):
        if (inspect.isclass(object) and issubclass(object, enum.Enum)) or (state.config['PYBIND11_COMPATIBILITY'] and hasattr(object, '__members__')):
            return EntryType.ENUM
        else: return EntryType.CLASS
    if inspect.isfunction(object) or inspect.isbuiltin(object) or inspect.isroutine(object):
        if state.config['PYBIND11_COMPATIBILITY'] and object.__doc__ and object.__doc__.startswith("{}(*args, **kwargs)\nOverloaded function.\n\n".format(name)):
            return EntryType.OVERLOADED_FUNCTION
        else:
            return EntryType.FUNCTION
    if inspect.isdatadescriptor(object):
        return EntryType.PROPERTY
    # Assume everything else is data. The builtin help help() (from pydoc) does
    # the same: https://github.com/python/cpython/blob/d29b3dd9227cfc4a23f77e99d62e20e063272de1/Lib/pydoc.py#L113
    if not inspect.isframe(object) and not inspect.istraceback(object) and not inspect.iscode(object):
        return EntryType.DATA

    # caller should print a warning in this case
    return None # pragma: no cover

def is_docstring_useless(type: EntryType, docstring):
    # Enum doc is by default set to a generic value. That's very useless.
    if type == EntryType.ENUM and docstring == 'An enumeration.': return True
    return not docstring or not docstring.strip()

def is_underscored_and_undocumented(state: State, type, path, docstring):
    if type == EntryType.MODULE:
        external_docs = state.module_docs
    elif type == EntryType.CLASS:
        external_docs = state.class_docs
    elif type == EntryType.ENUM:
        external_docs = state.enum_docs
    elif type in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION]:
        external_docs = state.function_docs
    elif type == EntryType.PROPERTY:
        external_docs = state.property_docs
    elif type == EntryType.DATA:
        external_docs = state.data_docs
        # Data don't have docstrings, those are from their type instead
        docstring = None
    else:
        assert type is None, type
        external_docs = {}

    return path[-1].startswith('_') and '.'.join(path) not in external_docs and is_docstring_useless(type, docstring)

# Builtin dunder functions have hardcoded docstrings. This is totally useless
# to have in the docs, so filter them out. Uh... kinda ugly.
_filtered_builtin_functions = set([
    # https://github.com/python/cpython/blob/401fff7423ca3c8bf1d02e594edfd1412616a559/Objects/typeobject.c#L10470
    # Matching the order there, be sure to follow it when updating
    ('__repr__', "Return repr(self)."),
    ('__hash__', "Return hash(self)."),
    ('__call__', "Call self as a function."),
    ('__str__', "Return str(self)."),
    ('__getattribute__', "Return getattr(self, name)."),
    ('__getattr__', "Implement getattr(self, name)."),
    ('__setattr__', "Implement setattr(self, name, value)."),
    ('__delattr__', "Implement delattr(self, name)."),
    ('__lt__', "Return self<value."),
    ('__le__', "Return self<=value."),
    ('__eq__', "Return self==value."),
    ('__ne__', "Return self!=value."),
    ('__gt__', "Return self>value."),
    ('__ge__', "Return self>=value."),
    ('__iter__', "Implement iter(self)."),
    ('__next__', "Implement next(self)."),
    ('__get__', "Return an attribute of instance, which is of type owner."),
    ('__set__', "Set an attribute of instance to value."),
    ('__delete__', "Delete an attribute of instance."),
    ('__init__',
        "Initialize self.  See help(type(self)) for accurate signature."),
    ('__new__',
        "Create and return a new object.  See help(type) for accurate signature."),
    ('__del__', "Called when the instance is about to be destroyed."),
    # TODO there's many more, maybe just add all?

    # https://github.com/python/cpython/blob/401fff7423ca3c8bf1d02e594edfd1412616a559/Objects/typeobject.c#L7342
    ('__init_subclass__',
        "This method is called when a class is subclassed.\n\n"
        "The default implementation does nothing. It may be\n"
        "overridden to extend subclasses.\n"),
    # https://github.com/python/cpython/blob/401fff7423ca3c8bf1d02e594edfd1412616a559/Objects/typeobject.c#L7328
    ('__subclasshook__',
        "Abstract classes can override this to customize issubclass().\n\n"
        "This is invoked early on by abc.ABCMeta.__subclasscheck__().\n"
        "It should return True, False or NotImplemented.  If it returns\n"
        "NotImplemented, the normal algorithm is used.  Otherwise, it\n"
        "overrides the normal algorithm (and the outcome is cached).\n")
])

# Python 3.6 has slightly different docstrings than 3.7
if sys.version_info >= (3, 7):
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

# Python 3.11 adds another
if sys.version_info >= (3, 11):
    _filtered_builtin_functions.update({
        ('__getstate__', "Helper for pickle.")
    })

# Python 3.12 changes the __format__ docstring
if sys.version_info >= (3, 11):
    _filtered_builtin_functions.update({
        ('__format__', "Default object formatter.\n\nReturn str(self) if format_spec is empty. Raise TypeError otherwise.")
    })

_filtered_builtin_properties = set([
    # https://github.com/python/cpython/blob/0d9d56c4e4246495f506f7fb319548fb105b535b/Objects/typeobject.c#L3553
    # (if defined) is gone in https://github.com/python/cpython/issues/112266
    # which is backported all the way to 3.11
    ('__dict__', "dictionary for instance variables" if sys.version_info >= (3, 11) else "dictionary for instance variables (if defined)"),
    ('__weakref__', "list of weak references to the object" if sys.version_info >= (3, 11) else "list of weak references to the object (if defined)")
])

_automatically_created_by_attrs = """
        Automatically created by attrs.
        """
_automatically_created_by_attrs_even_more_indented = """
            Automatically created by attrs.
            """
_generated_by_attrs_template = "Method generated by attrs for class XXX."
_filtered_attrs_functions = set([
    ('__ne__', """
    Check equality and either forward a NotImplemented or return the result
    negated.
    """),
    ('__lt__', _automatically_created_by_attrs),
    ('__le__', _automatically_created_by_attrs),
    ('__gt__', _automatically_created_by_attrs),
    ('__ge__', _automatically_created_by_attrs),
    ('__repr__', _automatically_created_by_attrs),
    ('__getstate__', _automatically_created_by_attrs_even_more_indented),
    ('__setstate__', _automatically_created_by_attrs_even_more_indented),
    # Attrs 20.1 override the above with a generic doc afterwards (ew, dirty)
    # and add __eq__() as well (before it had no docstring at all).
    # The __init__() has this generic doc as well, but we don't want to hide it
    # because it contains vital information on how to construct the class
    # TODO remove the originals once support for older attrs is dropped
    ('__eq__', _generated_by_attrs_template),
    ('__ne__', _generated_by_attrs_template),
    ('__lt__', _generated_by_attrs_template),
    ('__le__', _generated_by_attrs_template),
    ('__gt__', _generated_by_attrs_template),
    ('__ge__', _generated_by_attrs_template),
    ('__repr__', _generated_by_attrs_template),
])

def crawl_enum(state: State, path: List[str], enum_, parent_url):
    enum_entry = Empty()
    enum_entry.type = EntryType.ENUM
    enum_entry.object = enum_
    enum_entry.path = path
    enum_entry.url = '{}#{}'.format(parent_url, state.config['ID_FORMATTER'](EntryType.ENUM, path[-1:]))
    enum_entry.css_classes = ['m-doc']
    enum_entry.values = []

    if issubclass(enum_, enum.Enum):
        for i in enum_:
            subpath = path + [i.name]
            entry = Empty()
            entry.type = EntryType.ENUM_VALUE
            entry.path = subpath
            entry.url = '{}#{}'.format(parent_url, state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, subpath[-2:]))
            entry.css_classes = ['m-doc']
            state.name_map['.'.join(subpath)] = entry

    elif state.config['PYBIND11_COMPATIBILITY']:
        assert hasattr(enum_, '__members__')

        for name in enum_.__members__:
            subpath = path + [name]
            entry = Empty()
            entry.type = EntryType.ENUM_VALUE
            entry.path = subpath
            entry.url = '{}#{}'.format(parent_url, state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, subpath[-2:]))
            entry.css_classes = ['m-doc']
            state.name_map['.'.join(subpath)] = entry

    # Add itself to the name map
    state.name_map['.'.join(path)] = enum_entry

def crawl_class(state: State, path: List[str], class_):
    assert inspect.isclass(class_)

    # If this fires, it means there's a class duplicated in more than one
    # __all__ (or it gets picked up implicitly and then in __all__). It usually
    # means there's a mess in imports, unfortunately this is more common than
    # one would hope so we can't just assert.
    if id(class_) in state.crawled:
        for name, previous_entry in state.name_map.items():
            # Enum value entries don't have the object property, don't try to
            # match them
            if hasattr(previous_entry, 'object') and id(previous_entry.object) == id(class_):
                break
        else: # pragma: no cover
            assert False, "%s marked as crawled but can't find it" % '.'.join(path)
        logging.error("Class %s previously found in %s, only one occurrence will be chosen. Ensure each class is exposed only in a single module for generating correct documentation.", '.'.join(path), '.'.join(previous_entry.path))
        state.name_map['.'.join(path)] = previous_entry
        return

    state.crawled.add(id(class_))

    class_entry = Empty()
    class_entry.type = EntryType.CLASS
    class_entry.object = class_
    class_entry.path = path
    class_entry.css_classes = ['m-doc']
    class_entry.url = state.config['URL_FORMATTER'](EntryType.CLASS, path)[1]
    class_entry.members = []

    for name, object in inspect.getmembers(class_):
        type_ = object_type(state, object, name)
        subpath = path + [name]

        # Crawl the subclasses recursively (they also add itself to the
        # name_map)
        if type_ == EntryType.CLASS:
            if name in ['__base__', '__class__']:
                continue # TODO
            # Classes derived from typing.Generic in 3.6 have a _gorg property
            # that causes a crawl cycle, firing an assert in crawl_class(). Not
            # present from 3.7 onwards. Can't use isinstance(object, Generic)
            # because "Class typing.Generic cannot be used with class or
            # instance checks" (ugh), object.__base__ == Generic is also not
            # enough because it fails for typing.Iterator.__base__.
            if sys.version_info < (3, 7) and name == '_gorg' and type(object) == typing.GenericMeta: continue
            # __next_in_mro__ is an internal typing thing in 3.6, ignore as
            # well
            if sys.version_info < (3, 7) and name == '__next_in_mro__': continue
            if is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue

            crawl_class(state, subpath, object)

        # Crawl enum values (they also add itself to the name_map)
        elif type_ == EntryType.ENUM:
            if is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue

            crawl_enum(state, subpath, object, class_entry.url)

        # Add other members directly
        else:
            # Filter out private / unwanted members
            if type_ in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION]:
                # Filter out undocumented underscored methods (but not dunder
                # methods such as __init__)
                # TODO: this won't look into docs saved under a signature but
                #   for that we'd need to parse the signature first, ugh
                if not (name.startswith('__') and name.endswith('__')) and is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue
                # Filter out dunder methods that ...
                if name.startswith('__'):
                    # ... don't have their own docs
                    if (name, object.__doc__) in _filtered_builtin_functions: continue
                    # are added by typing.Generic on Py3.7+. Like above, can't
                    # use isinstance(object, Generic) because "Class
                    # typing.Generic cannot be used with class or instance
                    # checks"
                    if sys.version_info >= (3, 7) and name == '__init_subclass__':
                        # Before 3.12 it's completely undocumented and there's
                        # nothing else to catch on, so this filters out all
                        # undocumented cases
                        if sys.version_info < (3, 12) and not object.__doc__:
                            continue
                        # https://github.com/python/cpython/blame/401fff7423ca3c8bf1d02e594edfd1412616a559/Objects/typevarobject.c#L2175
                        if object.__doc__ == "Function to initialize subclasses.":
                            continue
                    if sys.version_info >= (3, 7) and name == '__class_getitem__':
                        # Before 3.11 it's completely undocumented and there's
                        # nothing else to catch on, so this filters out all
                        # undocumented cases
                        if sys.version_info < (3, 11) and not object.__doc__:
                            continue
                        # In 3.11 they OTOH get something very unique,
                        # especially the markdown-like formatting
                        # https://github.com/python/cpython/pull/31021
                        # In 3.12 the extra spaces are removed
                        if sys.version_info >= (3, 12) and object.__doc__.startswith("Parameterizes a generic class.\n\nAt least, parameterizing a generic class is the *main* thing"):
                            continue
                        if sys.version_info >= (3, 11) and object.__doc__.startswith("Parameterizes a generic class.\n\n        At least, parameterizing a generic class is the *main* thing"):
                            continue
                    # ... or are auto-generated by attrs
                    if state.config['ATTRS_COMPATIBILITY']:
                        # All methods generated by attrs 20.1+ have a generic
                        # docstring that contains the class name.
                        if (name, (object.__doc__ or '').replace(path[-1], 'XXX')) in _filtered_attrs_functions:
                            continue
                        # Before 20.1, the __eq__() unfortunately doesn't have
                        # a docstring, try to match it just from the param
                        # names
                        # TODO remove once support for older attrs is dropped
                        if name == '__eq__' and object.__doc__ is None:
                            try:
                                signature = inspect.signature(object)
                                if 'self' in signature.parameters and 'other' in signature.parameters:
                                    continue
                            except ValueError: # pragma: no cover
                                pass
            elif type_ == EntryType.PROPERTY:
                if (name, object.__doc__) in _filtered_builtin_properties: continue
                # TODO: are there any interesting dunder props?
                if is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue
            elif type_ == EntryType.DATA:
                if is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue
            else: # pragma: no cover
                assert type_ is None; continue # ignore unknown object types

            entry = Empty()
            entry.type = type_
            entry.object = object
            entry.path = subpath
            entry.url = '{}#{}'.format(class_entry.url, state.config['ID_FORMATTER'](type_, subpath[-1:]))
            entry.css_classes = ['m-doc']
            state.name_map['.'.join(subpath)] = entry

        class_entry.members += [name]

    # Data that don't have values but just type annotations are hidden here.
    # inspect.getmembers() ignores those probably because trying to access any
    # of them results in an AttributeError.
    if hasattr(class_, '__annotations__'):
        for name, type_ in class_.__annotations__.items():
            subpath = path + [name]

            # No docstrings (the best we could get would be a docstring of the
            # variable type, nope to that)
            if is_underscored_and_undocumented(state, EntryType.DATA, subpath, None): continue

            # If this name is known already, skip it -- here we don't have
            # anything except name and type, data inspected the classic way
            # have at least an object to point to (and a value)
            if name in class_entry.members: continue

            entry = Empty()
            entry.type = EntryType.DATA
            entry.object = None # TODO will this break things?
            entry.path = subpath
            entry.url = '{}#{}'.format(class_entry.url, state.config['ID_FORMATTER'](EntryType.DATA, subpath[-1:]))
            state.name_map['.'.join(subpath)] = entry
            class_entry.members += [name]

    # If attrs compatibility is enabled, look for more properties in hidden
    # places.
    if state.config['ATTRS_COMPATIBILITY'] and hasattr(class_, '__attrs_attrs__'):
        for attrib in class_.__attrs_attrs__:
            subpath = path + [attrib.name]

            # No docstrings for attrs (the best we could get would be a
            # docstring of the variable type, nope to that)
            if is_underscored_and_undocumented(state, EntryType.PROPERTY, subpath, None): continue

            # In some cases, the attribute can be present also among class
            # data (for example when using slots). Prefer the info provided by
            # attrs (instead of `continue`) as it can provide type annotation
            # also when the native annotation isn't used
            if attrib.name not in class_entry.members:
                class_entry.members += [attrib.name]

            entry = Empty()
            entry.type = EntryType.PROPERTY # TODO: or data?
            entry.object = attrib
            entry.path = subpath
            entry.url = '{}#{}'.format(class_entry.url, state.config['ID_FORMATTER'](EntryType.PROPERTY, subpath[-1:])) # TODO: or data?
            state.name_map['.'.join(subpath)] = entry

    # Add itself to the name map
    state.name_map['.'.join(path)] = class_entry

def crawl_module(state: State, path: List[str], module) -> List[Tuple[List[str], object]]:
    assert inspect.ismodule(module)

    # Assume this module is not crawled yet -- the parent crawl shouldn't even
    # put it to members if it's crawled already. Otherwise add itself to
    # the list of crawled objects to avoid going through it again.
    assert id(module) not in state.crawled
    state.crawled.add(id(module))

    # This module isn't a duplicate, thus we can now safely add itself to
    # parent's members, if this is not a root module
    if len(path) > 1:
        # It's possible to supply nested modules in INPUT_MODULES, but for each
        # such module all parents should be listed as well. We could probably
        # add some dummies for the missing modules but the extra logic for
        # deduplicating those if they get actually crawled later etc etc is
        # way more complicated than just telling the user to list everything.
        parent_path_str = '.'.join(path[:-1])
        assert parent_path_str in state.name_map, "%s listed in INPUT_MODULES without %s being known yet, add the parent explicitly earlier" % ('.'.join(path), parent_path_str)
        state.name_map[parent_path_str].members += [path[-1]]

    module_entry = Empty()
    module_entry.type = EntryType.MODULE
    module_entry.object = module
    module_entry.path = path
    module_entry.css_classes = ['m-doc']
    module_entry.url = state.config['URL_FORMATTER'](EntryType.MODULE, path)[1]
    module_entry.members = []

    # This gets returned to ensure the modules get processed in a breadth-first
    # order
    submodules_to_crawl: List[Tuple[List[str], object]] = []

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
                assert object.__name__ not in state.name_mapping
                state.name_mapping[object.__name__] = '.'.join(subpath)
            # logging.Logger objects have __module__ but don't have __name__,
            # check both
            elif hasattr(object, '__module__') and hasattr(object, '__name__'):
                subname = object.__module__ + '.' + object.__name__
                if subname != '.'.join(subpath):
                    assert subname not in state.name_mapping
                    state.name_mapping[subname] = '.'.join(subpath)

        # Now extract the actual docs
        for name in module.__all__:
            object = getattr(module, name)
            subpath = path + [name]
            type_ = object_type(state, object, name)

            # Crawl the submodules and subclasses recursively (they also add
            # itself to the name_map), add other members directly.
            if not type_: # pragma: no cover
                logging.warning("unknown symbol %s in %s", name, '.'.join(path))
                continue
            elif type_ == EntryType.MODULE:
                # TODO: this might fire if a module is in __all__ after it was
                # picked up implicitly before -- how to handle gracefully?
                assert id(object) not in state.crawled
                submodules_to_crawl += [(subpath, object)]
                # Not adding to module_entry.members, done by the nested
                # crawl_module() itself if it is sure that it isn't a
                # duplicated module
                continue
            elif type_ == EntryType.CLASS:
                crawl_class(state, subpath, object)
            elif type_ == EntryType.ENUM:
                crawl_enum(state, subpath, object, module_entry.url)
            else:
                assert type_ in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION, EntryType.DATA]
                entry = Empty()
                entry.type = type_
                entry.object = object
                entry.path = subpath
                entry.url = '{}#{}'.format(module_entry.url, state.config['ID_FORMATTER'](
                    # We have just one entry for all functions (and we don't
                    # know the parameters yet) so the link should lead to the
                    # generic name, not a particular overload
                    type_ if type_ != EntryType.OVERLOADED_FUNCTION else EntryType.FUNCTION,
                    subpath[-1:]))
                entry.css_classes = ['m-doc']
                state.name_map['.'.join(subpath)] = entry

            module_entry.members += [name]

    # Otherwise, enumerate the members using inspect. However, inspect lists
    # also imported modules, functions and classes, so take only those which
    # have __module__ equivalent to `path`.
    else:
        for name, object in inspect.getmembers(module):
            # If this is not a module, check if the enclosing module of the
            # object is what expected. If not, it's a class/function/...
            # imported from elsewhere and we don't want those.
            # TODO: xml.dom.domreg says the things from it should be imported
            #   as xml.dom.foo() and this check discards them, can it be done
            #   without manually adding __all__?
            if not inspect.ismodule(object):
                # Variables don't have the __module__ attribute, so check for
                # its presence. Right now *any* variable will be present in the
                # output, as there is no way to check where it comes from.
                if hasattr(object, '__module__') and map_name_prefix(state, object.__module__) != '.'.join(path):
                    continue

            # If this is a module, then things get complicated again and we
            # need to handle modules and packages differently. See also for
            # more info: https://stackoverflow.com/a/7948672
            else:
                # pybind11 submodules have __package__ set to None (instead of
                # '') for nested modules. Allow these. The parent's __package__
                # can be None (if it's a nested submodule), '' (if it's a
                # top-level module) or a string (if the parent is a Python
                # package), can't really check further.
                if state.config['PYBIND11_COMPATIBILITY'] and object.__package__ is None:
                    pass # yes, do nothing

                # The parent is a single-file module (not a package), these
                # don't have submodules so this is most definitely an imported
                # module. Source: https://docs.python.org/3/reference/import.html#packages
                elif not module.__package__: continue

                # The parent is a package and this is either a submodule or a
                # subpackage. Check that the __package__ of parent and child is
                # either the same or it's parent + child name
                elif object.__package__ not in [module.__package__, module.__package__ + '.' + name]: continue

            type_ = object_type(state, object, name)
            subpath = path + [name]

            # Filter out undocumented underscored names
            if is_underscored_and_undocumented(state, type_, subpath, object.__doc__): continue

            # Crawl the submodules and subclasses recursively (they also add
            # itself to the name_map), add other members directly.
            if type_ is None: # pragma: no cover
                # Ignore unknown object types (with __all__ we warn instead)
                continue
            elif type_ == EntryType.MODULE:
                submodules_to_crawl += [(subpath, object)]
                # Not adding to module_entry.members, done by the nested
                # crawl_module() itself if it is sure that it isn't a
                # duplicated module
                continue
            elif type_ == EntryType.CLASS:
                crawl_class(state, subpath, object)
            elif type_ == EntryType.ENUM:
                crawl_enum(state, subpath, object, module_entry.url)
            else:
                assert type_ in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION, EntryType.DATA]
                entry = Empty()
                entry.type = type_
                entry.object = object
                entry.path = subpath
                entry.url = '{}#{}'.format(module_entry.url, state.config['ID_FORMATTER'](
                    # We have just one entry for all functions (and we don't
                    # know the parameters yet) so the link should lead to the
                    # generic name, not a particular overload
                    type_ if type_ != EntryType.OVERLOADED_FUNCTION else EntryType.FUNCTION,
                    subpath[-1:]))
                entry.css_classes = ['m-doc']
                state.name_map['.'.join(subpath)] = entry

            module_entry.members += [name]

    # TODO: expose what's in __attributes__ as well (interaction with __all__?)

    # Add itself to the name map
    state.name_map['.'.join(path)] = module_entry

    return submodules_to_crawl

def make_relative_name(state: State, referrer_path: List[str], name):
    if name not in state.name_map:
        return name

    entry = state.name_map[name]

    # Strip common prefix from both paths. We always want to keep at least one
    # element from the entry path, so strip the last element off.
    common_prefix_length = len(os.path.commonprefix([referrer_path, entry.path[:-1]]))

    # Check for ambiguity of the shortened path -- for example, with referrer
    # being `module.sub.Foo`, target `module.Foo`, the path will get shortened
    # to `Foo`, making it seem like the target is `module.sub.Foo` instead of
    # `module.Foo`. To fix that, the shortened path needs to be `module.Foo`
    # instead of `Foo`.
    #
    # There's many corner cases, see test_inspect.InspectTypeLinks for the full
    # description, tests and verification against python's internal name
    # resolution rules.
    def is_ambiguous(shortened_path):
        # Concatenate the shortened path with a prefix of the referrer path,
        # going from longest to shortest, until we find a name that exists. If
        # the first found name is the actual target, it's not ambiguous --
        # for example, linking from `module.sub` to `module.sub.Foo` can be
        # done just with `Foo` even though `module.Foo` exists as well, as it's
        # "closer" to the referrer.
        for i in reversed(range(len(referrer_path))):
            potentially_ambiguous = referrer_path[:i] + shortened_path
            if '.'.join(potentially_ambiguous) in state.name_map:
                if potentially_ambiguous == entry.path:
                    return False
                else:
                    return True
        # the target *has to be* found
        assert False # pragma: no cover
    shortened_path = entry.path[common_prefix_length:]
    while common_prefix_length and is_ambiguous(shortened_path):
        common_prefix_length -= 1
        shortened_path = entry.path[common_prefix_length:]

    return '.'.join(shortened_path)

def make_name_relative_link(state: State, referrer_path: List[str], name) -> Tuple[str, str]:
    assert isinstance(name, str)

    # Not found, return as-is. However, if the prefix is one of the
    # INPUT_MODULES, emit a warning to notify the user of a potentially missing
    # stuff from the docs.
    if not name in state.name_map:
        for module in state.config['INPUT_MODULES']:
            if isinstance(module, str):
                module_name = module
            else:
                module_name = module.__name__
            if name.startswith(module_name + '.'):
                logging.warning("could not resolve a link to %s which is among INPUT_MODULES (referred from %s), possibly hidden/undocumented?", name, '.'.join(referrer_path))
                break
        return name, name

    # Make a shorter name that's relative to the referrer but still unambiguous
    relative_name = make_relative_name(state, referrer_path, name)

    entry = state.name_map[name]
    return relative_name, '<a href="{}" class="{}">{}</a>'.format(entry.url, ' '.join(entry.css_classes), relative_name)

def extract_type(type) -> str:
    # For types we concatenate the type name with its module unless it's
    # builtins (i.e., we want re.Match but not builtins.int). We need to use
    # __qualname__ instead of __name__ because __name__ doesn't take nested
    # classes into account.
    return (type.__module__ + '.' if type.__module__ != 'builtins' else '') + type.__qualname__

def enclosing_module_for(state: State, name: str) -> Optional[str]:
    path = name.split('.')
    for i in reversed(range(len(path))):
        name = '.'.join(path[:i])
        if name in state.name_map and state.name_map[name].type == EntryType.MODULE:
            return name
    return None

def add_module_dependency_for(state: State, object: Union[Any, str]) -> None:
    assert state.current_module

    # If not a string and not a module, try looking if its name-mapped type is
    # in our name map. If it is, and its enclosing module is as well, use that
    # to have name mapping correctly applied for it.
    name = None
    if not isinstance(object, str) and not inspect.ismodule(object):
        name_candidate = map_name_prefix(state, extract_type(object))
        if name_candidate in state.name_map:
            name = enclosing_module_for(state, name_candidate)

    # If the above didn't succeed, try other options
    if not name:
        # If it's a string, assume it's a parsed name that's already in the
        # name map, find the leaf module name and add it
        if isinstance(object, str):
            # We should get string names only for pybind11 types, nothing else
            # TODO er wait, what about unknown annotations? those probably
            #   shouldn't get here at all?
            assert state.config['PYBIND11_COMPATIBILITY']
            name = enclosing_module_for(state, object)
            # If there's no enclosing module, it's a builtin, for which we add
            # no dependency. Given that str is passed only from pybind, all
            # referenced names should be either builtin or known.
            if not name:
                assert '.' not in object
                return

        # If it's directly a module (such as `typing` or `enum` passed from
        # certain parts of the codebase), apply name mapping to it
        elif inspect.ismodule(object):
            name = map_name_prefix(state, object.__name__)

        # Otherwise it's a class/function/enum/..., extract module name from
        # it, apply name mapping
        else:
            name = map_name_prefix(state, object.__module__)

    # Add it only if it's not a module self-reference and if it's not builtins
    if name != 'builtins' and name != state.current_module:
        state.module_dependencies[state.current_module].add(name)

_pybind_name_rx = re.compile('[a-zA-Z0-9_]*')
_pybind_arg_name_rx = re.compile('[/*a-zA-Z0-9_]+')
_pybind_type_rx = re.compile('[a-zA-Z0-9_.]+')

def _pybind11_extract_default_argument(string):
    """Consumes a balanced []()-expression at begin of input string until `,`
    or `)`, while also replacing all `<Enum.FOO: -12354>` with just
    `Enum.FOO`."""
    stack = []
    default = ''
    i = 0
    while i < len(string):
        c = string[i]

        # At the end, what follows is the next argument or end of the argument
        # list, exit with what we got so far
        if len(stack) == 0 and (c == ',' or c == ')'):
            return string[i:], default

        # Pybind 2.6+ enum in the form of <Enum.FOO_BAR: -2986>, extract
        # everything until the colon and discard the rest. It can however be a
        # part of a rogue C++ type name, so pick the < only if directly at the
        # start or after a space or bracket, and the > only if at the end
        # again.
        if c == '<' and (i == 0 or string[i - 1] in [' ', '(', '[']) and -1 < string.find(':', i + 1) < string.find('>', i + 1):
            name_end = string.index(':', i + 1)
            default += string[i + 1:name_end]
            i = string.index('>', name_end + 1) + 1

            if i < len(string) and string[i] not in [',', ')', ']']:
                raise SyntaxError("Unexpected content after enum value: `{}`".format(string[i:]))

            continue

        # It can also be stuff like <FooBar object at 0x1234>, which is useless
        # and should be replaced with just a '...'. Similar check as in the
        # above -- enums and unrepresentable values can be combined together,
        # so
        if c == '<' and (i == 0 or string[i - 1] in [' ', '(', '[']) and -1 < string.find(' object at 0x', i + 1) < string.find('>', i + 1):
            address_end = string.index(' object at 0x', i)
            default += '...'
            i = string.index('>', address_end + 1) + 1

            if i < len(string) and string[i] not in [',', ')', ']']:
                raise SyntaxError("Unexpected content after object address value: `{}`".format(string[i:]))

            continue

        # Brackets
        if c == '(':
            stack.append(')')
        elif c == '[':
            stack.append(']')
        elif c == ')' or c == ']':
            if len(stack) == 0 or c != stack.pop():
                raise SyntaxError("Unmatched {} at pos {} in `{}`".format(c, i, string))

        # If there would be find_first_not_of(), I wouldn't have to iterate
        # byte by byte LIKE A CAVEMAN
        default += string[i]
        i += 1

    raise SyntaxError("Unexpected end of `{}`".format(string))

def _pybind_map_name_prefix_or_add_typing_suffix(state: State, input_type: str):
    # As of pybind11 2.12, the names match https://peps.python.org/pep-0585/
    # which replaces the original typing.List, Dict etc. with actual builtin
    # types to avoid duplication. To make testing simpler, this tool makes them
    # follow PEP585 with older pybind11 as well.
    input_type_lowercase = input_type.lower()
    if input_type_lowercase in ['dict', 'list', 'set', 'tuple']:
        return input_type_lowercase
    if input_type in ['Callable', 'Iterator', 'Iterable', 'Optional', 'Union']:
        # current_module might be unset when calling this from unittests etc.
        if state.current_module:
            add_module_dependency_for(state, typing)
        return 'typing.' + input_type
    else:
        type = map_name_prefix(state, input_type)
        # current_module might be unset when calling this from unittests etc.
        if state.current_module:
            add_module_dependency_for(state, type)
        return type

def parse_pybind_type(state: State, referrer_path: List[str], signature: str) -> Tuple[str, str, str, str]:
    match = _pybind_type_rx.match(signature)
    if match:
        input_type = match.group(0)
        signature = signature[len(input_type):]
        type = _pybind_map_name_prefix_or_add_typing_suffix(state, input_type)
        type_relative, type_link = make_name_relative_link(state, referrer_path, type)
    else:
        raise SyntaxError("Cannot match pybind type")

    lvl = 0
    i = 0
    while i < len(signature):
        c = signature[i]
        if c == '[':
            i += 1
            lvl += 1
            type += c
            type_relative += c
            type_link += c
            continue
        if lvl == 0:
            break
        if c == ']':
            i += 1
            lvl -= 1
            type += c
            type_relative += c
            type_link += c
            continue
        if c in ', ':
            i += 1
            type += c
            type_relative += c
            type_link += c
            continue
        match = _pybind_type_rx.match(signature[i:])
        if match is None:
            raise SyntaxError("Bad python type name: {} ".format(signature[i:]))
        input_type = match.group(0)
        i += len(input_type)
        input_type = _pybind_map_name_prefix_or_add_typing_suffix(state, input_type)
        type += input_type
        input_type_relative, input_type_link = make_name_relative_link(state, referrer_path, input_type)
        type_relative += input_type_relative
        type_link += input_type_link
    if lvl != 0:
        raise SyntaxError("Unbalanced [] in python type {}".format(signature))
    signature = signature[i:]
    return signature, type, type_relative, type_link

# Returns function name, summary, list of arguments (name, type, type with HTML
# links, default value) and return type. If argument parsing failed, the
# argument list is a single "ellipsis" item.
def parse_pybind_signature(state: State, referrer_path: List[str], signature: str) -> Tuple[str, str, List[Tuple[str, str, str, str, str]], str, str, str]:
    original_signature = signature # For error reporting
    name = _pybind_name_rx.match(signature).group(0)
    signature = signature[len(name):]
    args = []
    assert signature[0] == '('
    signature = signature[1:]

    # parse_pybind_type() can throw a SyntaxError in case it gets confused,
    # provide graceful handling for that along with own parse errors
    try:
        # Arguments
        while signature[0] != ')':
            # Name
            arg_name = _pybind_arg_name_rx.match(signature).group(0)
            assert arg_name
            signature = signature[len(arg_name):]

            # Type (optional)
            if signature.startswith(': '):
                signature = signature[2:]
                signature, arg_type, arg_type_relative, arg_type_link = parse_pybind_type(state, referrer_path, signature)
            else:
                arg_type, arg_type_relative, arg_type_link = None, None, None

            # Default (optional)
            if signature.startswith(' = '):
                signature = signature[1 if signature[0] == '=' else 3:]
                signature, default = _pybind11_extract_default_argument(signature)
            else:
                default = None

            args += [(arg_name, arg_type, arg_type_relative, arg_type_link, default)]

            if signature[0] == ')': break

            # Expecting the next argument now, if not there, we failed
            if not signature.startswith(', '): raise SyntaxError("Expected comma and next argument, got `{}`".format(signature))
            signature = signature[2:]

        assert signature[0] == ')'
        signature = signature[1:]

        # Return type (optional)
        if signature.startswith(' -> '):
            signature = signature[4:]
            signature, return_type, return_type_relative, return_type_link = parse_pybind_type(state, referrer_path, signature)
        else:
            return_type, return_type_relative, return_type_link = None, None, None

        # Expecting end of the signature line now, if not there, we failed
        if signature and signature[0] != '\n': raise SyntaxError("Expected end of the signature, got `{}`".format(signature))

    # Failed to parse, return with a single parameter with name being None and
    # docs
    except SyntaxError as e:
        end = original_signature.find('\n')
        logging.warning("cannot parse pybind11 function signature %s: %s", (original_signature[:end if end != -1 else None]), e)
        if end != -1 and len(original_signature) > end + 1 and original_signature[end + 1] == '\n':
            docstring = inspect.cleandoc(original_signature[end + 1:])
        else:
            docstring = ''
        return (name, docstring, [(None, None, None, None, None)], None, None, None)

    if len(signature) > 1 and signature[1] == '\n':
        docstring = inspect.cleandoc(signature[2:])
    else:
        docstring = ''

    return (name, docstring, args, return_type, return_type_relative, return_type_link)

def parse_pybind_docstring(state: State, referrer_path: List[str], doc: str) -> List[Tuple[str, str, List[Tuple[str, str, str]], str]]:
    name = referrer_path[-1]

    # Multiple overloads, parse each separately. It's not possible to fully
    # prevent accidentally matching contents of the docstring as a next
    # overload so at least expect each overload to start with two newlines and
    # a monotonic counter number, which hopefully skips most cases where a
    # function is referenced in the middle of a paragraph.
    overload_header = "{}(*args, **kwargs)\nOverloaded function.".format(name);
    if doc.startswith(overload_header):
        doc = doc[len(overload_header):]
        overloads = []
        id = 1
        while True:
            assert doc.startswith('\n\n{}. {}('.format(id, name))
            id = id + 1
            next = doc.find('\n\n{}. {}('.format(id, name))

            # Parse the signature and docs from known slice
            overloads += [parse_pybind_signature(state, referrer_path, doc[len(str(id - 1)) + 4:next])]
            assert overloads[-1][0] == name
            if next == -1: break

            # Continue to the next signature
            doc = doc[next:]

        return overloads

    # Normal function, parse and return the first signature
    else:
        return [parse_pybind_signature(state, referrer_path, doc)]

# Used to format function default arguments and data values. *Not* pybind's
# function default arguments, as those are parsed from a string representation.
def format_value(state: State, referrer_path: List[str], value) -> Optional[Tuple[str, str, str]]:
    if value is None:
        return str(value), str(value), str(value)
    # pybind enums don't inherit from enum.Enum but have the __members__
    # attribute instead
    if isinstance(value, enum.Enum) or (state.config['PYBIND11_COMPATIBILITY'] and hasattr(value.__class__, '__members__')):
        name = '.'.join([value.__class__.__module__, value.__class__.__qualname__, value.name])
        # Adding the `enum` module as a dependency isn't enough, here we need
        # the actual enum value definitions
        add_module_dependency_for(state, value.__class__)
        # TODO Python 3.8+ supports `a, *b`, switch to that once 3.7 is dropped
        return (value.name, ) + make_name_relative_link(state, referrer_path, name)
    # isbuiltin returns true if object is a builtin _function_ or _method_, not
    # just any builtin such as the False literal
    elif inspect.isfunction(value) or inspect.isbuiltin(value):
        # TODO if the function is in our name map, return its name and link to
        #   it maybe?
        out = '...'
        return out, out, html.escape(out)
    # All classes inherit __repr__ from the object base class, which prints
    # stuff like '<Foo object at 0x72a03a835870>'. Not useful, so do this only
    # if __repr__ is directly on the actual object type.
    # TODO could also do `type(value).__repr__ is not object.__repr_` instead,
    #   maybe that would improve this for subclasses where the parent already
    #   defines a reasonable __repr__?
    elif '__repr__' in type(value).__dict__:
        rendered = repr(value)
        # TODO: tuples of non-representable values will still be ugly
        # If the value is too large, return just an ellipsis
        out = rendered if len(rendered) < 128 else '...'
        return out, out, html.escape(out)
    else:
        return None

def prettify_multiline_error(error: str) -> str:
    return ' | {}\n'.format(error.replace('\n', '\n | '))

def extract_docs(state: State, external_docs, type: EntryType, path: List[str], doc: str, *, signature=None, summary_only=False) -> Tuple[str, str]:
    path_str = '.'.join(path)
    # If function signature is supplied, try that first
    if signature and path_str + signature in external_docs:
        path_signature_str = path_str + signature
    # If there's already info for all overloads together (or this is not a
    # function), use that
    elif path_str in external_docs:
        path_signature_str = path_str
    # Otherwise, create a new entry for the most specific key possible. That
    # way we can add a different docstring for each overload without them
    # clashing together.
    else:
        path_signature_str = path_str + signature if signature else path_str
        external_docs[path_signature_str] = {}

    external_doc_entry = external_docs[path_signature_str]

    # If we have parsed summary and content already, don't bother with the
    # docstring. Otherwise hammer the docs out of it and save those for
    # later.
    if external_doc_entry.get('summary') is None or external_doc_entry.get('content') is None:
        # some modules (xml.etree) have None as a docstring :(
        doc = inspect.cleandoc(doc or '').strip()

        if doc:
            # Do the same as in render_doc() to support directives with
            # multi-word field names and duplicate fields, restore the original
            # implementations again after.
            prev_extract_options = docutils.utils.extract_options
            prev_assemble_option_dict = docutils.utils.assemble_option_dict
            docutils.utils.extract_options = _docutils_extract_options
            docutils.utils.assemble_option_dict = _docutils_assemble_option_dict

            # Go through all registered docstring hooks and let them process
            # this one after another; stopping once there's nothing left. If
            # nothing left, the populated entries should be non-None.
            for hook in state.hooks_docstring:
                try:
                    doc = hook(
                        type=type,
                        path=path,
                        signature=signature,
                        doc=doc)

                    # The hook could have replaced the entry with a new dict
                    # instance, fetch it again to avoid looking at stale data
                    # below
                    external_doc_entry = external_docs[path_signature_str]

                    # Once there's nothing left to parse, stop executing the
                    # hooks.
                    if not doc: break

                except docutils.utils.SystemMessage:
                    logging.error("Failed to process a docstring for %s, ignoring:\n%s", path_signature_str, prettify_multiline_error(doc))
                    break

            # If there's still something left after the hooks (or there are no
            # hooks), process it as a plain unformatted text.
            else:
                summary, _, content = doc.partition('\n\n')

                # Turn both into a raw HTML block so it doesn't get further
                # processed by reST. For the content, wrap each paragraph in
                # <p> so it looks acceptable in the output.
                if summary:
                    summary = html.escape(summary)
                    summary = ".. raw:: html\n\n    " + summary.replace('\n', '\n    ')
                if content:
                    content = '\n'.join(['<p>{}</p>'.format(p) for p in html.escape(content).split('\n\n')])
                    content = ".. raw:: html\n\n    " + content.replace('\n', '\n    ')

                if external_doc_entry.get('summary') is None:
                    external_doc_entry['summary'] = summary
                if external_doc_entry.get('content') is None:
                    external_doc_entry['content'] = content

            # Restore original implementations again
            docutils.utils.extract_options = prev_extract_options
            docutils.utils.assemble_option_dict = prev_assemble_option_dict

        # If there isn't anything supplied for summary / content even after all
        # the processing above, set it to an empty string so this branch isn't
        # entered again next time.
        if external_doc_entry.get('summary') is None:
            external_doc_entry['summary'] = ''
        if external_doc_entry.get('content') is None:
            external_doc_entry['content'] = ''

    # Render. This can't be done just once and then cached because e.g. math
    # rendering needs to ensure each SVG formula has unique IDs on each page.
    try:
        summary = render_inline_rst(state, external_doc_entry['summary'])
    except docutils.utils.SystemMessage:
        logging.error("Failed to process summary for %s, ignoring:\n%s", path_signature_str, prettify_multiline_error(external_doc_entry['summary']))
        summary = ''

    if summary_only: return summary

    try:
        content = render_rst(state, external_doc_entry['content'])
    except docutils.utils.SystemMessage:
        logging.error("Failed to process content for %s, ignoring:\n%s", path_signature_str, prettify_multiline_error(external_doc_entry['content']))
        content = ''

    # Mark the docs as used (so it can warn about unused docs at the end)
    external_doc_entry['used'] = True
    return summary, content

def get_type_hints_or_nothing(state: State, path: List[str], object) -> Dict:
    # Calling get_type_hints on a pybind11 type (from extract_data_doc())
    # results in KeyError because there's no sys.modules['pybind11_builtins'].
    # Be pro-active and return an empty dict if that's the case.
    if state.config['PYBIND11_COMPATIBILITY'] and isinstance(object, type) and 'pybind11_builtins' in [a.__module__ for a in object.__mro__]:
        return {}

    try:
        return typing.get_type_hints(object)
    except Exception as e:
        # Gracefully handle an invalid name or a missing attribute, give up on
        # everything else (syntax error and so)
        if not isinstance(e, (AttributeError, NameError)): raise e
        logging.warning("failed to dereference type hints for %s (%s), falling back to non-dereferenced", '.'.join(path), e.__class__.__name__)
        return {}

def quoted_annotation(annotation: str) -> str:
    return '\'{}\''.format(annotation.replace('\'', '\\\''))

def extract_annotation(state: State, referrer_path: List[str], annotation) -> Tuple[str, str, str]:
    # Empty annotation, as opposed to a None annotation, handled below
    if annotation is inspect.Signature.empty:
        return None, None, None

    # If dereferencing with typing.get_type_hints() failed, we might end up
    # with forward-referenced types being plain strings. Keep them as is, since
    # those are most probably an error, but quote for stubs.
    if type(annotation) == str:
        return annotation, quoted_annotation(annotation), annotation

    # Or the plain strings might be inside (e.g. List['Foo']), which gets
    # converted by Python to ForwardRef. Hammer out the actual string and again
    # leave it as-is, since it's most probably an error. Quote for stubs.
    elif isinstance(annotation, typing.ForwardRef if sys.version_info >= (3, 7) else typing._ForwardRef):
        return annotation.__forward_arg__, quoted_annotation(annotation.__forward_arg__), annotation.__forward_arg__

    # Generic type names -- use their name directly
    # TODO define the TypeVar somewhere somehow instead of lazy quoting
    elif isinstance(annotation, typing.TypeVar):
        return annotation.__name__, quoted_annotation(annotation.__name__), annotation.__name__

    # Ellipsis -- print a literal `...`
    # TODO: any chance to link this to python official docs?
    elif annotation is ...:
        return ('...', )*3

    # If the annotation is from the typing module, it ... gets complicated. It
    # could be a "bracketed" type, in which case we want to recurse to its
    # types as well.
    elif (hasattr(annotation, '__module__') and annotation.__module__ == 'typing'):
        add_module_dependency_for(state, typing)

        # Optional or Union, handle those first
        if hasattr(annotation, '__origin__') and annotation.__origin__ is typing.Union:
            # FOR SOME REASON `annotation.__args__[1] is None` is always False,
            # so we have to use isinstance(). HOWEVER, we *can't* use
            # isinstance if:
            #   - it's a "bracketed" type, having __args__
            #     (see the `annotation_union_second_bracketed()` test)
            #   - it's a ForwardRef because get_type_hints_or_nothing() failed
            #     due to a type error (see the `annotation_union_of_undefined()`
            #     test)
            # because it'll die. So check that first.
            if (len(annotation.__args__) == 2 and
                not hasattr(annotation.__args__[1], '__args__') and
                # Same 3.6 ForwardRef workaround as above
                not isinstance(annotation.__args__[1], typing.ForwardRef if sys.version_info >= (3, 7) else typing._ForwardRef) and
                isinstance(None, annotation.__args__[1])
            ):
                name = 'typing.Optional'
                args = annotation.__args__[:1]
            else:
                name = 'typing.Union'
                args = annotation.__args__
        elif sys.version_info >= (3, 7) and hasattr(annotation, '_name') and annotation._name:
            name = 'typing.' + annotation._name
            # Any doesn't have __args__
            args = annotation.__args__ if hasattr(annotation, '__args__') else None
        # Python 3.6 has __name__ instead of _name
        elif sys.version_info < (3, 7) and hasattr(annotation, '__name__'):
            name = 'typing.' + annotation.__name__
            args = annotation.__args__
        # Any doesn't have __name__ in 3.6, and doesn't have anything in 3.11+
        # Not sure what commit caused that, probably https://github.com/python/cpython/pull/31841
        elif (sys.version_info < (3, 7) or sys.version_info >= (3, 11)) and annotation is typing.Any:
            name = 'typing.Any'
            args = None
        # Whoops, something we don't know yet. Warn and return a string
        # representation at least.
        else: # pragma: no cover
            logging.warning("can't inspect annotation %s for %s, falling back to a string representation", annotation, '.'.join(referrer_path))
            return (str(annotation), )*3

        # Add type links to name
        name_relative, name_link = make_name_relative_link(state, referrer_path, name)

        # Arguments of generic types, recurse inside
        if args:
            # For Callable, put the arguments into a nested list to separate
            # them from the return type
            if name == 'typing.Callable':
                assert len(args) >= 1

                nested_types = []
                nested_types_quoted = []
                nested_type_links = []
                for i in args[:-1]:
                    nested_type, nested_type_quoted, nested_type_link = extract_annotation(state, referrer_path, i)
                    nested_types += [nested_type]
                    nested_types_quoted += [nested_type_quoted]
                    nested_type_links += [nested_type_link]
                nested_return_type, nested_return_type_quoted, nested_return_type_link = extract_annotation(state, referrer_path, args[-1])

                # If nested parsing failed (the invalid annotation below),
                # fail the whole thing
                if None in nested_types or nested_return_type is None:
                    return None, None, None

                return (
                    '{}[[{}], {}]'.format(name, ', '.join(nested_types), nested_return_type),
                    '{}[[{}], {}]'.format(name, ', '.join(nested_types_quoted), nested_return_type_quoted),
                    '{}[[{}], {}]'.format(name_link, ', '.join(nested_type_links), nested_return_type_link)
                )

            else:
                nested_types = []
                nested_types_quoted = []
                nested_type_links = []
                for i in args:
                    nested_type, nested_type_quoted, nested_type_link = extract_annotation(state, referrer_path, i)
                    nested_types += [nested_type]
                    nested_types_quoted += [nested_type_quoted]
                    nested_type_links += [nested_type_link]

                # If nested parsing failed (the invalid annotation below),
                # fail the whole thing
                if None in nested_types:
                    return None, None, None

                return (
                    '{}[{}]'.format(name, ', '.join(nested_types)),
                    '{}[{}]'.format(name_relative, ', '.join(nested_types_quoted)),
                    '{}[{}]'.format(name_link, ', '.join(nested_type_links)),
                )

        else: return name, name_relative, name_link

    # Things like (float, int) instead of Tuple[float, int] or using np.array
    # instead of np.ndarray. Ignore with a warning.
    elif not isinstance(annotation, type):
        logging.warning("invalid annotation %s in %s, ignoring", annotation, '.'.join(referrer_path))
        return None, None, None

    # According to https://www.python.org/dev/peps/pep-0484/#using-none,
    # None and type(None) are equivalent. Calling extract_type() on None would
    # give us NoneType, which is unnecessarily long.
    elif annotation is type(None):
        # TODO Python 3.8+ supports `a, *b`, switch to that once 3.7 is dropped
        return ('None', ) + make_name_relative_link(state, referrer_path, 'None')

    # Otherwise it's a plain type. Turn it into a link.
    add_module_dependency_for(state, annotation)
    name = map_name_prefix(state, extract_type(annotation))
    # TODO Python 3.8+ supports `a, *b`, switch to that once 3.7 is dropped
    return (name, ) + make_name_relative_link(state, referrer_path, name)

def extract_module_doc(state: State, entry: Empty):
    assert inspect.ismodule(entry.object)

    # Call all scope enter hooks first
    for hook in state.hooks_pre_scope:
        hook(type=entry.type, path=entry.path)

    out = Empty()
    out.url = entry.url
    out.name = entry.path[-1]
    out.summary = extract_docs(state, state.module_docs, entry.type, entry.path, entry.object.__doc__, summary_only=True)

    # Call all scope exit hooks last
    for hook in state.hooks_post_scope:
        hook(type=entry.type, path=entry.path)

    return out

def extract_class_doc(state: State, entry: Empty):
    assert inspect.isclass(entry.object)

    # Call all scope enter hooks first
    for hook in state.hooks_pre_scope:
        hook(type=entry.type, path=entry.path)

    out = Empty()
    out.url = entry.url
    out.name = entry.path[-1]
    out.summary = extract_docs(state, state.class_docs, entry.type, entry.path, entry.object.__doc__, summary_only=True)

    # Call all scope exit hooks last
    for hook in state.hooks_post_scope:
        hook(type=entry.type, path=entry.path)

    return out

def extract_enum_doc(state: State, entry: Empty):
    assert state.current_module

    out = Empty()
    out.name = entry.path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.ENUM, entry.path[-1:])
    out.values = []
    out.has_value_details = False
    out.has_details = False

    # The happy case
    if issubclass(entry.object, enum.Enum):
        # Enum doc is by default set to a generic value. That's useless as well.
        if is_docstring_useless(EntryType.ENUM, entry.object.__doc__):
            docstring = ''
        else:
            docstring = entry.object.__doc__

        # TODO should probably do some name mapping here also?
        out.base = extract_type(entry.object.__base__)
        # Add the base as a dependency so the stubs can derive from it
        add_module_dependency_for(state, entry.object.__base__)
        out.base_relative, out.base_link = make_name_relative_link(state, entry.path, out.base)

        for i in entry.object:
            value = Empty()
            value.name = i.name
            value.id = state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, entry.path[-1:] + [i.name])
            value.value = repr(i.value)

            # Value doc gets by default inherited from the enum, that's useless
            # This gets further processed below.
            if i.__doc__ == entry.object.__doc__:
                value.content = ''
            else:
                value.content = i.__doc__

            out.values += [value]

    # Pybind11 enums are ... different
    elif state.config['PYBIND11_COMPATIBILITY']:
        assert hasattr(entry.object, '__members__')

        # Pybind 2.4 puts enum value docs inside the docstring. We don't parse
        # that yet and it adds clutter to the output (especially if the values
        # aren't documented), so cut that away
        # TODO: implement this and populate each value.content
        docstring = entry.object.__doc__.partition('\n\n')[0]

        out.base = None
        # Add the enum module as a dependency, the stub template will make
        # enum.Enum a base to make it recognizable as an actual enum
        add_module_dependency_for(state, enum)

        for name, v in entry.object.__members__.items():
            value = Empty()
            value. name = name
            value.id = state.config['ID_FORMATTER'](EntryType.ENUM_VALUE, entry.path[-1:] + [name])
            value.value = str(int(v))
            value.content = ''
            out.values += [value]

    # Call all scope enter before rendering the docs
    for hook in state.hooks_pre_scope:
        hook(type=entry.type, path=entry.path)

    out.summary, out.content = extract_docs(state, state.enum_docs, entry.type, entry.path, docstring)
    if out.content: out.has_details = True

    for value in out.values:
        # Keeping the same scope for the value docs as for the outer scope.
        # There's no distinction between summary and content for enum
        # values so put that together in one. The summary is only produced by
        # the raw docstring parser, the m.sphinx directives always produce only
        # the content.
        summary, value.content = extract_docs(state, state.enum_value_docs, EntryType.ENUM_VALUE, entry.path + [value.name], value.content)
        if summary:
            value.content = '<p>{}</p>\n{}'.format(summary, value.content).rstrip()
        if value.content:
            out.has_details = True
            out.has_value_details = True

    # Call all scope exit hooks after
    for hook in state.hooks_post_scope:
        hook(type=entry.type, path=entry.path)

    if not state.config['SEARCH_DISABLED']:
        page_url = state.name_map['.'.join(entry.path[:-1])].url

        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.ENUM)
        result.url = '{}#{}'.format(page_url, out.id)
        result.prefix = entry.path[:-1]
        result.name = entry.path[-1]
        state.search += [result]

        for value in out.values:
            result = Empty()
            result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.ENUM_VALUE)
            result.url = '{}#{}'.format(page_url, value.id)
            result.prefix = entry.path
            result.name = value.name
            state.search += [result]

    return out

def extract_function_doc(state: State, parent, entry: Empty) -> List[Any]:
    assert state.current_module
    assert inspect.isfunction(entry.object) or inspect.ismethod(entry.object) or inspect.isroutine(entry.object)

    # Enclosing page URL for search
    if not state.config['SEARCH_DISABLED']:
        page_url = state.name_map['.'.join(entry.path[:-1])].url

    # Extract the signature from the docstring for pybind11, since it can't
    # expose it to the metadata: https://github.com/pybind/pybind11/issues/990
    # What's not solvable with metadata, however, are function overloads ---
    # one function in Python may equal more than one function on the C++ side.
    # To make the docs usable, list all overloads separately.
    #
    # Some shitty packages might be setting __doc__ to None (attrs is one of
    # them), explicitly check for that first.
    if state.config['PYBIND11_COMPATIBILITY'] and entry.object.__doc__ and entry.object.__doc__.startswith(entry.path[-1] + '('):
        funcs = parse_pybind_docstring(state, entry.path, entry.object.__doc__)
        # The crawl (and object_type()) should have detected the overloadedness
        # already, so check that we have that consistent
        assert (len(funcs) > 1) == (entry.type == EntryType.OVERLOADED_FUNCTION)
        overloads = []
        for name, summary, args, type, type_relative, type_link in funcs:
            out = Empty()
            out.name = name
            out.params = []
            out.has_complex_params = False
            out.has_details = False
            # The parsed pybind11 annotation either works as a whole, or not at
            # all, so it's never quoted, only relative
            out.type, out.type_quoted, out.type_link = type, type_relative, type_link

            # There's no other way to check staticmethods than to check for
            # self being the name of first parameter :( No support for
            # classmethods, as C++11 doesn't have that
            out.is_classmethod = False
            if inspect.isclass(parent):
                out.is_method = True
                if args and args[0][0] == 'self':
                    out.is_staticmethod = False
                else:
                    out.is_staticmethod = True
            else:
                out.is_method = False
                out.is_staticmethod = False

            # If the arguments contain a literal * or / (which is only if
            # py::pos_only{} or py::kw_only{} got explicitly used), it's
            # following the usual logic:
            for arg in args:
                # If / is among the arguments, everything until the / is
                # positional-only
                if arg[0] == '/':
                    param_kind = 'POSITIONAL_ONLY'
                    break
                # Otherwise, if * is among the arguments, everything until the
                # * is positional-or-keyword. Assuming pybind11 sanity, so
                # not handling cases where * would be before / and such.
                if arg[0] == '*':
                    param_kind = 'POSITIONAL_OR_KEYWORD'
                    break

            # If they don't contain either, guesstimate whether the arguments
            # are positional-only or position-or-keyword. It's either all or none.
            # This is a brown magic, sorry.
            else:
                # For instance methods positional-only argument names are
                # either self (for the first argument) or arg(I-1) (for second
                # argument and further). Also, the `self` argument is
                # positional-or-keyword only if there are positional-or-keyword
                # arguments after it, otherwise it's positional-only.
                if inspect.isclass(parent) and not out.is_staticmethod:
                    assert args and args[0][0] == 'self'

                    param_kind = 'POSITIONAL_ONLY'
                    for i, arg in enumerate(args[1:]):
                        if arg[0] != 'arg{}'.format(i):
                            param_kind = 'POSITIONAL_OR_KEYWORD'
                            break

                # For static methods or free functions positional-only
                # arguments are argI.
                else:
                    param_kind = 'POSITIONAL_ONLY'
                    for i, arg in enumerate(args):
                        if arg[0] != 'arg{}'.format(i):
                            param_kind = 'POSITIONAL_OR_KEYWORD'
                            break

            param_names = []
            param_types = []
            signature = []
            for i, arg in enumerate(args):
                arg_name, arg_type, arg_type_relative, arg_type_link, arg_default = arg
                param = Empty()
                param.name = arg_name
                param_names += [arg_name]

                # Skip * and / placeholders, update the param_kind instead
                if arg_name == '/':
                    assert param_kind == 'POSITIONAL_ONLY'
                    param_kind = 'POSITIONAL_OR_KEYWORD'
                    continue
                if arg_name == '*':
                    assert param_kind == 'POSITIONAL_OR_KEYWORD'
                    param_kind = 'KEYWORD_ONLY'
                    continue

                # Don't include redundant type for the self argument
                if i == 0 and arg_name == 'self':
                    param.type, param.type_quoted, param.type_link = None, None, None
                    param_types += [None]
                    signature += ['self']
                else:
                    # The parsed pybind11 annotation either works as a whole,
                    # or not at all, so it's never quoted, only relative
                    param.type, param.type_quoted, param.type_link = arg_type, arg_type_relative, arg_type_link
                    param_types += [arg_type]
                    signature += ['{}: {}'.format(arg_name, arg_type)]

                if arg_default:
                    # If the type is a registered enum, try to make a link to
                    # the value -- for an enum of type `module.EnumType`,
                    # assuming the default is rendered as `EnumType.VALUE` (not
                    # fully qualified), concatenate it together to have
                    # `module.EnumType.VALUE`
                    if arg_type in state.name_map and state.name_map[arg_type].type == EntryType.ENUM:
                        param.default = '.'.join(state.name_map[arg_type].path[:-1] + [arg_default])
                        param.default_relative, param.default_link = make_name_relative_link(state, entry.path, param.default)
                    else:
                        param.default, param.default_relative = arg_default, arg_default
                        param.default_link = html.escape(arg_default)
                else:
                    param.default, param.default_relative, param.default_link = None, None, None
                if arg_type or arg_default: out.has_complex_params = True

                # *args / **kwargs can still appear in the parsed signatures if
                # the function accepts py::args / py::kwargs directly
                if arg_name == '*args':
                    param.name = 'args'
                    param.kind = 'VAR_POSITIONAL'
                elif arg_name == '**kwargs':
                    param.name = 'kwargs'
                    param.kind = 'VAR_KEYWORD'
                else:
                    param.kind = param_kind

                out.params += [param]

            # Format the anchor, include types only if there's really more than
            # one overload
            if entry.type == EntryType.OVERLOADED_FUNCTION:
                out.id = state.config['ID_FORMATTER'](EntryType.OVERLOADED_FUNCTION, [name] + param_types)
            else:
                out.id = state.config['ID_FORMATTER'](EntryType.FUNCTION, [name])

            # Call all scope enter hooks for this particular overload
            for hook in state.hooks_pre_scope:
                hook(type=entry.type, path=entry.path, param_names=param_names)

            # Get summary and details. Passing the signature as well, so
            # different overloads can (but don't need to) have different docs.
            out.summary, out.content = extract_docs(state, state.function_docs, entry.type, entry.path, summary, signature='({})'.format(', '.join(signature)))
            if out.content: out.has_details = True

            # Call all scope exit hooks for this particular overload
            for hook in state.hooks_post_scope:
                hook(type=entry.type, path=entry.path, param_names=param_names)

            overloads += [out]

    # Sane introspection path for non-pybind11 code
    else:
        out = Empty()
        out.name = entry.path[-1]
        out.id = state.config['ID_FORMATTER'](EntryType.FUNCTION, entry.path[-1:])
        out.params = []
        out.has_complex_params = False
        out.has_details = False

        # Decide if classmethod or staticmethod in case this is a method
        if inspect.isclass(parent):
            out.is_method = True
            out.is_classmethod = inspect.ismethod(entry.object)
            out.is_staticmethod = out.name in parent.__dict__ and isinstance(parent.__dict__[out.name], staticmethod)
        else:
            out.is_method = False

        # First try to get fully dereferenced type hints (with strings
        # converted to actual annotations). If that fails (e.g. because a type
        # doesn't exist), we'll take the non-dereferenced annotations from
        # inspect instead.
        type_hints = get_type_hints_or_nothing(state, entry.path, entry.object)

        try:
            signature = inspect.signature(entry.object)

            if 'return' in type_hints:
                out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, type_hints['return'])
            else:
                out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, signature.return_annotation)
            param_names = []
            for i in signature.parameters.values():
                param = Empty()
                param.name = i.name
                param_names += [i.name]
                if i.name in type_hints:
                    param.type, param.type_quoted, param.type_link = extract_annotation(state, entry.path, type_hints[i.name])
                else:
                    param.type, param.type_quoted, param.type_link = extract_annotation(state, entry.path, i.annotation)
                if param.type:
                    out.has_complex_params = True
                if i.default is inspect.Signature.empty:
                    param.default, param.default_relative, param.default_link = None, None, None
                else:
                    param.default, param.default_relative, param.default_link = format_value(state, entry.path, i.default) or ('...', )*3
                    out.has_complex_params = True
                param.kind = str(i.kind)
                out.params += [param]

        # In CPython, some builtin functions (such as math.log) do not provide
        # metadata about their arguments. Source:
        # https://docs.python.org/3/library/inspect.html#inspect.signature
        except ValueError:
            param = Empty()
            param.name = None
            param.type, param.type_quoted, param.type_link = None, None, None
            param.default, param.default_relative, param.default_link = None, None, None
            out.params = [param]
            out.type, out.type_quoted, out.type_link = None, None, None
            param_names = []

        # Call all scope enter hooks
        for hook in state.hooks_pre_scope:
            hook(type=entry.type, path=entry.path, param_names=param_names)

        # Get summary and details
        # TODO: pass signature as well once @overload becomes a thing
        out.summary, out.content = extract_docs(state, state.function_docs, entry.type, entry.path, entry.object.__doc__)
        if out.content: out.has_details = True

        # Call all scope exit hooks
        for hook in state.hooks_post_scope:
            hook(type=entry.type, path=entry.path, param_names=param_names)

        overloads = [out]

    # Mark the functions as overloaded if there's more than one overload
    for out in overloads:
        out.is_overloaded = len(overloads) != 1
    # The stub template will decorate the function with @typing.overload
    if len(overloads) != 1:
        add_module_dependency_for(state, typing)

    # Common path for parameter / exception / return value docs and search
    path_str = '.'.join(entry.path)
    for out in overloads:
        # In case of introspection error, there's just a single param with name
        # and everything else being None, replace it with ... to match what the
        # HTML output shows
        signature = '({})'.format(', '.join(['{}: {}'.format(param.name, param.type) if param.type else param.name or '...' for param in out.params]))
        param_names = [param.name for param in out.params]

        # Call all scope enter hooks for this particular overload
        for hook in state.hooks_pre_scope:
            hook(type=entry.type, path=entry.path, param_names=param_names)

        # Get docs for each param and for the return value. Try this
        # particular overload first, if not found then fall back to generic
        # docs for all overloads.
        if path_str + signature in state.function_docs:
            function_docs = state.function_docs[path_str + signature]
        elif path_str in state.function_docs:
            function_docs = state.function_docs[path_str]
        else:
            function_docs = None
        if function_docs:
            # Having no parameters documented is okay, having self
            # undocumented as well. But having the rest documented only
            # partially isn't okay.
            if function_docs.get('params'):
                param_docs = function_docs['params']
                used_params = set()
                for param in out.params:
                    if param.name not in param_docs:
                        if param.name != 'self':
                            logging.warning("%s%s parameter %s is not documented", path_str, signature, param.name)
                        continue
                    try:
                        param.content = render_inline_rst(state, param_docs[param.name])
                    except docutils.utils.SystemMessage:
                        logging.error("Failed to process doc for %s param %s, ignoring:\n%s", path_str, param.name,  prettify_multiline_error(param_docs[param.name]))
                        param.content = ''
                    used_params.add(param.name)
                    out.has_param_details = True
                    out.has_details = True
                # Having unused param docs isn't okay either
                for name, _ in param_docs.items():
                    if name not in used_params:
                        logging.warning("%s%s documents parameter %s, which isn't in the signature", path_str, signature, name)

            if function_docs.get('raise'):
                out.exceptions = []
                for type_, content in function_docs['raise']:
                    exception = Empty()
                    exception.type = type_
                    exception.type_relative, exception.type_link = make_name_relative_link(state, entry.path, type_)
                    exception.content = render_inline_rst(state, content)
                    out.exceptions += [exception]
                out.has_details = True

            if function_docs.get('return'):
                try:
                    out.return_value = render_inline_rst(state, function_docs['return'])
                except docutils.utils.SystemMessage:
                    logging.error("Failed to process return doc for %s, ignoring:\n%s", path_str, prettify_multiline_error(function_docs['return']))
                    out.return_value = ''
                out.has_details = True

        # Call all scope exit hooks for this particular overload
        for hook in state.hooks_post_scope:
            hook(type=entry.type, path=entry.path, param_names=param_names)

        if not state.config['SEARCH_DISABLED']:
            result = Empty()
            result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNCTION)
            result.url = '{}#{}'.format(page_url, out.id)
            result.prefix = entry.path[:-1]
            result.name = entry.path[-1]
            result.params = []
            # If the function is overloaded, add arguments to each to
            # distinguish between them
            if len(overloads) != 1:
                for i in range(len(out.params)):
                    param = out.params[i]
                    # TODO use param.type_relative if it ever exists again in
                    #   addition to param.type_quoted
                    result.params += ['{}: {}'.format(param.name, make_relative_name(state, entry.path, param.type)) if param.type else param.name]
            state.search += [result]

    return overloads

def extract_property_doc(state: State, parent, entry: Empty):
    assert state.current_module

    out = Empty()
    out.name = entry.path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.PROPERTY, entry.path[-1:])
    out.has_details = False

    # If this is a property hammered out of attrs, we parse it differently.
    # These *might* satisfy inspect.isdatadescriptor if these alias real
    # properties found by other means, but that's not always the case, so no
    # asserting for that.
    if state.config['ATTRS_COMPATIBILITY'] and type(entry.object).__name__ == 'Attribute' and type(entry.object).__module__ == 'attr._make':
        # Unfortunately we can't get any docstring for these
        docstring = ''

        # TODO: are there readonly attrs?
        out.is_gettable = True
        out.is_settable = True
        out.is_deletable = True
        out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, entry.object.type)

    # If this is a slot, there won't be any fget / fset / fdel. Assume they're
    # gettable and settable (couldn't find any way to make them *inspectably*
    # readonly, all solutions involved throwing from __setattr__()) and
    # deletable as well (calling del on it seems to simply remove any
    # previously set value).
    # TODO: any better way to detect that those are slots?
    elif entry.object.__class__.__name__ == 'member_descriptor' and entry.object.__class__.__module__ == 'builtins':
        assert inspect.isdatadescriptor(entry.object)
        # Unfortunately we can't get any docstring for these
        docstring = ''

        out.is_gettable = True
        out.is_settable = True
        out.is_deletable = True

        # First try to get fully dereferenced type hints (with strings
        # converted to actual annotations). If that fails (e.g. because a type
        # doesn't exist), we'll take the non-dereferenced annotations instead.
        type_hints = get_type_hints_or_nothing(state, entry.path, parent)

        if out.name in type_hints:
            out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, type_hints[out.name])
        elif hasattr(parent, '__annotations__') and out.name in parent.__annotations__:
            out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, parent.__annotations__[out.name])
        else:
            out.type, out.type_quoted, out.type_link = None, None, None

    # The properties can be defined using the low-level descriptor protocol
    # instead of the higher-level property() decorator. That means there's no
    # fget / fset / fdel, instead we need to look into __get__ / __set__ /
    # __delete__ directly. This is fairly rare (datetime.date is one and
    # BaseException.args is another I could find), so don't bother with it much
    # --- assume readonly. Some docstrings are there for properties; see the
    # inspect_string.DerivedException test class for details.
    elif entry.object.__class__.__name__ == 'getset_descriptor' and entry.object.__class__.__module__ == 'builtins':
        assert inspect.isdatadescriptor(entry.object)
        docstring = entry.object.__doc__

        out.is_gettable = True
        out.is_settable = False
        out.is_deletable = False
        out.type, out.type_quoted, out.type_link = None, None, None

    # Otherwise it's a classic property
    else:
        assert inspect.isdatadescriptor(entry.object)
        is_classic_property = True

        # TODO figure out how to do pybind11 writeonly properties in the stub
        #   template
        out.is_gettable = entry.object.fget is not None
        out.is_settable = entry.object.fset is not None
        out.is_deletable = entry.object.fdel is not None

        if entry.object.fget or (entry.object.fset and entry.object.__doc__):
            docstring = entry.object.__doc__
        else:
            assert entry.object.fset
            docstring = entry.object.fset.__doc__

        # For the type, if the property is gettable, get it from getters's
        # return type. For write-only properties get it from setter's second
        # argument annotation.
        try:
            if entry.object.fget:
                signature = inspect.signature(entry.object.fget)

                # First try to get fully dereferenced type hints (with strings
                # converted to actual annotations). If that fails (e.g. because
                # a type doesn't exist), we'll take the non-dereferenced
                # annotations from inspect instead. This is deliberately done
                # *after* inspecting the signature because pybind11 properties
                # would throw TypeError from typing.get_type_hints(). This way
                # they throw ValueError from inspect and we don't need to
                # handle TypeError in get_type_hints_or_nothing().
                type_hints = get_type_hints_or_nothing(state, entry.path, entry.object.fget)

                if 'return' in type_hints:
                    out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, type_hints['return'])
                else:
                    out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, signature.return_annotation)
            else:
                assert entry.object.fset
                signature = inspect.signature(entry.object.fset)

                # Same as the lengthy comment above
                type_hints = get_type_hints_or_nothing(state, entry.path, entry.object.fset)

                # Get second parameter name, then try to fetch it from
                # type_hints and if that fails get its annotation from the
                # non-dereferenced version
                value_parameter = list(signature.parameters.values())[1]
                if value_parameter.name in type_hints:
                    out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, type_hints[value_parameter.name])
                else:
                    out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, value_parameter.annotation)

        except ValueError:
            # pybind11 properties have the type in the docstring
            if state.config['PYBIND11_COMPATIBILITY']:
                if entry.object.fget:
                    out.type, out.type_quoted, out.type_link = parse_pybind_signature(state, entry.path, entry.object.fget.__doc__)[3:]
                else:
                    assert entry.object.fset
                    parsed_args = parse_pybind_signature(state, entry.path, entry.object.fset.__doc__)[2]
                    # If argument parsing failed, we're screwed
                    if len(parsed_args) == 1:
                        out.type, out.type_quoted, out.type_link = None, None, None
                    else:
                        out.type, out.type_quoted, out.type_link = parsed_args[1][1:4]
            else:
                out.type, out.type_quoted, out.type_link = None, None, None

    # Call all scope enter hooks before rendering the docs
    for hook in state.hooks_pre_scope:
        hook(type=entry.type, path=entry.path)

    # Render the docs
    out.summary, out.content = extract_docs(state, state.property_docs, entry.type, entry.path, docstring)
    if out.content:
        out.has_details = True

    # Call all scope exit hooks after rendering the docs
    for hook in state.hooks_post_scope:
        hook(type=entry.type, path=entry.path)

    # Exception docs, if any
    exception_docs = state.property_docs.get('.'.join(entry.path), {}).get('raise')
    if exception_docs:
        out.exceptions = []
        for type_, content in exception_docs:
            exception = Empty()
            exception.type = type_
            exception.type_relative, exception.type_link = make_name_relative_link(state, entry.path, type_)
            exception.content = render_inline_rst(state, content)
            out.exceptions += [exception]
        out.has_details = True

    if not state.config['SEARCH_DISABLED']:
        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.PROPERTY)
        result.url = '{}#{}'.format(state.name_map['.'.join(entry.path[:-1])].url, out.id)
        result.prefix = entry.path[:-1]
        result.name = entry.path[-1]
        state.search += [result]

    return out

def extract_data_doc(state: State, parent, entry: Empty):
    assert state.current_module
    assert not inspect.ismodule(entry.object) and not inspect.isclass(entry.object) and not inspect.isroutine(entry.object) and not inspect.isframe(entry.object) and not inspect.istraceback(entry.object) and not inspect.iscode(entry.object)

    # Call all scope enter hooks before rendering the docs
    for hook in state.hooks_pre_scope:
        hook(type=entry.type, path=entry.path)

    out = Empty()
    out.name = entry.path[-1]
    out.id = state.config['ID_FORMATTER'](EntryType.DATA, entry.path[-1:])
    # Welp. https://stackoverflow.com/questions/8820276/docstring-for-variable
    out.summary, out.content = extract_docs(state, state.data_docs, entry.type, entry.path, '')
    out.has_details = bool(out.content)

    # Call all scope exit hooks after rendering the docs
    for hook in state.hooks_post_scope:
        hook(type=entry.type, path=entry.path)

    # First try to get fully dereferenced type hints (with strings converted to
    # actual annotations). If that fails (e.g. because a type doesn't exist),
    # we'll take the non-dereferenced annotations instead.
    type_hints = get_type_hints_or_nothing(state, entry.path, parent)

    if out.name in type_hints:
        out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, type_hints[out.name])
    elif hasattr(parent, '__annotations__') and out.name in parent.__annotations__:
        out.type, out.type_quoted, out.type_link = extract_annotation(state, entry.path, parent.__annotations__[out.name])
    else:
        out.type, out.type_quoted, out.type_link = None, None, None

    out.value, out.value_relative, out.value_link = format_value(state, entry.path, entry.object) or (None, None, None)

    if not state.config['SEARCH_DISABLED']:
        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.DATA)
        result.url = '{}#{}'.format(state.name_map['.'.join(entry.path[:-1])].url, out.id)
        result.prefix = entry.path[:-1]
        result.name = entry.path[-1]
        state.search += [result]

    return out

def render(*, config, template: str, url: str, filename: str, env: jinja2.Environment, **kwargs):
    template = env.get_template(template)
    rendered = template.render(URL=url,
        SEARCHDATA_FORMAT_VERSION=searchdata_format_version,
        **config, **kwargs)
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(filename, 'wb') as f:
        f.write(rendered.encode('utf-8'))
        # Add back a trailing newline so we don't need to bother with
        # patching test files to include a trailing newline to make Git
        # happy. Can't use keep_trailing_newline because that'd add it
        # also for nested templates :( The rendered file should never contain a
        # trailing newline on its own. Also add it only in case the file isn't
        # empty, which can happen with generated stubs. If non-empty, it should
        # never contain a trailing newline on its own.
        if rendered:
            assert not rendered.endswith('\n')
            f.write(b'\n')

def render_module(state: State, path, module, env):
    # Save name of current module for populating module dependencies and
    # initialize the dependency set. It could already be present in
    # module_dependencies if render_class() for an inner class was called
    # before, don't overwrite in that case.
    assert not state.current_module
    path_str = '.'.join(path)
    state.current_module = path_str
    state.module_dependencies.setdefault(path_str, set())

    # Call all scope enter hooks first
    for hook in state.hooks_pre_scope:
        hook(type=EntryType.MODULE, path=path)

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
    page.summary, page.content = extract_docs(state, state.module_docs, EntryType.MODULE, path, module.__doc__)
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
    page.has_function_details = False
    page.has_data_details = False

    # Find itself in the global map, save the summary back there for index
    entry = state.name_map[path_str]
    entry.summary = page.summary

    # Extract docs for all members
    for name in entry.members:
        subpath = path + [name]
        subpath_str = '.'.join(subpath)
        member_entry = state.name_map[subpath_str]

        if member_entry.type != EntryType.DATA and not object.__doc__: # pragma: no cover
            logging.warning("%s is undocumented", subpath_str)

        if member_entry.type == EntryType.MODULE:
            page.modules += [extract_module_doc(state, member_entry)]
        elif member_entry.type == EntryType.CLASS:
            # If we're generating stubs, add the whole parsed class instead of
            # just a name, summary and reference. All classes inside given
            # module are parsed before the module itself because crawl_module()
            # first puts all nested names into state.name_map and only then the
            # module itself.
            if state.config['OUTPUT_STUBS']:
                page.classes += [state.parsed_classes[subpath_str]]
            else:
                page.classes += [extract_class_doc(state, member_entry)]
        elif member_entry.type == EntryType.ENUM:
            enum_ = extract_enum_doc(state, member_entry)
            page.enums += [enum_]
            if enum_.has_details:
                page.has_enum_details = True
        elif member_entry.type in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION]:
            functions = extract_function_doc(state, module, member_entry)
            page.functions += functions
            for function in functions:
                if function.has_details:
                    page.has_function_details = True
        elif member_entry.type == EntryType.DATA:
            data = extract_data_doc(state, module, member_entry)
            page.data += [data]
            if data.has_details:
                page.has_data_details = True
        else: # pragma: no cover
            assert False

    # At this point the module dependencies should be filled for everything in
    # this module as well as all (recursive) classes. To verify that's indeed
    # the case, remove current module name from the dict afterwards -- anything
    # that'd attempt to insert afterwards would fail with a KeyError.
    page.dependencies = []
    for dependency in state.module_dependencies[path_str]:
        dependency_path = dependency.split('.')
        common_prefix_length = len(os.path.commonprefix([dependency_path, path]))
        # If there's no common prefix, it's an unrelated module
        if not common_prefix_length:
            page.dependencies += [('', dependency)]
        # If the common prefix is the whole module path, the dependency is from
        # a submodule (so this file is a __init__.py)
        elif len(path) == common_prefix_length:
            page.dependencies += [('.', '.'.join(dependency_path[common_prefix_length:]))]
        # Otherwise the dependency is a sibling module or siblings of parents,
        # add one dot for each. Yes, this can also produce a single dot as
        # above, but the difference is that above the file is a __init__.py so
        # `from . import sub` refers to a submodule, while here
        # `from . import sub` refers to the enclosing __init__.py so a sibling.
        else:
            page.dependencies += [('.'*(len(path) - common_prefix_length), '.'.join(dependency_path[common_prefix_length:]))]
    # Make the list independent from the order in which the dependencies were
    # discovered
    page.dependencies.sort()
    del state.module_dependencies[path_str]

    if not state.config['SEARCH_DISABLED']:
        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.MODULE)
        result.url = page.url
        result.prefix = path[:-1]
        result.name = path[-1]
        state.search += [result]

    # Render also the python stub file if requested
    if state.config['OUTPUT_STUBS'] is not None:
        # If the module has submodules, put it into <module>/__init__.pyi so
        # submodules can be next to it. It could be done always, but writing
        # just <module>.pyi if there are no submodules makes the output
        # cleaner.
        if page.modules:
            stub_filename = os.path.join(*path, '__init__' + state.config['STUB_EXTENSION'])
        else:
            stub_filename = os.path.join(*path[:-1], path[-1] + state.config['STUB_EXTENSION'])

        render(config=state.config,
            template='stub.pyi',
            filename=os.path.join(state.config['OUTPUT_STUBS'], stub_filename),
            url=url,
            env=env,
            page=page)

    # Render the regular HTML output, unless disabled
    if state.config['OUTPUT'] is not None:
        # Perform HTML escaping for everything going into the template. Done
        # here instead of inside extract_*_doc() to avoid having to unescape in
        # certain cases.
        for enum in page.enums:
            for value in enum.values:
                value.value = html.escape(value.value)
        for function in page.functions:
            for param in function.params:
                if param.default:
                    param.default = html.escape(param.default)
                    param.default_relative = html.escape(param.default_relative)
                    # param.default_link may contain HTML and thus had to be
                    # escaped early
        for data in page.data:
            if data.value:
                data.value = html.escape(data.value)
                data.value_relative = html.escape(data.value_relative)
                # data.value_link may contain HTML and thus had to be escaped
                # early

        render(config=state.config,
            template='module.html',
            filename=os.path.join(state.config['OUTPUT'], filename),
            url=url,
            env=env,
            page=page)

    # Call all scope exit hooks last
    for hook in state.hooks_post_scope:
        hook(type=EntryType.MODULE, path=path)

    # Reset name of current module to ensure it isn't mistakenly filled with
    # something unrelated
    state.current_module = None

def render_class(state: State, path, class_, env):
    # Save name of the enclosing module for populating module dependencies and
    # initialize the dependency set. It could already be present in
    # module_dependencies if render_class() for an inner class was called
    # before, don't overwrite in that case.
    #
    # Can't use class_.__module__ as that may not respect name mapping either
    # from config or from the __all__ members, have to iterate backwards until
    # the path prefix is a module.
    assert not state.current_module
    path_str = '.'.join(path)
    state.current_module = enclosing_module_for(state, path_str)
    state.module_dependencies.setdefault(state.current_module, set())

    # Call all scope enter hooks first
    for hook in state.hooks_pre_scope:
        hook(type=EntryType.CLASS, path=path)

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
    page.summary, page.content = extract_docs(state, state.class_docs, EntryType.CLASS, path, class_.__doc__)
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
    page.has_members = False
    page.has_enum_details = False
    page.has_function_details = False
    page.has_property_details = False
    page.has_data_details = False

    # Find itself in the global map, save the summary back there for index
    entry = state.name_map[path_str]
    entry.summary = page.summary

    # Extract docs for all members
    for name in entry.members:
        subpath = path + [name]
        subpath_str = '.'.join(subpath)
        member_entry = state.name_map[subpath_str]

        # TODO: yell only if there's also no external doc content
        if member_entry.type != EntryType.DATA and not object.__doc__: # pragma: no cover
            logging.warning("%s is undocumented", subpath_str)

        if member_entry.type == EntryType.CLASS:
            # If we're generating stubs, add the whole parsed class instead of
            # just a name, summary and reference. All inner classes are parsed
            # before the class itself because crawl_class() first puts all
            # nested names into state.name_map and only then the class itself.
            if state.config['OUTPUT_STUBS']:
                page.classes += [state.parsed_classes[subpath_str]]
            else:
                page.classes += [extract_class_doc(state, member_entry)]
            page.has_members = True
        elif member_entry.type == EntryType.ENUM:
            enum_ = extract_enum_doc(state, member_entry)
            page.enums += [enum_]
            if enum_.has_details:
                page.has_enum_details = True
            page.has_members = True
        elif member_entry.type in [EntryType.FUNCTION, EntryType.OVERLOADED_FUNCTION]:
            for function in extract_function_doc(state, class_, member_entry):
                if name.startswith('__'):
                    page.dunder_methods += [function]
                elif function.is_classmethod:
                    page.classmethods += [function]
                elif function.is_staticmethod:
                    page.staticmethods += [function]
                else:
                    page.methods += [function]
                if function.has_details:
                    page.has_function_details = True
            page.has_members = True
        elif member_entry.type == EntryType.PROPERTY:
            property = extract_property_doc(state, class_, member_entry)
            page.properties += [property]
            if property.has_details:
                page.has_property_details = True
            page.has_members = True
        elif member_entry.type == EntryType.DATA:
            data = extract_data_doc(state, class_, member_entry)
            page.data += [data]
            if data.has_details:
                page.has_data_details = True
            page.has_members = True
        else: # pragma: no cover
            assert False

    if not state.config['SEARCH_DISABLED']:
        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)
        result.url = page.url
        result.prefix = path[:-1]
        result.name = path[-1]
        state.search += [result]

    # If we're generating stubs, the parsed data gets used in render_module()
    # instead of it using just the output of extract_class_doc(). It
    # additionally needs a name member to be a superset of what
    # extract_class_doc() produces so it works with regular HTML output as
    # well.
    if state.config['OUTPUT_STUBS']:
        parsed_class = copy.deepcopy(page)
        parsed_class.name = path[-1]
        state.parsed_classes[path_str] = parsed_class

    # Render the regular HTML output, unless disabled
    if state.config['OUTPUT'] is not None:
        # Perform HTML escaping for everything going into the template. Done
        # here instead of inside extract_*_doc() to avoid having to unescape in
        # certain cases.
        for enum in page.enums:
            for value in enum.values:
                value.value = html.escape(value.value)
        for function in page.classmethods + page.staticmethods + page.dunder_methods + page.methods:
            for param in function.params:
                if param.default:
                    param.default = html.escape(param.default)
                    param.default_relative = html.escape(param.default_relative)
                    # param.default_link may contain HTML and thus had to be
                    # escaped early
        for data in page.data:
            if data.value:
                data.value = html.escape(data.value)
                data.value_relative = html.escape(data.value_relative)
                # data.value_link may contain HTML and thus had to be escaped
                # early

        render(config=state.config,
            template='class.html',
            filename=os.path.join(state.config['OUTPUT'], filename),
            url=url,
            env=env,
            page=page)

    # Call all scope exit hooks last
    for hook in state.hooks_post_scope:
        hook(type=EntryType.CLASS, path=path)

    # Reset name of current module to ensure it isn't mistakenly filled with
    # something unrelated
    state.current_module = None

# Extracts image paths and transforms them to just the filenames
class ExtractImages(Transform):
    # Max Docutils priority is 990, be sure that this is applied at the very
    # last
    default_priority = 991

    # There is no simple way to have stateful transforms (the publisher always
    # gets just the class, not the instance) so we have to make all data
    # awfully global. UGH.
    # TODO: maybe the pending nodes could solve this?
    _url_formatter = None
    _external_data = set()

    def __init__(self, document, startnode):
        Transform.__init__(self, document, startnode=startnode)

    def apply(self):
        ExtractImages._external_data = set()
        for image in self.document.findall(docutils.nodes.image):
            # Skip absolute URLs
            if urllib.parse.urlparse(image['uri']).netloc: continue

            # TODO: is there a non-private access to current document source
            # path?
            absolute_uri = os.path.join(os.path.dirname(self.document.settings._source), image['uri']) if isinstance(self.document.settings._source, str) else image['uri']
            ExtractImages._external_data.add(absolute_uri)

            # Patch the URL according to the URL formatter
            image['uri'] = ExtractImages._url_formatter(EntryType.STATIC, [absolute_uri])[1]

class DocumentationWriter(m.htmlsanity.SaneHtmlWriter):
    def get_transforms(self):
        return m.htmlsanity.SaneHtmlWriter.get_transforms(self) + [ExtractImages]

def publish_rst(state: State, source, *, source_path=None, translator_class=m.htmlsanity.SaneHtmlTranslator):
    # Make the URL formatter known to the image extractor so it can use it for
    # patching the URLs
    ExtractImages._url_formatter = state.config['URL_FORMATTER']

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
    # TODO for external docs it *somehow* needs to supply the *proper* filename
    #   and line range to it for better error reporting and relative includes,
    #   this is too awful
    if not source_path:
        source_path=os.path.join(state.config['INPUT'], "file.rst")
    pub.set_source(source=source, source_path=source_path)
    pub.publish()

    # External images to pull later
    state.external_data = state.external_data.union(ExtractImages._external_data)

    return pub

def render_rst(state: State, source):
    return publish_rst(state, source).writer.parts.get('body').rstrip()

class _SaneInlineHtmlTranslator(m.htmlsanity.SaneHtmlTranslator):
    # Unconditionally force compact paragraphs. This means the inline HTML
    # won't be wrapped in a <p> which is exactly what we want.
    def should_be_compact_paragraph(self, node):
        return True

def render_inline_rst(state: State, source):
    return publish_rst(state, source, translator_class=_SaneInlineHtmlTranslator).writer.parts.get('body').rstrip()

# Copy of docutils.utils.extract_options which doesn't throw BadOptionError on
# multi-word field names but instead turns the body into a tuple containing the
# extra arguments as a prefix and the original data as a suffix. The original
# restriction goes back to a nondescript "updated" commit from 2002, with no
# change of this behavior since:
# https://github.com/docutils-mirror/docutils/commit/508483835d95632efb5dd6b69c444a956d0fb7df
def _docutils_extract_options(field_list):
    option_list = []
    for field in field_list:
        field_name_parts = field[0].astext().split()
        name = str(field_name_parts[0].lower())
        body = field[1]
        if len(body) == 0:
            data = None
        elif len(body) > 1 or not isinstance(body[0], docutils.nodes.paragraph) \
              or len(body[0]) != 1 or not isinstance(body[0][0], docutils.nodes.Text):
            raise docutils.utils.BadOptionDataError(
                  'extension option field body may contain\n'
                  'a single paragraph only (option "%s")' % name)
        else:
            data = body[0][0].astext()
        if len(field_name_parts) > 1:
            # Supporting just one argument, don't need more right now (and
            # allowing any number would make checks on the directive side too
            # complicated)
            if len(field_name_parts) != 2: raise docutils.utils.BadOptionError(
                'extension option field name may contain either one or two words')
            data = tuple(field_name_parts[1:] + [data])
        option_list.append((name, data))
    return option_list

# ... and allowing duplicate options as well. This restriction goes back to the
# initial commit in 2002. Here for duplicate options we expect the converter to
# give us a list and we merge those lists; if not, we throw
# DuplicateOptionError as in the original code.
def _docutils_assemble_option_dict(option_list, options_spec):
    options = {}
    for name, value in option_list:
        convertor = options_spec[name]  # raises KeyError if unknown
        if convertor is None:
            raise KeyError(name)        # or if explicitly disabled
        try:
            converted = convertor(value)
        except (ValueError, TypeError) as detail:
            raise detail.__class__('(option: "%s"; value: %r)\n%s'
                                   % (name, value, ' '.join(detail.args)))
        if name in options:
            if isinstance(converted, list):
                assert isinstance(options[name], list) and not isinstance(options[name], tuple)
                options[name] += converted
            else:
                raise docutils.utils.DuplicateOptionError('duplicate non-list option "%s"' % name)
        else:
            options[name] = converted
    return options

def render_doc(state: State, filename):
    logging.debug("parsing docs from %s", filename)

    # Page begin hooks are called before this in run(), once for all docs since
    # these functions are not generating any pages

    # Render the file. The directives should take care of everything, so just
    # discard the output afterwards. Some directives (such as py:function) have
    # multi-word field names and can be duplicated, so we have to patch the
    # option extractor to allow that. See _docutils_extract_options and
    # _docutils_assemble_option_dict above for details.
    with open(filename, 'r') as f:
        prev_extract_options = docutils.utils.extract_options
        prev_assemble_option_dict = docutils.utils.assemble_option_dict
        docutils.utils.extract_options = _docutils_extract_options
        docutils.utils.assemble_option_dict = _docutils_assemble_option_dict

        publish_rst(state, f.read(), source_path=filename)

        docutils.utils.extract_options = prev_extract_options
        docutils.utils.assemble_option_dict = prev_assemble_option_dict

def render_page(state: State, path, input_filename, env):
    # If not generating the regular HTML output, we shouldn't even be here
    assert state.config['OUTPUT'] is not None

    filename, url = state.config['URL_FORMATTER'](EntryType.PAGE, path)

    logging.debug("generating %s", filename)

    # Call all registered page begin hooks
    for hook in state.hooks_pre_page:
        hook(path=path)

    page = Empty()
    page.filename = filename
    page.url = url
    page.prefix_wbr = path[0]

    # Call all scope enter hooks before
    for hook in state.hooks_pre_scope:
        hook(type=EntryType.PAGE, path=path)

    # Render the file
    with open(input_filename, 'r') as f:
        try:
            pub = publish_rst(state, f.read(), source_path=input_filename)
        except docutils.utils.SystemMessage:
            logging.error("Failed to process %s, rendering an empty page", input_filename)

            # Empty values for fields expected by other code
            page.breadcrumb = [(os.path.basename(input_filename), url)]
            page.summary = ''
            page.content = ''
            entry = state.name_map['.'.join(path)]
            entry.summary = page.summary
            entry.name = page.breadcrumb[-1][0]
            render(config=state.config,
                template='page.html',
                filename=os.path.join(state.config['OUTPUT'], filename),
                url=url,
                env=env,
                page=page)
            return

    # Call all scope exit hooks last
    for hook in state.hooks_post_scope:
        hook(type=EntryType.PAGE, path=path)

    # Extract metadata from the page
    metadata = {}
    for docinfo in pub.document.findall(docutils.nodes.docinfo):
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
    page.breadcrumb = [(pub.writer.parts.get('title'), url)]

    # Set page content and add extra metadata from there
    page.content = pub.writer.parts.get('body').rstrip()
    for key, value in metadata.items(): setattr(page, key, value)
    if not hasattr(page, 'summary'): page.summary = ''

    # Find itself in the global map, save the page title and summary back there
    # for index
    entry = state.name_map['.'.join(path)]
    entry.summary = page.summary
    entry.name = page.breadcrumb[-1][0]

    if not state.config['SEARCH_DISABLED']:
        result = Empty()
        result.flags = ResultFlag.from_type(ResultFlag.NONE, EntryType.PAGE)
        result.url = page.url
        result.prefix = path[:-1]
        result.name = path[-1]
        state.search += [result]

    render(config=state.config,
        template='page.html',
        filename=os.path.join(state.config['OUTPUT'], filename),
        url=url,
        env=env,
        page=page)

def is_html_safe(string):
    return '<' not in string and '>' not in string and '&' not in string and '"' not in string and '\'' not in string

def build_search_data(state: State, merge_subtrees=True, add_lookahead_barriers=True, merge_prefixes=True) -> bytearray:
    trie = Trie()
    map = ResultMap()

    symbol_count = 0
    for result in state.search:
        # Decide on prefix joiner
        if EntryType(result.flags.type) in [EntryType.MODULE, EntryType.CLASS, EntryType.FUNCTION, EntryType.PROPERTY, EntryType.ENUM, EntryType.ENUM_VALUE, EntryType.DATA]:
            joiner = '.'
        elif EntryType(result.flags.type) == EntryType.PAGE:
            joiner = ' » '
        else: # pragma: no cover
            assert False

        # Handle function arguments
        name_with_args = result.name
        name = result.name
        suffix_length = 0
        if hasattr(result, 'params') and result.params is not None:
            # Some very heavily annotated function parameters might cause the
            # suffix_length to exceed 256, which won't fit into the serialized
            # search data. However that *also* won't fit in the search result
            # list so there's no point in storing so much. Truncate it to 48
            # chars which should fit the full function name in the list in most
            # cases, yet be still long enough to be able to distinguish
            # particular overloads.
            # TODO: the suffix_length has to be calculated on UTF-8
            params = ', '.join(result.params)
            assert is_html_safe(params) # this is not C++, so no <>&
            if len(params) > 49:
                params = params[:48] + '…'
            name_with_args += '(' + params + ')'
            suffix_length += len(params.encode('utf-8')) + 2

        complete_name = joiner.join(result.prefix + [name_with_args])
        # TODO needs escaping once page names are exposed to search
        assert is_html_safe(complete_name) # this is not C++, so no <>&
        index = map.add(complete_name, result.url, suffix_length=suffix_length, flags=result.flags)

        # Add functions the second time with () appended, everything is the
        # same except for suffix length which is 2 chars shorter
        if hasattr(result, 'params') and result.params is not None:
            index_args = map.add(complete_name, result.url,
                suffix_length=suffix_length - 2, flags=result.flags)

        # Add the result multiple times with all possible prefixes
        prefixed_name = result.prefix + [name]
        for i in range(len(prefixed_name)):
            lookahead_barriers = []
            name = ''
            for j in prefixed_name[i:]:
                if name:
                    lookahead_barriers += [len(name)]
                    name += joiner
                # TODO needs escaping once page names are exposed to search
                assert is_html_safe(j) # this is not C++, so no <>&
                name += j
            trie.insert(name.lower(), index, lookahead_barriers=lookahead_barriers if add_lookahead_barriers else [])

            # Add functions the second time with () appended, referencing
            # the other result that expects () appended. The lookahead
            # barrier is at the ( character to avoid the result being shown
            # twice.
            if hasattr(result, 'params') and result.params is not None:
                trie.insert(name.lower() + '()', index_args, lookahead_barriers=lookahead_barriers + [len(name)] if add_lookahead_barriers else [])

        # Add this symbol to total symbol count
        symbol_count += 1

    # For each node in the trie sort the results so the found items have sane
    # order by default
    trie.sort(map)

    return serialize_search_data(
        Serializer(
            file_offset_bytes=state.config['SEARCH_FILE_OFFSET_BYTES'],
            result_id_bytes=state.config['SEARCH_RESULT_ID_BYTES'],
            name_size_bytes=state.config['SEARCH_NAME_SIZE_BYTES']
        ),
        trie=trie,
        map=map,
        type_map=search_type_map,
        symbol_count=symbol_count,
        merge_subtrees=merge_subtrees,
        merge_prefixes=merge_prefixes,
    )

def run(basedir, config, *, templates=default_templates, search_add_lookahead_barriers=True, search_merge_subtrees=True, search_merge_prefixes=True):
    # Populate the INPUT, if not specified, make it absolute
    if config['INPUT'] is None: config['INPUT'] = basedir
    else: config['INPUT'] = os.path.join(basedir, config['INPUT'])

    # Make the output dirs absolute
    if config['OUTPUT'] is not None:
        config['OUTPUT'] = os.path.join(config['INPUT'], config['OUTPUT'])
        if not os.path.exists(config['OUTPUT']):
            os.makedirs(config['OUTPUT'])
    if config['OUTPUT_STUBS'] is not None:
        config['OUTPUT_STUBS'] = os.path.join(config['INPUT'], config['OUTPUT_STUBS'])
        if not os.path.exists(config['OUTPUT_STUBS']):
            os.makedirs(config['OUTPUT_STUBS'])

    # Guess MIME type of the favicon
    if config['FAVICON']:
        config['FAVICON'] = (config['FAVICON'], mimetypes.guess_type(config['FAVICON'])[0])

    state = State(config)

    # Prepare Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates), trim_blocks=True,
        lstrip_blocks=True, enable_async=True)
    # Filter to return formatted URL or the full URL, if already absolute
    def format_url(path):
        if urllib.parse.urlparse(path).netloc: return path

        # If file is found relative to the conf file, use that
        if os.path.exists(os.path.join(config['INPUT'], path)):
            path = os.path.join(config['INPUT'], path)
        # Otherwise use path relative to script directory
        else:
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

        return config['URL_FORMATTER'](EntryType.STATIC, [path])[1]
    # Filter to return URL for given symbol. If the path is a string, first try
    # to treat it as an URL -- either it needs to have the scheme or at least
    # one slash for relative links (in contrast, Python names don't have
    # slashes). If that fails,  turn it into a list and try to look it up in
    # various dicts.
    def path_to_url(path):
        if isinstance(path, str):
            if urllib.parse.urlparse(path).netloc or '/' in path: return path
            path = [path]
        entry = state.name_map['.'.join(path)]
        return entry.url

    env.filters['format_url'] = format_url
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
            enum_doc_contents=state.enum_docs,
            enum_value_doc_contents=state.enum_value_docs,
            function_doc_contents=state.function_docs,
            property_doc_contents=state.property_docs,
            data_doc_contents=state.data_docs,
            hooks_post_crawl=state.hooks_post_crawl,
            hooks_pre_scope=state.hooks_pre_scope,
            hooks_post_scope=state.hooks_post_scope,
            hooks_docstring=state.hooks_docstring,
            hooks_pre_page=state.hooks_pre_page,
            hooks_post_run=state.hooks_post_run)

    # First process the doc input files so we have all data for rendering
    # module/class pages. This needs to be done first so the crawl after can
    # have a look at the external data and include documented underscored
    # members as well. On the other hand, this means nothing in render_doc()
    # has access to the module hierarchy -- all actual content rendering has to
    # happen later.
    for file in config['INPUT_DOCS']:
        render_doc(state, os.path.join(basedir, file))

    # Crawl all input modules to gather the name tree, put their names into a
    # list for the index. The crawl is done breadth-first, so the function
    # returns a list of submodules to be crawled next.
    class_index = []
    modules_to_crawl = []
    for module in config['INPUT_MODULES']:
        if isinstance(module, str):
            module_name = module
            module = importlib.import_module(module)
        else:
            module_name = module.__name__
        module_path = module_name.split('.')
        modules_to_crawl += [(module_path, module)]
        # Add the module to the class index only if it's a top-level one,
        # otherwise expect that it'll appear somewhere deeper on its own
        if len(module_path) == 1:
            class_index += [module_name]
    while modules_to_crawl:
        path, object = modules_to_crawl.pop(0)
        if id(object) in state.crawled: continue
        modules_to_crawl += crawl_module(state, path, object)

    # Add special pages to the name map. The pages are done after so they can
    # override these.
    for page in special_pages:
        entry = Empty()
        entry.type = EntryType.SPECIAL
        entry.path = [page]
        entry.url = config['URL_FORMATTER'](EntryType.SPECIAL, entry.path)[1]
        state.name_map[page] = entry

    # Do the same for pages
    # TODO: turn also into some crawl_page() function? once we have subpages?
    page_index = []
    for page in config['INPUT_PAGES']:
        page_name = os.path.splitext(os.path.basename(page))[0]

        entry = Empty()
        entry.type = EntryType.PAGE
        entry.path = [page_name]
        entry.url = config['URL_FORMATTER'](EntryType.PAGE, entry.path)[1]
        entry.filename = os.path.join(config['INPUT'], page)
        state.name_map[page_name] = entry

        # The index page doesn't go to the index
        if page_name != 'index': page_index += [page_name]

    # Call all registered post-crawl hooks
    for hook in state.hooks_post_crawl:
        hook(name_map=state.name_map)

    # Go through all crawled names and render modules, classes and pages. A
    # side effect of the render is entry.summary (and entry.name for pages)
    # being filled.
    # TODO: page name need to be added earlier for intersphinx!
    for entry in state.name_map.values():
        # If there is no object, the entry is an external reference. Skip
        # those. Can't do `not entry.object` because that gives ValueError
        # for numpy ("use a.any() or a.all()")
        if hasattr(entry, 'object') and entry.object is None:
            continue

        if entry.type == EntryType.MODULE:
            render_module(state, entry.path, entry.object, env)
        elif entry.type == EntryType.CLASS:
            render_class(state, entry.path, entry.object, env)
        elif entry.type == EntryType.PAGE:
            render_page(state, entry.path, entry.filename, env)

    # Warn if there are any unused contents left after processing everything
    for docs in ['module', 'class', 'enum', 'function', 'property', 'data']:
        unused_docs = [key for key, value in getattr(state, f'{docs}_docs').items() if not 'used' in value]
        if unused_docs:
            logging.warning("The following %s doc contents were unused: %s", docs, unused_docs)

    # All collected module dependencies should be consumed and removed by
    # render_module() at this point. If not, it might be because the same class
    # appears in two distinct modules, or a module somewhere in the path isn't
    # crawled. Neither of those is an error.
    if state.module_dependencies:
        logging.debug("Some module dependencies were not consumed: {}".format(state.module_dependencies))

    # The following is all relevant to the HTML output only, skip if disabled
    if state.config['OUTPUT'] is not None:
        # Create module and class index from the toplevel name list.
        # Recursively go from the top-level index list and gather all
        # class/module children.
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
            assert entry.type == EntryType.PAGE, "page %s already used as %s (%s)" % (page_index[i], entry.type, entry.url)

            index_entry = Empty()
            index_entry.kind = 'page'
            index_entry.name = entry.name
            index_entry.url = entry.url
            index_entry.summary = entry.summary
            index_entry.has_nestable_children = False
            index_entry.children = []

            page_index[i] = index_entry

        index = Empty()
        index.classes = class_index
        index.pages = page_index
        for file in special_pages[1:]: # exclude index
            filename, url = config['URL_FORMATTER'](EntryType.SPECIAL, [file])
            render(config=config,
                template=file + '.html',
                filename=os.path.join(config['OUTPUT'], filename),
                url=url,
                env=env,
                index=index)

        # Create index.html if it was not provided by the user
        if 'index.rst' not in [os.path.basename(i) for i in config['INPUT_PAGES']]:
            logging.debug("writing index.html for an empty main page")

            filename, url = config['URL_FORMATTER'](EntryType.SPECIAL, ['index'])

            page = Empty()
            page.filename = filename
            page.url = url
            page.breadcrumb = [(config['PROJECT_TITLE'], url)]
            render(config=config,
                template='page.html',
                filename=os.path.join(config['OUTPUT'], filename),
                url=url,
                env=env,
                page=page)

        if not state.config['SEARCH_DISABLED']:
            logging.debug("building search data for {} symbols".format(len(state.search)))

            data = build_search_data(state, add_lookahead_barriers=search_add_lookahead_barriers, merge_subtrees=search_merge_subtrees, merge_prefixes=search_merge_prefixes)

            # Joining twice, first before passing those to the URL formatter
            # and second after. If SEARCH_DOWNLOAD_BINARY is a string, use that
            # as a filename.
            # TODO: any chance we could write the file *before* it gets ever
            # passed to URL formatters so we can add cache buster hashes to its
            # URL?
            if state.config['SEARCH_DOWNLOAD_BINARY']:
                with open(os.path.join(config['OUTPUT'], config['URL_FORMATTER'](EntryType.STATIC, [os.path.join(config['OUTPUT'], state.config['SEARCH_DOWNLOAD_BINARY'] if isinstance(state.config['SEARCH_DOWNLOAD_BINARY'], str) else searchdata_filename.format(search_filename_prefix=state.config['SEARCH_FILENAME_PREFIX']))])[0]), 'wb') as f:
                    f.write(data)
            else:
                with open(os.path.join(config['OUTPUT'], config['URL_FORMATTER'](EntryType.STATIC, [os.path.join(config['OUTPUT'], searchdata_filename_b85.format(search_filename_prefix=state.config['SEARCH_FILENAME_PREFIX']))])[0]), 'wb') as f:
                    f.write(base85encode_search_data(data))

            # OpenSearch metadata, in case we have the base URL
            if state.config['SEARCH_BASE_URL']:
                logging.debug("writing OpenSearch metadata file")

                template = env.get_template('opensearch.xml')
                rendered = template.render(**state.config)
                output = os.path.join(config['OUTPUT'], 'opensearch.xml')
                with open(output, 'wb') as f:
                    f.write(rendered.encode('utf-8'))
                    # Add back a trailing newline so we don't need to bother
                    # with patching test files to include a trailing newline to
                    # make Git happy. Can't use keep_trailing_newline because
                    # that'd add it also for nested templates :( The rendered
                    # file should never contain a trailing newline on its own.
                    assert not rendered.endswith('\n')
                    f.write(b'\n')

        # Copy referenced files
        for i in config['STYLESHEETS'] + config['EXTRA_FILES'] + ([config['PROJECT_LOGO']] if config['PROJECT_LOGO'] else []) + ([config['FAVICON'][0]] if config['FAVICON'] else []) + list(state.external_data) + ([] if config['SEARCH_DISABLED'] else ['search.js']):
            # Skip absolute URLs
            if urllib.parse.urlparse(i).netloc: continue

            # If file is found relative to the conf file, use that
            if os.path.exists(os.path.join(config['INPUT'], i)):
                i = os.path.join(config['INPUT'], i)

            # Otherwise use path relative to script directory
            else:
                i = os.path.join(os.path.dirname(os.path.realpath(__file__)), i)

            output = os.path.join(config['OUTPUT'], config['URL_FORMATTER'](EntryType.STATIC, [i])[0])
            output_dir = os.path.dirname(output)
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            logging.debug("copying %s to output", i)
            shutil.copy(i, output)

    # Call all registered finalization hooks
    for hook in state.hooks_post_run: hook()

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', help="configuration file")
    parser.add_argument('--templates', help="template directory", default=default_templates)
    parser.add_argument('--debug', help="verbose debug output", action='store_true')
    args = parser.parse_args()

    # Set an environment variable indicating m.css is being run. This can be
    # used for REALLY DIRTY hacks when monkey-patching imported modules is not
    # enough (for example in order to change behavior inside native modules and
    # such)
    #
    # Since this is done here in __main__, it can't be checked by a test.
    os.environ['MCSS_GENERATING_OUTPUT'] = '1'

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

    run(os.path.dirname(os.path.abspath(args.conf)), config, templates=os.path.abspath(args.templates))
