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

import xml.etree.ElementTree as ET
import argparse
import urllib.parse
import logging
import mimetypes
import os
import shutil
from types import SimpleNamespace as Empty
from typing import Tuple, Dict, Any, List
from urllib.parse import urljoin

from jinja2 import Environment, FileSystemLoader

default_templates = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/csharp/')

class Node:
    def __init__(self):
        self.id:int = None
        self.children: Dict[str, Node] = {}

def make_url(path: List[str]) -> str:
    return '.'.join(path) + '.html'

def run(file, output, templates):
    basedir = os.path.dirname(file)

    try:
        tree = ET.parse(file)
    except ET.ParseError as e:
        logging.error("XML parse error in %s: %s", file, e)
        return

    root = tree.getroot()
    assert root.tag == 'doc'

    logging.debug("Parsing %s", file)

    assembly = root.find('assembly/name').text

    #state = State(output, templates)

    parsed: List[Any] = []
    tree: Node = Node()

    # Go through all members and build a hierarchy tree + parsed summaries for
    # linking
    members = root.find('members')
    for member in members:
        assert member.tag == 'member'

        # Skip unknown types for now
        # TODO: implement all of them
        if member.attrib['name'][0] not in ['N', 'T', 'M']:
            logging.warning("unknown type of %s, skipping", member.attrib['name'])
            continue

        # Split the name into a path, take extra care to exclude function
        # parameters, because these have dots as well
        name = member.attrib['name'][2:]
        parenthesis = name.find('(')
        if parenthesis != -1:
            path = name[:parenthesis].split('.')
            path[-1] += name[parenthesis:]
        else:
            path = name.split('.')

        # Find where to put it
        node: Node = tree
        for i in path:
            # Not there yet, add a new entry
            if not i in node.children: node.children[i] = Node()

            # Dig deeper
            node = node.children[i]

        # The found entry should not be initalized yet -- that would mean there
        # are duplicated entries in the tree
        assert node is not tree
        if node.id is not None: # TODO turn into an assert
            logging.fatal("duplicated entry %s, previously at %s, aborting", name, node.id)
            exit(1)

        # Entry index is current position in the parsed array
        node.id = len(parsed)

        # Populate the parsed entry
        entry = Empty()
        entry.path = path
        entry.type = member.attrib['name'][0]
        entry.summary = member.find('summary').text # TODO

        # Namespace properties
        if entry.type == 'N':
            pass

        # Class, interface, struct, enum, delegate propertoes
        elif entry.type == 'T':
            pass

        # Field properties
        # TODO wasisdas???
        #elif entry.type == 'F':
            #pass

        # Property properties
        # TODO
        #elif entry.type == 'P':
            #pass

        # Method properties
        elif entry.type == 'M':
            # TODO: returns, param
            pass

        # Event properties
        #elif entry.type == 'E':
            #pass

        else: assert False # pragma: no cover

        # Add the entry to the list
        parsed += [entry]

    # Prepare Jinja environment
    # TODO cleanup
    env = Environment(loader=FileSystemLoader(templates),
                      trim_blocks=True, lstrip_blocks=True, enable_async=True)
    # Filter to return file basename or the full URL, if absolute
    def basename_or_url(path):
        if urllib.parse.urlparse(path).netloc: return path
        return os.path.basename(path)
    env.filters['basename_or_url'] = basename_or_url
    env.filters['urljoin'] = urljoin
    if not os.path.exists(output):
        os.makedirs(output)
    templates = {
        'N': 'namespace.html',
        'T': 'type.html'
    }

    # TODO: ugh
    config = {
        'M_THEME_COLOR': '#22272e',
        'M_FAVICON': 'favicon-dark.png',
        'M_PAGE_FINE_PRINT': '[default]',
        'M_SEARCH_DISABLED': False,
        'M_SEARCH_DOWNLOAD_BINARY': False,
        'M_SEARCH_HELP':
"""<p class="m-noindent">Search for namespaces, types, methods and other
symbols. You can omit any prefix from the symbol path; adding a <code>.</code>
suffix lists all members of given symbol.</p>
<p class="m-noindent">Use <span class="m-label m-dim">&darr;</span>
/ <span class="m-label m-dim">&uarr;</span> to navigate through the list,
<span class="m-label m-dim">Enter</span> to go.
<span class="m-label m-dim">Tab</span> autocompletes common prefix, you can
copy a link to the result using <span class="m-label m-dim">⌘</span>
<span class="m-label m-dim">L</span> while <span class="m-label m-dim">⌘</span>
<span class="m-label m-dim">M</span> produces a Markdown link.</p>""",
        'HTML_EXTRA_STYLESHEET': [
            'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
            '../css/m-dark+doxygen.compiled.css']
    }

    # Guess MIME type of the favicon
    if config['M_FAVICON']:
        config['M_FAVICON'] = (config['M_FAVICON'], mimetypes.guess_type(config['M_FAVICON'])[0])

    # Go through the tree and assume everything that doesn't have an ID yet and
    # doesn't have members is a namespace, things having members are a class
    # TODO: why the heck do they document the N: then?!
    def recurse_tree_find_hidden_namespaces(parsed, path, node: Node):
        for name, child in node.children.items():
            if child.id is None:
                # If any child has members, it's definitely not a namespace
                type = 'N'
                for _, grandchild in child.children.items():
                    if grandchild.id is not None and parsed[grandchild.id].type == 'M':
                        type = 'T'
                        break

                entry = Empty()
                entry.path = path + [name]
                entry.type = type
                entry.summary = None
                child.id = len(parsed)
                parsed += [entry]

            recurse_tree_find_hidden_namespaces(parsed, path + [name], child)
    recurse_tree_find_hidden_namespaces(parsed, [], tree)

    # We have a tree, now generate docs for each entry
    for entry in parsed:
        # Include only namespaces and types, everything else is handled inside
        # these
        if entry.type not in ['N', 'T']: continue

        # Page content
        page = Empty()
        page.summary = entry.summary # TODO
        if entry.type == 'N': page.namespaces = []
        page.types = []
        if entry.type == 'T': page.methods = []

        # Breadcrumb, name, URL
        page.breadcrumb = []
        for i in range(len(entry.path)):
            page.breadcrumb += [(entry.path[i], make_url(entry.path[:(i + 1)]))]
        page.name = page.breadcrumb[-1][0] # TODO this iz redudnantntntntn
        page.url = page.breadcrumb[-1][1]

        # Collect the children
        node = tree
        #print(path)
        for i in entry.path:
            #print(i)
            node = node.children[i]
        #print(node.children)
        for name, child_node in node.children.items():
            child = parsed[child_node.id]

            if child.type == 'N':
                assert entry.type == 'N'
                namespace = Empty()
                namespace.url = make_url(child.path)
                namespace.name = name
                namespace.summary = child.summary
                page.namespaces += [namespace]
            elif child.type == 'T':
                type = Empty()
                type.url = make_url(child.path)
                type.name = name
                type.summary = child.summary
                page.types += [type]
            elif child.type == 'M':
                print("YAYYYYY")
                if not entry.type == 'T':
                    print(entry.type, name)
                    assert False
                method = Empty()
                method.name = name
                method.summary = child.summary
                page.methods += [method]
            else: assert False # pragma: no cover

        # Render
        logging.debug("rendering %s", page.url)
        template = env.get_template(templates[entry.type])
        rendered = template.render(page=page,
            PROJECT_NAME=assembly, **config)
        with open(os.path.join(output, page.url), 'wb') as f:
            f.write(rendered.encode('utf-8'))
            # Add back a trailing newline so we don't need to bother with
            # patching test files to include a trailing newline to make Git
            # happy
            # TODO could keep_trailing_newline fix this better?
            f.write(b'\n')

    # Copy referenced files
    # TODO: ugh
    for i in config['HTML_EXTRA_STYLESHEET'] + ([config['M_FAVICON'][0]] if config['M_FAVICON'] else []) + ([] if config['M_SEARCH_DISABLED'] else ['search.js']):
        # Skip absolute URLs
        if urllib.parse.urlparse(i).netloc: continue

        # If file is found relative to the Doxyfile, use that
        if os.path.exists(os.path.join(basedir, i)):
            i = os.path.join(basedir, i)

        # Otherwise use path relative to script directory
        else:
            i = os.path.join(os.path.dirname(os.path.realpath(__file__)), i)

        logging.debug("copying %s to output", i)
        shutil.copy(i, os.path.join(output, os.path.basename(i)))

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="where the XMLDoc file is")
    parser.add_argument('--output', help="output directory", default='output')
    parser.add_argument('--templates', help="template directory", default=default_templates)
    parser.add_argument('--debug', help="verbose debug output", action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    fileabs = os.path.abspath(args.file)
    run(fileabs, os.path.join(os.path.dirname(fileabs), args.output), os.path.abspath(args.templates))
