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

Links
#####

:breadcrumb: {filename}/plugins.rst Pelican plugins
:footer:
    .. note-dim::
        :class: m-text-center

        `« Math and code <{filename}/plugins/math-and-code.rst>`_ | `Pelican plugins <{filename}/plugins.rst>`_

.. role:: py(code)
    :language: py
.. role:: rst(code)
    :language: rst

m.css plugins make linking to external content almost too easy. If your website
is about coding, chances are quite high that you will be linking to
repositories, documentation or bugtrackers. Manually copy-pasting links from
the browser gets quite annoying after a while and also doesn't really help with
keeping the reST sources readable.

Because not everybody needs to link to all services provided here, the
functionality is separated into a bunch of separate plugins, each having its
own requirements.

.. contents::
    :class: m-block m-default

`GitHub`_
=========

Download the `m/gh.py <{filename}/plugins.rst>`_ file, put it
including the ``m/`` directory into one of your :py:`PLUGIN_PATHS` and add
:py:`m.gh` package to your :py:`PLUGINS` in ``pelicanconf.py``:

.. code:: python

    PLUGINS += ['m.gh']

Use the :rst:`:gh:` interpreted text role for linking. The plugin mimics how
`GitHub Flavored Markdown <https://help.github.com/articles/autolinked-references-and-urls/>`_
parses inter-site links, with some extensions on top. In addition to well-known
references to commits and issues/PRs via ``@`` and ``#``, ``$`` is for linking
to a tree (or file in given tree) and ``^`` is for linking to a tag/release. If
your link target doesn't contain any of these characters and contains more than
one slash, the target is simply prepended with ``https://github.com/``.

Link text is equal to link target for repository, commit and issue/PR links,
otherwise the full expanded URL is used. Similarly to builtin linking
functionality, if you want a custom text for a link, use the
:rst:`:gh:`link text <link-target>`` syntax.

.. code-figure::

    .. code:: rst

        -   Profile link: :gh:`mosra`
        -   Repository link: :gh:`mosra/m.css`
        -   Commit link: :gh:`mosra/m.css@4d362223f107cffd8731a0ea031f9353a0a2c7c4`
        -   Issue/PR link: :gh:`mosra/magnum#123`
        -   Tree link: :gh:`mosra/m.css$next`
        -   Tag link: :gh:`mosra/magnum^snapshot-2015-05`
        -   File link: :gh:`mosra/m.css$master/css/m-dark.css`
        -   Arbitrary link: :gh:`mosra/magnum/graphs/contributors`
        -   :gh:`Link with custom title <getpelican/pelican>`

    -   Profile link: :gh:`mosra`
    -   Repository link: :gh:`mosra/m.css`
    -   Commit link: :gh:`mosra/m.css@4d362223f107cffd8731a0ea031f9353a0a2c7c4`
    -   Issue/PR link: :gh:`mosra/magnum#123`
    -   Tree link: :gh:`mosra/m.css$next`
    -   Tag link: :gh:`mosra/magnum^snapshot-2015-05`
    -   File link: :gh:`mosra/m.css$master/css/m-dark.css`
    -   Arbitrary link: :gh:`mosra/magnum/graphs/contributors`
    -   :gh:`Link with custom title <getpelican/pelican>`

`OpenGL functions and extensions`_
==================================

Download the `m/gl.py <{filename}/plugins.rst>`_ file, put it
including the ``m/`` directory into one of your :py:`PLUGIN_PATHS` and add
:py:`m.gl` package to your :py:`PLUGINS` in ``pelicanconf.py``:

.. code:: python

    PLUGINS += ['m.gl']

Use the :rst:`:glfn:` interpreted text role for linking to functions,
:rst:`:glext:` for linking to OpenGL / OpenGL ES extensions, :rst:`:webglext:`
for linking to WebGL extensions and :rst:`:glfnext:` for linking to extension
functions. In the link target the leading ``gl`` prefix of functions and the
leading ``GL_`` prefix of extensions is prepended automatically.

Link text is equal to full function name including the ``gl`` prefix and
``()`` for functions, equal to extension name or equal to extension function
link, including the vendor suffix. For :rst:`:glfn:`, :rst:`:glext:` and
:rst:`:webglext:` it's possible to specify alternate link text using the
well-known syntax.

.. code-figure::

    .. code:: rst

        -   Function link: :glfn:`DispatchCompute`
        -   Extension link: :glext:`ARB_direct_state_access`
        -   WebGL extension link: :webglext:`OES_texture_float`
        -   Extension function link: :glfnext:`SpecializeShader <ARB_gl_spirv>`
        -   :glfn:`Custom link title <DrawElementsIndirect>`

    -   Function link: :glfn:`DispatchCompute`
    -   Extension link: :glext:`ARB_direct_state_access`
    -   WebGL extension link: :webglext:`OES_texture_float`
    -   Extension function link: :glfnext:`SpecializeShader <ARB_gl_spirv>`
    -   :glfn:`Custom link title <DrawElementsIndirect>`

`Doxygen documentation`_
========================

