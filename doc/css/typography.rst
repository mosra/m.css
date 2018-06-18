..
    This file is part of m.css.

    Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
..

Typography
##########

:breadcrumb: {filename}/css.rst CSS
:footer:
    .. note-dim::
        :class: m-text-center

        `« Grid <{filename}/css/grid.rst>`_ | `CSS <{filename}/css.rst>`_ | `Components » <{filename}/css/components.rst>`_

.. role:: css(code)
    :language: css
.. role:: html(code)
    :language: html

Right after being responsive, typography is the second most important thing in
m.css. The `m-components.css <{filename}/css.rst>`_ file styles the most often
used HTML elements to make them look great by default.

.. contents::
    :class: m-block m-default

`Paragraphs, quotes and poems`_
===============================

Each :html:`<p>` element inside :html:`<main>` has the first line indented, is
justified and is separated from the following content by some padding. The
:html:`<blockquote>` elements are indented with a distinctive line on the left.
Because the indentation may look distracting for manually wrapped line blocks,
assign :css:`.m-poem` to such paragraph to indent all lines the same way. To
remove the indentation and justification altogether, use :css:`.m-noindent`.

.. code-figure::

    .. code:: html

        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean id elit
        posuere, consectetur magna congue, sagittis est. Pellentesque est neque,
        aliquet nec consectetur in, mattis ac diam. Aliquam placerat justo ut purus
        interdum, ac placerat lacus consequat.</p>

        <blockquote><p>Ut dictum enim posuere metus porta, et aliquam ex condimentum.
        Proin sagittis nisi leo, ac pellentesque purus bibendum sit
        amet.</p></blockquote>

        <p class="m-poem">
        Curabitur<br/>
        sodales<br/>
        arcu<br/>
        elit</p>

        <p class="m-noindent">Mauris id suscipit mauris, in scelerisque lectus. Aenean
        nec nunc eu sem tincidunt imperdiet ut non elit. Integer nisi tellus,
        ullamcorper vitae euismod quis, venenatis eu nulla.</p>

    .. raw:: html

        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean id elit
        posuere, consectetur magna congue, sagittis est. Pellentesque est neque,
        aliquet nec consectetur in, mattis ac diam. Aliquam placerat justo ut purus
        interdum, ac placerat lacus consequat.</p>

        <blockquote><p>Ut dictum enim posuere metus porta, et aliquam ex condimentum.
        Proin sagittis nisi leo, ac pellentesque purus bibendum sit
        amet.</p></blockquote>

        <p class="m-poem">
        Curabitur<br/>
        sodales<br/>
        arcu<br/>
        elit</p>

        <p class="m-noindent">Mauris id suscipit mauris, in scelerisque lectus. Aenean
        nec nunc eu sem tincidunt imperdiet ut non elit. Integer nisi tellus,
        ullamcorper vitae euismod quis, venenatis eu nulla.</p>

`Lists, diaries`_
=================

Ordered and unordered lists have padding on bottom only on the first level.
Mark the list with :css:`.m-unstyled` to remove the asterisks/numbers and
indentation.

.. code-figure::

    .. code:: html

        <ul>
          <li>Item 1</li>
          <li>
            Item 2
            <ol>
              <li>An item</li>
              <li>Another item</li>
            </ol>
          </li>
          <li>Item 3</li>
        </ul>

        <ol class="m-unstyled">
          <li>Item of an unstyled list</li>
          <li>Another item of an unstyled list</li>
        </ol>

    .. raw:: html

        <ul>
        <li>Item 1</li>
        <li>
          Item 2
          <ol>
            <li>An item</li>
            <li>Another item</li>
          </ol>
        </li>
        <li>Item 3</li>
        </ul>

        <ol class="m-unstyled">
          <li>Item of an unstyled list</li>
          <li>Another item of an unstyled list</li>
        </ol>

It's possible to convert a list to a single line with items separated by ``|``
to save vertical space on mobile devices and responsively change it back on
larger screens. Mark such list with :css:`.m-block-bar-*`:

