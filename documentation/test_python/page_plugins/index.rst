This shows some plugins
#######################

This project is :gh:`on GitHub <mosra/m.css>` and

.. class:: m-table

====== ======
The    tables
====== ======
render nicer now.
====== ======

.. note-success::

    Yup!

.. role:: link-flat(link)
    :class: m-flat

See, :glfn:`DrawElements` is the grandpa of :vkfn:`CmdDraw`. But
:link-flat:`not everything is as it "seems" to be <javascript:alert("boo!")>`
--- however the typography makes that bearable. Python bindings for
:dox:`Corrade::Containers` and Magnum are nice too:

.. code:: pycon

    >>> from magnum import *
    >>> a = Vector3(1.0, 2.0, 3.0)
    >>> a.dot()
    14.0

.. fancy-line:: Custom plugins!

And now something totally different:

.. raw:: html

    <style>
    div.m-plot svg { font-family: DejaVu Sans; }
    </style>

.. plot:: A plot with a single color
    :type: barh
    :labels:
        First
        Second
    :units: meters, i guess?
    :values: 15 30
    :colors: success
