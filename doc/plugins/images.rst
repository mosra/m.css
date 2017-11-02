..
    This file is part of m.css.

    Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>

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

Images
######

:breadcrumb: {filename}/plugins.rst Pelican plugins
:footer:
    .. note-dim::
        :class: m-text-center

        `« Components <{filename}/plugins/components.rst>`_ | `Pelican plugins <{filename}/plugins.rst>`_ | `Math and code » <{filename}/plugins/math-and-code.rst>`_

Gives sane defaults to images and figures and provides a way to present
beautiful image galleries.

.. contents::
    :class: m-block m-default

`How to use`_
=============

Download the `m/images.py <{filename}/plugins.rst>`_ file, put it including the
``m/`` directory into one of your :py:`PLUGIN_PATHS` and add ``m.images``
package to your :py:`PLUGINS` in ``pelicanconf.py``. To use the image grid
feature, in addition you need the `Pillow <https://pypi.python.org/pypi/Pillow>`_
library installed. This plugin assumes presence of
`m.htmlsanity <{filename}/plugins/htmlsanity.rst>`_.

.. code:: python

    PLUGINS += ['m.htmlsanity', 'm.images']
    M_IMAGES_REQUIRE_ALT_TEXT = False

`Images, figures`_
==================

The plugin overrides the builtin
`image <http://docutils.sourceforge.net/docs/ref/rst/directives.html#image>`__
and `figure <http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure>`__
directives and:

-   Adds :css:`.m-image` / :css:`.m-figure` CSS classes to them so they have
    the expected m.css `image <{filename}/css/components.rst#images>`_ and
    `figure <{filename}/css/components.rst#figures>`_ styling.
-   Removes the :rst:`:align:`, :rst:`:figwidth:` and :rst:`:scale:` options,
    as this is better handled by m.css features.
-   To maintain accessibility easier, makes it possible to enforce :rst:`:alt:`
    text for every image and figure by setting :py:`M_IMAGES_REQUIRE_ALT_TEXT`
    to :py:`True`.

You can add `additional CSS classes <{filename}/css/components.rst#images>`_ to
images or figures via the :rst:`:class:` or :rst:`:figclass:` options,
respectively. If you want the image or figure to be clickable, use the
:rst:`:target:` option. The alt text can be specified using the :rst:`:alt:`
option for both images and figures.

.. code-figure::

    .. code:: rst

        .. image:: flowers.jpg
            :target: flowers.jpg
            :alt: Flowers

        .. figure:: ship.jpg
            :alt: Ship

            A Ship

            Photo © `The Author <http://blog.mosra.cz/>`_

    .. container:: m-row

        .. container:: m-col-m-6

            .. image:: {filename}/static/flowers-small.jpg
                :target: {filename}/static/flowers.jpg

        .. container:: m-col-m-6

            .. figure:: {filename}/static/ship-small.jpg

                A Ship

                Photo © `The Author <http://blog.mosra.cz/>`_

`Image grid`_
=============

Use the :rst:`.. image-grid::` directive for creating
`image grid <{filename}/css/components.rst#image-grid>`_. Directive contents
are a list of image URLs, blank lines separate grid rows. The plugin
automatically extracts size information and scales the images accordingly, in
addition EXIF properties such as aperture, shutter speed and ISO are extracted
and displayed in the caption on hover. The images are also made clickable, the
target is the image file itself.

Example of a two-row image grid is below. Sorry for reusing the same two images
all over (I'm making it easier for myself); if you want to see a live example
with non-repeating images, head over to `my blog <http://blog.mosra.cz/cesty/mainau/>`_.

.. code:: rst

    .. image-grid::

        {filename}/ship.jpg
        {filename}/flowers.jpg

        {filename}/flowers.jpg
        {filename}/ship.jpg

.. image-grid::

    {filename}/static/ship.jpg
    {filename}/static/flowers.jpg

    {filename}/static/flowers.jpg
    {filename}/static/ship.jpg

.. note-warning::

    Unlike with the image and figure directives above, Pelican *needs* to have
    the images present on a filesystem to extract size information. It's
    advised to use the builtin *absolute* ``{filename}`` or ``{attach}`` syntax
    for `linking to internal content <http://docs.getpelican.com/en/stable/content.html#linking-to-internal-content>`_.
