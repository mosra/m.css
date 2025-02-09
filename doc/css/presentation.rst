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

Presentation
############

:breadcrumb: {filename}/css.rst CSS
:footer:
    .. note-dim::
        :class: m-text-center

        `« Page layout <{filename}/css/page-layout.rst>`_ | `CSS <{filename}/css.rst>`_ | `Themes » <{filename}/css/themes.rst>`_

.. |x| unicode:: U+00D7 .. nicer multiply sign

The `m-presentation.css <{filename}/css.rst>`_ file allows you to easily reuse
existing m.css features and components like math rendering or code highlighting
to create presentations (slide decks, keynotes, ..., you name it) that match
your website theme.

.. note-success::

    Check out the `m.css presentation generator <{filename}/presentation.rst>`_
    --- a standalone Python script for creating presentations directly from
    :abbr:`reST <reStructuredText>` sources using m.css components.

.. contents::
    :class: m-block m-default

`Features`_
===========

-   Reuse all existing m.css components to create presentations
-   Ability to show a "presenter view" with additional notes
-   Print directly to PDF on supported browsers for maximal compatibility
-   CSS-only with a possibility to implement extra features using JavaScript

`Basic markup structure`_
=========================

A minimal markup structure is below, very similar to the one for ganeric
`page layout <{filename}/css/page-layout.rst>`_ --- with :html:`<html lang="en">`
and a :html:`<meta>` tag specifying the file encoding, which should be the
first thing in :html:`<head>`. It's also important to specify that the site is
responsive via the :html:`<meta name="viewport">` tag.

The presentation style imposes some constraints on the layout grid --- in
particular, for the presentation mode, the content should span all 12 rows of
the `grid system <{filename}/css/grid.rst>`_. This is different from the
presenter view that's `described below <#presenter-view>`_. Specifying
:css:`.m-container-inflatable` will make it possible for components such as
code blocks or images to make use of the whole screen width. If you don't like
it, simply don't specify the class.

.. code:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Presentation title</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <link rel="stylesheet" href="m-dark-presentation.css" />
    </head>
    <body>
    <div class="m-container m-container-inflatable">
      <div class="m-row">
        <div class="m-col-l-12">
          <article>
            <section id="first">
              <!-- here goes the first slide -->
            </section>
            <section id="second">
              <!-- here goes the second slide -->
            </section>
            <!-- ... -->
          </article>
        </div>
      </div>
    </div>
    </body>
    </html>

The :html:`<article>` contains actual contents of the presentation, with every
:html:`<section>` being one slide. The ``id`` attribute is important, it's used
to flip through the slides. Note that nested :html:`<section>`\ s are not
possible.

`Cover slides`_
---------------

Cover slides simply contain a :html:`<h1>` element and an optional subtitle in
:html:`<h2>`. The :html:`<h1>` fills the slide with a darker background.

.. code:: html

    <section id="cover">
      <h1>A presentation title</h1>
      <h2>A presentation subtitle</h2>
    </section>

.. note-info::

    See how a basic presentation `looks <{filename}/css/presentation/example.html>`_.

`Content slides`_
-----------------

Putting :html:`<h2>` first into the :html:`<section>` makes it a content slide.
After that, you can fill the rest with the usual m.css components, including
various grid layouts. `See below <#content-scaling-and-aspect-ratio>`_ for
general information about how the content responsiveness is handled.

.. code:: html

    <section id="overview">
      <h2>Overview</h2>
      <div class="m-row">
        <div class="m-col-t-6">
          <ul>
            <li>A list</li>
            <li>of things</li>
            <li>to present</li>
          </ul>
        </div>
        <div class="m-col-t-6">
          <pre>some_code: {
        // to show
        as_part(of_the, slide);
    }</pre>
        </div>
      </div>
    </section>

`"Boot screen"`_
----------------

Sometimes it's desirable to have some "boot screen" even before the first cover
slide --- for example with organizer notes or a link to open a presenter view
window. This can be done by addding an :html:`<aside>` element before all other
:html:`<section>` elements. It gets a darker background and extra space for
content after :html:`<h1>`. It doesn't require the ``id`` attribute as it's
often not desired to flip back to the boot screen during a presentation --- but
if you specify it, you'll be able to do that.

.. code:: html
    :class: m-inverted
    :hl_lines: 2 3 4 5 6 7 8 9

    <article>
      <aside>
        <h1>A presentation title</h1>
        <ul>
          <li>Power up the beam</li>
          <li><a href="presenter/">Open presenter view</a></a>
          <li>Have a glass of water</li>
        </ul>
      </aside>
      <section id="cover">
        ...

The boot screen is also shown neither the `presenter view`_ nor included when
`printing to a PDF`_.

`Background images on cover slides`_
------------------------------------

Add :css:`.m-presentation-cover` CSS class together with a background image to
a `cover slide <#cover-slides>`_. This will make the :html:`<h1>` /
:html:`<h2>` headings fully white and the cover image will be scaled to cover
the whole slide. If you have a bright background image, use the :css:`.m-inverted`
CSS class to make the headings black.

