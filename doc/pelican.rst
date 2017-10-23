..
    This file is part of m.css.

    Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>

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

Pelican
#######

.. role:: sh(code)
    :language: sh

`Pelican <https://getpelican.com/>`_ is a static site generator powered by
Python and unlike most other static site generators, it uses
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ instead of
Markdown for authoring content. ``m.css`` provides a theme for it, together
with a set of useful plugins.

.. note-warning::

    Please, in this case, don't judge the book by its cover --- the
    :abbr:`reST <reStructuredText>` website might look like it was made in 1992
    and never updated since, but believe me, it's a remarkably designed format.
    Once you dive into it, you will not want to go back to Markdown.

`Quick start`_
==============

Install Pelican either via ``pip`` or using your system package manager. Note
that in order to use ``m.css`` `plugins <{filename}/plugins.rst>`_ later, you
may want to install the Python 3 version.

.. code:: sh

    # You may need sudo here
    pip install pelican

Once you have Pelican installed, create a directory for your website and
bootstrap it:

.. code:: sh

    mkdir ~/my-cool-site/
    cd ~/my-cool-site/
    pelican-quickstart

This command will ask you a few questions. You don't need the URL prefix for
now, but you definitely want a Makefile and an auto-reload script to be
generated. Leave the rest at its defaults. Once the quickstart script finishes,
you can run the auto-reloading like this:

.. todo: remove the auto-reload script when Pelican has it builtin

.. code:: sh

    make devserver

It will print quite some output about processing things and serving the data to
the console. Open your fresh website at http://localhost:8000. The site is now
empty, so let's create a simple article and put it into ``content/``
subdirectory with a ``.rst`` extension. For this example that would be
``~/my-cool-site/content/my-cool-article.rst``:

.. code:: rst

    My cool article
    ###############

    :date: 2017-09-14 23:04
    :category: Cool things
    :tags: cool, article, mine
    :summary: This article has a cool summary.

    This article has not only cool summary, but also has cool contents. Lorem?
    *Ipsum.* `Hi, google! <http://google.com>`_

If you did everything right, the auto-reload script should pick the file up and
process it (check the console output). Then it's just a matter of refreshing
your browser to see it on the page.

.. note-info::

    Currently, if Pelican encounters an error when processing the article, it
    will just stop refreshing and you need to restart it by executing
    :sh:`make devserver` again.

*That's it!* Congratulations, you successfully made your first steps with
Pelican. The default theme might be a bit underwhelming, so let's fix that.
Click on the headers below to get to know more.

`Writing content » <{filename}/pelican/writing-content.rst>`_
=============================================================

Quick guide and tips for writing content using :abbr:`reST <reStructuredText>`.
Chances are that you already know your way around from Sphinx or other
documentation tools, nevertheless there are some hidden tricks that you might
not know about yet.

`Theme » <{filename}/pelican/theme.rst>`_
=========================================

A feature-packed theme with modern and responsive design that exposes all of
``m.css`` functionality with goodies on top such as social meta tags,
breadcrumb navigation and more.
