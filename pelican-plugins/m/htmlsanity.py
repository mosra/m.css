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

import os.path
import re

import six
from six.moves.urllib.parse import urlparse, urlunparse, urljoin

from docutils.writers.html5_polyglot import HTMLTranslator
from docutils.transforms import Transform
import docutils
from docutils import nodes, utils
from docutils.utils import smartquotes

import pelican.signals
from pelican.readers import RstReader
from pelican.contents import Content, Author, Category, Tag, Static

import logging

logger = logging.getLogger(__name__)

try:
    import pyphen
except ImportError:
    pyphen = None

settings = {}
words_re = re.compile("""\w+""", re.UNICODE|re.X)

class SmartQuotes(docutils.transforms.universal.SmartQuotes):
    """Smart quote transform

    Copy-paste of docutils builtin smart_quotes feature, patched to *not*
    replace quotes etc. in inline code blocks.  Original source from
    https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/transforms/universal.py#L207

    Contrary to the builtin, this is controlled via HTMLSANITY_SMART_QUOTES
    instead of smart_quotes in DOCUTILS_SETTINGS, so the original smart quotes
    implementation is not executed.
    """

    def apply(self):
        # We are using our own config variable instead of
        # self.document.settings.smart_quotes in order to avoid the builtin
        # SmartQuotes to be executed as well
        if not settings['M_HTMLSANITY_SMART_QUOTES']:
            return
        try:
            alternative = settings['M_HTMLSANITY_SMART_QUOTES'].startswith('alt')
        except AttributeError:
            alternative = False
        # print repr(alternative)

        document_language = self.document.settings.language_code

        # "Educate" quotes in normal text. Handle each block of text
        # (TextElement node) as a unit to keep context around inline nodes:
        for node in self.document.traverse(nodes.TextElement):
            # skip preformatted text blocks and special elements:
            if isinstance(node, (nodes.FixedTextElement, nodes.Special)):
                continue
            # nested TextElements are not "block-level" elements:
            if isinstance(node.parent, nodes.TextElement):
                continue

            # list of text nodes in the "text block":
            # Patched here to exclude text spans inside literal nodes.
            # Hopefully two nesting levels are enough.
            txtnodes = [txtnode for txtnode in node.traverse(nodes.Text)
                        if not isinstance(txtnode.parent,
                                          nodes.option_string) and
                           not isinstance(txtnode.parent,
                                          nodes.literal) and
                           not isinstance(txtnode.parent.parent,
                                          nodes.literal)]

            # language: use typographical quotes for language "lang"
            lang = node.get_language_code(document_language)
            # use alternative form if `smart-quotes` setting starts with "alt":
            if alternative:
                if '-x-altquot' in lang:
                    lang = lang.replace('-x-altquot', '')
                else:
                    lang += '-x-altquot'
            # drop subtags missing in quotes:
            for tag in utils.normalize_language_tag(lang):
                if tag in smartquotes.smartchars.quotes:
                    lang = tag
                    break
            else: # language not supported: (keep ASCII quotes)
                lang = ''

            # Iterator educating quotes in plain text:
            # '2': set all, using old school en- and em- dash shortcuts
            teacher = smartquotes.educate_tokens(self.get_tokens(txtnodes),
                                                 attr='2', language=lang)

            for txtnode, newtext in zip(txtnodes, teacher):
                txtnode.parent.replace(txtnode, nodes.Text(newtext))

            self.unsupported_languages = set() # reset

