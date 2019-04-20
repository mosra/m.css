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
import enum
import urllib.parse
import html
import importlib
import inspect
import logging
import mimetypes
import os
import sys
import shutil

from types import SimpleNamespace as Empty
from importlib.machinery import SourceFileLoader
from typing import Tuple, Dict, Any, List
from urllib.parse import urljoin
from distutils.version import LooseVersion

import jinja2

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../plugins'))
import m.htmlsanity

default_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/python/')

default_config = {
    'PROJECT_TITLE': 'My Python Project',
    'PROJECT_SUBTITLE': None,
    'MAIN_PROJECT_URL': None,
    'INPUT_MODULES': [],
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
}

def is_internal_function_name(name: str) -> bool:
    """If the function name is internal.

    Skips underscored functions but keeps special functions such as __init__.
    """
    return name.startswith('_') and not (name.startswith('__') and name.endswith('__'))

def is_internal_or_imported_module_member(parent, path: str, name: str, object) -> bool:
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
        if hasattr(object, '__module__') and object.__module__ != '.'.join(path):
            return True

    # If this is a module, then things get complicated again and we need to
    # handle modules and packages differently. See also for more info:
    # https://stackoverflow.com/a/7948672
    else:
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

def make_url(path: List[str]) -> str:
    return '.'.join(path) + '.html'

def extract_brief(doc: str) -> str:
    if not doc: return '' # some modules (xml.etree) have that :(
    doc = inspect.cleandoc(doc)
    end = doc.find('\n\n')
    return html.escape(doc if end == -1 else doc[:end])

def extract_type(type) -> str:
    # For types we concatenate the type name with its module unless it's
    # builtins (i.e., we want re.Match but not builtins.int).
    return (type.__module__ + '.' if type.__module__ != 'builtins' else '') + type.__name__

def extract_annotation(annotation) -> str:
    # TODO: why this is not None directly?
    if annotation is inspect.Signature.empty: return None

    # To avoid getting <class 'foo.bar'> for types (and getting foo.bar
    # instead) but getting the actual type for types annotated with e.g.
    # List[int], we need to check if the annotation is actually from the
    # typing module or it's directly a type. In Python 3.7 this worked with
    # inspect.isclass(annotation), but on 3.6 that gives True for annotations
    # as well and then we would get just List instead of List[int].
    if annotation.__module__ == 'typing': return str(annotation)
    return extract_type(annotation)

def render(config, template: str, page, env: jinja2.Environment):
    template = env.get_template(template)
    rendered = template.render(page=page, FILENAME=page.url, **config)
    with open(os.path.join(config['OUTPUT'], page.url), 'wb') as f:
        f.write(rendered.encode('utf-8'))
        # Add back a trailing newline so we don't need to bother with
        # patching test files to include a trailing newline to make Git
        # happy
        # TODO could keep_trailing_newline fix this better?
        f.write(b'\n')

def extract_module_doc(path: List[str], module):
    assert inspect.ismodule(module)

    out = Empty()
    out.url = make_url(path)
    out.name = path[-1]
    out.brief = extract_brief(module.__doc__)
    return out

def extract_class_doc(path: List[str], class_):
    assert inspect.isclass(class_)

    out = Empty()
    out.url = make_url(path)
    out.name = path[-1]
    out.brief = extract_brief(class_.__doc__)
    return out

def extract_enum_doc(path: List[str], enum_):
    assert issubclass(enum_, enum.Enum)

    out = Empty()
    out.name = path[-1]

    # Enum doc is by default set to a generic value. That's useless as well.
    if enum_.__doc__ == 'An enumeration.':
        out.brief = ''
    else:
        out.brief = extract_brief(enum_.__doc__)

    out.base = extract_type(enum_.__base__)
    out.values = []
    out.has_details = False
    out.has_value_details = False

    for i in enum_:
        value = Empty()
        value.name = i.name
        value.value = html.escape(repr(i.value))

        # Value doc gets by default inherited from the enum, that's useless
        if i.__doc__ == enum_.__doc__:
            value.brief = ''
        else:
            value.brief = extract_brief(i.__doc__)

        if value.brief:
            out.has_details = True
            out.has_value_details = True
        out.values += [value]

    return out

