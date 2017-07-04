import re

from docutils.writers.html5_polyglot import HTMLTranslator
from docutils.transforms import Transform
import docutils
from docutils import nodes, utils
from docutils.utils import smartquotes

import pelican.signals
from pelican.readers import RstReader

try:
    import pyphen
except ImportError:
    pyphen = None

# These come from settings
enable_hyphenation = False
smart_quotes = False
hyphenation_lang = 'en'
docutils_settings = {}

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

    # Original SmartQuotes have priority 850, we are patching them so we need
    # a lower number
    default_priority = 849

    def apply(self):
        # We are using our own config variable instead of
        # self.document.settings.smart_quotes in order to avoid the builtin
        # SmartQuotes to be executed as well
        global smart_quotes
        if not smart_quotes:
            return
        try:
            alternative = smart_quotes.startswith('alt')
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
                if lang not in self.unsupported_languages:
                    self.document.reporter.warning('No smart quotes '
                        'defined for language "%s".'%lang, base_node=node)
                self.unsupported_languages.add(lang)
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
        global enable_hyphenation
        if not enable_hyphenation:
            return

        document_language = self.document.settings.language_code

        pyphen_for_lang = {}

        # Go through all text words and hyphenate them
        for node in self.document.traverse(nodes.TextElement):
            # Skip preformatted text blocks, special elements and field names
            if isinstance(node, (nodes.FixedTextElement, nodes.Special, nodes.field_name)):
                continue

            # Proper language-dependent hyphenation
            lang = node.get_language_code(document_language)

            # Create new Pyphen object for given lang, if not yet cached. I'm
            # assuming this is faster than recreating the instance for every
            # text node
            if lang not in pyphen_for_lang:
                pyphen_for_lang[lang] = pyphen.Pyphen(lang=lang)

            for txtnode in node.traverse(nodes.Text):
                # Exclude:
                #  - literals and spans inside literals
                #  - field bodies (such as various :save_as: etc.)
                if isinstance(txtnode.parent, nodes.literal) or isinstance(txtnode.parent.parent, nodes.literal) or isinstance(txtnode.parent.parent, nodes.field_body):
                    continue

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

    # Use HTML5 <section> tag for sections (instead of <div class="section">)
    def visit_section(self, node):
        self.section_level += 1
        self.body.append(
            self.starttag(node, 'section'))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</section>\n')

    # Literal -- print as <code> (instead of some <div>)
    def visit_literal(self, node):
        # special case: "code" role
        classes = node.get('classes', [])
        if 'code' in classes:
            # filter 'code' from class arguments
            node['classes'] = [cls for cls in classes if cls != 'code']
            self.body.append(self.starttag(node, 'code', ''))
            return
        self.body.append(
            self.starttag(node, 'code', ''))
        text = node.astext()
        # remove hard line breaks (except if in a parsed-literal block)
        if not isinstance(node.parent, nodes.literal_block):
            text = text.replace('\n', ' ')
        # Protect text like ``--an-option`` and the regular expression
        # ``[+]?(\d+(\.\d*)?|\.\d+)`` from bad line wrapping
        for token in self.words_and_spaces.findall(text):
            if token.strip() and self.sollbruchstelle.search(token):
                self.body.append('<span class="pre">%s</span>'
                                    % self.encode(token))
            else:
                self.body.append(self.encode(token))
        self.body.append('</code>')
        # Content already processed:
        raise nodes.SkipNode

    def depart_literal(self, node):
        # skipped unless literal element is from "code" role:
        self.body.append('</code>')

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
            isinstance(node.parent, nodes.compound)):
            # Never compact paragraphs in document or compound.
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
        self.compact_p = None

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

def render_rst(value):
    extra_params = {'initial_header_level': '2',
                    'syntax_highlight': 'short',
                    'input_encoding': 'utf-8',
                    'exit_status_level': 2,
                    'embed_stylesheet': False}
    if docutils_settings:
        extra_params.update(docutils_settings)

    pub = docutils.core.Publisher(
        writer=SaneHtmlWriter(),
        source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.writer.translator_class = _SaneFieldBodyTranslator
    pub.process_programmatic_settings(None, extra_params, None)
    pub.set_source(source=value)
    pub.publish(enable_exit_status=True)
    return pub.writer.parts.get('body')

def hyphenate(value, enable=None, lang=None):
    if enable is None: enable = enable_hyphenation
    if lang is None: lang = hyphenation_lang
    if not enable: return value
    pyphen_ = pyphen.Pyphen(lang=lang)
    return words_re.sub(lambda m: pyphen_.inserted(m.group(0), '\u00AD'), str(value))

def configure_pelican(pelicanobj):
    pelicanobj.settings['JINJA_FILTERS']['render_rst'] = render_rst
    pelicanobj.settings['JINJA_FILTERS']['hyphenate'] = hyphenate

    global enable_hyphenation, smart_quotes, hyphenation_lang, docutils_settings
    enable_hyphenation = pelicanobj.settings.get('HTMLSANITY_HYPHENATION', False)
    smart_quotes = pelicanobj.settings.get('HTMLSANITY_SMART_QUOTES', False)
    hyphenation_lang = pelicanobj.settings['DEFAULT_LANG']
    docutils_settings = pelicanobj.settings['DOCUTILS_SETTINGS']

def add_reader(readers):
    readers.reader_classes['rst'] = SaneRstReader

def register():
    pelican.signals.initialized.connect(configure_pelican)
    pelican.signals.readers_init.connect(add_reader)