class Pyphen(Transform):
    """Hyphenation using pyphen

    Enabled or disabled using HTMLSANITY_HYPHENATION boolean option, defaulting
    to ``False``.
    """

    # Max Docutils priority is 990, be sure that this is applied at the very
    # last
    default_priority = 991

    def __init__(self, document, startnode):
        Transform.__init__(self, document, startnode=startnode)

    def apply(self):
        if not settings['M_HTMLSANITY_HYPHENATION']:
            return

        document_language = self.document.settings.language_code

        pyphen_for_lang = {}

        # Go through all text words and hyphenate them
        for node in self.document.traverse(nodes.TextElement):
            # Skip preformatted text blocks, special elements and field names
            if isinstance(node, (nodes.FixedTextElement, nodes.Special, nodes.field_name)):
                continue

            for txtnode in node.traverse(nodes.Text):
                # Exclude:
                #  - document title
                #  - literals and spans inside literals
                #  - raw code (such as SVG)
                if isinstance(txtnode.parent, nodes.title) or \
                   isinstance(txtnode.parent, nodes.literal) or \
                   isinstance(txtnode.parent.parent, nodes.literal) or \
                   isinstance(txtnode.parent, nodes.raw):
                    continue

                # From fields include only the summary
                if isinstance(txtnode.parent.parent, nodes.field_body):
                    field_name_index = txtnode.parent.parent.parent.first_child_matching_class(nodes.field_name)
                    if txtnode.parent.parent.parent[field_name_index][0] != 'summary':
                        continue

                # Useful for debugging, don't remove ;)
                #print(repr(txtnode.parent), repr(txtnode.parent.parent), repr(txtnode.parent.parent.parent))

                # Proper language-dependent hyphenation. Can't be done for
                # `node` as a paragraph can consist of more than one language.
                lang = txtnode.parent.get_language_code(document_language)

                # Create new Pyphen object for given lang, if not yet cached.
                # I'm assuming this is faster than recreating the instance for
                # every text node
                if lang not in pyphen_for_lang:
                    if lang not in pyphen.LANGUAGES: continue
                    pyphen_for_lang[lang] = pyphen.Pyphen(lang=lang)

                txtnode.parent.replace(txtnode, nodes.Text(words_re.sub(lambda m: pyphen_for_lang[lang].inserted(m.group(0), '\u00AD'), txtnode.astext())))

