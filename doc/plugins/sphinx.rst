..
    This file is part of m.css.

    Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>

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

Sphinx
######

:breadcrumb: {filename}/plugins.rst Plugins
:footer:
    .. note-dim::
        :class: m-text-center

        `« Metadata <{filename}/plugins/metadata.rst>`_ | `Plugins <{filename}/plugins.rst>`_

.. role:: html(code)
    :language: html
.. role:: py(code)
    :language: py
.. role:: rst(code)
    :language: rst

Makes it possible to document APIs with the `Python doc theme <{filename}/documentation/python.rst>`_
using external files in a way similar to `Sphinx <https://www.sphinx-doc.org/>`_.

.. contents::
    :class: m-block m-default

`How to use`_
=============

`Pelican`_
----------

List the plugin in your :py:`PLUGINS`.

.. code:: py

    PLUGINS += ['m.sphinx']

`Module, class and data docs`_
==============================

The :rst:`.. py:module::`, :rst:`.. py:class::` and :rst:`.. py:data::`
directives provide a way to supply module, class and data documentation
content. Directive option is the name to document, directive contents are
the actual contents; in addition the :py:`:summary:` option can override the
docstring extracted using inspection. No restrictions are made on the contents,
it's possible to make use of any additional plugins in the markup. Example:

.. code:: rst

    .. py:module:: mymodule
        :summary: A top-level module.

        This is the top-level module.

        Usage
        -----

        .. code:: pycon

            >>> import mymodule
            >>> mymodule.foo()
            Hello world!

    .. py:data:: mymodule.ALMOST_PI
        :summary: :math:`\pi`, but *less precise*.

Compared to docstrings, the :py:`:summary:` is interpreted as
:abbr:`reST <reStructuredText>`, which means you can keep the docstring
formatting simpler (for display inside IDEs or via the builtin :py:`help()`),
while supplying an alternative and more complex-formatted summary for the
actual rendered docs.

.. note-info::

    Modules, classes and data described using these directives have to actually
    exist (i.e., accessible via inspection) in given module. If given name
    doesn't exist, a warning will be printed during processing and the
    documentation ignored.
