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

Doxygen theme
#############

.. role:: cpp(code)
    :language: cpp
.. role:: html(code)
    :language: html
.. role:: ini(code)
    :language: ini
.. role:: jinja(code)
    :language: jinja
.. role:: py(code)
    :language: py
.. role:: sh(code)
    :language: sh

A drop-in replacement for the stock `Doxygen <http://www.doxygen.org>`_ HTML
output, generated from Doxygen-produced XML files. Generated filenames and URLs
are fully compatible with the stock output to avoid broken links once you
switch.

.. contents::
    :class: m-block m-default

`Basic usage`_
==============

Everything you need is a Python script and a bunch of template files. You can
get that by cloning :gh:`the m.css GitHub repository <mosra/m.css$master/doxygen>`
and looking into the ``doxygen/`` directory:

.. code:: sh

    git clone git://github.com/mosra/m.css
    cd m.css/doxygen

The script requires Python 3.6, depends on `Jinja2 <http://jinja.pocoo.org/>`_
for templating and `Pygments <http://pygments.org/>`_ for code block
highlighting. You can install the dependencies via ``pip`` or your distribution
package manager:

.. code:: sh

    pip install jinja2 Pygments

If your documentation includes math formulas, in addition you need some LaTeX
distribution installed. Use your distribution package manager, for example on
Ubuntu:

.. code:: sh

    sudo apt-get install texlive-base texlive-latex-extra texlive-fonts-extra

.. note-success::

    This tool makes use of the ``latex2svg.py`` utility from :gh:`tuxu/latex2svg`,
    © 2017 `Tino Wagner <http://www.tinowagner.com/>`_, licensed under
    :gh:`MIT <tuxu/latex2svg$master/LICENSE.md>`.

Now, in order to preserve your original Doxygen configuration, create a new
``Doxyfile-mcss`` file next to your original ``Doxyfile`` and put the following
inside:

.. code:: ini

    @INCLUDE               = Doxyfile
    GENERATE_HTML          = NO
    GENERATE_XML           = YES
    XML_PROGRAMLISTING     = NO

This will derive the configuration from the original ``Doxyfile``, disables
builtin Doxygen HTML output and enables XML output instead, with some unneeded
features disabled for faster processing. Now run ``dox2html5.py`` and point it
to your ``Doxyfile-mcss``:

.. code:: sh

    ./dox2html5.py path/to/your/Doxyfile-mcss

It will run ``doxygen`` to generate the XML output, processes it and generates
the HTML output in the configured output directory. After the script is done,
just open generated ``index.html`` to see the result.

`Features`_
===========

-   Modern, valid, mobile-friendly HTML5 markup without table layouts
-   Minimalistic design without unnecessary chrome and UI elements
-   URLs fully compatible with stock Doxygen HTML output to preserve existing
    links
-   Focused on presenting the actual written documentation while reducing
    questionable auto-generated content
-   Math rendered as `embedded SVG <{filename}/css/components.rst#math>`_
    instead of raster images / MathJax
-   Uses Pygments for better code highlighting

`Important differences to stock HTML output`_
---------------------------------------------

-   Detailed description is put first and foremost on a page, *before* the
    member listing
-   Table of contents is generated for compound references as well, containing
    all sections of detailed description together with anchors to member
    listings.
-   Private members and anonymous namespaces are always ignored, however
    private virtual functions are listed in case they are documented
    (`why? <http://www.gotw.ca/publications/mill18.htm>`_)
-   Inner classes are listed in the public/protected type sections instead of
    being listed in a separate section ignoring their public/private status
-   Class references contain also their template specification on the linked
    page
-   Function signatures don't contain :cpp:`constexpr` and :cpp:`noexcept`
    anymore. These keywords are instead added as flags to the function
    description together with :cpp:`virtual`\ ness and :cpp:`explicit`\ ity. On
    the other hand, important properties like :cpp:`static`, :cpp:`const` and
    r-value overloads *are* part of function signature.
-   For better visual alignment, function listing is done using the C++11
    trailing return type (:cpp:`auto` in front) and typedef listing is done
    with :cpp:`using`). However, the detailed documentation is kept in the
    original form.
-   Function and macro parameters and enum values are vertically aligned in
    the member listing for better readability.
-   Default class template parameters are not needlessly repeated in each
    member detailed docs

`Intentionally unsupported features`_
-------------------------------------

.. note-danger:: Warning: opinions

    This list presents my opinions. Not everybody likes my opinions.

Features that I don't see a point in because they just artifically inflate the
amount of generated content for no added value.

-   Class hierarchy graphs are ignored (it only inflates the documentation with
    little added value)
-   Alphabetical list of symbols and alphabetical list of all members of a
    class is not created (the API *should be* organized in a way that makes
    this unnecessary)
-   Verbatim listing of parsed headers, "Includes" and "Included By" lists are
    not present (use your IDE or GitHub instead)
-   Undocumented or private members and content of anonymous namespaces are
    ignored (if things are undocumented or intentionally hidden, why put them
    in the documentation)
-   Brief description for enum values is ignored (only the detailed description
    is used, as the brief description was never used anywhere else than next to
    the detailed description)
