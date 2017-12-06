#!/usr/bin/env python

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

import xml.etree.ElementTree as ET
import argparse
import sys
import re
import html
import os
import glob
import shutil
import subprocess
import urllib.parse
import logging
from types import SimpleNamespace as Empty
from typing import Tuple, Dict, Any, List

from jinja2 import Environment, FileSystemLoader

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, BashSessionLexer, get_lexer_by_name, find_lexer_class_for_filename

sys.path.append("../pelican-plugins")
import m.latex2svg
import m.math
import m.ansilexer

xref_id_rx = re.compile(r"""(.*)_1(_[a-z-]+[0-9]+)$""")
slugify_nonalnum_rx = re.compile(r"""[^\w\s-]""")
slugify_hyphens_rx = re.compile(r"""[-\s]+""")

class State:
    def __init__(self):
        self.basedir = ''
        self.compounds: Dict[str, Any] = {}
        self.doxyfile: Dict[str, str] = {}
        self.images: List[str] = []

def slugify(text: str) -> str:
    # Maybe some Unicode normalization would be nice here?
    return slugify_hyphens_rx.sub('-', slugify_nonalnum_rx.sub('', text.lower()).strip())

def add_wbr(text: str) -> str:
    # Stuff contains HTML code, do not touch!
    if '<' in text: return text

    if '::' in text: # C++ names
        return text.replace('::', '::<wbr/>')
    elif '_' in text: # VERY_LONG_UPPER_CASE macro names
        return text.replace('_', '_<wbr/>')

    # These characters are quite common, so at least check that there is no
    # space (which may hint that the text is actually some human language):
    elif '/' in text and not ' ' in text: # URLs
        return text.replace('/', '/<wbr/>')
    else:
        return text

def parse_ref(state: State, element: ET.Element) -> str:
    id = element.attrib['refid']

    if element.attrib['kindref'] == 'compound':
        url = id + '.html'
    elif element.attrib['kindref'] == 'member':
        i = id.rindex('_1')
        url = id[:i] + '.html' + '#' + id[i+2:]
    else: # pragma: no cover
        logging.critical("unknown <ref> kind {}".format(element.attrib['kindref']))
        assert False

    if 'external' in element.attrib:
        for i in state.doxyfile['TAGFILES']:
            name, _, baseurl = i.partition('=')
            if os.path.basename(name) == os.path.basename(element.attrib['external']):
                url = os.path.join(baseurl, url)
                break
        else: # pragma: no cover
            logging.critical("tagfile {} not specified in Doxyfile".format(element.attrib['external']))
            assert False
        class_ = 'm-dox-external'
    else:
        class_ = 'm-dox'

    return '<a href="{}" class="{}">{}</a>'.format(url, class_, add_wbr(html.escape(element.text)))

def extract_id(element: ET.Element) -> str:
    id = element.attrib['id']
    i = id.rindex('_1')
    return id[i+2:]

def fix_type_spacing(type: str) -> str:
    return type.replace('&lt; ', '&lt;').replace(' &gt;', '&gt;').replace(' &amp;', '&amp;').replace(' *', '*')

def parse_type(state: State, type: ET.Element) -> str:
    # Constructors and typeless enums might not have it
    if type is None: return None
    out = html.escape(type.text) if type.text else ''

    i: ET.Element
    for i in type:
        if i.tag == 'ref':
            out += parse_ref(state, i)
        elif i.tag == 'anchor':
            out += '<a name="{}"></a>'.format(extract_id(i))
        else: # pragma: no cover
            logging.warning("ignoring {} in <type>".format(i.tag))

        if i.tail: out += html.escape(i.tail)

    # Remove spacing inside <> and before & and *
    return fix_type_spacing(out)