def extract_function_doc(path: List[str], function):
    assert inspect.isfunction(function) or inspect.ismethod(function) or inspect.isroutine(function)

    out = Empty()
    out.name = path[-1]
    out.brief = extract_brief(function.__doc__)
    out.params = []
    out.has_complex_params = False
    out.has_details = False

    try:
        signature = inspect.signature(function)
        out.type = extract_annotation(signature.return_annotation)
        for i in signature.parameters.values():
            param = Empty()
            param.name = i.name
            param.type = extract_annotation(i.annotation)
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

    return out

def extract_property_doc(path: List[str], property):
    assert inspect.isdatadescriptor(property)

    out = Empty()
    out.name = path[-1]
    out.brief = extract_brief(property.__doc__)
    out.is_settable = property.fset is not None
    out.is_deletable = property.fdel is not None
    out.has_details = False

    try:
        signature = inspect.signature(property.fget)
        out.type = extract_annotation(signature.return_annotation)
    except ValueError:
        out.type = None

    return out

def extract_data_doc(parent, path: List[str], data):
    assert not inspect.ismodule(data) and not inspect.isclass(data) and not inspect.isroutine(data) and not inspect.isframe(data) and not inspect.istraceback(data) and not inspect.iscode(data)

    out = Empty()
    out.name = path[-1]
    # Welp. https://stackoverflow.com/questions/8820276/docstring-for-variable
    out.brief = ''
    out.has_details = False
    if hasattr(parent, '__annotations__') and out.name in parent.__annotations__:
        out.type = extract_annotation(parent.__annotations__[out.name])
    else:
        out.type = None
    # The autogenerated <foo.bar at 0xbadbeef> is useless, so provide the value
    # only if __repr__ is implemented for given type
    if '__repr__' in type(data).__dict__:
        out.value = html.escape(repr(data))
    else:
        out.value = None

    return out

