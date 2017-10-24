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
from docutils.parsers.rst.states import Inliner
from docutils import nodes, utils
from docutils.parsers import rst
from pelican import signals
import xml.etree.ElementTree as ET

import logging

logger = logging.getLogger(__name__)

symbol_mapping = {}
symbol_prefixes = ['']

def init(pelicanobj):
    global symbol_mapping, symbol_prefixes

    tagfiles = pelicanobj.settings.get('M_DOX_TAGFILES', [])

    # Pre-round to populate subclasses

    for tagfile, path, prefixes in tagfiles:
        symbol_prefixes += prefixes

        tree = ET.parse(tagfile)
        root = tree.getroot()
        for child in root:
            if child.tag == 'compound' and 'kind' in child.attrib:
                # Linking to pages
                if child.attrib['kind'] == 'page':
                    link = path + child.find('filename').text + '.html'
                    symbol_mapping[child.find('name').text] = link

                    # Page sections
                    for section in child.findall('docanchor'):
                        symbol_mapping[section.text] = link + '#' + section.text

                # Linking to files
                if child.attrib['kind'] == 'file':
                    link = path + child.find('filename').text + ".html"
                    symbol_mapping[child.find('path').text + child.find('name').text] = link

                    for member in child.findall('member'):
                        if not 'kind' in member.attrib: continue

                        # Preprocessor defines and macros
                        if member.attrib['kind'] == 'define':
                            symbol_mapping[member.find('name').text + ('()' if member.find('arglist').text else '')] = link + '#' + member.find('anchor').text

                # Linking to namespaces, structs and classes
                if child.attrib['kind'] in ['class', 'struct', 'namespace']:
                    symbol_mapping[child.find('name').text] = path + child.find('filename').text
                    name = child.find('name').text
                    link = path + child.find('filename').text
                    symbol_mapping[name] = link
                    for member in child.findall('member'):
                        if not 'kind' in member.attrib: continue

                        # Typedefs, constants
                        if member.attrib['kind'] == 'typedef' or member.attrib['kind'] == 'enumvalue':
                            symbol_mapping[name + '::' + member.find('name').text] = link + '#' + member.find('anchor').text

                        # Functions
                        if member.attrib['kind'] == 'function':
                            symbol_mapping[name + '::' + member.find('name').text + "()"] = link + '#' + member.find('anchor').text

                        # Enums with values
                        if member.attrib['kind'] == 'enumeration':
                            enumeration = name + '::' + member.find('name').text
                            symbol_mapping[enumeration] = link + '#' + member.find('anchor').text

                            for value in member.findall('enumvalue'):
                                symbol_mapping[enumeration + '::' + value.text] = link + '#' + value.attrib['anchor']

def dox(name, rawtext, text, lineno, inliner: Inliner, options={}, content=[]):
    title, target = parse_link(text)
    if not title: title = target

    for prefix in symbol_prefixes:
        if prefix + target in symbol_mapping:
            url = symbol_mapping[prefix + target]
            node = nodes.reference(rawtext, title, refuri=url, **options)
            return [node], []

    # TODO: print file and line
    #msg = inliner.reporter.warning(
        #'Doxygen symbol %s not found' % target, line=lineno)
    #prb = inliner.problematic(rawtext, rawtext, msg)
    logger.warning('Doxygen symbol `%s` not found, rendering as monospace' % target)
    node = nodes.literal(rawtext, title, **options)
    return [node], []

def register():
    signals.initialized.connect(init)

    rst.roles.register_local_role('dox', dox)