def parse_desc_internal(state: State, element: ET.Element, immediate_parent: ET.Element = None, trim = True):
    out = Empty()
    out.section = None
    out.templates = {}
    out.params = {}
    out.return_value = None

    # DOXYGEN <PARA> PATCHING 1/5
    #
    # In the optimistic case, when parsing the <para> element, the parsed
    # content is treated as single reasonable paragraph and the caller is told
    # to write both <p> and </p> enclosing tag.
    #
    # Unfortunately Doxygen puts some *block* elements inside a <para> element
    # instead of closing it before and opening it again after. That is making
    # me raging mad. Nested paragraphs are no way valid HTML and they are ugly
    # and problematic in all ways you can imagine, so it's needed to be
    # patched. See the long ranty comments below for more parts of the story.
    out.write_paragraph_start_tag = element.tag == 'para'
    out.write_paragraph_close_tag = element.tag == 'para'
    out.is_reasonable_paragraph = element.tag == 'para'

    out.parsed: str = ''
    if element.text:
        out.parsed = html.escape(element.text.strip() if trim else element.text)

    # Needed later for deciding whether we can strip the surrounding <p> from
    # the content
    paragraph_count = 0
    has_block_elements = False

    i: ET.Element
    for i in element:
        # DOXYGEN <PARA> PATCHING 2/5
        #
        # Upon encountering a block element nested in <para>, we need to act.
        # If there was any content before, we close the paragraph. If there
        # wasn't, we tell the caller to not even open the paragraph. After
        # processing the following tag, there probably won't be any paragraph
        # open, so we also tell the caller that there's no need to close
        # anything (but it's not that simple, see for more patching at the end
        # of the cycle iteration).
        #
        # Those elements are:
        # - <heading>
        # - <blockquote>
        # - <simplesect> and <xrefsect>
        # - <verbatim>
        # - <variablelist>, <itemizedlist>, <orderedlist>
        # - <image>, <table>
        # - block <formula>
        # - <programlisting> (complex block/inline autodetection involved, so
        #   the check is deferred to later in the loop)
        #
        # Note that <parameterlist> and <simplesect kind="return"> are
        # extracted out of the text flow, so these are removed from this check.
        #
        # In addition, there's special handling to achieve things like this:
        #   <ul>
        #     <li>A paragraph
        #       <ul>
        #         <li>A nested list item</li>
        #       </ul>
        #     </li>
        # I.e., not wrapping "A paragraph" in a <p>, but only if it's
        # immediately followed by another and it's the first paragraph in a
        # list item. We check that using the immediate_parent variable.
        if (i.tag in ['heading', 'blockquote', 'xrefsect', 'variablelist', 'verbatim', 'itemizedlist', 'orderedlist', 'image', 'table'] or (i.tag == 'simplesect' and i.attrib['kind'] != 'return') or (i.tag == 'formula' and i.text.startswith('\[ ') and i.text.endswith(' \]'))) and element.tag == 'para' and out.write_paragraph_close_tag:
            out.is_reasonable_paragraph = False
            out.parsed = out.parsed.rstrip()
            if not out.parsed:
                out.write_paragraph_start_tag = False
            elif immediate_parent and immediate_parent.tag == 'listitem' and i.tag in ['itemizedlist', 'orderedlist']:
                out.write_paragraph_start_tag = False
            else:
                out.parsed += '</p>'
            out.write_paragraph_close_tag = False

        # Block elements
        if i.tag in ['sect1', 'sect2', 'sect3']:
            assert element.tag != 'para' # should be top-level block element
            has_block_elements = True

            parsed = parse_desc_internal(state, i)
            assert parsed.section
            assert not parsed.templates and not parsed.params and not parsed.return_value

            # Top-level section has no ID or title
            if not out.section: out.section = ('', '', [])
            out.section = (out.section[0], out.section[1], out.section[2] + [parsed.section])
            out.parsed += '<section id="{}">{}</section>'.format(extract_id(i), parsed.parsed)

        elif i.tag == 'title':
            assert element.tag != 'para' # should be top-level block element
            has_block_elements = True

            if element.tag == 'sect1':
                tag = 'h2'
            elif element.tag == 'sect2':
                tag = 'h3'
            elif element.tag == 'sect3':
                tag = 'h4'
            else: # pragma: no cover
                assert False
            id = extract_id(element)
            title = html.escape(i.text)

            # Populate section info
            assert not out.section
            out.section = (id, title, [])
            out.parsed += '<{0}><a href="#{1}">{2}</a></{0}>'.format(tag, id, title)

        elif i.tag == 'heading':
            has_block_elements = True

            if i.attrib['level'] == '1':
                tag = 'h2'
            elif i.attrib['level'] == '2':
                tag = 'h3'
            elif i.attrib['level'] == '3':
                tag = 'h4'
            elif i.attrib['level'] == '4':
                tag = 'h5'
            else: # pragma: no cover
                assert False
            logging.warning("Prefer @section over Markdown heading for properly generated TOC")
            out.parsed += '<{0}>{1}</{0}>'.format(tag, html.escape(i.text))

        elif i.tag == 'para':
            assert element.tag != 'para' # should be top-level block element
            paragraph_count += 1

            # DOXYGEN <PARA> PATCHING 3/5
            #
            # Parse contents of the paragraph, don't trim whitespace around
            # nested elements but trim it at the begin and end of the paragraph
            # itself. Also, some paragraphs are actually block content and we
            # might not want to write the start/closing tag.
            #
            # Also, to make things even funnier, parameter and return value
            # description come from inside of some paragraph, so bubble them up
            # and assume they are not scattered all over the place (ugh).
            #
            # There's also the patching of nested lists that results in the
            # immediate_parent variable in the section 2/5 -- we pass the
            # parent only if this is the first paragraph inside it.
            parsed = parse_desc_internal(state, i, element if paragraph_count == 1 and not has_block_elements else None, False)
            parsed.parsed = parsed.parsed.strip()
            if not parsed.is_reasonable_paragraph:
                has_block_elements = True
            if parsed.parsed:
                if parsed.write_paragraph_start_tag: out.parsed += '<p>'
                out.parsed += parsed.parsed
                if parsed.write_paragraph_close_tag: out.parsed += '</p>'
            if parsed.templates:
                assert not out.templates
                out.templates = parsed.templates
            if parsed.params:
                assert not out.params
                out.params = parsed.params
            if parsed.return_value:
                assert not out.return_value
                out.return_value = parsed.return_value

            # Assert we didn't miss anything important
            assert not parsed.section

        elif i.tag == 'blockquote':
            has_block_elements = True
            out.parsed += '<blockquote>{}</blockquote>'.format(parse_desc(state, i))

        elif i.tag in ['itemizedlist', 'orderedlist']:
            has_block_elements = True
            tag = 'ul' if i.tag == 'itemizedlist' else 'ol'
            out.parsed += '<{}>'.format(tag)
            for li in i:
                assert li.tag == 'listitem'
                out.parsed += '<li>{}</li>'.format(parse_desc(state, li))
            out.parsed += '</{}>'.format(tag)

        elif i.tag == 'table':
            has_block_elements = True
            out.parsed += '<table class="m-table">'
            inside_tbody = False

            row: ET.Element
            for row in i:
                assert row.tag == 'row'
                is_header_row = True
                row_data = ''
                for entry in row:
                    assert entry.tag == 'entry'
                    is_header = entry.attrib['thead'] == 'yes'
                    is_header_row = is_header_row and is_header
                    row_data += '<{0}>{1}</{0}>'.format('th' if is_header else 'td', parse_desc(state, entry))
                if is_header_row:
                    assert not inside_tbody # Assume there's only one header row
                    out.parsed += '<thead><tr>{}</tr></thead><tbody>'.format(row_data)
                    inside_tbody = True
                else:
                    out.parsed += '<tr>{}</tr>'.format(row_data)

            if inside_tbody: out.parsed += '</tbody>'
            out.parsed += '</table>'

        elif i.tag == 'simplesect':
            # Return value is separated from the text flow
            if i.attrib['kind'] == 'return':
                assert not out.return_value
                out.return_value = parse_desc(state, i)
            else:
                has_block_elements = True
                if i.attrib['kind'] == 'see':
                    out.parsed += '<aside class="m-note m-default"><h4>See also</h4>'
                elif i.attrib['kind'] == 'note':
                    out.parsed += '<aside class="m-note m-info"><h4>Note</h4>'
                elif i.attrib['kind'] == 'attention':
                    out.parsed += '<aside class="m-note m-warning"><h4>Attention</h4>'
                else: # pragma: no cover
                    out.parsed += '<aside class="m-note">'
                    logging.warning("ignoring {} kind of <simplesect>".format(i.attrib['kind']))
                out.parsed += parse_desc(state, i)
                out.parsed += '</aside>'

        elif i.tag == 'xrefsect':
            has_block_elements = True

            id = i.attrib['id']
            match = xref_id_rx.match(id)
            file = match.group(1)
            if file.startswith(('deprecated', 'bug')):
                color = 'm-danger'
            elif file.startswith('todo'):
                color = 'm-dim'
            else:
                color = 'm-default'
            out.parsed += '<aside class="m-note {}"><h4><a href="{}.html#{}" class="m-dox">{}</a></h4>{}</aside>'.format(
                color, file, match.group(2), i.find('xreftitle').text, parse_desc(state, i.find('xrefdescription')))

        elif i.tag == 'parameterlist':
            has_block_elements = True

            out.param_kind = i.attrib['kind']
            assert out.param_kind in ['param', 'templateparam']
            for param in i:
                # This is an overcomplicated shit, so check sanity
                assert param.tag == 'parameteritem'
                assert len(param.findall('parameternamelist')) == 1
                assert param.find('parameternamelist').find('parametertype') is None
                assert len(param.find('parameternamelist').findall('parametername')) == 1

                name = param.find('parameternamelist').find('parametername')
                description = parse_desc(state, param.find('parameterdescription'))
                if i.attrib['kind'] == 'param':
                    out.params[name.text] = (description, name.attrib['direction'] if 'direction' in name.attrib else '')
                else:
                    assert i.attrib['kind'] == 'templateparam'
                    out.templates[name.text] = description

        elif i.tag == 'variablelist':
            has_block_elements = True
            out.parsed += '<dl class="m-dox">'

            for var in i:
                if var.tag == 'varlistentry':
                    out.parsed += '<dt>{}</dt>'.format(parse_type(state, var.find('term')).strip())
                else:
                    assert var.tag == 'listitem'
                    out.parsed += '<dd>{}</dd>'.format(parse_desc(state, var))

            out.parsed += '</dl>'

        elif i.tag == 'verbatim':
            has_block_elements = True
            out.parsed += '<pre class="m-code">{}</pre>'.format(html.escape(i.text))

        elif i.tag == 'programlisting':
            # If it seems to be a standalone code paragraph, don't wrap it in
            # <p> and use <pre>:
            # - is either alone in the paragraph, with no text or other
            #   elements around
            # - or is a code snippet (filename instead of just .ext). Doxygen
            #   unfortunately doesn't put @snippet in its own paragraph even
            #   if it's separated by blank lines. It does so for @include and
            #   related, though.
            if element.tag == 'para' and (((not element.text or not element.text.strip()) and (not i.tail or not i.tail.strip()) and len([listing for listing in element]) == 1) or ('filename' in i.attrib and not i.attrib['filename'].startswith('.'))):
                code_block = True

            # Looks like inline code, but has multiple code lines, so it's
            # suspicious. Use code block, but warn.
            elif len([codeline for codeline in i]) > 1:
                code_block = True
                logging.warning("Inline code has multiple lines, fallback to a code block")

            # Otherwise wrap it in <p> and use <code>
            else:
                code_block = False

                # Doxygen doesn't add a space before <programlisting> if it's
                # inline, add it manually in case there should be a space
                # before it. However, it does add a space after it always.
                if out.parsed and not out.parsed[-1].isspace() and not out.parsed[-1] in '([{':
                    out.parsed += ' '

            # DOXYGEN <PARA> PATCHING 4/5
            #
            # Specialization of similar paragraph cleanup code above.
            if code_block:
                out.is_reasonable_paragraph = False
                has_block_elements = True
                out.parsed = out.parsed.rstrip()
                if not out.parsed:
                    out.write_paragraph_start_tag = False
                else:
                    out.parsed += '</p>'
                out.write_paragraph_close_tag = False

            # Hammer unhighlighted code out of the block
            # TODO: preserve links
            code = ''
            codeline: ET.Element
            for codeline in i:
                assert codeline.tag == 'codeline'

                tag: ET.Element
                for tag in codeline:
                    assert tag.tag == 'highlight'
                    if tag.text: code += tag.text

                    token: ET.Element
                    for token in tag:
                        if token.tag == 'sp':
                            if 'value' in token.attrib:
                                code += chr(int(token.attrib['value']))
                            else:
                                code += ' '
                        elif token.tag == 'ref':
                            # Ignoring <ref> until a robust solution is found
                            # (i.e., also ignoring false positives)
                            code += token.text
                        else: # pragma: no cover
                            logging.warning("Unknown {} in a code block ".format(token.tag))

                        if token.tail: code += token.tail

                    if tag.tail: code += tag.tail

                code += '\n'

            # Strip whitespace around if inline code, strip only trailing
            # whitespace if a block
            if not code_block: code = code.strip()

            if not 'filename' in i.attrib:
                logging.warning("No filename attribute in <programlisting>, assuming C++")
                filename = 'file.cpp'
            else:
                filename = i.attrib['filename']

            # Custom mapping of filenames to languages
            mapping = [('.h', 'c++'),
                       ('.h.cmake', 'c++'),
                       ('.h.nostrip', 'c++'),
                       # Pygments knows only .vert, .frag, .geo
                       ('.glsl', 'glsl'),
                       ('.conf', 'ini'),
                       ('.ansi', m.ansilexer.AnsiLexer)]
            for key, v in mapping:
                if not filename.endswith(key): continue

                if isinstance(v, str):
                    lexer = get_lexer_by_name(v)
                else:
                    lexer = v()
                break

            # Otherwise try to find lexer by filename
            else:
                # Put some bogus prefix to the filename in case it is just
                # `.ext`
                lexer = find_lexer_class_for_filename("code" + filename)
                if not lexer:
                    logging.warning("Unrecognized language of {} in <programlisting>, highlighting disabled".format(filename))
                    lexer = TextLexer()
                else: lexer = lexer()

            # Style console sessions differently
            if (isinstance(lexer, BashSessionLexer) or
                isinstance(lexer, m.ansilexer.AnsiLexer)):
                class_ = 'm-console'
            else:
                class_ = 'm-code'

            formatter = HtmlFormatter(nowrap=True)
            highlighted = highlight(code, lexer, formatter)
            # Strip whitespace around if inline code, strip only trailing
            # whitespace if a block
            highlighted = highlighted.rstrip() if code_block else highlighted.strip()
            out.parsed += '<{0} class="{1}">{2}</{0}>'.format('pre' if code_block else 'code', class_, highlighted)

        elif i.tag == 'image':
            has_block_elements = True
            name = i.attrib['name']
            path = None

            if i.attrib['type'] == 'html':
                # Discover the real path of the image
                for candidate in state.doxyfile['IMAGE_PATH']:
                    path = os.path.join(state.basedir, candidate, name)
                    if os.path.exists(path):
                        state.images += [path]
                        break
                else:
                    logging.warning("Image {} was not found in any IMAGE_PATH".format(name))

                alt = i.text
                if not alt:
                    alt = 'Image'
                    logging.warning("Image {} has no alt text".format(name))

                out.parsed += '<img class="m-image" src="{}" alt="{}" />'.format(name, html.escape(alt))

        # Either block or inline because DOXYGEN!!! WHAT!!!
        elif i.tag == 'formula':
            # Inline formula
            if i.text.startswith('$ ') and i.text.endswith(' $'):
                rendered = m.latex2svg.latex2svg('${}$'.format(i.text[2:-2]), params=m.math.latex2svg_params)

                # CSS classes and styling for proper vertical alignment. Depth is relative
                # to font size, describes how below the line the text is. Scaling it back
                # to 12pt font, scaled by 125% as set above in the config.
                attribs = ' class="m-math" style="vertical-align: -{:.1f}pt;"'.format(rendered['depth']*12*1.25)
                out.parsed += m.math._patch(i.text, rendered, attribs)

            # Block formula
            else:
                assert i.text.startswith('\[ ') and i.text.endswith(' \]')
                has_block_elements = True
                rendered = m.latex2svg.latex2svg('$${}$$'.format(i.text[3:-3]), params=m.math.latex2svg_params)
                out.parsed += '<div class="m-math">{}</div>'.format(m.math._patch(i.text, rendered, ''))

        # Inline elements
        elif i.tag == 'anchor':
            out.parsed += '<a name="{}"></a>'.format(extract_id(i))

        elif i.tag == 'computeroutput':
            out.parsed += '<code>{}</code>'.format(parse_inline_desc(state, i))

        elif i.tag == 'emphasis':
            out.parsed += '<em>{}</em>'.format(parse_inline_desc(state, i))

        elif i.tag == 'bold':
            out.parsed += '<strong>{}</strong>'.format(parse_inline_desc(state, i))

        elif i.tag == 'ref':
            out.parsed += parse_ref(state, i)

        elif i.tag == 'ulink':
            out.parsed += '<a href="{}">{}</a>'.format(html.escape(i.attrib['url']), add_wbr(parse_inline_desc(state, i)))

        # WHAT THE HELL WHY IS THIS NOT AN XML ENTITY
        elif i.tag == 'ndash': out.parsed += '&ndash;'
        elif i.tag == 'mdash': out.parsed += '&mdash;'

        # Something new :O
        else: # pragma: no cover
            logging.warning("Ignoring <{}> in desc".format(i.tag))

        # DOXYGEN <PARA> PATCHING 5/5
        #
        # Besides putting notes and blockquotes and shit inside paragraphs,
        # Doxygen also doesn't attempt to open a new <para> for the ACTUAL NEW
        # PARAGRAPH after they end. So I do it myself and give a hint to the
        # caller that they should close the <p> again.
        if element.tag == 'para' and not out.write_paragraph_close_tag and i.tail and i.tail.strip():
            out.parsed += '<p>'
            out.write_paragraph_close_tag = True
            # There is usually some whitespace in between, get rid of it as
            # this is a start of a new paragraph. Stripping of the whole thing
            # is done by the caller.
            out.parsed += html.escape(i.tail.lstrip())

        # Otherwise strip only if requested by the called
        elif i.tail:
            out.parsed += html.escape(i.tail.strip() if trim else i.tail)

    # Brief description always needs to be single paragraph because we're
    # sending it out without enclosing <p>.
    if element.tag == 'briefdescription':
        assert not has_block_elements and paragraph_count <= 1
        if paragraph_count == 1:
            assert out.parsed.startswith('<p>') and out.parsed.endswith('</p>')
            out.parsed = out.parsed[3:-4]

    # Strip superfluous <p> for simple elments (list items, parameter and
    # return value description, table cells), but only if there is just a
    # single paragraph
    elif (element.tag in ['listitem', 'parameterdescription', 'entry'] or (element.tag == 'simplesect' and element.attrib['kind'] == 'return')) and not has_block_elements and paragraph_count == 1 and out.parsed:
        assert out.parsed.startswith('<p>') and out.parsed.endswith('</p>')
        out.parsed = out.parsed[3:-4]

    return out