.. code:: html
    :class: m-inverted
    :hl_lines: 1 2

    <section id="..." class="m-presentation-cover"
        style="background-image: url('image.jpg')">
      <h1>A presentation title</h1>
      ...
    </section>

`Flipping through the content`_
===============================

Initially, the first :html:`<section>` (or :html:`<aside>`) contained in the
:html:`<article>` element is displayed and all others are hidden. Flipping
through the presentation is done by changing the hash part of page URL, for
example going to ``#overview`` will show contents of the
:html:`<section id="overview">` slide.

To provide on-screen controls, add a :html:`<nav>` element with links to
previous, next and cover slide at the end of every :html:`<section>` element:

.. code:: html
    :class: m-inverted
    :hl_lines: 4 5 6 7 8

    <section id="features">
      <h2>Features</h2>
      ...
      <nav>
        <a class="m-presentation-prev" href="#overview"></a>
        <a class="m-presentation-cover" href="#cover">4 / 17</a>
        <a class="m-presentation-next" href="#usage"></a>
      </nav>
    </section>

The :html:`<nav>` element will be tucked to bottom right of the slide in a dim
small font. The :css:`.m-presentation-prev` and :css:`.m-presentation-next`
links will be filled with the « or » character by the style. It's possible to
omit the center :css:`.m-presentation-cover` link. To preserve the alignment on
the first and last slide but hide the inactive controls, simply replace given
link with an empty :html:`<a></a>` placeholder. The navigation controls are
shown in the `presenter view`_ but removed when `printing to a PDF`_.

.. note-success::

    The `m.css presentation framework <{filename}/presentation.rst>`_ is able
    to generate the on-screen controls automatically, together with a tiny
    JavaScript driver code that attaches to key / touch events for easier use.

`Content scaling and aspect ratio`_
===================================

The content scales uniformly to fill 100% of window width and, as long as you
stick to using responsive m.css components, the output should keep the same
layout regardless on window size.

Because the content keeps the same layout regardless of screen size, it's not
desirable to use any responsive grid features of m.css --- in particular, if
you want to split content into multiple columns, use the
`"tiny" CSS classes <{filename}/css/grid.rst#detailed-grid-properties>`_
(:css:`.m-col-t-*`, :css:`.m-push-t-*` etc.) unconditionally.

.. note-info::

    At the moment, the style is hardcoded to a 16:9 aspect ratio, which affects
    presenter view and print page size.

`Presenter view`_
=================

A common case is to have the presentation displayed on an external screen or a
projector and at the same time have a "presenter view" with additional notes
displayed on the main screen.

The m.css presentation style allows to create a presenter view using the
following markup. Important is adding the :css:`.m-presenter` class to the root
:html:`<html>` element and limiting the contents to 10 columns on large screens
using :css:`.m-col-l-10`. Then for every :html:`<section>` where you need to
have additional presenter notes, add them to a new :html:`<aside>` element at
the end.

.. code:: html
    :class: m-inverted
    :hl_lines: 2 9 13 14 15

    <!DOCTYPE html>
    <html lang="en" class="m-presenter">
    ...
    <body>
    <div class="m-container m-container-inflatable">
      <div class="m-row">
        <div class="m-col-l-10 m-push-m-1">
          <article>
            ...
            <section id="features">
              <h2>Features</h2>
              ...
              <aside class="m-presenter">
                <!-- here go presenter notes -->
              </aside>
            </section>
            ...
          </article>
        </div>
      </div>
    </div>
    </body>
    </html>

The presenter view will display the slide content in a smaller area at the top,
with presenter notes below. The view follows usual m.css responsiveness rules,
so it can be tucked to a very narrow window for example, with the slide being
scaled but notes keeping a fixed size.

The presenter notes are displayed in a black font on a white background and
aren't designed for advanced layouting capabilities apart from basic
paragraphs, links and list items.

.. note-success::

    The `m.css presentation framework <{filename}/presentation.rst>`_ makes it
    possible to have flipping through the slides synchronized between the
    presentation and presenter view window.

`Printing to a PDF`_
====================

It's possible to convert the presentation to a PDF simply by using browser's
print functionality. At the moment, Chromium-based browsers are the only which
respect CSS page size, borders and background/foreground colors.

.. block-warning:: Printing with Firefox

    Unfortunately at the moment Firefox doesn't respect CSS :css:`@page` size
    and the Firefox-specific :css:`color-adjust: exact;` option works only
    halfway, background colors are preserved but all fonts are turned black.

    With some manual work, it's possible to print from Firefox as well. You
    need to manually override page size to 16:9 aspect ratio (m.css uses
    29.7\ |x|\ 16.7 mm), enable borderless print and toggle the "Print
    background colors" to preserve both background color and font color.

The printed version preserves only the slide content, hiding the "boot screen"
or navigation controls, if any. At the moment, printing from the presenter view
will print only the slide content, without presenter notes.