.. code-figure::

    .. code:: html

        <ul class="m-block-bar-m">
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>

    .. raw:: html

        <ul class="m-block-bar-m">
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>

.. note-success::

    Shrink your browser window to see the effect in the above list.

Mark your definition list with :css:`.m-diary` to put the titles next to
definitions.

.. code-figure::

    .. code:: html

        <dl class="m-diary">
          <dt>07:30:15</dt>
          <dd>Woke up. The hangover is crazy today.</dd>
          <dt>13:47:45</dt>
          <dd>Got up from bed. Trying to find something to eat.</dd>
          <dt>23:34:13</dt>
          <dd>Finally put my pants on. Too late.</dd>
        </dl>

    .. raw:: html

        <dl class="m-diary">
          <dt>07:30:15</dt>
          <dd>Woke up. The hangover is crazy today.</dd>
          <dt>13:47:45</dt>
          <dd>Got up from bed. Trying to find something to eat.</dd>
          <dt>23:34:13</dt>
          <dd>Finally put my pants on. Too late.</dd>
        </dl>

The lists are compact by default, wrap item content in :html:`<p>` to make them
inflated. Paragraphs in list items are neither indented nor justified.

.. code-figure::

    .. code:: html

        <ul>
          <li>
            <p>Item 1, first paragraph.</p>
            <p>Item 1, second paragraph.</p>
          </li>
          <li>
            <p>Item 2</p>
            <ol>
              <li><p>An item</p></li>
              <li><p>Another item</p></li>
            </ol>
          </li>
          <li><p>Item 3</p></li>
        </ul>

    .. raw:: html

        <ul>
          <li>
            <p>Item 1, first paragraph.</p>
            <p>Item 1, second paragraph.</p>
          </li>
          <li>
            <p>Item 2</p>
            <ol>
              <li><p>An item</p></li>
              <li><p>Another item</p></li>
            </ol>
          </li>
          <li><p>Item 3</p></li>
        </ul>

`Headings`_
===========

The :html:`<h1>` is meant to be a page heading, thus it is styled a bit
differently --- it's bigger and has :css:`1rem` padding after. The :html:`<h2>`
to :html:`<h6>` are smaller and have just :css:`0.5rem` padding after, to be
closer to the content that follows. Wrapping part of the heading in a
:css:`.m-thin` will make it appear thinner, depending on used CSS theme.

.. code-figure::

    .. code:: html

        <h1>Heading 1 <span class="m-thin">with subtitle</span></h1>
        <h2>Heading 2 <span class="m-thin">with subtitle</span></h2>
        <h3>Heading 3 <span class="m-thin">with subtitle</span></h3>
        <h4>Heading 4 <span class="m-thin">with subtitle</span></h4>
        <h5>Heading 5 <span class="m-thin">with subtitle</span></h5>
        <h6>Heading 6 <span class="m-thin">with subtitle</span></h6>

    .. raw:: html

        <h1>Heading 1 <span class="m-thin">with subtitle</span></h1>
        <h2>Heading 2 <span class="m-thin">with subtitle</span></h2>
        <h3>Heading 3 <span class="m-thin">with subtitle</span></h3>
        <h4>Heading 4 <span class="m-thin">with subtitle</span></h4>
        <h5>Heading 5 <span class="m-thin">with subtitle</span></h5>
        <h6>Heading 6 <span class="m-thin">with subtitle</span></h6>

.. note-warning::

    Headings are styled in a slightly different way for
    `page sections <{filename}/css/page-layout.rst#main-content>`_ and
    `article headers <{filename}/css/page-layout.rst#articles>`_, clicks the
    links for more information. There is also a possibility to put
    `breadcrumb navigation <{filename}/css/page-layout.rst#breadcrumb-navigation>`_
    in the :html:`<h1>` element.

`Transitions`_
==============

Horizontal line is centered and fills 75% of the parent element. For a more
fancy transition, use :css:`.m-transition` on a paragraph.