def parse_desc(state: State, element: ET.Element) -> str:
    if element is None: return ''

    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element)
    assert not parsed.templates and not parsed.params and not parsed.return_value
    assert not parsed.section # might be problematic
    return parsed.parsed

def parse_var_desc(state: State, element: ET.Element) -> str:
    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element.find('detaileddescription'))
    parsed.parsed += parse_desc(state, element.find('inbodydescription'))
    assert not parsed.templates and not parsed.params and not parsed.return_value
    assert not parsed.section # might be problematic
    return parsed.parsed

def parse_toplevel_desc(state: State, element: ET.Element):
    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element)
    assert not parsed.return_value
    if parsed.params:
        logging.warning("Use @tparam instead of @param for documenting class templates, @param is ignored")
    return (parsed.parsed, parsed.templates, parsed.section[2] if parsed.section else '')

def parse_typedef_desc(state: State, element: ET.Element):
    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element.find('detaileddescription'))
    parsed.parsed += parse_desc(state, element.find('inbodydescription'))
    assert not parsed.params and not parsed.return_value
    assert not parsed.section # might be problematic
    return (parsed.parsed, parsed.templates)

def parse_func_desc(state: State, element: ET.Element):
    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element.find('detaileddescription'))
    parsed.parsed += parse_desc(state, element.find('inbodydescription'))
    assert not parsed.section # might be problematic
    return (parsed.parsed, parsed.templates, parsed.params, parsed.return_value)

