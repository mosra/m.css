m.images
########

:summary: no.

Image:

.. image:: {static}/ship.jpg

Image with link:

.. image:: {static}/ship.jpg
    :target: {static}/ship.jpg

Image, class on top, custom alt:

.. image:: {static}/ship.jpg
    :class: m-fullwidth
    :alt: A Ship

Image with link, class on top:

.. image:: {static}/ship.jpg
    :target: {static}/ship.jpg
    :class: m-fullwidth

Figure:

.. figure:: {static}/ship.jpg

    A Ship

    Yes.

Figure with link and only a caption:

.. figure:: {static}/ship.jpg
    :target: {static}/ship.jpg

    A Ship

Figure with link and class on top:

.. figure:: {static}/ship.jpg
    :target: {static}/ship.jpg
    :figclass: m-fullwidth

    A Ship

Image grid:

.. image-grid::

    {static}/ship.jpg
    {static}/flowers.jpg

    {static}/flowers.jpg
    {static}/ship.jpg

Image grid with a PNG file, JPEG with sparse EXIF data, JPEG with no EXIF data
and long exposure (>1 second):

.. image-grid::

    {static}/tiny.png
    {static}/sparseexif.jpg
    {static}/noexif.jpg
    {static}/longexposure.jpg
