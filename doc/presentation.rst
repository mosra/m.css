Presentation framework
######################

Create modern-looking presentations to be viewed in a browser or printed to a
PDF directly from :abbr:`reST <reStructuredText>` sources, utilizing existing
m.css components for easy-to-author content and lightweight output.

.. button-success:: http://mcss.mosra.cz/presentation/example/

    Live demo

    a m.css showcase

.. contents::
    :class: m-block m-default

`Basic usage`_
==============

The presentation generator is a single script that makes use of many existing
m.css features, so the easiest way is to clone the whole repository:

.. code:: sh

    git clone git://github.com/mosra/m.css
    cd m.css/presentation

The script requires at least Python 3.4 and at minimal depends on
`Docutils <http://docutils.sourceforge.net/>`_ for :abbr:`reST <reStructuredText>`
parsing and `Jinja2 <http://jinja.pocoo.org/>`_ for templating. Further
dependencies might be required if you enable particular plugins, `more on that
below <#plugins>`_. You can install it via ``pip`` or your distribution package
manager:

.. code:: sh

    # You may need sudo here
    pip3 install docutils jinja2

.. note-danger::

    Similarly to the m.css `Pelican theme <{filename}/pelican/theme.rst>`_ and
    `plugins <{filename}/plugins.rst>`_, at least Python 3.4 is required; some
    plugins (such as the `math plugin <{filename}/plugins/math-and-code.rst#math>`_)
    may need even newer versions. Python 2 is not supported.

Now, with everything set up, let's write a minimal presentation and save it
with a ``.rst`` extension:

.. code:: rst

    My presentation
    ###############

    Welcome
    =======

    Agenda:

    1.  Show that simple things are simple
    2.  And advanced things are not hard either

    Is it that easy?
    ================

    Absolutely!

        It's really *that* easy.

        --- The presenter

    And that's it
    =============

    Thank you!

Now run the tool on your file and enable a server with auto-reload:

.. code:: shell-session

    $ ./present.py path/to/your/presentation.rst -rl
    INFO:root:serving on http://localhost:8000 with autoreload ...
    INFO:root:watching 1 paths

The script will generate the output to an ``output/`` subdirectory next to
your file and make it available at http://localhost:8000. When you open the URL
in a browser, you can navigate through the slides using arrow keys, touch swipe
or the on-screen controls.

If you change anything in the file, the output will get automatically
regenrated --- and any new files you reference, include or link to will get
added to the watch list as well for a consistent experience. Seeing the updated
presentation in your browser is then just one :label-default:`F5` away. If your
browser is modern enough, you can also try printing out the content to a PDF
for an even better reusability. See the
`docs about PDF printing <{filename}/css/presentation.rst#printing-to-a-pdf>`_
for more information.

`Writing content`_
==================

The presentation sources are written in reStructuredText. If you don't know it
already from other m.css features or e.g. Sphinx, here is a basic
`overview of the syntax <{filename}/pelican/writing-content.rst>`_. The guide
is written for the m.css Pelican theme, but most of it applies here as well.

.. TODO: metadata: cover, bundle
.. TODO: subtitles and section subtitles

`Slide customization`_
======================

.. TODO: describe all these:

.. code:: rst

    :cover: image.jpg
    :js:
        EmscriptenApplication.js
    :css:
        showcase.css
    :bundle:
        build-emscripten-wasm/Application.js
        build-emscripten-wasm/Application.wasm
    :after:
        .. raw:: html

`"Boot screen"`_
================

`Presenter mode and presenter notes`_
=====================================

.. code:: rst

    A presentation slide
    ====================

    -   Simple words
    -   for the audience

    .. presenter::

        Additional details that are worth mentioning for this slide.

`Configuration`_
================

`Command-line options`_
=======================