class SaneHtmlTranslator(HTMLTranslator):
    """Sane HTML translator

    Patched version of docutils builtin HTML5 translator, improving the output
    further.
    """

    # Overrides the ones from docutils HTML5 writer to enable the soft hyphen
    # character
    special_characters = {ord('&'): '&amp;',
                          ord('<'): '&lt;',
                          ord('"'): '&quot;',
                          ord('>'): '&gt;',
                          ord('@'): '&#64;', # may thwart address harvesters
                          ord('\u00AD'): '&shy;'}

    def __init__(self, document):
        HTMLTranslator.__init__(self, document)

        # There's a minor difference between docutils 0.13 and 0.14 that breaks
        # stuff. Monkey-patch it here.
        if not hasattr(self, 'in_word_wrap_point'):
            self.in_word_wrap_point = HTMLTranslator.sollbruchstelle

    # Somehow this does the trick and removes docinfo from the body. Was
    # present in the HTML4 translator but not in the HTML5 one, so copying it
    # verbatim over
    def visit_docinfo(self, node):
        self.context.append(len(self.body))
        self.body.append(self.starttag(node, 'table',
                                       CLASS='docinfo',
                                       frame="void", rules="none"))
        self.body.append('<col class="docinfo-name" />\n'
                         '<col class="docinfo-content" />\n'
                         '<tbody valign="top">\n')
        self.in_docinfo = True

    def depart_docinfo(self, node):
        self.body.append('</tbody>\n</table>\n')
        self.in_docinfo = False
        start = self.context.pop()
        self.docinfo = self.body[start:]
        self.body = []

    # Have <abbr> properly with title
    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr('title'):
            attrs['title'] = node['title']
        self.body.append(self.starttag(node, 'abbr', '', **attrs))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

    # Remove useless cruft from images, such as width, height, scale; don't put
    # URI in alt text.
    def visit_image(self, node):
        atts = {}
        uri = node['uri']
        ext = os.path.splitext(uri)[1].lower()
        if ext in self.object_image_types:
            atts['data'] = uri
            atts['type'] = self.object_image_types[ext]
        else:
            atts['src'] = uri
            if 'alt' in node: atts['alt'] = node['alt']
        if (isinstance(node.parent, nodes.TextElement) or
            (isinstance(node.parent, nodes.reference) and
             not isinstance(node.parent.parent, nodes.TextElement))):
            # Inline context or surrounded by <a>...</a>.
            suffix = ''
        else:
            suffix = '\n'
        if ext in self.object_image_types:
            # do NOT use an empty tag: incorrect rendering in browsers
            self.body.append(self.starttag(node, 'object', suffix, **atts) +
                             node.get('alt', uri) + '</object>' + suffix)
        else:
            self.body.append(self.emptytag(node, 'img', suffix, **atts))

    def depart_image(self, node):
        pass

    # Use HTML5 <section> tag for sections (instead of <div class="section">)
    def visit_section(self, node):
        self.section_level += 1
        self.body.append(
            self.starttag(node, 'section'))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</section>\n')

    # Legend inside figure -- print as <span> (instead of <div class="legend">,
    # as that's not valid inside HTML5 <figure> element)
    def visit_legend(self, node):
        self.body.append(self.starttag(node, 'span'))

    def depart_legend(self, node):
        self.body.append('</span>\n')

    # Literal -- print as <code> (instead of some <span>)
    def visit_literal(self, node):
        self.body.append(self.starttag(node, 'code', ''))

    def depart_literal(self, node):
        self.body.append('</code>')

    # Literal block -- use <pre> without nested <code> and useless classes
    def visit_literal_block(self, node):
        self.body.append(self.starttag(node, 'pre', ''))

    def depart_literal_block(self, node):
        self.body.append('</pre>\n')

    # Anchor -- drop the useless classes
    def visit_reference(self, node):
        atts = {}
        if 'refuri' in node:
            atts['href'] = node['refuri']
            if ( self.settings.cloak_email_addresses
                 and atts['href'].startswith('mailto:')):
                atts['href'] = self.cloak_mailto(atts['href'])
                self.in_mailto = True
        else:
            assert 'refid' in node, \
                   'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
        # why?!?!
        #if not isinstance(node.parent, nodes.TextElement):
            #assert len(node) == 1 and isinstance(node[0], nodes.image)
        self.body.append(self.starttag(node, 'a', '', **atts))

    def depart_reference(self, node):
        self.body.append('</a>')
        if not isinstance(node.parent, nodes.TextElement):
            self.body.append('\n')
        self.in_mailto = False

    # Use <aside> instead of a meaningless <div>
    def visit_topic(self, node):
        self.body.append(self.starttag(node, 'aside'))
        self.topic_classes = node['classes']

    def depart_topic(self, node):
        self.body.append('</aside>\n')
        self.topic_classes = []

    # Don't use <colgroup> or other shit in tables
    def visit_colspec(self, node):
        self.colspecs.append(node)
        # "stubs" list is an attribute of the tgroup element:
        node.parent.stubs.append(node.attributes.get('stub'))

    def depart_colspec(self, node):
        # write out <colgroup> when all colspecs are processed
        if isinstance(node.next_node(descend=False, siblings=True),
                      nodes.colspec):
            return
        if 'colwidths-auto' in node.parent.parent['classes'] or (
            'colwidths-auto' in self.settings.table_style and
            ('colwidths-given' not in node.parent.parent['classes'])):
            return

    # Don't put comments into the HTML output
    def visit_comment(self, node,
                      sub=re.compile('-(?=-)').sub):
        raise nodes.SkipNode

    # Containers don't need those stupid "docutils" class names
    def visit_container(self, node):
        atts = {}
        self.body.append(self.starttag(node, 'div', **atts))

    def depart_container(self, node):
        self.body.append('</div>\n')

    # Use HTML5 <figure> element for figures
    def visit_figure(self, node):
        atts = {}
        if node.get('id'):
            atts['ids'] = [node['id']]
        if node.get('width'):
            atts['style'] = 'width: %s' % node['width']
        self.body.append(self.starttag(node, 'figure', **atts))

    def depart_figure(self, node):
        self.body.append('</figure>\n')

    def visit_caption(self, node):
        self.body.append(self.starttag(node, 'figcaption', ''))

    def depart_caption(self, node):
        self.body.append('</figcaption>\n')

    # Line blocks are <p> with lines separated using simple <br />. No need for
    # nested <div>s.
    def visit_line(self, node):
        pass

    def depart_line(self, node):
        self.body.append('<br />\n')

    def visit_line_block(self, node):
        self.body.append(self.starttag(node, 'p'))

    def depart_line_block(self, node):
        self.body.append('</p>\n')

    # Copied from the HTML4 translator, somehow not present in the HTML5 one.
    # Not having this generates *a lot* of <p> tags everywhere.
    def should_be_compact_paragraph(self, node):
        """
        Determine if the <p> tags around paragraph ``node`` can be omitted.
        """
        if (isinstance(node.parent, nodes.document) or
            isinstance(node.parent, nodes.compound) or
            isinstance(node.parent, nodes.field_body)):
            # Never compact paragraphs in document, compound or directly in
            # field bodies (such as article summary or page footer)
            return False
        for key, value in node.attlist():
            if (node.is_not_default(key) and
                not (key == 'classes' and value in
                     ([], ['first'], ['last'], ['first', 'last']))):
                # Attribute which needs to survive.
                return False
        first = isinstance(node.parent[0], nodes.label) # skip label
        for child in node.parent.children[first:]:
            # only first paragraph can be compact
            if isinstance(child, nodes.Invisible):
                continue
            if child is node:
                break
            return False
        parent_length = len([n for n in node.parent if not isinstance(
            n, (nodes.Invisible, nodes.label))])
        if ( self.compact_simple
             or self.compact_field_list
             or self.compact_p and parent_length == 1):
            return True
        return False

    def visit_paragraph(self, node):
        if self.should_be_compact_paragraph(node):
            self.context.append('')
        else:
            self.body.append(self.starttag(node, 'p', ''))
            self.context.append('</p>\n')

    def depart_paragraph(self, node):
        self.body.append(self.context.pop())

    # Titles in topics should be <h3>
    def visit_title(self, node):
        """Only 6 section levels are supported by HTML."""
        check_id = 0  # TODO: is this a bool (False) or a counter?
        close_tag = '</p>\n'
        if isinstance(node.parent, nodes.topic):
            self.body.append(
                  self.starttag(node, 'h3', ''))
            close_tag = '</h3>\n'
        elif isinstance(node.parent, nodes.sidebar):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='sidebar-title'))
        elif isinstance(node.parent, nodes.Admonition):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='admonition-title'))
        elif isinstance(node.parent, nodes.table):
            self.body.append(
                  self.starttag(node, 'caption', ''))
            close_tag = '</caption>\n'
        elif isinstance(node.parent, nodes.document):
            self.body.append(self.starttag(node, 'h1', '', CLASS='title'))
            close_tag = '</h1>\n'
            self.in_document_title = len(self.body)
        else:
            assert isinstance(node.parent, nodes.section)
            h_level = self.section_level + self.initial_header_level - 1
            atts = {}
            if (len(node.parent) >= 2 and
                isinstance(node.parent[1], nodes.subtitle)):
                atts['CLASS'] = 'with-subtitle'
            self.body.append(
                  self.starttag(node, 'h%s' % h_level, '', **atts))
            atts = {}
            if node.hasattr('refid'):
                atts['class'] = 'toc-backref'
                atts['href'] = '#' + node['refid']
            if atts:
                self.body.append(self.starttag({}, 'a', '', **atts))
                close_tag = '</a></h%s>\n' % (h_level)
            else:
                close_tag = '</h%s>\n' % (h_level)
        self.context.append(close_tag)

    def depart_title(self, node):
        self.body.append(self.context.pop())
        if self.in_document_title:
            self.title = self.body[self.in_document_title:-1]
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]

