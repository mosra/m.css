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