-   Initializers of defines and variables are unconditionally ignored (look in
    the sources, if you *really* need that)
-   No section with list of examples or linking from function/class
    documentation to related example code (he example code should be
    accompanied with corresponding tutorial page instead)
-   :cpp:`inline` functions are not marked as such (I see it as an unimportant
    implementation detail)

`Not yet implemented features`_
-------------------------------

-   Code search. I want to provide something that's actually usable to replace
    the terribly slow stock client-side search, but I'm not there yet.
-   Clickable symbols in code snippets. Doxygen has quite a lot of false
    positives while a lot of symbols stay unmatched. I need to find a way
    around that.

`Configuration`_
================

The script takes most of the configuration from the ``Doxyfile`` itself,
(ab)using the following builtin options:

.. class:: m-table m-fullwidth

=============================== ===============================================
Variable                        Description
=============================== ===============================================
:ini:`@INCLUDE`                 Includes in ``Doxyfile``\ s are supported
:ini:`PROJECT_NAME`             Rendered in top navbar, footer fine print and
                                page title
:ini:`PROJECT_BRIEF`            If set, appended in a thinner font to
                                :ini:`PROJECT_NAME`
:ini:`OUTPUT_DIRECTORY`         Used to discover where Doxygen generates the
                                files
:ini:`XML_OUTPUT`               Used to discover where Doxygen puts the
                                generated XML
:ini:`HTML_OUTPUT`              The output will be written here
:ini:`TAGFILES`                 Used to discover what base URL to prepend to
                                external references
:ini:`HTML_EXTRA_STYLESHEET`    List of CSS files to include. Relative paths
                                are also searched relative to the
                                ``dox2html5.py`` script. See below for more
                                information.
:ini:`HTML_EXTRA_FILES`         List of extra files to copy (for example
                                additional CSS files that are :css:`@import`\ ed
                                from the primary one). Relative paths are also
                                searched relative to the ``dox2html5.py``
                                script.
=============================== ===============================================

In addition, the m.css Doxygen theme recognizes the following extra options:

.. class:: m-table m-fullwidth

=================================== =======================================
Variable                            Description
=================================== =======================================
:ini:`M_THEME_COLOR`                Color for :html:`<meta name="theme-color"/>`,
                                    corresponding to the CSS style. See below
                                    for more information.
:ini:`M_PAGE_HEADER`                HTML code to put at the top of every page.
                                    Useful for example to link to different
                                    versions of the same documentation. The
                                    ``{filename}`` placeholder is replaced with
                                    current file name.
:ini:`M_CLASS_TREE_EXPAND_LEVELS`   How many levels of the class tree to
                                    expand. ``0`` means only the top-level
                                    symbols are shown. If not set, ``1`` is
                                    used.
:ini:`M_FILE_TREE_EXPAND_LEVELS`    How many levels of the file tree to expand.
                                    ``0`` means only the top-level dirs/files
                                    are shown. If not set, ``1`` is used.
:ini:`M_EXPAND_INNER_TYPES`         Whether to expand inner types (e.g. a class
                                    inside a class) in the symbol tree. If not
                                    set, ``0`` is used.
=================================== =======================================

Note that namespace, directory and page lists are always fully expanded as
these are not expected to be excessively large.

By default, the `dark m.css theme <{filename}/css/themes.rst#dark>`_ together
with Doxygen-theme-specific additions is used, which corresponds to the
following configuration:

.. code:: ini

    HTML_EXTRA_STYLESHEET = \
        https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600 \
        ../css/m-dark+doxygen.compiled.css
    M_THEME_COLOR = #22272e

If you have a site already using the ``m-dark.compiled.css`` file, there's
another file called ``m-dark.doxygen.compiled.css``, which contains just the
Doxygen-theme-specific additions so you can reuse the already cached
``m-dark.compiled.css`` file from your main site:

.. code:: ini

    HTML_EXTRA_STYLESHEET = \
        https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600 \
        ../css/m-dark.compiled.css \
        ../css/m-dark.doxygen.compiled.css
    M_THEME_COLOR = #22272e

