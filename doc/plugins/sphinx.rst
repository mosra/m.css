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

`Python doc theme`_
-------------------

List the plugin in your :py:`PLUGINS`.

.. code:: py

    PLUGINS += ['m.sphinx']

.. note-info::

    This plugin is available only for the `Python doc theme <{filename}/documentation/python.rst>`_,
    not usable for Pelican or Doxygen themes.

`Module, class, enum, function, property and data docs`_
========================================================

The :rst:`.. py:module::`, :rst:`.. py:class::`, :rst:`.. py:enum::`,
:rst:`.. py:function::`, :rst:`.. py:property::` and :rst:`.. py:data::`
directives provide a way to supply module, class, enum, function / method,
property and data documentation content.

Directive option is the name to document, directive contents are the actual
contents; in addition all the directives have the :py:`:summary:` option that
can override the docstring extracted using inspection. No restrictions are made
on the contents, it's also possible to make use of any additional plugins in
the markup. Example:

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

.. note-warning::

    Modules, classes and data described using these directives have to actually
    exist (i.e., accessible via inspection) in given module. If given name
    doesn't exist, a warning will be printed during processing and the
    documentation ignored.

The :rst:`.. py:function::` directive supports additional options ---
:py:`:param <name>:` for documenting parameters and :py:`:return:` for
documenting the return value. It's allowed to have either none or all
parameters documented (the ``self`` parameter can be omitted), having them
documented only partially or documenting parameters that are not present in the
function signature will cause a warning. Example:

.. code:: rst

    .. py:function:: mymodule.MyContainer.add
        :param key:                 Key to add
        :param value:               Corresponding value
        :param overwrite_existing:  Overwrite existing value if already present
            in the container
        :return:                    The inserted tuple or the existing
            key/value pair in case ``overwrite_existing`` is not set

        Add a key/value pair to the container, optionally overwriting the
        previous value.