Download the `m/dox.py <{filename}/plugins.rst>`_ file, put it
including the ``m/`` directory into one of your :py:`PLUGIN_PATHS` and add
:py:`m.dox` package to your plugins in ``pelicanconf.py``. The plugin uses
Doxygen tag files to get a list of linkable symbols and you need to provide
list of 3-tuples containing tag file path, URL prefix and list of implicitly
prepended namespaces in :py:`M_DOX_TAGFILES` configuration to make the plugin
work. Example configuration:

.. code:: python

    PLUGINS += ['m.dox']
    M_DOX_TAGFILES = [
        ('doxygen/corrade.tag', 'http://doc.magnum.graphics/corrade/', ['Corrade::']),
        ('doxygen/magnum.tag', 'http://doc.magnum.graphics/magnum/', ['Magnum::'])]

Use the :rst:`:dox:` interpreted text role for linking to documented symbols.
All link targets understood by Doxygen's ``@ref`` or ``@link`` commands are
understood by this plugin as well, in addition it's possible to link to the
documentation index page by specifying the tag file basename w/o extension as
link target. In order to save you some typing, the leading namespace(s)
mentioned in the :py:`M_DOX_TAGFILES` setting can be omitted when linking to
given symbol.

Link text is equal to link target in all cases except for pages and sections,
where page/section title is extracted from the tagfile. It's possible to
specify custom link title using the :rst:`:dox:`link title <link-target>``
syntax. If a symbol can't be found, a warning is printed to output and link
target is rendered in monospace font (or, if custom link title is specified,
just the title is rendered, as normal text). You can append ``#anchor`` to
``link-target`` to link to anchors that are not present in the tag file (such
as ``#details`` for the detailed docs or ``#pub-methods`` for jumping straight
to a list of public member functions), the same works for query parameters
starting with ``?``.

.. code-figure::

    .. code:: rst

        -   Function link: :dox:`Utility::Directory::mkpath()`
        -   Class link: :dox:`Interconnect::Emitter`
        -   Page link: :dox:`building-corrade`
        -   :dox:`Custom link title <testsuite>`
        -   :dox:`Link to documentation index page <corrade>`
        -   :dox:`Link to an anchor <Interconnect::Emitter#pub-methods>`

    -   Function link: :dox:`Utility::Directory::mkpath()`
    -   Class link: :dox:`Interconnect::Emitter`
    -   Page link: :dox:`building-corrade`
    -   :dox:`Custom link title <testsuite>`
    -   :dox:`Link to documentation index page <corrade>`
    -   :dox:`Link to an anchor <Interconnect::Emitter#pub-methods>`

.. note-success::

    If you haven't noticed yet, m.css also provides a
    `full-featured Doxygen theme <{filename}/doxygen.rst>`_ with first-class
    search functionality. Check it out!

`Abbreviations`_
================

While not exactly a link but rather a way to produce correct :html:`<abbr>`
elements, it belongs here as it shares a similar syntax.

Download the `m/abbr.py <{filename}/plugins.rst>`_ file, put it
including the ``m/`` directory into one of your :py:`PLUGIN_PATHS` and add
:py:`m.abbr` package to your :py:`PLUGINS` in ``pelicanconf.py``. This plugin
assumes presence of `m.htmlsanity <{filename}/plugins/htmlsanity.rst>`_.

.. code:: python

    PLUGINS += ['m.htmlsanity', 'm.abbr']

The plugin overrides the builtin Pelican
`abbr interpreted text role <http://docs.getpelican.com/en/stable/content.html#file-metadata>`_
and makes its syntax consistent with other common roles of :abbr:`reST <reStructuredText>`
and m.css.

Use the :rst:`:abbr:` interpreted text role for creating abbreviations with
title in angle brackets:

.. code-figure::

    .. code:: rst

        :abbr:`HTML <HyperText Markup Language>` and :abbr:`CSS <Cascading Style Sheets>`
        are *all you need* for producing rich content-oriented websites.

    :abbr:`HTML <HyperText Markup Language>` and :abbr:`CSS <Cascading Style Sheets>`
    are *all you need* for producing rich content-oriented websites.

`File size queries`_
====================

Okay, this is not a link at all, but --- sometimes you might want to display
size of a file, for example to tell the users how big the download will be.

Download the `m/filesize.py <{filename}/plugins.rst>`_ file, put it
including the ``m/`` directory into one of your :py:`PLUGIN_PATHS` and add
:py:`m.filesize` package to your :py:`PLUGINS` in ``pelicanconf.py``.

.. code:: python

    PLUGINS += ['m.filesize']

Use the :rst:`filesize` interpreted text role to display the size of a file
including units. The :rst:`filesize-gz` role compresses the file using GZip
first before calculating the size.

.. code-figure::

    .. code:: rst

        The compiled ``m-dark.compiled.css`` CSS file has
        :filesize:`{filename}/../css/m-dark.compiled.css` but only
        :filesize-gz:`{filename}/../css/m-dark.compiled.css` when the server
        sends it compressed.

    The compiled ``m-dark.compiled.css`` CSS file has
    :filesize:`{filename}/../css/m-dark.compiled.css` but only
    :filesize-gz:`{filename}/../css/m-dark.compiled.css` when the server
    sends it compressed.
