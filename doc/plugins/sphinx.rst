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

Download the `m/sphinx.py <{filename}/plugins.rst>`_ file, put it including the
``m/`` directory into one of your :py:`PLUGIN_PATHS` and add ``m.sphinx``
package to your :py:`PLUGINS` in ``pelicanconf.py``. The plugin uses Sphinx
inventory files to get a list of linkable symbols and you need to provide
list of tuples containing tag file path, URL prefix, an optional list of
implicitly prepended paths and an optional list of CSS classes for each link in
:py:`M_SPHINX_INVENTORIES`. Every Sphinx-generated documentation contains an
``objects.inv`` file in its root directory (and the root directory is the URL
prefix as well), for example for Python 3 it's located at
https://docs.python.org/3/objects.inv. Download the files and specify path to
them and the URL they were downloaded from, for example:

.. code:: python

    PLUGINS += ['m.sphinx']
    M_SPHINX_INVENTORIES = [
        ('sphinx/python.inv', 'https://docs.python.org/3/', ['xml.']),
        ('sphinx/numpy.inv', 'https://docs.scipy.org/doc/numpy/', [], ['m-flat'])]

`Python doc theme`_
-------------------

List the plugin in your :py:`PLUGINS`. The :py:`M_SPHINX_INVENTORIES`
configuration option is interpreted the same way as in case of the `Pelican`_
plugin.

.. code:: py

    PLUGINS += ['m.sphinx']
    M_SPHINX_INVENTORIES = [...]

`Links to external Sphinx documentation`_
=========================================

Use the :rst:`:ref:` interpreted text role for linking to symbols defined in
:py:`M_SPHINX_INVENTORIES`. In order to save you some typing, the leading
name(s) mentioned there can be omitted when linking to given symbol.

Link text is equal to link target unless the target provides its own title
(such as documentation pages), function links have ``()`` appended to make it
clear it's a function. It's possible to specify custom link title using the
:rst:`:ref:`link title <link-target>``` syntax. If a symbol can't be found, a
warning is printed to output and link target is rendered in a monospace font
(or, if custom link title is specified, just the title is rendered, as normal
text). You can append ``#anchor`` to ``link-target`` to link to anchors that
are not present in the inventory file, the same works for query parameters
starting with ``?``. Adding custom CSS classes can be done by deriving the role
and adding the :rst:`:class:` option.

Since there's many possible targets and there can be conflicting names,
sometimes it's desirable to disambiguate. If you suffix the link target with
``()``, the plugin will restrict the name search to just functions. You can
also restrict the search to a particular type by prefixing the target with a
concrete target name and a colon --- for example,
:rst:`:ref:`std:doc:using/cmdline`` will link to the ``using/cmdline`` page of
standard documentation.

The :rst:`:ref:` a good candidate for a `default role <http://docutils.sourceforge.net/docs/ref/rst/directives.html#default-role>`_
--- setting it using :rst:`.. default-role::` will then make it accessible
using plain backticks:

.. code-figure::

    .. code:: rst

        .. default-role:: ref

        .. role:: ref-flat(ref)
            :class: m-flat

        -   Function link: :ref:`open()`
        -   Class link (with the ``xml.`` prefix omitted): :ref:`etree.ElementTree`
        -   Page link: :ref:`std:doc:using/cmdline`
        -   :ref:`Custom link title <PyErr_SetString>`
        -   Flat link: :ref-flat:`os.path.join()`
        -   Link using a default role: `str.partition()`

    .. default-role:: ref

    .. role:: ref-flat(ref)
        :class: m-flat

    -   Function link: :ref:`open()`
    -   Class link (with the ``xml.`` prefix omitted): :ref:`etree.ElementTree`
    -   Page link: :ref:`std:doc:using/cmdline`
    -   :ref:`Custom link title <PyErr_SetString>`
    -   Flat link: :ref-flat:`os.path.join()`
    -   Link using a default role: `str.partition()`

.. note-success::

    For linking to Doxygen documentation, a similar functionality is provided
    by the `m.dox <{filename}/plugins/links.rst#doxygen-documentation>`_
    plugin.

`Module, class, enum, function, property and data docs`_
========================================================

In the Python doc theme, the :rst:`.. py:module::`, :rst:`.. py:class::`,
:rst:`.. py:enum::`, :rst:`.. py:function::`, :rst:`.. py:property::` and
:rst:`.. py:data::` directives provide a way to supply module, class, enum,
function / method, property and data documentation content.

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