def parse_define_desc(state: State, element: ET.Element):
    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element.find('detaileddescription'))
    parsed.parsed += parse_desc(state, element.find('inbodydescription'))
    assert not parsed.templates
    assert not parsed.section # might be problematic
    return (parsed.parsed, parsed.params, parsed.return_value)

def parse_inline_desc(state: State, element: ET.Element) -> str:
    if element is None: return ''

    # Verify that we didn't ignore any important info by accident
    parsed = parse_desc_internal(state, element)
    assert not parsed.templates and not parsed.params and not parsed.return_value
    assert not parsed.section
    return parsed.parsed

def parse_enum(state: State, element: ET.Element):
    assert element.tag == 'memberdef' and element.attrib['kind'] == 'enum'

    enum = Empty()
    enum.id = extract_id(element)
    enum.type = parse_type(state, element.find('type'))
    enum.name = element.find('name').text
    if enum.name.startswith('@'): enum.name = '(anonymous)'
    enum.brief = parse_desc(state, element.find('briefdescription'))
    enum.description = parse_desc(state, element.find('detaileddescription')) + parse_desc(state, element.find('inbodydescription'))
    enum.is_protected = element.attrib['prot'] == 'protected'
    enum.is_strong = False
    if 'strong' in element.attrib:
        enum.is_strong = element.attrib['strong'] == 'yes'
    enum.values = []

    enum.has_value_details = False
    enumvalue: ET.Element
    for enumvalue in element.findall('enumvalue'):
        value = Empty()
        value.id = extract_id(enumvalue)
        value.name = enumvalue.find('name').text
        # There can be an implicit initializer for enum value
        value.initializer = html.escape(enumvalue.findtext('initializer', ''))
        if ''.join(enumvalue.find('briefdescription').itertext()).strip():
            logging.warning("Ignoring brief description of enum value {}::{}".format(enum.name, value.name))
        value.description = parse_desc(state, enumvalue.find('detaileddescription'))
        if value.description: enum.has_value_details = True
        enum.values += [value]

    enum.has_details = enum.description or enum.has_value_details
    return enum if enum.brief or enum.has_details or enum.has_value_details else None

def parse_template_params(state: State, element: ET.Element, description):
    if element is None: return False, None
    assert element.tag == 'templateparamlist'

    has_template_details = False
    templates = []
    i: ET.Element
    for i in element:
        assert i.tag == 'param'

        template = Empty()
        template.type = parse_type(state, i.find('type'))
        declname = i.find('declname')
        if declname is not None:
            # declname or decltype?!
            template.name = declname.text
        else:
            # Doxygen sometimes puts both in type, extract that
            parts = template.type.partition(' ')
            template.type = parts[0]
            template.name = parts[2]
        default = i.find('defval')
        template.default = parse_type(state, default) if default is not None else ''
        if template.name in description:
            template.description = description[template.name]
            del description[template.name]
            has_template_details = True
        else:
            template.description = ''
        templates += [template]

    # Some param description got unused
    if description:
        logging.warning("Template parameter description doesn't match parameter names: {}".format(repr(description)))

    return has_template_details, templates

def parse_typedef(state: State, element: ET.Element):
    assert element.tag == 'memberdef' and element.attrib['kind'] == 'typedef'

    typedef = Empty()
    typedef.id = extract_id(element)
    typedef.is_using = element.findtext('definition', '').startswith('using')
    typedef.type = parse_type(state, element.find('type'))
    typedef.args = parse_type(state, element.find('argsstring'))
    typedef.name = element.find('name').text
    typedef.brief = parse_desc(state, element.find('briefdescription'))
    typedef.description, templates = parse_typedef_desc(state, element)
    typedef.is_protected = element.attrib['prot'] == 'protected'
    typedef.has_template_details, typedef.templates = parse_template_params(state, element.find('templateparamlist'), templates)

    typedef.has_details = typedef.description or typedef.has_template_details
    return typedef if typedef.brief or typedef.has_details else None

def parse_func(state: State, element: ET.Element):
    assert element.tag == 'memberdef' and element.attrib['kind'] == 'function'

    func = Empty()
    func.id = extract_id(element)
    func.type = parse_type(state, element.find('type'))
    func.name = fix_type_spacing(html.escape(element.find('name').text))
    func.brief = parse_desc(state, element.find('briefdescription'))
    func.description, templates, params, func.return_value = parse_func_desc(state, element)

    # Extract function signature to prefix, suffix and various flags. Important
    # things affecting caller such as static or const (and rvalue overloads)
    # are put into signature prefix/suffix, other things to various is_*
    # properties.
    if func.type == 'constexpr': # Constructors
        func.type = ''
        func.is_constexpr = True
    elif func.type.startswith('constexpr'):
        func.type = func.type[10:]
        func.is_constexpr = True
    else:
        func.is_constexpr = False
    func.prefix = ''
    func.is_explicit = element.attrib['explicit'] == 'yes'
    func.is_virtual = element.attrib['virt'] != 'non-virtual'
    if element.attrib['static'] == 'yes':
        func.prefix += 'static '
    signature = element.find('argsstring').text
    if signature.endswith(' noexcept'):
        signature = signature[:-9]
        func.is_noexcept = True
    else:
        func.is_noexcept = False
    if signature.endswith('=default'):
        signature = signature[:-8]
        func.is_defaulted = True
    else:
        func.is_defaulted = False
    if signature.endswith('=delete'):
        signature = signature[:-7]
        func.is_deleted = True
    else:
        func.is_deleted = False
    if signature.endswith('=0'):
        signature = signature[:-2]
        func.is_pure_virtual = True
    else:
        func.is_pure_virtual = False
    func.suffix = html.escape(signature[signature.rindex(')') + 1:].strip())
    if func.suffix: func.suffix = ' ' + func.suffix
    func.is_protected = element.attrib['prot'] == 'protected'
    func.is_private = element.attrib['prot'] == 'private'

    func.has_template_details, func.templates = parse_template_params(state, element.find('templateparamlist'), templates)

    func.has_param_details = False
    func.params = []
    for p in element.findall('param'):
        name = p.find('declname')
        param = Empty()
        param.name = name.text if name is not None else ''
        param.type = parse_type(state, p.find('type'))

        # Recombine parameter name and array information back
        array = p.find('array')
        if array is not None:
            if name is not None:
                assert param.type.endswith(')')
                param.type = param.type[:-1] + name.text + ')' + array.text
            else:
                param.type += array.text
        elif name is not None:
            param.type += ' ' + name.text

        param.default = parse_type(state, p.find('defval'))
        if param.name in params:
            param.description, param.direction = params[param.name]
            del params[param.name]
            func.has_param_details = True
        else:
            param.description, param.direction = '', ''
        func.params += [param]

    # Some param description got unused
    if params: logging.warning("Function parameter description doesn't match parameter names: {}".format(repr(params)))

    func.has_details = func.description or func.has_template_details or func.has_param_details or func.return_value
    return func if func.brief or func.has_details else None

