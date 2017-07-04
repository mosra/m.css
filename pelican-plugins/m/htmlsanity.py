import re

from docutils.writers.html5_polyglot import HTMLTranslator
import docutils
from docutils import nodes

import pelican.signals
from pelican.readers import RstReader

class SaneHtmlTranslator(HTMLTranslator):
    """Sane HTML translator

    Patched version of docutils builtin HTML5 translator, improving the output
    further.
    """

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

class SaneRstReader(RstReader):
    writer_class = SaneHtmlWriter
    field_body_translator_class = _SaneFieldBodyTranslator

def add_reader(readers):
    readers.reader_classes['rst'] = SaneRstReader

def register():
    pelican.signals.readers_init.connect(add_reader)