.. code-figure::

    .. code:: html

        ...
        <hr/>
        ...
        <p class="m-transition">~ ~ ~</p>
        ...

    .. raw:: html

        <p>Vivamus dui quam, volutpat eu lorem sit amet, molestie tristique erat.
        Vestibulum dapibus est eu risus pellentesque volutpat.</p>
        <hr/>
        <p>Aenean tellus turpis, suscipit quis iaculis ut, suscipit nec magna.
        Vestibulum finibus sit amet neque nec volutpat. Suspendisse sit amet nisl in
        orci posuere mattis.</p>
        <p class="m-transition">~ ~ ~</p>
        <p> Praesent eu metus sed felis faucibus placerat ut eu quam. Aliquam convallis
        accumsan ante sit amet iaculis. Phasellus rhoncus hendrerit leo vitae lacinia.
        Maecenas iaculis dui ex, eu interdum lacus ornare sit amet.</p>

.. note-info::

    Transitions can be conveniently created with a :rst:`.. transition::`
    directive in your :abbr:`reST <reStructuredText>` markup using the
    `Pelican Components plugin <{filename}/plugins/components.rst#transitions>`_.

`Preformatted blocks`_
======================

The :html:`pre` element preserves your whitespace and adds a convenient
scrollbar if the content is too wide. If inside an
`inflatable nested grid <{filename}/css/grid.rst#inflatable-nested-grid>`_, it
will have negative margin to make its contents aligned with surrounding text.

.. code-figure::

    .. code:: html

        <pre>
        int main() {
            return 0;
        }
        </pre>

    .. raw:: html

        <pre>
        int main() {
            return 0;
        }
        </pre>

.. note-info::

    The Components page has additional information about
    `code block styling <{filename}/css/components.rst#code>`_.

`Inline elements`_
==================

.. code-figure::

    .. code:: html

        A <a href="#">link</a>, <em>emphasised text</em>, <strong>strong text</strong>,
        <abbr title="abbreviation">abbr</abbr> shown inside a normal text flow to
        verify that they don't break text flow. Then there is <small>small text</small>,
        <sup>super</sup>, <sub>sub</sub> and <s>that is probably all I can think of
        right now</s> oh, there is also <mark>marked text</mark> and
        <code>int a = some_code();</code>.

    .. raw:: html

        A <a href="#">link</a>, <em>emphasised text</em>, <strong>strong text</strong>,
        <abbr title="abbreviation">abbr</abbr> shown inside a normal text flow to
        verify that they don't break text flow. Then there is <small>small text</small>,
        <sup>super</sup>, <sub>sub</sub> and <s>that is probably all I can think of
        right now</s> oh, there is also <mark>marked text</mark> and
        <code>int a = some_code();</code>.

.. note-info::

    The Components page has additional information about
    `text styling <{filename}/css/components.rst#text>`_.

`Text alignment`_
=================

Use :css:`.m-text-left`, :css:`.m-text-right` or :css:`.m-text-center` to
align text inside its parent element. Use :css:`.m-text-top`,
:css:`.m-text-middle` and :css:`.m-text-bottom` to align text vertically for
example in a table cell. See `Floating around <{filename}/css/grid.rst#floating-around>`_
in the grid system for aligning and floating blocks in a similar way.

`Padding`_
==========

Block elements :html:`<p>`, :html:`<ol>`, :html:`<ul>`, :html:`<dl>`,
:html:`<blockqote>`, :html:`<pre>` and :html:`<hr>` by default have :css:`1rem`
padding on the bottom, except when they are the last child, to avoid excessive
spacing. A special case is lists --- components directly inside :html:`<li>`
elements have :css:`1rem` padding on the bottom, except when the :html:`<li>`
is last, to achieve consistent spacing for inflated lists.

The :css:`1rem` padding on the bottom can be disabled with :css:`.m-nopadb`,
similarly as with `grid layouts <{filename}/css/grid.rst#grid-padding>`_.