def parse_var(state: State, element: ET.Element):
    assert element.tag == 'memberdef' and element.attrib['kind'] == 'variable'

    var = Empty()
    var.id = extract_id(element)
    var.type = parse_type(state, element.find('type'))
    if var.type.startswith('constexpr'):
        var.type = var.type[10:]
        var.is_constexpr = True
    else:
        var.is_constexpr = False
    var.is_static = element.attrib['static'] == 'yes'
    var.is_protected = element.attrib['prot'] == 'protected'
    var.is_private = element.attrib['prot'] == 'private'
    var.name = element.find('name').text
    var.brief = parse_desc(state, element.find('briefdescription'))
    var.description = parse_var_desc(state, element)

    var.has_details = not not var.description
    return var if var.brief or var.has_details else None

def parse_define(state: State, element: ET.Element):
    assert element.tag == 'memberdef' and element.attrib['kind'] == 'define'

    define = Empty()
    define.id = extract_id(element)
    define.name = element.find('name').text
    define.brief = parse_desc(state, element.find('briefdescription'))
    define.description, params, define.return_value = parse_define_desc(state, element)

    define.has_param_details = False
    define.params = None
    for p in element.findall('param'):
        if define.params is None: define.params = []
        name = p.find('defname')
        if name is not None:
            if name.text in params:
                description, _ = params[name.text]
                del params[name.text]
                define.has_param_details = True
            else:
                description = ''
            define.params += [(name.text, description)]

    # Some param description got unused
    if params: logging.warning("Define parameter description doesn't match parameter names: {}".format(repr(params)))

    define.has_details = define.description or define.return_value
    return define if define.brief or define.has_details else None

def extract_metadata(state: State, xml):
    # index.xml will be parsed later in parse_index_xml()
    if os.path.basename(xml) == 'index.xml': return

    logging.debug("Extracting metadata from {}".format(os.path.basename(xml)))

    tree = ET.parse(xml)
    root = tree.getroot()

    compounddef: ET.Element = root.find('compounddef')
    if compounddef.attrib['kind'] not in ['namespace', 'class', 'struct', 'union', 'dir', 'file', 'page']:
        logging.debug("No useful info in {}, skipping".format(os.path.basename(xml)))
        return

    compound = Empty()
    compound.id  = compounddef.attrib['id']
    compound.kind = compounddef.attrib['kind']
    # Compound name is page filename, so we have to use title there
    compound.name = html.escape(compounddef.find('title').text if compound.kind == 'page' else compounddef.find('compoundname').text)
    compound.url = compound.id + '.html'
    compound.brief = parse_desc(state, compounddef.find('briefdescription'))
    compound.has_details = compound.brief or compounddef.find('detaileddescription')
    compound.children = []
    compound.parent = None # is filled in by build_tree()

    if compound.kind in ['class', 'struct', 'union']:
        # Fix type spacing
        compound.name = fix_type_spacing(compound.name)

        # Parse template list for classes
        _, compound.templates = parse_template_params(state, compounddef.find('templateparamlist'), {})

    # Files have <innerclass> and <innernamespace> but that's not what we want,
    # so separate the children queries based on compound type
    if compounddef.attrib['kind'] in ['namespace', 'class', 'struct', 'union']:
        for i in compounddef.findall('innerclass'):
            compound.children += [i.attrib['refid']]
        for i in compounddef.findall('innernamespace'):
            compound.children += [i.attrib['refid']]
    elif compounddef.attrib['kind'] in ['dir', 'file']:
        for i in compounddef.findall('innerdir'):
            compound.children += [i.attrib['refid']]
        for i in compounddef.findall('innerfile'):
            compound.children += [i.attrib['refid']]
    elif compounddef.attrib['kind'] == 'page':
        for i in compounddef.findall('innerpage'):
            compound.children += [i.attrib['refid']]

    state.compounds[compound.id] = compound

def build_tree(state: State):
    for _, compound in state.compounds.items():
        for child in compound.children:
            if child in state.compounds:
                state.compounds[child].parent = compound.id

    # Strip name of parent symbols from names to get leaf names
    for _, compound in state.compounds.items():
        if not compound.parent or compound.kind in ['file', 'page']:
            compound.leaf_name = compound.name
            continue

        # Strip parent namespace/class from symbol name
        if compound.kind in ['namespace', 'struct', 'class', 'union']:
            prefix = state.compounds[compound.parent].name + '::'
            assert compound.name.startswith(prefix)
            compound.leaf_name = compound.name[len(prefix):]

        # Strip parent dir from dir name
        elif compound.kind == 'dir':
            prefix = state.compounds[compound.parent].name + '/'
            assert compound.name.startswith(prefix)
            compound.leaf_name = compound.name[len(prefix):]

        # Other compounds are not in any index pages or breadcrumb, so leaf
        # name not needed