class _SaneFieldBodyTranslator(SaneHtmlTranslator):
    """
    Copy of _FieldBodyTranslator with the only difference being inherited from
    SaneHtmlTranslator instead of HTMLTranslator
    """

    def __init__(self, document):
        SaneHtmlTranslator.__init__(self, document)

    def astext(self):
        return ''.join(self.body)

    # Not sure why this is here
    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

class SaneHtmlWriter(docutils.writers.html5_polyglot.Writer):
    def __init__(self):
        docutils.writers.html5_polyglot.Writer.__init__(self)

        self.translator_class = SaneHtmlTranslator

    def get_transforms(self):
        return docutils.writers.html5_polyglot.Writer.get_transforms(self) + [SmartQuotes, Pyphen]

class SaneRstReader(RstReader):
    writer_class = SaneHtmlWriter
    field_body_translator_class = _SaneFieldBodyTranslator

# Implementation of SaneRstReader adapted from
# https://github.com/getpelican/pelican/blob/7336de45cbb5f60e934b65f823d0583b48a6c96b/pelican/readers.py#L206
# for compatibility with stock Pelican 3.7.1 that doesn't have writer_class or
# field_body_translator_class fields, so we override _parse_metadata and
# _get_publisher directly.
# TODO: remove when 3.8 with https://github.com/getpelican/pelican/pull/2163
# is released
class SaneRstReaderPelican371(RstReader):
    def _parse_metadata(self, document):
        """Return the dict containing document metadata"""
        formatted_fields = self.settings['FORMATTED_FIELDS']

        output = {}
        for docinfo in document.traverse(docutils.nodes.docinfo):
            for element in docinfo.children:
                if element.tagname == 'field':  # custom fields (e.g. summary)
                    name_elem, body_elem = element.children
                    name = name_elem.astext()
                    if name in formatted_fields:
                        visitor = _SaneFieldBodyTranslator(document)
                        body_elem.walkabout(visitor)
                        value = visitor.astext()
                    else:
                        value = body_elem.astext()
                elif element.tagname == 'authors':  # author list
                    name = element.tagname
                    value = [element.astext() for element in element.children]
                else:  # standard fields (e.g. address)
                    name = element.tagname
                    value = element.astext()
                name = name.lower()

                output[name] = self.process_metadata(name, value)
        return output

    def _get_publisher(self, source_path):
        extra_params = {'initial_header_level': '2',
                        'syntax_highlight': 'short',
                        'input_encoding': 'utf-8',
                        'exit_status_level': 2,
                        'embed_stylesheet': False}
        user_params = self.settings.get('DOCUTILS_SETTINGS')
        if user_params:
            extra_params.update(user_params)

        pub = docutils.core.Publisher(
            writer=SaneHtmlWriter(),
            source_class=self.FileInput,
            destination_class=docutils.io.StringOutput)
        pub.set_components('standalone', 'restructuredtext', 'html')
        pub.process_programmatic_settings(None, extra_params, None)
        pub.set_source(source_path=source_path)
        pub.publish(enable_exit_status=True)
        return pub