def render_module(config, path, module, env):
    logging.debug("generating %s.html", '.'.join(path))

    url_base = ''
    breadcrumb = []
    for i in path:
        url_base += i + '.'
        breadcrumb += [(i, url_base + 'html')]

    page = Empty()
    page.brief = extract_brief(module.__doc__)
    page.url = breadcrumb[-1][1]
    page.breadcrumb = breadcrumb
    page.prefix_wbr = '.<wbr />'.join(path + [''])
    page.modules = []
    page.classes = []
    page.enums = []
    page.functions = []
    page.data = []
    page.has_enum_details = False

    # This is actually complicated -- if the module defines __all__, use that.
    # The __all__ is meant to expose the public API, so we don't filter out
    # underscored things.
    if hasattr(module, '__all__'):
        for name in module.__all__:
            # Everything available in __all__ is already imported, so get those
            # directly
            object = getattr(module, name)
            subpath = path + [name]

            # We allow undocumented submodules (since they're often in the
            # standard lib), but not undocumented classes etc. Render the
            # submodules and subclasses recursively.
            if inspect.ismodule(object):
                page.modules += [extract_module_doc(subpath, object)]
                render_module(config, subpath, object, env)
            elif inspect.isclass(object) and not issubclass(object, enum.Enum):
                page.classes += [extract_class_doc(subpath, object)]
                render_class(config, subpath, object, env)
            elif inspect.isclass(object) and issubclass(object, enum.Enum):
                enum_ = extract_enum_doc(subpath, object)
                page.enums += [enum_]
                if enum_.has_details: page.has_enum_details = True
            elif inspect.isfunction(object) or inspect.isbuiltin(object):
                page.functions += [extract_function_doc(subpath, object)]
            # Assume everything else is data. The builtin help help() (from
            # pydoc) does the same:
            # https://github.com/python/cpython/blob/d29b3dd9227cfc4a23f77e99d62e20e063272de1/Lib/pydoc.py#L113
            # TODO: unify this query
            elif not inspect.isframe(object) and not inspect.istraceback(object) and not inspect.iscode(object):
                page.data += [extract_data_doc(module, subpath, object)]
            else: # pragma: no cover
                logging.warning("unknown symbol %s in %s", name, '.'.join(path))

    # Otherwise, enumerate the members using inspect. However, inspect lists
    # also imported modules, functions and classes, so take only those which
    # have __module__ equivalent to `path`.
    else:
        # Get (and render) inner modules
        for name, object in inspect.getmembers(module, inspect.ismodule):
            if is_internal_or_imported_module_member(module, path, name, object): continue

            subpath = path + [name]
            page.modules += [extract_module_doc(subpath, object)]
            render_module(config, subpath, object, env)

        # Get (and render) inner classes
        for name, object in inspect.getmembers(module, lambda o: inspect.isclass(o) and not issubclass(o, enum.Enum)):
            if is_internal_or_imported_module_member(module, path, name, object): continue

            subpath = path + [name]
            if not object.__doc__: logging.warning("%s is undocumented", '.'.join(subpath))

            page.classes += [extract_class_doc(subpath, object)]
            render_class(config, subpath, object, env)

        # Get enums
        for name, object in inspect.getmembers(module, lambda o: inspect.isclass(o) and issubclass(o, enum.Enum)):
            if is_internal_or_imported_module_member(module, path, name, object): continue

            subpath = path + [name]
            if not object.__doc__: logging.warning("%s is undocumented", '.'.join(subpath))

            enum_ = extract_enum_doc(subpath, object)
            page.enums += [enum_]
            if enum_.has_details: page.has_enum_details = True

        # Get inner functions
        for name, object in inspect.getmembers(module, lambda o: inspect.isfunction(o) or inspect.isbuiltin(o)):
            if is_internal_or_imported_module_member(module, path, name, object): continue

            subpath = path + [name]
            if not object.__doc__: logging.warning("%s() is undocumented", '.'.join(subpath))

            page.functions += [extract_function_doc(subpath, object)]

        # Get data
        # TODO: unify this query
        for name, object in inspect.getmembers(module, lambda o: not inspect.ismodule(o) and not inspect.isclass(o) and not inspect.isroutine(o) and not inspect.isframe(o) and not inspect.istraceback(o) and not inspect.iscode(o)):
            if is_internal_or_imported_module_member(module, path, name, object): continue

            page.data += [extract_data_doc(module, path + [name], object)]

    render(config, 'module.html', page, env)

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