def parse_xml(state: State, xml: str):
    # Reset counter for unique math formulas
    m.math.counter = 0

    logging.info("Parsing {}".format(os.path.basename(xml)))

    tree = ET.parse(xml)
    root = tree.getroot()
    assert root.tag == 'doxygen'

    compounddef: ET.Element = root[0]
    assert compounddef.tag == 'compounddef'
    assert len([i for i in root]) == 1

    # Ignoring private structs/classes, unnamed namespaces, files and
    # directories that have absolute location (i.e., outside of the
    # main source tree)
    if ((compounddef.attrib['kind'] in ['struct', 'class', 'union'] and compounddef.attrib['prot'] == 'private') or
        (compounddef.attrib['kind'] == 'namespace' and '@' in compounddef.find('compoundname').text) or
        (compounddef.attrib['kind'] in ['dir', 'file'] and os.path.isabs(compounddef.find('location').attrib['file']))):
        logging.debug("only private things in {}, skipping".format(os.path.basename(xml)))
        return None

    compound = Empty()
    compound.kind = compounddef.attrib['kind']
    compound.id = compounddef.attrib['id']
    # Compound name is page filename, so we have to use title there
    compound.name = compounddef.find('title').text if compound.kind == 'page' else compounddef.find('compoundname').text
    compound.has_template_details = False
    compound.templates = None
    compound.brief = parse_desc(state, compounddef.find('briefdescription'))
    compound.description, templates, compound.sections = parse_toplevel_desc(state, compounddef.find('detaileddescription'))
    compound.dirs = []
    compound.files = []
    compound.namespaces = []
    compound.classes = []
    compound.enums = []
    compound.typedefs = []
    compound.funcs = []
    compound.vars = []
    compound.defines = []
    compound.public_types = []
    compound.public_static_funcs = []
    compound.typeless_funcs = []
    compound.public_funcs = []
    compound.public_static_vars = []
    compound.public_vars = []
    compound.protected_types = []
    compound.protected_static_funcs = []
    compound.protected_funcs = []
    compound.protected_static_vars = []
    compound.protected_vars = []
    compound.private_funcs = []
    compound.related = []
    compound.groups = []
    compound.has_enum_details = False
    compound.has_typedef_details = False
    compound.has_func_details = False
    compound.has_var_details = False
    compound.has_define_details = False

    # Build breadcrumb
    if compound.kind in ['namespace', 'struct', 'class', 'union', 'file', 'dir', 'page']:
        # Gather parent compounds
        path_reverse = [compound.id]
        while path_reverse[-1] in state.compounds and state.compounds[path_reverse[-1]].parent:
            path_reverse += [state.compounds[path_reverse[-1]].parent]

        # Fill breadcrumb with leaf names and URLs
        compound.breadcrumb = []
        for i in reversed(path_reverse):
            compound.breadcrumb += [(state.compounds[i].leaf_name, state.compounds[i].url)]

    if compound.kind == 'page':
        # Drop TOC for pages, if not requested
        if compounddef.find('tableofcontents') is None:
            compound.sections = []

        if compound.brief:
            # Remove duplicated brief in pages. Doxygen sometimes adds a period
            # at the end, try without it also.
            # TODO: create follow-up to https://github.com/doxygen/doxygen/pull/624
            wrapped_brief = '<p>{}</p>'.format(compound.brief)
            if compound.description.startswith(wrapped_brief):
                compound.description = compound.description[len(wrapped_brief):]
            elif compound.brief[-1] == '.':
                wrapped_brief = '<p>{}</p>'.format(compound.brief[:-1])
                if compound.description.startswith(wrapped_brief):
                    compound.description = compound.description[len(wrapped_brief):]

    compounddef_child: ET.Element
    for compounddef_child in compounddef:
        # Directory / file
        if compounddef_child.tag in ['innerdir', 'innerfile']:
            id = compounddef_child.attrib['refid']

            # Add it only if we have documentation for it
            if id in state.compounds and state.compounds[id].has_details:
                file = state.compounds[id]

                f = Empty()
                f.url = file.url
                f.name = file.leaf_name
                f.brief = file.brief

                if compounddef_child.tag == 'innerdir':
                    compound.dirs += [f]
                else:
                    assert compounddef_child.tag == 'innerfile'
                    compound.files += [f]

        # Namespace / class
        elif compounddef_child.tag in ['innernamespace', 'innerclass']:
            id = compounddef_child.attrib['refid']

            # Add it only if it's not private and we have documentation for it
            if (compounddef_child.tag != 'innerclass' or not compounddef_child.attrib['prot'] == 'private') and id in state.compounds and state.compounds[id].has_details:
                symbol = state.compounds[id]

                if compounddef_child.tag == 'innernamespace':
                    namespace = Empty()
                    namespace.url = symbol.url
                    namespace.name = symbol.leaf_name if compound.kind == 'namespace' else symbol.name
                    namespace.brief = symbol.brief
                    compound.namespaces += [namespace]

                else:
                    assert compounddef_child.tag == 'innerclass'

                    class_ = Empty()
                    class_.kind = symbol.kind
                    class_.url = symbol.url
                    class_.name = symbol.leaf_name if compound.kind in ['namespace', 'class', 'struct', 'union'] else symbol.name
                    class_.brief = symbol.brief
                    class_.templates = symbol.templates

                    # Put classes into the public/protected section for
                    # inner classes
                    if compound.kind in ['class', 'struct', 'union']:
                        if compounddef_child.attrib['prot'] == 'public':
                            compound.public_types += [('class', class_)]
                        else:
                            assert compounddef_child.attrib['prot'] == 'protected'
                            compound.protected_types += [('class', class_)]
                    else:
                        assert compound.kind in ['namespace', 'file']
                        compound.classes += [class_]

        # Other, grouped in sections
        elif compounddef_child.tag == 'sectiondef':
            if compounddef_child.attrib['kind'] == 'enum':
                for memberdef in compounddef_child:
                    enum = parse_enum(state, memberdef)
                    if enum:
                        compound.enums += [enum]
                        if enum.has_details: compound.has_enum_details = True

            elif compounddef_child.attrib['kind'] == 'typedef':
                for memberdef in compounddef_child:
                    typedef = parse_typedef(state, memberdef)
                    if typedef:
                        compound.typedefs += [typedef]
                        if typedef.has_details: compound.has_typedef_details = True

            elif compounddef_child.attrib['kind'] == 'func':
                for memberdef in compounddef_child:
                    func = parse_func(state, memberdef)
                    if func:
                        compound.funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'var':
                for memberdef in compounddef_child:
                    var = parse_var(state, memberdef)
                    if var:
                        compound.vars += [var]
                        if var.has_details: compound.has_var_details = True

            elif compounddef_child.attrib['kind'] == 'define':
                for memberdef in compounddef_child:
                    define = parse_define(state, memberdef)
                    if define:
                        compound.defines += [define]
                        if define.has_details: compound.has_define_details = True

            elif compounddef_child.attrib['kind'] == 'public-type':
                for memberdef in compounddef_child:
                    if memberdef.attrib['kind'] == 'enum':
                        member = parse_enum(state, memberdef)
                        if member and member.has_details: compound.has_enum_details = True
                    else:
                        assert memberdef.attrib['kind'] == 'typedef'
                        member = parse_typedef(state, memberdef)
                        if member and member.has_details: compound.has_typedef_details = True

                    if member: compound.public_types += [(memberdef.attrib['kind'], member)]

            elif compounddef_child.attrib['kind'] == 'public-static-func':
                for memberdef in compounddef_child:
                    func = parse_func(state, memberdef)
                    if func:
                        compound.public_static_funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'public-func':
                for memberdef in compounddef_child:
                    func = parse_func(state, memberdef)
                    if func:
                        if func.type:
                            compound.public_funcs += [func]
                        else:
                            compound.typeless_funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'public-static-attrib':
                for memberdef in compounddef_child:
                    var = parse_var(state, memberdef)
                    if var:
                        compound.public_static_vars += [var]
                        if var.has_details: compound.has_var_details = True

            elif compounddef_child.attrib['kind'] == 'public-attrib':
                for memberdef in compounddef_child:
                    var = parse_var(state, memberdef)
                    if var:
                        compound.public_vars += [var]
                        if var.has_details: compound.has_var_details = True

            elif compounddef_child.attrib['kind'] == 'protected-type':
                for memberdef in compounddef_child:
                    if memberdef.attrib['kind'] == 'enum':
                        member = parse_enum(state, memberdef)
                        if member and member.has_details: compound.has_enum_details = True
                    else:
                        assert memberdef.attrib['kind'] == 'typedef'
                        member = parse_typedef(state, memberdef)
                        if member and member.has_details: compound.has_typedef_details = True

                    if member: compound.protected_types += [(memberdef.attrib['kind'], member)]

            elif compounddef_child.attrib['kind'] == 'protected-static-func':
                for memberdef in compounddef_child:
                    func = parse_func(state, memberdef)
                    if func:
                        compound.protected_static_funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'protected-func':
                for memberdef in compounddef_child:
                    func = parse_func(state, memberdef)
                    if func:
                        if func.type:
                            compound.protected_funcs += [func]
                        else:
                            compound.typeless_funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'protected-static-attrib':
                for memberdef in compounddef_child:
                    var = parse_var(state, memberdef)
                    if var:
                        compound.protected_static_vars += [var]
                        if var.has_details: compound.has_var_details = True

            elif compounddef_child.attrib['kind'] == 'protected-attrib':
                for memberdef in compounddef_child:
                    var = parse_var(state, memberdef)
                    if var:
                        compound.protected_vars += [var]
                        if var.has_details: compound.has_var_details = True

            elif compounddef_child.attrib['kind'] == 'private-func':
                # Gather only private functions that are virtual and
                # documented
                for memberdef in compounddef_child:
                    if memberdef.attrib['virt'] == 'non-virtual' or (not memberdef.find('briefdescription').text and not memberdef.find('detaileddescription').text):
                        assert True # only because coverage.py can't handle continue :/
                        continue # pragma: no cover

                    func = parse_func(state, memberdef)
                    if func:
                        compound.private_funcs += [func]
                        if func.has_details: compound.has_func_details = True

            elif compounddef_child.attrib['kind'] == 'related':
                for memberdef in compounddef_child:
                    if memberdef.attrib['kind'] == 'enum':
                        enum = parse_enum(state, memberdef)
                        if enum:
                            compound.related += [('enum', enum)]
                            if enum.has_details: compound.has_enum_details = True
                    elif memberdef.attrib['kind'] == 'typedef':
                        typedef = parse_typedef(state, memberdef)
                        if typedef:
                            compound.related += [('typedef', typedef)]
                            if typedef.has_details: compound.has_typedef_details = True
                    elif memberdef.attrib['kind'] == 'function':
                        func = parse_func(state, memberdef)
                        if func:
                            compound.related += [('func', func)]
                            if func.has_details: compound.has_func_details = True
                    elif memberdef.attrib['kind'] == 'variable':
                        var = parse_var(state, memberdef)
                        if var:
                            compound.related += [('var', var)]
                            if var.has_details: compound.has_var_details = True
                    elif memberdef.attrib['kind'] == 'define':
                        define = parse_define(state, memberdef)
                        if define:
                            compound.related += [('define', define)]
                            if define.has_details: compound.has_define_details = True
                    else: # pragma: no cover
                        logging.warning("unknown related <memberdef> kind {}".format(memberdef.attrib['kind']))

            elif compounddef_child.attrib['kind'] == 'user-defined':
                list = []

                memberdef: ET.Element
                for memberdef in compounddef_child.findall('memberdef'):
                    if memberdef.attrib['kind'] == 'enum':
                        enum = parse_enum(state, memberdef)
                        if enum:
                            list += [('enum', enum)]
                            if enum.has_details: compound.has_enum_details = True
                    elif memberdef.attrib['kind'] == 'typedef':
                        typedef = parse_typedef(state, memberdef)
                        if typedef:
                            list += [('typedef', typedef)]
                            if typedef.has_details: compound.has_typedef_details = True
                    elif memberdef.attrib['kind'] == 'function':
                        func = parse_func(state, memberdef)
                        if func:
                            list += [('func', func)]
                            if func.has_details: compound.has_func_details = True
                    elif memberdef.attrib['kind'] == 'variable':
                        var = parse_var(state, memberdef)
                        if var:
                            list += [('var', var)]
                            if var.has_details: compound.has_var_details = True
                    elif memberdef.attrib['kind'] == 'define':
                        define = parse_define(state, memberdef)
                        if define:
                            list += [('define', define)]
                            if define.has_details: compound.has_define_details = True
                    else: # pragma: no cover
                        logging.warning("unknown user-defined <memberdef> kind {}".format(memberdef.attrib['kind']))

                if list:
                    group = Empty()
                    group.name = compounddef_child.find('header').text
                    group.id = slugify(group.name)
                    group.description = parse_desc(state, compounddef_child.find('description'))
                    group.members = list
                    compound.groups += [group]

            elif compounddef_child.attrib['kind'] not in ['private-type',
                                                          'private-static-func',
                                                          'private-static-attrib',
                                                          'private-attrib',
                                                          'friend']: # pragma: no cover
                logging.warning("unknown <sectiondef> kind {}".format(compounddef_child.attrib['kind']))

        elif compounddef_child.tag == 'templateparamlist':
            compound.has_template_details, compound.templates = parse_template_params(state, compounddef_child, templates)

        elif (compounddef_child.tag not in ['compoundname',
                                            'briefdescription',
                                            'detaileddescription',
                                            'location',
                                            'includes',
                                            'includedby',
                                            'incdepgraph',
                                            'invincdepgraph',
                                            'inheritancegraph',
                                            'collaborationgraph',
                                            'listofallmembers',
                                            'tableofcontents'] and
            not (compounddef.attrib['kind'] == 'page' and compounddef_child.tag == 'title')): # pragma: no cover
            logging.warning("Ignoring <{}> in <compounddef>".format(compounddef_child.tag))

    # Decide about the prefix (it may contain template parameters, so we
    # had to wait until everything is parsed)
    if compound.kind in ['namespace', 'struct', 'class', 'union']:
        # The name itself can contain templates (e.g. a specialized template),
        # so properly escape and fix spacing there as well
        compound.prefix_wbr = add_wbr(fix_type_spacing(html.escape(compound.name)))

        if compound.templates:
            compound.prefix_wbr += '&lt;'
            for index, t in enumerate(compound.templates):
                if index != 0: compound.prefix_wbr += ', '
                if t.name:
                    compound.prefix_wbr += t.name
                else:
                    compound.prefix_wbr += '_{}'.format(index+1)
            compound.prefix_wbr += '&gt;'

        compound.prefix_wbr += '::<wbr/>'

    parsed = Empty()
    parsed.version = root.attrib['version']

    # Decide about save as filename. Pages mess this up, because index page has
    # "indexpage" as a name so we have to use the compound name instead
    parsed.save_as = (compounddef.find('compoundname').text if compound.kind == 'page' else compound.id) + '.html'

    parsed.compound = compound
    return parsed

