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

Pelican plugins
###############

.. role:: py(code)
    :language: py

The `Pelican theme <{filename}/pelican/theme.rst>`_ provided by m.css uses only
a part of the functionality on its own, the rest is exposed by various plugins.

`Usage`_
========

Each plugin is a standalone ``*.py`` file that is meant to be downloaded and
put into a ``m/`` subdirectory into one of your :py:`PLUGIN_PATHS`. Then you
add given :py:`m.something` package to your :py:`PLUGINS` in ``pelicanconf.py``
and restart Pelican. Download the plugins below or
:gh:`grab the whole Git repository <mosra/m.css>`:

-   :gh:`m.htmlsanity <mosra/m.css$master/pelican-plugins/m/htmlsanity.py>`
-   :gh:`m.components <mosra/m.css$master/pelican-plugins/m/components.py>`
-   :gh:`m.images <mosra/m.css$master/pelican-plugins/m/images.py>`
-   :gh:`m.math  <mosra/m.css$master/pelican-plugins/m/math.py>` (needs also :gh:`latex2svg <mosra/m.css$master/pelican-plugins/m/latex2svg.py>`),
    :gh:`m.code <mosra/m.css$master/pelican-plugins/m/code.py>`
-   :gh:`m.gh <mosra/m.css$master/pelican-plugins/m/gh.py>`,
    :gh:`m.dox <mosra/m.css$master/pelican-plugins/m/dox.py>`,
    :gh:`m.gl <mosra/m.css$master/pelican-plugins/m/gl.py>`,
    :gh:`m.abbr <mosra/m.css$master/pelican-plugins/m/abbr.py>`,
    :gh:`m.filesize <mosra/m.css$master/pelican-plugins/m/filesize.py>`

Click on the headings below to get to know more.

`HTML sanity » <{filename}/plugins/htmlsanity.rst>`_
====================================================

The :py:`m.htmlsanity` plugin is essential for m.css. It makes your markup
valid HTML5, offers a few opt-in typographical improvements and enables you to
make full use of features provided by other plugins.

`Components » <{filename}/plugins/components.rst>`_
===================================================

All `CSS components <{filename}/css/components.rst>`_ are exposed by the
:py:`m.components` plugin, so you can use them via :abbr:`reST <reStructuredText>`
directives without needing to touch HTML and CSS directly.

`Images » <{filename}/plugins/images.rst>`_
===========================================

Image-related CSS components are implemented by the :py:`m.images` plugin,
overriding builtin :abbr:`reST <reStructuredText>` functionality and providing
a convenient automatic way to arrange photos in an image grid.

`Math and code » <{filename}/plugins/math-and-code.rst>`_
=========================================================

The :py:`m.math` and :py:`m.code` plugins use external libraries for math
rendering and syntax highlighting, so they are provided as separate packages
that you can but don't have to use. With these, math and code snippets can be
entered directly in your :abbr:`reST <reStructuredText>` sources.

`Links » <{filename}/plugins/links.rst>`_
=========================================

The :py:`m.gh`, :py:`m.dox`, :py:`m.gl`, :py:`m.abbr` and :py:`m.fiilesize`
plugins make it easy for you to link to GitHub projects, issues or PRs, to
Doxygen documentation and do more useful things.
