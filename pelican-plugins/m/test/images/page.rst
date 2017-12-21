m.images
########

:summary: no.

Image:

.. image:: {filename}/ship.jpg

Image with link:

.. image:: {filename}/ship.jpg
    :target: {filename}/ship.jpg

Image, class on top, custom alt:

.. image:: {filename}/ship.jpg
    :class: m-fullwidth
    :alt: A Ship

Image with link, class on top:

.. image:: {filename}/ship.jpg
    :target: {filename}/ship.jpg
    :class: m-fullwidth

Figure:

.. figure:: {filename}/ship.jpg

    A Ship

    Yes.

Figure with link and only a caption:

.. figure:: {filename}/ship.jpg
    :target: {filename}/ship.jpg

    A Ship

Figure with link and class on top:

.. figure:: {filename}/ship.jpg
    :target: {filename}/ship.jpg
    :figclass: m-fullwidth

    A Ship

Image grid:

.. image-grid::

    {filename}/ship.jpg
    {filename}/flowers.jpg

    {filename}/flowers.jpg
    {filename}/ship.jpg

Image grid with a PNG file, JPEG with sparse EXIF data, JPEG with no EXIF data
and long exposure (>1 second):

.. image-grid::

    {filename}/tiny.png
    {filename}/sparseexif.jpg
    {filename}/noexif.jpg
    {filename}/longexposure.jpg
