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
package to your :py:`PLUGINS` in ``pelicanconf.py``. The
:py:`M_SPHINX_INVENTORIES` option is described in the
`Links to external Sphinx documentation`_ section below.

.. code:: python

    PLUGINS += ['m.sphinx']
    M_SPHINX_INVENTORIES = [...]

`Python doc theme`_
-------------------

List the plugin in your :py:`PLUGINS`. The :py:`M_SPHINX_INVENTORIES`
configuration option is described in the `Links to external Sphinx documentation`_
section below, additionally it supports also the inverse --- saving internal
symbols to a file to be linked from elsewhere, see
`Creating an Intersphinx inventory file`_ for a description of the
:py:`M_SPHINX_INVENTORY_OUTPUT` option.

.. code:: py

    PLUGINS += ['m.sphinx']
    M_SPHINX_INVENTORIES = [...]
    M_SPHINX_INVENTORY_OUTPUT = 'objects.inv'

`Links to external Sphinx documentation`_
=========================================

Sphinx provides a so-called Intersphinx files to make names from one
documentation available for linking from elsewhere. The plugin supports the
(current) version 2 of those inventory files, version 1 is not supported. You
need to provide a list of tuples containing tag file path, URL prefix, an
optional list of implicitly prepended paths and an optional list of CSS classes
for each link in :py:`M_SPHINX_INVENTORIES`. Every Sphinx-generated
documentation contains an ``objects.inv`` file in its root directory (and the
root directory is the URL prefix as well), for example for Python 3 it's
located at https://docs.python.org/3/objects.inv. Download the files and
specify path to them and the URL they were downloaded from, for example:

.. code:: py

    M_SPHINX_INVENTORIES = [
        ('sphinx/python.inv', 'https://docs.python.org/3/', ['xml.']),
        ('sphinx/numpy.inv', 'https://docs.scipy.org/doc/numpy/', [], ['m-flat'])]

Use the :rst:`:ref:` interpreted text role for linking to those symbols. Link
text is equal to link target unless the target provides its own title (such as
documentation pages), function links have ``()`` appended to make it clear it's
a function. It's possible to specify custom link title using the :rst:`:ref:`
link title <link-target>``` syntax. If a symbol can't be found, a warning is
printed to output and link target is rendered in a monospace font (or, if
custom link title is specified, just the title is rendered, as normal text).
You can append ``#anchor`` to ``link-target`` to link to anchors that are not
present in the inventory file, the same works for query parameters starting
with ``?``. Adding custom CSS classes can be done by deriving the role and
adding the :rst:`:class:` option.

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

When used with the Python doc theme, the :rst:`:ref` can be used also for
linking to internal types, while external types, classes and enums are also
linked to from all signatures.

.. note-success::

    For linking to Doxygen documentation, a similar functionality is provided
    by the `m.dox <{filename}/plugins/links.rst#doxygen-documentation>`_
    plugin.

`Creating an Intersphinx inventory file`_
=========================================

In the Python doc theme, the :py:`M_SPHINX_INVENTORY_OUTPUT` option can be used
to produce an Intersphinx inventory file --- basically an inverse of
:py:`M_SPHINX_INVENTORIES`. Set it to a filename and the plugin will fill it
with all names present in the documentation. Commonly, Sphinx projects expect
this file to be named ``objects.inv`` and located in the documentation root, so
doing the following will ensure it can be easily used:

.. code:: py

    M_SPHINX_INVENTORY_OUTPUT = 'objects.inv'

.. block-info:: Inventory file format

    The format is unfortunately not well-documented in Sphinx itself and this
    plugin additionally makes some extensions to it, so the following is a
    description of the file structure as used by m.css. File header is a few
    textual lines as shown below, while everything after is zlib-compressed.
    The plugin creates the inventory file in the (current) version 2 and at the
    moment hardcodes project name to ``X`` and version to ``0``::

        # Sphinx inventory version 2
        # Project: X
        # Version: 0
        # The remainder of this file is compressed using zlib.

    When decompressing the rest, the contents are again textual, each line
    being one entry::

        mymodule.MyClass py:class 2 mymodule.MyClass.html -
        mymodule.foo py:function 2 mymodule.html#foo -
        my-page std:doc 2 my-page.html A documentation page

    .. class:: m-table

    =========== ===============================================================
    Field       Description
    =========== ===============================================================
    name        Name of the module, class, function, page... Basically the link
                target used by :rst:`:ref:`.
    type        Type. Files created by the ``m.sphinx`` plugins always use only
                the following types; Sphinx-created files may have arbitrary
                other types such as ``c:function``. This type is what can be
                used in :rst:`:ref:` to further disambiguate the target.

                -   ``py:module`` for modules
                -   ``py:class`` for classes
                -   ``py:function`` :label-warning:`m.css-specific` for
                    functions, but currently also methods, class methods and
                    static methods. Sphinx uses ``py:classmethod``,
                    ``py:staticmethod`` and ``py:method`` instead.
                -   ``py:attribute`` for properties
                -   ``py:enum`` :label-warning:`m.css-specific` for enums.
                    Sphinx treats those the same as ``py:class``.
                -   ``py:enumvalue`` :label-warning:`m.css-specific` for enum
                    values. Sphinx treats those the same as ``py:data``.
                -   ``py:data`` for data
                -   ``std:doc`` for pages
    ``2``       A `mysterious number <https://github.com/dahlia/sphinx-fakeinv/blob/02589f374471fa47073ab6cbac38258c3060a988/sphinx_fakeinv.py#L92-L93>`_.
                `Sphinx implementation <https://github.com/sphinx-doc/sphinx/blob/a498960de9039b0d0c8d24f75f32fa4acd5b75e1/sphinx/util/inventory.py#L129>`_
                denotes this as ``prio`` but doesn't use it in any way.
    url         Full url of the page. There's a minor space-saving
                optimization --- if the URL ends with ``$``, it should be
                composed as :py:`location = location[:-1] + name`. The plugin
                can recognize this feature but doesn't make use of it when
                writing the file.
    title       Link title. If set to ``-``, :py:`name` should be used as a
                link title instead.
    =========== ===============================================================

    For debugging purposes, the ``sphinx.py`` plugin script can decode and
    print inventory files passed to it on the command line. See ``--help`` for
    more options.

    .. code:: shell-session

        $ ./m/sphinx.py python.inv
        # Sphinx inventory version 2
        # Project: Python
        # Version: 3.7
        # The remainder of this file is compressed using zlib.
        CO_FUTURE_DIVISION c:var 1 c-api/veryhigh.html#c.$ -
        PYMEM_DOMAIN_MEM c:var 1 c-api/memory.html#c.$ -
        PYMEM_DOMAIN_OBJ c:var 1 c-api/memory.html#c.$ -
        ...


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