def parse_index_xml(state: State, xml):
    logging.info("Parsing {}".format(os.path.basename(xml)))

    tree = ET.parse(xml)
    root = tree.getroot()
    assert root.tag == 'doxygenindex'

    # Top-level symbols, files and pages. Separated to nestable (namespaces,
    # dirs) and non-nestable so we have these listed first.
    top_level_namespaces = []
    top_level_classes = []
    top_level_dirs = []
    top_level_files = []
    top_level_pages = []

    # Non-top-level symbols, files and pages, assigned later
    orphans_nestable = {}
    orphan_pages = {}
    orphans = {}

    # Map of all entries
    entries = {}

    i: ET.Element
    for i in root:
        assert i.tag == 'compound'

        entry = Empty()
        entry.id = i.attrib['refid']

        # Ignore unknown / undocumented compounds
        if entry.id not in state.compounds or not state.compounds[entry.id].has_details:
            continue

        compound = state.compounds[entry.id]
        entry.kind = compound.kind
        entry.name = compound.leaf_name
        entry.url = compound.url
        entry.brief = compound.brief
        entry.children = []
        entry.has_nestable_children = False

        # If a top-level thing, put it directly into the list
        if not compound.parent:
            if compound.kind == 'namespace':
                top_level_namespaces += [entry]
            elif compound.kind in ['class', 'struct', 'union']:
                top_level_classes += [entry]
            elif compound.kind == 'dir':
                top_level_dirs += [entry]
            elif compound.kind == 'file':
                top_level_files += [entry]
            else:
                assert compound.kind == 'page'
                # Ignore index page in page listing
                if entry.id == 'indexpage': continue
                top_level_pages += [entry]

        # Otherwise put it into orphan map
        else:
            if compound.kind in ['namespace', 'dir']:
                if not compound.parent in orphans_nestable:
                    orphans_nestable[compound.parent] = []
                orphans_nestable[compound.parent] += [entry]
            elif compound.kind == 'page':
                if not compound.parent in orphan_pages:
                    orphan_pages[compound.parent] = {}
                orphan_pages[compound.parent][entry.id] = entry
            else:
                assert compound.kind in ['class', 'struct', 'union', 'file']
                if not compound.parent in orphans:
                    orphans[compound.parent] = []
                orphans[compound.parent] += [entry]

        # Put it also in the global map so we can reference it later when
        # getting rid of orphans
        entries[entry.id] = entry

    # Structure containing top-level symbols, files and pages, nestable items
    # (namespaces, directories) first
    parsed = Empty()
    parsed.version = root.attrib['version']
    parsed.index = Empty()
    parsed.index.symbols = top_level_namespaces + top_level_classes
    parsed.index.files = top_level_dirs + top_level_files
    parsed.index.pages = top_level_pages

    # Assign nestable children to their parents first, if the parents exist
    for parent, children in orphans_nestable.items():
        if not parent in entries: continue
        entries[parent].has_nestable_children = True
        entries[parent].children = children

    # Add child pages to their parent pages. The user-defined order matters, so
    # preserve it.
    for parent, children in orphan_pages.items():
        assert parent in entries
        compound = state.compounds[parent]
        for child in compound.children:
            entries[parent].children += [children[child]]

    # Add children to their parents, if the parents exist
    for parent, children in orphans.items():
        if parent in entries: entries[parent].children += children

    return parsed