def render_class(config, path, class_, env):
    logging.debug("generating %s.html", '.'.join(path))

    url_base = ''
    breadcrumb = []
    for i in path:
        url_base += i + '.'
        breadcrumb += [(i, url_base + 'html')]

    page = Empty()
    page.brief = extract_brief(class_.__doc__)
    page.url = breadcrumb[-1][1]
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

    # Get inner classes
    for name, object in inspect.getmembers(class_, lambda o: inspect.isclass(o) and not issubclass(o, enum.Enum)):
        if name in ['__base__', '__class__']: continue # TODO
        if name.startswith('_'): continue

        subpath = path + [name]
        if not object.__doc__: logging.warning("%s is undocumented", '.'.join(subpath))

        page.classes += [extract_class_doc(subpath, object)]
        render_class(config, subpath, object, env)

    # Get enums
    for name, object in inspect.getmembers(class_, lambda o: inspect.isclass(o) and issubclass(o, enum.Enum)):
        if name.startswith('_'): continue

        subpath = path + [name]
        if not object.__doc__: logging.warning("%s is undocumented", '.'.join(subpath))

        enum_ = extract_enum_doc(subpath, object)
        page.enums += [enum_]
        if enum_.has_details: page.has_enum_details = True

    # Get methods
    for name, object in inspect.getmembers(class_, inspect.isroutine):
        # Filter out underscored methods (but not dunder methods)
        if is_internal_function_name(name): continue

        # Filter out dunder methods that don't have their own docs
        if name.startswith('__') and (name, object.__doc__) in _filtered_builtin_functions: continue

        subpath = path + [name]
        if not object.__doc__: logging.warning("%s() is undocumented", '.'.join(subpath))

        function = extract_function_doc(subpath, object)
        function.is_classmethod = inspect.ismethod(object)
        function.is_staticmethod = name in class_.__dict__ and isinstance(class_.__dict__[name], staticmethod)

        if name.startswith('__'):
            page.dunder_methods += [function]
        elif function.is_classmethod:
            page.classmethods += [function]
        elif function.is_staticmethod:
            page.staticmethods += [function]
        else:
            page.methods += [function]

    # Get properties
    for name, object in inspect.getmembers(class_, inspect.isdatadescriptor):
        if (name, object.__doc__) in _filtered_builtin_properties:
            continue
        if name.startswith('_'): continue # TODO: are there any dunder props?

        subpath = path + [name]
        if not object.__doc__: logging.warning("%s is undocumented", '.'.join(subpath))

        page.properties += [extract_property_doc(subpath, object)]

    # Get data
    # TODO: unify this query
    for name, object in inspect.getmembers(class_, lambda o: not inspect.ismodule(o) and not inspect.isclass(o) and not inspect.isroutine(o) and not inspect.isframe(o) and not inspect.istraceback(o) and not inspect.iscode(o) and not inspect.isdatadescriptor(o)):
        if name.startswith('_'): continue

        subpath = path + [name]
        page.data += [extract_data_doc(class_, subpath, object)]

    render(config, 'class.html', page, env)

def run(basedir, config, templates):
    # Prepare Jinja environment
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates), trim_blocks=True,
        lstrip_blocks=True, enable_async=True)
    # Filter to return file basename or the full URL, if absolute
    def basename_or_url(path):
        if urllib.parse.urlparse(path).netloc: return path
        return os.path.basename(path)
    # Filter to return URL for given symbol or the full URL, if absolute
    def path_to_url(path):
        if urllib.parse.urlparse(path).netloc: return path
        return path + '.html'
    env.filters['basename_or_url'] = basename_or_url
    env.filters['path_to_url'] = path_to_url
    env.filters['urljoin'] = urljoin
    env.filters['render_rst'] = m.htmlsanity.render_rst

    # Make the output dir absolute
    config['OUTPUT'] = os.path.join(basedir, config['OUTPUT'])
    if not os.path.exists(config['OUTPUT']): os.makedirs(config['OUTPUT'])

    # Guess MIME type of the favicon
    if config['FAVICON']:
        config['FAVICON'] = (config['FAVICON'], mimetypes.guess_type(config['FAVICON'])[0])

    for module in config['INPUT_MODULES']:
        if isinstance(module, str):
            module_name = module
            module = importlib.import_module(module)
        else:
            module_name = module.__name__

        render_module(config, [module_name], module, env)

    # Create index.html
    # TODO: use actual reST source and have this just as a fallback
    page = Empty()
    page.breadcrumb = [(config['PROJECT_TITLE'], 'index.html')]
    page.url = page.breadcrumb[-1][1]
    render(config, 'page.html', page, env)

    # Copy referenced files
    for i in config['STYLESHEETS'] + config['EXTRA_FILES'] + ([config['FAVICON'][0]] if config['FAVICON'] else []) + ([] if config['SEARCH_DISABLED'] else ['search.js']):
        # Skip absolute URLs
        if urllib.parse.urlparse(i).netloc: continue

        # If file is found relative to the conf file, use that
        if os.path.exists(os.path.join(basedir, i)):
            i = os.path.join(basedir, i)

        # Otherwise use path relative to script directory
        else:
            i = os.path.join(os.path.dirname(os.path.realpath(__file__)), i)

        logging.debug("copying %s to output", i)
        shutil.copy(i, os.path.join(config['OUTPUT'], os.path.basename(i)))

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
