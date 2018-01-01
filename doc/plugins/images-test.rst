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

Test
####

:save_as: plugins/images/test/index.html
:breadcrumb: {filename}/plugins.rst Pelican plugins
             {filename}/plugins/images.rst

`Images, figures`_
==================

All images should have no ``alt`` text, unless specified manually.

Image with link:

.. image:: {filename}/static/ship-small.jpg
    :target: {filename}/static/ship.jpg

Image, class on top, custom alt:

.. image:: {filename}/static/ship.jpg
    :class: m-fullwidth
    :alt: A Ship

Image with link, class on top:

.. image:: {filename}/static/ship.jpg
    :target: {filename}/static/ship.jpg
    :class: m-fullwidth

Figure with link and only a caption:

.. figure:: {filename}/static/ship-small.jpg
    :target: {filename}/static/ship.jpg

    A Ship

Figure with link and class on top:

.. figure:: {filename}/static/ship-small.jpg
    :target: {filename}/static/ship.jpg
    :figclass: m-fullwidth

    A Ship

Image grid, not inflated:

.. image-grid::

    {filename}/static/ship.jpg
    {filename}/static/flowers.jpg

Image grid, inflated:

.. container:: m-container-inflated

    .. image-grid::

        {filename}/static/flowers.jpg
        {filename}/static/ship.jpg
