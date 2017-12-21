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

import os
from docutils.parsers import rst
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives, states
from docutils.nodes import fully_normalize_name, whitespace_normalize_name
from docutils.parsers.rst.roles import set_classes
from docutils import nodes
from pelican import signals
from pelican import StaticGenerator

# If Pillow is not available, it's not an error unless one uses the image grid
# functionality
try:
    import PIL.Image
    import PIL.ExifTags
except ImportError:
    PIL = None

settings = {}

class Image(Directive):
    """Image directive

    Copy of docutils.parsers.rst.directives.Image with:

    -   the align, scale, width, height options removed (handled better by
        m.css)
    -   .m-image CSS class added
    -   adding a outer container for clickable image to make the clickable area
        cover only the image
    -   optionally dying when alt text is not present
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'alt': directives.unchanged_required,
                   'name': directives.unchanged,
                   'class': directives.class_option,
                   'target': directives.unchanged_required}

    # Overriden by Figure
    image_class = 'm-image'

    def run(self):
        messages = []
        reference = directives.uri(self.arguments[0])
        self.options['uri'] = reference
        reference_node = None
        if 'target' in self.options:
            block = states.escape2null(
                self.options['target']).splitlines()
            block = [line for line in block]
            target_type, data = self.state.parse_target(
                block, self.block_text, self.lineno)
            if target_type == 'refuri':
                reference_node = nodes.reference(refuri=data)
            elif target_type == 'refname':
                reference_node = nodes.reference(
                    refname=fully_normalize_name(data),
                    name=whitespace_normalize_name(data))
                reference_node.indirect_reference_name = data
                self.state.document.note_refname(reference_node)
            else:                           # malformed target
                messages.append(data)       # data is a system message
            del self.options['target']

        # Remove the classes from the image element, will be added either to it
        # or to the wrapping element later
        set_classes(self.options)
        classes = self.options.get('classes', [])
        if 'classes' in self.options: del self.options['classes']
        image_node = nodes.image(self.block_text, **self.options)

        if not 'alt' in self.options and settings['M_IMAGES_REQUIRE_ALT_TEXT']:
            error = self.state_machine.reporter.error(
                    'Images and figures require the alt text. See the M_IMAGES_REQUIRE_ALT_TEXT option.',
                    image_node,
                    line=self.lineno)
            return [error]

        self.add_name(image_node)
        if reference_node:
            if self.image_class:
                container_node = nodes.container()
                container_node['classes'] += [self.image_class] + classes
                reference_node += image_node
                container_node += reference_node
                return messages + [container_node]
            else:
                reference_node += image_node
                return messages + [reference_node]
        else:
            if self.image_class: image_node['classes'] += [self.image_class] + classes
            return messages + [image_node]

class Figure(Image):
    """Figure directive

    Copy of docutils.parsers.rst.directives.Figure with:

    -   the align, figwidth options removed (handled better by m.css)
    -   .m-figure CSS class added
    """

    option_spec = Image.option_spec.copy()
    option_spec['figclass'] = directives.class_option
    has_content = True

    image_class = None

    def run(self):
        figclasses = self.options.pop('figclass', None)
        (image_node,) = Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        figure_node = nodes.figure('', image_node)
        if figclasses:
            figure_node['classes'] += figclasses
        figure_node['classes'] += ['m-figure']

        if self.content:
            node = nodes.Element()          # anonymous container for parsing
            self.state.nested_parse(self.content, self.content_offset, node)
            first_node = node[0]
            if isinstance(first_node, nodes.paragraph):
                caption = nodes.caption(first_node.rawsource, '',
                                        *first_node.children)
                caption.source = first_node.source
                caption.line = first_node.line
                figure_node += caption
            elif not (isinstance(first_node, nodes.comment)
                      and len(first_node) == 0):
                error = self.state_machine.reporter.error(
                      'Figure caption must be a paragraph or empty comment.',
                      nodes.literal_block(self.block_text, self.block_text),
                      line=self.lineno)
                return [figure_node, error]
            if len(node) > 1:
                figure_node += nodes.legend('', *node[1:])
        return [figure_node]

class ImageGrid(rst.Directive):
    has_content = True

    def run(self):
        grid_node = nodes.container()
        grid_node['classes'] += ['m-imagegrid', 'm-container-inflate']

        rows = [[]]
        total_widths = [0]
        for uri in self.content:
            # New line, calculating width from 0 again
            if not uri:
                rows.append([])
                total_widths.append(0)
                continue

            # Open the files and calculate the overall width
            absuri = uri.format(filename=os.path.join(os.getcwd(), settings['PATH']))
            im = PIL.Image.open(absuri)

            # Get EXIF info, if it's there
            if hasattr(im, '_getexif') and im._getexif() is not None:
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in im._getexif().items()
                    if k in PIL.ExifTags.TAGS and len(str(v)) < 256
                }

                # Not all info might be present
                caption = []
                if 'FNumber' in exif:
                    caption += ["F{}".format(float(float(exif['FNumber'][0])/float(exif['FNumber'][1])))]
                if 'ExposureTime' in exif:
                    numerator, denominator = exif['ExposureTime']
                    if int(numerator) > int(denominator):
                        caption += ["{} s".format(float(numerator)/float(denominator))]
                    else:
                        caption += ["{}/{} s".format(numerator, denominator)]
                if 'ISOSpeedRatings' in exif:
                    caption += ["ISO {}".format(exif['ISOSpeedRatings'])]
                caption = ', '.join(caption)

            # It's not (e.g. a PNG file), empty caption
            else: caption = ""

            rel_width = float(im.width)/im.height
            total_widths[-1] += rel_width
            rows[-1].append((uri, rel_width, caption))

        for i, row in enumerate(rows):
            row_node = nodes.container()

            for uri, rel_width, caption in row:
                image_reference = rst.directives.uri(uri)
                image_node = nodes.image('', uri=image_reference)

                # <figurecaption> in case there's a caption
                if caption:
                    text_nodes, _ = self.state.inline_text(caption, self.lineno)
                    text_node = nodes.paragraph('', '', *text_nodes)
                    overlay_node = nodes.caption()
                    overlay_node.append(text_node)

                # Otherwise an empty <div>
                else: overlay_node = nodes.container()

                link_node = nodes.reference('', refuri=image_reference)
                link_node.append(image_node)
                link_node.append(overlay_node)
                wrapper_node = nodes.figure(width="{:.3f}%".format(rel_width*100.0/total_widths[i]))
                wrapper_node.append(link_node)
                row_node.append(wrapper_node)

            grid_node.append(row_node)

        return [grid_node]

def configure(pelicanobj):
    settings['PATH'] = pelicanobj.settings.get('PATH', 'content')
    settings['M_IMAGES_REQUIRE_ALT_TEXT'] = pelicanobj.settings.get('M_IMAGES_REQUIRE_ALT_TEXT', False)

def register():
    signals.initialized.connect(configure)

    rst.directives.register_directive('image', Image)
    rst.directives.register_directive('figure', Figure)
    rst.directives.register_directive('image-grid', ImageGrid)