def parse_doxyfile(state: State, doxyfile, config = None):
    logging.info("Parsing configuration from {}".format(doxyfile))

    comment_re = re.compile(r"""^\s*(#.*)?$""")
    variable_re = re.compile(r"""^\s*(?P<key>[A-Z0-9_@]+)\s*=\s*(?P<quote>"?)(?P<value>.*)(?P=quote)\s*(?P<backslash>\\?)$""")
    variable_continuation_re = re.compile(r"""^\s*(?P<key>[A-Z_]+)\s*\+=\s*(?P<quote>"?)(?P<value>.*)(?P=quote)\s*(?P<backslash>\\?)$""")
    continuation_re = re.compile(r"""^\s*(?P<quote>['"]?)(?P<value>.*)(?P=quote)\s*(?P<backslash>\\?)$""")

    # Defaults so we don't fail with minimal Doxyfiles and also that the
    # user-provided Doxygen can append to them. They are later converted to
    # string or kept as a list based on type, so all have to be a list of
    # strings now.
    if not config: config = {
        'PROJECT_NAME': ['My Project'],
        'OUTPUT_DIRECTORY': [''],
        'XML_OUTPUT': ['xml'],
        'HTML_OUTPUT': ['html'],
        'IMAGE_PATH': [],
        'HTML_EXTRA_STYLESHEET': [
            'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
            '../css/m-dark+doxygen.compiled.css'],
        'HTML_EXTRA_FILES': [],

        'M_CLASS_TREE_EXPAND_LEVELS': ['1'],
        'M_FILE_TREE_EXPAND_LEVELS': ['1'],
        'M_EXPAND_INNER_TYPES': ['0'],
        'M_THEME_COLOR': ['#22272e']
    }

    def parse_value(var):
        if var.group('quote') == '"':
            out = [var.group('value')]
        else:
            out = var.group('value').split()

        if var.group('quote') and var.group('backslash') == '\\':
            backslash = True
        elif out and out[-1].endswith('\\'):
            backslash = True
            out[-1] = out[-1][:-1].rstrip()
        else:
            backslash = False

        return [i.replace('\\"', '"') for i in out], backslash

    with open(doxyfile) as f:
        continued_line = None
        for line in f:
            line = line.strip()

            # Ignore comments and empty lines. Comment also stops line
            # continuation
            if comment_re.match(line):
                continued_line = None
                continue

            # Line continuation from before, append the line contents to it
            if continued_line:
                var = continuation_re.match(line)
                value, backslash = parse_value(var)
                config[continued_line] += value
                if not backslash: continued_line = None
                continue

            # Variable
            var = variable_re.match(line)
            if var:
                key = var.group('key')
                value, backslash = parse_value(var)

                # Another file included, parse it
                if key == '@INCLUDE':
                    parse_doxyfile(state, os.path.join(os.path.dirname(doxyfile), ' '.join(value)), config)
                    assert not backslash
                else:
                    config[key] = value

                if backslash: continued_line = key
                continue

            # Variable, adding to existing
            var = variable_continuation_re.match(line)
            if var:
                key = var.group('key')
                if not key in config: config[key] = []
                value, backslash = parse_value(var)
                config[key] += value
                if backslash: continued_line = key

                # only because coverage.py can't handle continue
                continue # pragma: no cover

            logging.warning("Umatchable line in Doxyfile: {}".format(line)) # pragma: no cover

    # String values that we want
    for i in ['PROJECT_NAME',
              'PROJECT_BRIEF',
              'OUTPUT_DIRECTORY',
              'HTML_OUTPUT',
              'XML_OUTPUT',
              'M_PAGE_HEADER',
              'M_THEME_COLOR']:
        if i in config: state.doxyfile[i] = ' '.join(config[i])

    # Int values that we want
    for i in ['M_CLASS_TREE_EXPAND_LEVELS',
              'M_FILE_TREE_EXPAND_LEVELS',
              'M_EXPAND_INNER_TYPES']:
        if i in config: state.doxyfile[i] = int(' '.join(config[i]))

    # List values that we want. Drop empty lines.
    for i in ['TAGFILES',
              'IMAGE_PATH',
              'HTML_EXTRA_STYLESHEET',
              'HTML_EXTRA_FILES']:
        if i in config:
            state.doxyfile[i] = [line for line in config[i] if line]

default_index_pages = ['pages', 'files', 'namespaces', 'annotated']
default_wildcard = '*.xml'
default_templates = 'templates/'

def run(doxyfile, templates=default_templates, wildcard=default_wildcard, index_pages=default_index_pages):
    state = State()
    state.basedir = os.path.dirname(doxyfile)

    parse_doxyfile(state, doxyfile)
    xml_input = os.path.join(state.basedir, state.doxyfile['OUTPUT_DIRECTORY'], state.doxyfile['XML_OUTPUT'])
    xml_files_metadata = [os.path.join(xml_input, f) for f in glob.glob(os.path.join(xml_input, "*.xml"))]
    xml_files = [os.path.join(xml_input, f) for f in glob.glob(os.path.join(xml_input, wildcard))]
    html_output = os.path.join(state.basedir, state.doxyfile['OUTPUT_DIRECTORY'], state.doxyfile['HTML_OUTPUT'])

    if not os.path.exists(html_output):
        os.makedirs(html_output)

    env = Environment(loader=FileSystemLoader(templates),
                      trim_blocks=True, lstrip_blocks=True, enable_async=True)

    # Filter to return file basename or the full URL, if absolute
    def basename_or_url(path):
        if urllib.parse.urlparse(path).netloc: return path
        return os.path.basename(path)
    env.filters['basename_or_url'] = basename_or_url

    # Do a pre-pass and gather:
    # - brief descriptions of all classes, namespaces, dirs and files because
    #   the brief desc is not part of the <inner*> tag
    # - template specifications of all classes so we can include that in the
    #   linking pages
    # - get URLs of namespace, classe, file docs and pages so we can link to
    #   them from breadcrumb navigation
    logging.info("Parsing metadata from {} files".format(len(xml_files_metadata)))
    file: str
    for file in xml_files_metadata:
        extract_metadata(state, file)

    build_tree(state)

    for file in xml_files:
        if os.path.basename(file) == 'index.xml':
            parsed = parse_index_xml(state, file)

            for i in index_pages:
                file = '{}.html'.format(i)

                template = env.get_template(file)
                rendered = template.render(index=parsed.index,
                    DOXYGEN_VERSION=parsed.version,
                    FILENAME=file,
                    **state.doxyfile)

                output = os.path.join(html_output, file)
                with open(output, 'w') as f:
                    f.write(rendered)
        else:
            parsed = parse_xml(state, file)
            if not parsed: continue

            template = env.get_template('{}.html'.format(parsed.compound.kind))
            rendered = template.render(compound=parsed.compound,
                DOXYGEN_VERSION=parsed.version,
                FILENAME=parsed.save_as,
                **state.doxyfile)

            output = os.path.join(html_output, parsed.save_as)
            with open(output, 'w') as f:
                f.write(rendered)

    # Copy all referenced files, skip absolute URLs
    for i in state.images + state.doxyfile['HTML_EXTRA_STYLESHEET'] + state.doxyfile['HTML_EXTRA_FILES']:
        if urllib.parse.urlparse(i).netloc: continue
        logging.info("copying {} to output".format(i))
        shutil.copy(i, os.path.join(html_output, os.path.basename(i)))

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('doxyfile', help="where the Doxyfile is")
    parser.add_argument('--templates', help="template directory", default=default_templates)
    parser.add_argument('--wildcard', help="only process files matching the wildcard", default=default_wildcard)
    parser.add_argument('--index-pages', nargs='+', help="index page templates", default=default_index_pages)
    parser.add_argument('--no-doxygen', help="don't run Doxygen before", action='store_true')
    parser.add_argument('--debug', help="verbose debug output", action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not args.no_doxygen:
        subprocess.run(["doxygen", args.doxyfile], cwd=os.path.dirname(args.doxyfile))

    run(args.doxyfile, args.templates, args.wildcard, args.index_pages)