If you prefer the `light m.css theme <{filename}/css/themes.rst#light>`_
instead, use the following configuration (and, similarly, you can use
``m-light.compiled.css`` together with ``m-light.doxygen.compiled-css`` in
place of ``m-light+doxygen.compiled.css``:

.. code:: ini

    HTML_EXTRA_STYLESHEET = \
        https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700,700i%7CSource+Code+Pro:400,400i,600 \
        ../css/m-light+doxygen.compiled.css
    M_THEME_COLOR = #cb4b16

See the `CSS files`_ section below for more information about customizing the
CSS files.

`Command-line options`_
=======================

.. code:: shell-session

    ./dox2html5.py [-h] [--templates TEMPLATES] [--wildcard WILDCARD]
                   [--index-pages INDEX_PAGES [INDEX_PAGES ...]]
                   [--no-doxygen] [--debug]
                   doxyfile

Arguments:

-   ``doxyfile`` --- where the Doxyfile is

Options:

-   ``-h``, ``--help`` --- show this help message and exit
-   ``--templates TEMPLATES`` --- template directory. Defaults to the
    ``templates/`` subdirectory if not set.
-   ``--wildcard WILDCARD`` --- only process files matching the wildcard.
    Useful for debugging to speed up / restrict the processing to a subset of
    files. Defaults to ``*.xml`` if not set.
-   ``--index-pages INDEX_PAGES [INDEX_PAGES ...]`` --- index page templates.
    By default, if not set, the index pages are matching stock Doxygen, i.e.
    ``annotated.html``, ``files.html``, ``namespaces.html`` and ``pages.html``.
    See `Navigation page templates`_ section below for more information.
-   ``--no-doxygen`` --- don't run Doxygen before. By default Doxygen is run
    before the script to refresh the generated XML output.
-   ``--debug`` --- verbose debug output. Useful for debugging.

`Content`_
==========

Brief and detailed description is parsed as-is with the following
modifications:

-   Function parameter documentation, return value documentation and template
    parameter documentation is extracted out of the text flow to allow for more
    flexible styling, it's also reordered to match parameter order and warnings
    are emitted if there are mismatches.
-   To make text content wrap better on narrow screens, :html:`<wbr/>` tags are
    added after ``::`` and ``_`` in long symbols in link titles and after ``/``
    in URLs.

Single-paragraph list items, function parameter description, table cell content
and return value documentation is stripped from the enclosing :html:`<p>` tag
to make the output more compact. If multiple paragraphs are present, nothing is
stripped. In case of lists, they are then rendered in an inflated form.
However, in order to achieve even spacing also with single-paragraph items,
it's needed use some explicit markup. Adding :html:`<p></p>` to a
single-paragraph item will make sure the enclosing :html:`<p>` is not stripped.

.. code-figure::

    .. code:: c++

        /**
        -   A list

            of multiple

            paragraphs.

        -   Another item

            <p></p>

            -   A sub list

                Another paragraph
        */

    .. raw:: html

        <ul>
          <li>
            <p>A list</p>
            <p>of multiple</p>
            <p>paragraphs.</p>
          </li>
          <li>
            <p>Another item</p>
            <ul>
              <li>
                <p>A sub list</p>
                <p>Another paragraph</p>
              </li>
            </ul>
          </li>
        </ul>

`Images and figures`_
---------------------

To match the stock HTML output, images that are marked with ``html`` target are
used. If image name is present, the image is rendered as a figure with caption.

.. block-warning:: Doxygen patches

    Current stable release of Doxygen has broken copying of images for the XML
    output. You need to apply :gh:`doxygen/doxygen#629` in order to fix that.

`Pages, sections and table of contents`_
----------------------------------------

Table of contents is unconditionally generated for all compound documentation
pages and includes both ``@section`` blocks in the detailed documentation as
well as the reference sections. If your documentation is using Markdown-style
headers (prefixed with ``##``, for example), the script is not able to generate
TOC entries for these. Upon encountering them, tt will warn and suggest to use
the ``@section`` command instead.

Table of contents for pages is generated only if they specify
``@tableofcontents`` in their documentation block.

.. block-warning:: Doxygen patches

    Note that recognition of the ``@tableofcontents`` command requires Doxygen
    with :gh:`doxygen/doxygen#625` applied. Brief description of pages is
    ignored and not extracted to the page index unless Doxygen has
    :gh:`doxygen/doxygen#624` applied.

`C++ support`_
--------------

.. block-warning:: Doxygen patches

    In order to properly detect template parameters for type aliases (the
    :cpp:`using` keyword), Doxygen with :gh:`doxygen/doxygen#626` applied is
    required. Rendering underlying enum types and enum strongness then requires
    :gh:`doxygen/doxygen#627`.

`Code highlighting`_
--------------------

Every code snippet should be annotated with language-specific extension like in
the example below. If not, the theme will assume C++ and emit a warning on
output. Language of snippets included via ``@include`` and related commands is
autodetected from filename.

.. code:: c++

    /**
    @code{.cpp}
    int main() { }
    @endcode
    */

Besides native Pygments mapping of file extensions to languages, there are the
following special cases:

.. class:: m-table m-fullwidth

=================== ===========================================================
Filename suffix     Detected language
=================== ===========================================================
``.h``              C++ (instead of C)
``.h.cmake``        C++ (instead of CMake), as this extension is often used for
                    C++ headers that are preprocessed with CMake
``.h.nostrip``      C++. Useful for embedding code snippets with Doxygen
                    comment block, as Doxygen would strip them with plain
                    ``.h``.
``.glsl``           GLSL. For some reason, stock Pygments detect only
                    ``.vert``, ``.frag`` and ``.geo`` extensions as GLSL.
``.conf``           INI (key-value configuration files)
``.ansi``           `Colored terminal output <{filename}/css/components.rst#colored-terminal-output>`_.
                    Use ``.shell-session`` pseudo-extension for simple
                    uncolored terminal output.
=================== ===========================================================

The theme has experimental support for inline code highlighting. Inline code is
distinguished from code blocks using the following rules:

-   Code that is delimited from surrounding paragraphs with an empty line is
    considered as block.
-   Code that is coming from ``@include``, ``@snippet`` and related commands
    that paste external file content is always considered as block.
-   Code that is coming from ``@code`` and is not alone in a paragraph is
    considered as inline.
-   For compatibility reasons, if code that is detected as inline consists of
    more than one line, it's rendered as code block and a warning is printed to
    output.

Inline highlighted code is written also using the ``@code`` command, but as
writing things like

.. code:: c++

    /** Returns @code{.cpp} Magnum::Vector2 @endcode, which is
        @code{.glsl} vec2 @endcode in GLSL. */

is too verbose, it's advised to configure some aliases in your ``Doxyfile-mcss``.
For example, you can configure an alias for general inline code snippets and
shorter versions for commonly used languages like C++ and CMake.

.. code:: ini

    ALIASES += \
        "cb{1}=@code{\1}" \
        "ce=@endcode" \
        "cpp=@code{.cpp}" \
        "cmake=@code{.cmake}"

With this in place the above could be then written simply as:

.. code:: c++

    /** Returns @cpp Magnum::Vector2 @ce, which is @cb{.glsl} vec2 @ce in GLSL. */

If you need to preserve compatibility with stock Doxygen HTML output (because
it renders all ``@code`` sections as blocks), use the following fallback
aliases in the original ``Doxyfile``:

.. code:: ini

    ALIASES += \
        "cb{1}=<tt>" \
        "ce=</tt>" \
        "cpp=<tt>" \
        "cmake=<tt>"

.. block-warning:: Doxygen limitations

    It's not possible to use inline code highlighting in ``@brief``
    description. Code placed there is moved by Doxygen to the detailed
    description.

    It's not possible to put a ``@code`` block (delimited by blank lines) to a
    Markdown list. A workaround is to use explicit HTML markup instead. See
    `Content`_ for more information about list behavior.

    .. code-figure::

        .. code:: c++

            /**
            <ul>
            <li>
                A paragraph.

                @code{.cpp}
                #include <os>
                @endcode
            </li>
            <li>
                Another paragraph.

                Yet another
            </li>
            </ul>
            */

        .. raw:: html

            <ul>
              <li>
                <p>A paragraph.</p>
                <pre class="m-code"><span class="cp">#include</span> <span class="cpf">&lt;os&gt;</span><span class="cp"></span></pre>
              </li>
              <li>
                <p>Another paragraph.</p>
                <p>Yet another</p>
              </li>
            </ul>

.. block-warning:: Doxygen patches

    Note that proper language detection for code snippets requires Doxygen with
    :gh:`doxygen/doxygen#621` applied, otherwise all snippets will fall back to
    C++ highlighting. Using ANSI color escape codes in terminal output require
    Doxygen with :gh:`doxygen/doxygen#623` applied, otherwise the codes will be
    present in the rendered output in their raw form.

`Customizing the template`_
===========================

The rest of the documentation explains how to customize the builtin template to
better suit your needs. Each documentation file is generated from one of the
template files that are bundled with the script. However, it's possible to
provide your own Jinja2 template files for customized experience as well as
modify the CSS styling.

`CSS files`_
------------

By default, compiled CSS files are used to reduce amount of HTTP requests and
bandwidth needed for viewing the documentation. However, for easier
customization and debugging it's better to use the unprocessed stylesheets. The
:ini:`HTML_EXTRA_STYLESHEET` lists all files that go to the :html:`<link rel="stylesheet" />`
in the resulting HTML markup, while :ini:`HTML_EXTRA_FILES` lists the
indirectly referenced files that need to be copied to the output as well. Below
is an example configuration corresponding to the dark theme:

.. code:: ini

    HTML_EXTRA_STYLESHEET = \
        https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600 \
        ../css/m-dark.css \
        ../css/m-doxygen.css
    HTML_EXTRA_FILES = \
        ../css/m-grid.css \
        ../css/m-components.css \
        ../css/pygments-dark.css \
        ../css/pygments-console.css
    M_THEME_COLOR = #22272e

After making desired changes to the source files, it's possible to postprocess
them back to the compiled version using the ``postprocess.py`` utility as
explained in the `CSS themes <{filename}/css/themes.rst#make-your-own>`_
documentation. In case of the dark theme, the ``m-dark+doxygen.compiled.css``
and ``m-dark.doxygen.compiled.css`` files are produced like this:

.. code:: sh

    cd css
    ./postprocess.py m-dark.css m-doxygen.css -o m-dark+doxygen.compiled.css
    ./postprocess.py m-dark.css m-doxygen.css --no-import -o m-dark.doxygen.compiled.css

`Compound documentation template`_
----------------------------------

For compound documentation one output HTML file corresponds to one input XML
file and there are some naming conventions imposed by Doxygen.

.. class:: m-table m-fullwidth

======================= =======================================================
Filename                Use
======================= =======================================================
``class.html``          Class documentation, read from ``class*.xml`` and saved
                        as ``class*.html``
``dir.html``            Directory documentation, read from ``dir_*.xml`` and
                        saved as ``dir_*.html``
``example.html``        Example code listing, read from ``*-example.xml`` and
                        saved as ``*-example.html``
``file.html``           File documentation, read from ``*.xml`` and saved as
                        ``*.html``
``namespace.html``      Namespace documentation, read fron ``namespace*.xml``
                        and saved as ``namespace*.html``
``page.html``           Page, read from ``*.xml``/``indexpage.xml`` and saved
                        as ``*.html``/``index.html``
``struct.html``         Struct documentation, read from ``struct*.xml`` and
                        saved as ``struct*.html``
``union.html``          Union documentation, read from ``union*.xml`` and saved
                        as ``union*.html``
======================= =======================================================

Each template is passed a subset of the ``Doxyfile`` configuration values from
the above table and in addition the following variables:

.. class:: m-table m-fullwidth

=========================== ===================================================
Variable                    Description
=========================== ===================================================
:py:`FILENAME`              Name of given output file
:py:`DOXYGEN_VERSION`       Version of Doxygen that generated given XML file
=========================== ===================================================

In addition to builtin Jinja2 filters, the the ``basename_or_url`` filter
returns either a basename of file path, if the path is relative; or a full URL,
if the argument is an absolute URL. It's useful in cases like this:

.. code:: html+jinja

  {% for css in HTML_EXTRA_STYLESHEET %}
  <link rel="stylesheet" href="{{ css|basename_or_url }}" />
  {% endfor %}

The actual page contents are provided in a :py:`compound` object, which has the
following properties. All exposed data are meant to be pasted directly to the
HTML code without any escaping.

.. class:: m-table m-fullwidth

======================================= =======================================
Property                                Description
======================================= =======================================
:py:`compound.kind`                     One of :py:`'class'`, :py:`'dir'`,
                                        :py:`'example'`, :py:`'file'`,
                                        :py:`'namespace'`, :py:`'page'`,
                                        :py:`'struct'`, :py:`'union'`, used to
                                        choose a template file from above
:py:`compound.id`                       Unique compound identifier, usually
                                        corresponding to output file name
:py:`compound.name`                     Compound name
:py:`compound.templates`                Template specification. Set only for
                                        classes. See `Template properties`_ for
                                        details.
:py:`compound.has_template_details`     If there is a detailed documentation
                                        of template parameters
:py:`compound.sections`                 Sections of detailed description. See
                                        `Section properties`_ for details.
:py:`compound.brief`                    Brief description. Can be empty. [1]_
:py:`compound.description`              Detailed description. Can be empty. [2]_
:py:`compound.dirs`                     List of directories in this compound.
                                        Set only for directories. See
                                        `Directory properties`_ for details.
:py:`compound.files`                    List of files in this compound. Set
                                        only for directories and files. See
                                        `File properties`_ for details.
:py:`compound.namespaces`               List of namespaces in this compound.
                                        Set only for files and namespaces. See
                                        `Namespace properties`_ for details.
:py:`compound.classes`                  List of classes in this compound. Set
                                        only for files and namespaces. See
                                        `Class properties`_ for details.
:py:`compound.enums`                    List of enums in this compound. Set
                                        only for files and namespaces. See
                                        `Enum properties`_ for details.
:py:`compound.typedefs`                 List of typedefs in this compound. Set
                                        only for files and namespaces. See
                                        `Typedef properties`_ for details.
:py:`compound.funcs`                    List of functions in this compound. Set
                                        only for files and namespaces. See
                                        `Function properties`_ for details.
:py:`compound.vars`                     List of variables in this compound. Set
                                        only for files and namespaces. See
                                        `Variable properties`_ for details.
:py:`compound.defines`                  List of defines in this compound. Set
                                        only for files. See `Define properties`_
                                        for details.
:py:`compound.public_types`             List of public types. Set only for
                                        classes. See `Type properties`_ for
                                        details.
:py:`compound.public_static_funcs`      List of public static functions. Set
                                        only for classes. See
                                        `Function properties`_ for details.
:py:`compound.public_funcs`             List of public functions. Set only for
                                        classes. See `Function properties`_ for
                                        details.
:py:`compound.public_static_vars`       List of public static variables. Set
                                        only for classes. See
                                        `Variable properties`_ for details.
:py:`compound.public_vars`              List of public variables. Set only for
                                        classes. See `Variable properties`_ for
                                        details.
:py:`compound.protected_types`          List of protected types. Set only for
                                        classes. See `Type properties`_ for
                                        details.
:py:`compound.protected_static_funcs`   List of protected static functions. Set
                                        only for classes. See
                                        `Function properties`_ for details.
:py:`compound.protected_funcs`          List of protected functions. Set only
                                        for classes. See `Function properties`_
                                        for details.
:py:`compound.protected_static_vars`    List of protected static variables. Set
                                        only for classes. See
                                        `Variable properties`_ for details.
:py:`compound.protected_vars`           List of protected variables. Set only
                                        for classes. See `Variable properties`_
                                        for details.
:py:`compound.private_funcs`            List of documented private virtual
                                        functions. Set only for classes. See
                                        `Function properties`_ for details.
:py:`compound.related`                  List of related non-member symbols. Set
                                        only for classes. See
                                        `Related properties`_ for details.
:py:`compound.groups`                   List of user-defined groups in this
                                        compound. See `Group properties`_ for
                                        details.
:py:`compound.has_enum_details`         If there is at least one enum with full
                                        description block [5]_
:py:`compound.has_typedef_details`      If there is at least one typedef with
                                        full description block [5]_
:py:`compound.has_func_details`         If there is at least one function with
                                        full description block [5]_
:py:`compound.has_var_details`          If there is at least one variable with
                                        full description block [5]_
:py:`compound.has_define_details`       If there is at least one define with
                                        full description block [5]_
:py:`compound.breadcrumb`               List of :py:`(title, URL)` tuples for
                                        breadcrumb navigation. Set only for
                                        classes, directories, files, namespaces
                                        and pages.
:py:`compound.prefix_wbr`               Fully-qualified symbol prefix for given
                                        compound with trailing ``::`` with
                                        :html:`<wbr/>` tag before every ``::``.
                                        Set only for classes, namespaces,
                                        structs and unions; on templated
                                        classes contains also the list of
                                        template parameter names.
:py:`compound.save_as`                  Filename including extension where the
                                        result will be saved
======================================= =======================================

`Section properties`_
`````````````````````

The :py:`compound.sections` property defines a Table of Contents for given
detailed description. It's a list of :py:`(id, title, children)` tuples, where
:py:`id` is the link anchor, :py:`title` is section title and :py:`children` is
a recursive list of nested sections. If the list is empty, given detailed
description either has no sections or the TOC was not explicitly requested via
``@tableofcontents`` in case of pages.

`Directory properties`_
```````````````````````

The :py:`compound.dirs` property contains a list of directories, where every
item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`dir.url`               URL of the file containing detailed directory docs
:py:`dir.name`              Directory name (just the leaf)
:py:`dir.brief`             Brief description. Can be empty. [1]_
=========================== ===================================================

`File properties`_
``````````````````

The :py:`compound.files` property contains a list of files, where every item
has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`file.url`              URL of the file containing detailed file docs
:py:`file.name`             File name (just the leaf)
:py:`file.brief`            Brief description. Can be empty. [1]_
=========================== ===================================================

`Namespace properties`_
```````````````````````

The :py:`compound.namespaces` property contains a list of namespaces, where
every item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`namespace.url`         URL of the file containing detailed namespace docs
:py:`namespace.name`        Namespace name. Fully qualified in case it's in a
                            file documentation, just the leaf name if in a
                            namespace documentation.
:py:`namespace.brief`       Brief description. Can be empty. [1]_
=========================== ===================================================

`Class properties`_
```````````````````

The :py:`compound.classes` property contains a list of classes, where every
item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`class_.kind`           One of :py:`'class'`, :py:`'struct'`, :py:`'union'`
:py:`class_.url`            URL of the file containing detailed class docs
:py:`class_.name`           Class name. Fully qualified in case it's in a file
                            documentation, just the leaf name if in a namespace
                            documentation.
:py:`class_.templates`      Template specification. See `Template properties`_
                            for details.
:py:`class_.brief`          Brief description. Can be empty. [1]_
=========================== ===================================================

`Enum properties`_
``````````````````

The :py:`compound.enums` property contains a list of enums, where every item
has the following properties:

.. class:: m-table m-fullwidth

=============================== ===============================================
Property                        Description
=============================== ===============================================
:py:`enum.id`                   Identifier hash [3]_
:py:`enum.type`                 Enum type or empty if implicitly typed [6]_
:py:`enum.is_strong`            If the enum is strong
:py:`enum.name`                 Enum name [4]_
:py:`enum.brief`                Brief description. Can be empty. [1]_
:py:`enum.description`          Detailed description. Can be empty. [2]_
:py:`enum.has_details`          If there is enough content for the full
                                description block [5]_
:py:`enum.is_protected`         If the enum is :cpp:`protected`. Set only for
                                member types.
:py:`enum.values`               List of enum values
:py:`enum.has_value_details`    If the enum values have description
=============================== ===============================================

Every item of :py:`enum.values` has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`value.id`              Identifier hash [3]_
:py:`value.name`            Value name [4]_
:py:`value.initializer`     Value initializer. Can be empty. [1]_
:py:`value.description`     Detailed description. Can be empty. [2]_
=========================== ===================================================

`Typedef properties`_
`````````````````````

The :py:`compound.typedefs` property contains a list of typedefs, where every
item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`typedef.id`            Identifier hash [3]_
:py:`typedef.is_using`      Whether it is a :cpp:`typedef` or an :cpp:`using`
:py:`typedef.type`          Typedef type, or what all goes before the name for
                            function pointer typedefs [6]_
:py:`typedef.args`          Typedef arguments, or what all goes after the name
                            for function pointer typedefs [6]_
:py:`typedef.name`          Typedef name [4]_
:py:`typedef.templates`     Template specification. Set only in case of
                            :cpp:`using`. . See `Template properties`_ for
                            details.
:py:`typedef.brief`         Brief description. Can be empty. [1]_
:py:`typedef.description`   Detailed description. Can be empty. [2]_
:py:`typedef.has_details`   If there is enough content for the full description
                            block [4]_
:py:`typedef.is_protected`  If the typedef is :cpp:`protected`. Set only for
                            member types.
=========================== ===================================================

`Function properties`_
``````````````````````

The :py:`commpound.funcs`, :py:`compound.public_static_funcs`,
:py:`compound.public_funcs`, :py:`compound.protected_static_funcs`,
:py:`compound.protected_funcs`, :py:`compound.private_funcs` and
:py:`compound.related_funcs` properties contain a list of functions, where
every item has the following properties:

.. class:: m-table m-fullwidth

=============================== ===============================================
Property                        Description
=============================== ===============================================
:py:`func.id`                   Identifier hash [3]_
:py:`func.type`                 Function return type [6]_
:py:`func.name`                 Function name [4]_
:py:`func.templates`            Template specification. See
                                `Template properties`_ for details.
:py:`func.has_template_details` If template parameters have description
:py:`func.params`               List of function parameters. See below for
                                details.
:py:`func.has_param_details`    If function parameters have description
:py:`func.return_value`         Return value description. Can be empty.
:py:`func.brief`                Brief description. Can be empty. [1]_
:py:`func.description`          Detailed description. Can be empty. [2]_
:py:`func.has_details`          If there is enough content for the full
                                description block [5]_
:py:`func.prefix`               Function signature prefix, containing keywords
                                such as :cpp:`static`. Information about
                                :cpp:`constexpr`\ ness, :cpp:`explicit`\ ness
                                and :cpp:`virtual`\ ity is removed from the
                                prefix and available via other properties.
:py:`func.suffix`               Function signature suffix, containing keywords
                                such as :cpp:`const` and r-value overloads.
                                Information about :cpp:`noexcept`, pure
                                :cpp:`virtual`\ ity and :cpp:`delete`\ d /
                                :cpp:`default`\ ed functions is removed from
                                the suffix and available via other properties.
:py:`func.is_protected`         If the function is :cpp:`protected`. Set only
                                for member functions.
:py:`func.is_private`           If the function is :cpp:`private`. Set only for
                                member functions.
:py:`func.is_explicit`          If the function is :cpp:`explicit`. Set only
                                for member functions.
:py:`func.is_virtual`           If the function is :cpp:`virtual`. Set only for
                                member functions.
:py:`func.is_pure_virtual`      If the function is pure :cpp:`virtual`. Set
                                only for member functions.
:py:`func.is_noexcept`          If the function is :cpp:`noexcept`
:py:`func.is_constexpr`         If the function is :cpp:`constexpr`
:py:`func.is_defaulted`         If the function is :cpp:`default`\ ed
:py:`func.is_deleted`           If the function is :cpp:`delete`\ d
=============================== ===============================================

The :py:`func.params` is a list of function parameters and their description.
Each item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`param.name`            Parameter name (if not anonymous)
:py:`param.type`            Parameter type, together with name and array
                            specification [6]_
:py:`param.default`         Default parameter value, if any [6]_
:py:`param.description`     Optional parameter description. If set,
                            :py:`func.has_param_details` is set as well.
:py:`param.direction`       Parameter direction. One of :py:`'in'`, :py:`'out'`,
                            :py:`'inout'` or :py:`''` if unspecified.
=========================== ===================================================

`Variable properties`_
``````````````````````

The :py:`compound.vars`, :py:`compound.public_vars` and
:py:`compound.protected_vars` properties contain a list of variables, where
every item has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`var.id`                Identifier hash [3]_
:py:`var.type`              Variable type [6]_
:py:`var.name`              Variable name [4]_
:py:`var.brief`             Brief description. Can be empty. [1]_
:py:`var.description`       Detailed description. Can be empty. [2]_
:py:`var.has_details`       If there is enough content for the full description
                            block [5]_
:py:`var.is_static`         If the variable is :cpp:`static`. Set only for
                            member variables.
:py:`var.is_protected`      If the variable is :cpp:`protected`. Set only for
                            member variables.
:py:`var.is_constexpr`      If the variable is :cpp:`constexpr`
=========================== ===================================================

`Define properties`_
````````````````````

The :py:`compound.defines` property contains a list of defines, where every
item has the following properties:

.. class:: m-table m-fullwidth

=============================== ===============================================
Property                        Description
=============================== ===============================================
:py:`define.id`                 Identifier hash [3]_
:py:`define.name`               Define name
:py:`define.params`             List of macro parameter names. See below for
                                details.
:py:`define.has_param_details`  If define parameters have description
:py:`define.return_value`       Return value description. Can be empty.
:py:`define.brief`              Brief description. Can be empty. [1]_
:py:`define.description`        Detailed description. Can be empty. [2]_
:py:`define.has_details`        If there is enough content for the full
                                description block [5]_
=============================== ===============================================

The :py:`define.params` is set to :py:`None` if the macro is just a variable.
If it's a function, each item is a tuple consisting of name and optional
description. If the description is set, :py:`define.has_param_details` is set
as well. You can use :jinja:`{% if define.params != None %}` to disambiguate
between preprocessor macros and variables in your code.

`Type properties`_
``````````````````

For classes, the :py:`compound.public_types` and :py:`compound.protected_types`
contains a list of :py:`(kind, type)` tuples, where ``kind`` is one of
:py:`'class'`, :py:`'enum'` or :py:`'typedef'` and ``type`` is a corresponding
type of object described above.

`Template properties`_
``````````````````````

The :py:`compound.templates`, :py:`typedef.templates` and :py:`func.templates`
properties contain either :py:`None` if given symbol is a full template
specialization or a list of template parameters, where every item has the
following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`template.type`         Template parameter type (:cpp:`class`,
                            :cpp:`typename` or a type)
:py:`template.name`         Template parameter name
:py:`template.default`      Template default value. Can be empty.
:py:`template.description`  Optional template description. If set,
                            :py:`i.has_template_details` is set as well.
=========================== ===================================================

You can use :jinja:`{% if i.templates != None %}` to test for the field
presence in your code.

`Related properties`_
`````````````````````

The :py:`compound.related` contains a list of related non-member symbols. Each
symbol is a tuple of :py:`(kind, member)`, where :py:`kind` is one of
:py:`'dir'`, :py:`'file'`, :py:`'namespace'`, :py:`'class'`, :py:`'enum'`,
:py:`'typedef'`, :py:`'func'`, :py:`'var'` or :py:`'define'` and :py:`member`
is a corresponding type of object described above.

`Group properties`_
```````````````````

The :py:`compound.groups` contains a list of user-defined groups. Each item has
the following properties:

======================= =======================================================
Property                Description
======================= =======================================================
:py:`group.id`          Group identifier [3]_
:py:`group.name`        Group name
:py:`group.description` Group description [2]_
:py:`group.members`     Group members. Each item is a tuple of
                        :py:`(kind, member)`, where :py:`kind` is one of
                        :py:`'namespace'`, :py:`'class'`, :py:`'enum'`,
                        :py:`'typedef'`, :py:`'func'`, :py:`'var'` or
                        :py:`'define'` and :py:`member` is a corresponding type
                        of object described above.
======================= =======================================================

.. [1] :py:`i.brief` is a single-line paragraph without the enclosing :html:`<p>`
    element, rendered as HTML. Can be empty in case of function overloads.
.. [2] :py:`i.description` is HTML code with the full description, containing
    paragraphs, notes, code blocks, images etc. Can be empty in case just the
    brief description is present.
.. [3] :py:`i.id` is a hash used to link to the member on the page, usually
    appearing after ``#`` in page URL
.. [4] :py:`i.name` is just the member name, not qualified. Prepend
    :py:`compound.prefix_wbr` to it to get the fully qualified name.
.. [5] :py:`compound.has_*_details` and :py:`i.has_details` are :py:`True` if
    there is detailed description, function/template/macro parameter
    documentation or enum value listing that makes it worth to render the full
    description block. If :py:`False`, the member should be included only in
    the brief listing on top of the page to avoid unnecessary repetition.
.. [6] :py:`i.type` and :py:`param.default` is rendered as HTML and usually
    contains links to related documentation

`Navigation page templates`_
----------------------------

By default the theme tries to match the original Doxygen listing pages. These
pages are generated from the ``index.xml`` file and their template name
corresponds to output file name.

.. class:: m-table m-fullwidth

======================= =======================================================
Filename                Use
======================= =======================================================
``annotated.html``      Class listing
``files.html``          File and directory listing
``namespaces.html``     Namespace listing
``pages.html``          Page listing
======================= =======================================================

By default it's those four pages, but you can configure any other pages via
the ``--index-pages`` option as mentioned in the `Command-line options`_
section.

Each template is passed a subset of the ``Doxyfile`` configuration values from
the above table and in addition the :py:`FILENAME` and :py:`DOXYGEN_VERSION`
variables as above. The navigation tree is provided in an :py:`index` object,
which has the following properties:

.. class:: m-table m-fullwidth

=========================== ===================================================
Property                    Description
=========================== ===================================================
:py:`index.symbols`         List of all namespaces + classes
:py:`index.files`           List of all dirs + files
:py:`index.pages`           List of all pages
=========================== ===================================================

The form of each list entry is the same:

.. class:: m-table m-fullwidth

=============================== ===============================================
Property                        Description
=============================== ===============================================
:py:`i.kind`                    Entry kind (one of :py:`'namespace'`,
                                :py:`'class'`, :py:`'struct'`, :py:`'union'`,
                                :py:`'dir'`, :py:`'file'`, :py:`'page'`)
:py:`i.name`                    Name
:py:`i.url`                     URL of the file with detailed documentation
:py:`i.brief`                   Brief documentation
:py:`i.has_nestable_children`   If the list has nestable children (i.e., dirs
                                or namespaces)
:py:`i.children`                Recursive list of child entries
=============================== ===============================================

Each list is ordered in a way that all namespaces are before all classes and
all directories are before all files.