def render_rst(value):
    extra_params = {'initial_header_level': '2',
                    'syntax_highlight': 'short',
                    'input_encoding': 'utf-8',
                    'exit_status_level': 2,
                    'embed_stylesheet': False}
    if settings['DOCUTILS_SETTINGS']:
        extra_params.update(settings['DOCUTILS_SETTINGS'])

    pub = docutils.core.Publisher(
        writer=SaneHtmlWriter(),
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.writer.translator_class = _SaneFieldBodyTranslator
    pub.process_programmatic_settings(None, extra_params, None)
    pub.set_source(source=value)
    pub.publish(enable_exit_status=True)
    return pub.writer.parts.get('body').strip()

def hyphenate(value, enable=None, lang=None):
    if enable is None: enable = settings['M_HTMLSANITY_HYPHENATION']
    if lang is None: lang = settings['DEFAULT_LANG']
    if not enable: return value
    pyphen_ = pyphen.Pyphen(lang=lang)
    return words_re.sub(lambda m: pyphen_.inserted(m.group(0), '&shy;'), str(value))

def dehyphenate(value, enable=None):
    if enable is None: enable = settings['M_HTMLSANITY_HYPHENATION']
    if not enable: return value
    return value.replace('&shy;', '')

# TODO: merge into expand_link when 3.8
# with https://github.com/getpelican/pelican/pull/2164 (or the _link_replacer
# part of it) is released
def expand_link_fn(link, content, fn):
    link_regex = r"""^
        (?P<markup>)(?P<quote>)
        (?P<path>{0}(?P<value>.*))
        $""".format(settings['INTRASITE_LINK_REGEX'])
    links = re.compile(link_regex, re.X)
    return links.sub(
        lambda m: fn(content.get_siteurl(), m),
        link)

def expand_link(link, content):
    return expand_link_fn(link, content, content._link_replacer)

# The replacer() function is adapted from
# https://github.com/getpelican/pelican/blob/3.7.1/pelican/contents.py#L213
# in order to be compatible with Pelican <= 3.7.1 that doesn't have it
# available publicly as _link_replacer
# TODO: remove when 3.8 with https://github.com/getpelican/pelican/pull/2164
# (or the _link_replacer part of it) is released
def expand_link_pelican371(link, content):
    def replacer(siteurl, m):
        what = m.group('what')
        value = urlparse(m.group('value'))
        path = value.path
        origin = m.group('path')

        # XXX Put this in a different location.
        if what in {'filename', 'attach'}:
            if path.startswith('/'):
                path = path[1:]
            else:
                # relative to the source path of this content
                path = content.get_relative_source_path(
                    os.path.join(content.relative_dir, path)
                )

            if path not in content._context['filenames']:
                unquoted_path = path.replace('%20', ' ')

                if unquoted_path in content._context['filenames']:
                    path = unquoted_path

            linked_content = content._context['filenames'].get(path)
            if linked_content:
                if what == 'attach':
                    if isinstance(linked_content, Static):
                        linked_content.attach_to(content)
                    else:
                        logger.warning(
                            "%s used {attach} link syntax on a "
                            "non-static file. Use {filename} instead.",
                            content.get_relative_source_path())
                origin = '/'.join((siteurl, linked_content.url))
                origin = origin.replace('\\', '/')  # for Windows paths.
            else:
                logger.warning(
                    "Unable to find `%s`, skipping url replacement.",
                    value.geturl(), extra={
                        'limit_msg': ("Other resources were not found "
                                        "and their urls not replaced")})
        elif what == 'category':
            origin = '/'.join((siteurl, Category(path, content.settings).url))
        elif what == 'tag':
            origin = '/'.join((siteurl, Tag(path, content.settings).url))
        elif what == 'index':
            origin = '/'.join((siteurl, content.settings['INDEX_SAVE_AS']))
        elif what == 'author':
            origin = '/'.join((siteurl, Author(path, content.settings).url))
        else:
            logger.warning(
                "Replacement Indicator '%s' not recognized, "
                "skipping replacement",
                what)

        # keep all other parts, such as query, fragment, etc.
        parts = list(value)
        parts[2] = origin
        origin = urlunparse(parts)

        return ''.join((m.group('markup'), m.group('quote'), origin,
                        m.group('quote')))

    return expand_link_fn(link, content, replacer)

def expand_links(text, content):
    return content._update_content(text, content.get_siteurl())

# To be consistent with both what Pelican does now with '/'.join(SITEURL, url)
# and with https://github.com/getpelican/pelican/pull/2196
def format_siteurl(url):
    return urljoin(settings['SITEURL'] + ('/' if not settings['SITEURL'].endswith('/') else ''), url)

def configure_pelican(pelicanobj):
    pelicanobj.settings['JINJA_FILTERS']['render_rst'] = render_rst
    pelicanobj.settings['JINJA_FILTERS']['expand_links'] = expand_links
    pelicanobj.settings['JINJA_FILTERS']['format_siteurl'] = format_siteurl
    pelicanobj.settings['JINJA_FILTERS']['hyphenate'] = hyphenate
    pelicanobj.settings['JINJA_FILTERS']['dehyphenate'] = dehyphenate

    # TODO: remove when 3.8 with https://github.com/getpelican/pelican/pull/2164
    # (or the _link_replacer part of it) is released
    if not hasattr(Content, '_link_replacer'):
        logger.warning('Unpatched Pelican <= 3.7.1 detected, monkey-patching for expand_link filter support')
        pelicanobj.settings['JINJA_FILTERS']['expand_link'] = expand_link_pelican371
    else:
        pelicanobj.settings['JINJA_FILTERS']['expand_link'] = expand_link

    global settings
    settings['M_HTMLSANITY_HYPHENATION'] = pelicanobj.settings.get('M_HTMLSANITY_HYPHENATION', False)
    settings['M_HTMLSANITY_SMART_QUOTES'] = pelicanobj.settings.get('M_HTMLSANITY_SMART_QUOTES', False)
    for i in 'DEFAULT_LANG', 'DOCUTILS_SETTINGS', 'INTRASITE_LINK_REGEX', 'SITEURL':
        settings[i] = pelicanobj.settings[i]

def add_reader(readers):
    # TODO: remove when 3.8 with https://github.com/getpelican/pelican/pull/2163
    # is released
    if not hasattr(RstReader, 'writer_class') or not hasattr(RstReader, 'field_body_translator_class'):
        logger.warning('Unpatched Pelican <= 3.7.1 detected, monkey-patching for htmlsanity support')
        readers.reader_classes['rst'] = SaneRstReaderPelican371
    else:
        readers.reader_classes['rst'] = SaneRstReader

def register():
    pelican.signals.initialized.connect(configure_pelican)
    pelican.signals.readers_init.connect(add_reader)
