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

Theme
#####

:breadcrumb: {filename}/pelican.rst Pelican
:footer:
    .. note-dim::
        :class: m-text-center

        `« Writing content <{filename}/pelican/writing-content.rst>`_ | `Pelican <{filename}/pelican.rst>`_

.. role:: rst(code)
    :language: rst

The second largest offering of m.css is a full-featured theme for the
`Pelican static site generator <https://getpelican.com/>`_. The theme is
designed to fit both the use case of a simple blog consisting of just articles
or a full product/project/portfolio website where the blog is only a side dish.

.. contents::
    :class: m-block m-default

`Quick start`_
==============

Following the `Pelican quick start guide <{filename}/pelican.rst#quick-start>`_,
it's assumed you already have at least Python 3.4 and the Python 3 version of
Pelican installed. The easiest way to start is putting the
:gh:`whole Git repository <mosra/m.css>` of m.css into your project, for
example as a submodule:

.. code:: sh

    git submodule add git://github.com/mosra/m.css

The most minimal configuration to use the theme is the following. Basically you
need to tell Pelican where the theme resides (it's in the ``pelican-theme/``
subdir of your m.css submodule), then you tell it to put the static contents of
the theme into a ``static/`` directory in the root of your webserver; the
:py:`M_CSS_FILES` variable is a list of CSS files that the theme needs. You can
put there any files you need, but there need to be at least the files mentioned
on the `CSS themes <{filename}/css/themes.rst>`_ page. The :py:`M_THEME_COLOR`
specifies color used for the :html:`<meta name="theme-color" />` tag
corresponding to given theme; if not set, it's simply not present. Lastly, the
theme uses some Jinja2 filters from the `m.htmlsanity <{filename}/plugins/htmlsanity.rst>`_
plugin, so that plugin needs to be loaded as well.

.. code:: py

    THEME = 'm.css/pelican-theme'
    THEME_STATIC_DIR = 'static'
    DIRECT_TEMPLATES = ['index']

    M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
                   '/static/m-dark.css']
    M_THEME_COLOR = '#22272e'

    PLUGIN_PATHS = ['m.css/pelican-plugins']
    PLUGINS = ['m.htmlsanity']

Here you can take advantage of the ``pelicanconf.py`` and ``publishconf.py``
distinction --- use ``m-dark.css`` for local development and override the
:py:`M_CSS_FILES` to use the smaller, faster and more compatible ``m-dark.compiled.css``
for publishing.

If you would want to use the light theme instead, the configuration is this
(again with ``m-light.css`` possibly replaced with ``m-light.compiled.css``):

.. code:: py

    M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700,700i%7CSource+Code+Pro:400,400i,600',
                   '/static/m-light.css']
    M_THEME_COLOR = '#cb4b16'

.. note-info::

    To reduce confusion, new configuration variables specific to m.css theme
    and plugins are prefixed with ``M_``. Configuration variables without
    prefix are builtin Pelican options.

`Configuration`_
================

Value of :py:`SITENAME` is used in the :html:`<title>` tag, separated with a
``|`` character from page title. If page title is the same as :py:`SITENAME`
(for example on the index page), only the page title is shown. The static part
of the website with pages is treated differently from the "blog" part with
articles and there are two additional configuration options :py:`M_BLOG_URL` and
:py:`M_BLOG_NAME` that control how various parts of the theme link to the blog
and how blog pages are named in the :html:`<title>` element. The :py:`M_BLOG_URL`
can be either absolute or relative to :py:`SITEURL`. If :py:`M_BLOG_NAME` /
:py:`M_BLOG_URL` are not set, the theme assumes they are the same as
:py:`SITENAME` / :py:`SITEURL`.

.. code:: py

    SITENAME = 'Your Brand'
    SITEURL = ''

    M_BLOG_NAME = 'Your Brand Blog'
    M_BLOG_URL = 'blog/'

`Top navbar`_
-------------

:py:`M_SITE_LOGO` is an image file that will be used as a brand logo on left
side of the navbar, :py:`M_SITE_LOGO_TEXT` is brand logo text. Specifying just
one of these does the expected thing, if neither of them is specified, the
theme will use :py:`SITENAME` in place of :py:`M_SITE_LOGO_TEXT`. The brand
logo/text is a link that leads to :py:`SITTEURL`.

:py:`M_LINKS_NAVBAR1` and :py:`M_LINKS_NAVBAR2` variables contain links to put
in the top navbar. On narrow screens, the navbar is divided into two columns,
links from the first variable are in the left column while links from the
second variable are in the right column. Omit the second variable if you want
the links to be in a single column. Omitting both variables will cause the
hamburger menu link on small screen sizes to not even be present.

Both variables have the same format --- a list of 4-tuples, where first item is
link title, second the URL, third page slug of the corresponding page (used
to highlight currently active menu item) and fourth is a list of sub-menu items
(which are 3-tuples --- link title, URL and page slug). Providing an empty slug
will make the menu item never highlighted; providing an empty list of sub-menu
items will not add any submenu. All blog-related pages (articles, article
listing, authors, tags, categories etc.) have the slug set to a special value
``[blog]``. The URL is prepended with :py:`SITEURL` unless it contains also
domain name, then it's left as-is (`detailed behavior <{filename}/plugins/htmlsanity.rst#siteurl-formatting>`_).

Example configuration, matching example markup from the
`CSS page layout <{filename}/css/page-layout.rst#sub-menus-in-the-navbar>`__
documentation:

.. code:: py

    M_SITE_LOGO_TEXT = 'Your Brand'

    M_LINKS_NAVBAR1 = [('Features', 'features/', 'features', []),
                       ('Showcase', 'showcase/', 'showcase', []),
                       ('Download', 'download/', 'download', [])]

    M_LINKS_NAVBAR2 = [('Blog', 'blog/', '[blog]', [
                            ('News', 'blog/news/', ''),
                            ('Archive', 'blog/archive/', '')]),
                       ('Contact', 'contact/', 'contact', [])]

`Footer navigation`_
--------------------

Similarly to the top navbar, :py:`M_LINKS_FOOTER1`, :py:`M_LINKS_FOOTER2`,
:py:`M_LINKS_FOOTER3` and :py:`M_LINKS_FOOTER4` variables contain links to put
in the footer navigation. The links are arranged in four columns, which get
reduced to just two columns on small screens. Omitting :py:`M_LINKS_FOOTER4`
will fill the last column with a *Blog* entry, linking to the Archives page and
listing all blog categories; you can disable that entry by setting
:py:`M_LINKS_FOOTER4 = []`. Omitting any of the remaining variables will make
given column empty, omitting all variables will not render the navigation at
all.

The variables are lists of 2-tuples, containing link title and URL. First item
is used for column header, if link URL of the first item is empty, given column
header is just a plain :html:`<h3>` without a link. The URLs are processed in
the same way as in the `top navbar`_. A tuple entry with empty title (i.e.,
:py:`('', '')`) will put a spacer into the list.

Footer fine print can be specified via :py:`M_FINE_PRINT`. Contents of the
variable are processed as :abbr:`reST <reStructuredText>`, so you can use all
the formatting and linking capabilities in there. If :py:`M_FINE_PRINT` is not
specified, the theme will use the following instead. Set
:py:`M_FINE_PRINT = None` to disable rendering of the fine print completely.

.. code:: py

    M_FINE_PRINT = SITENAME + """. Powered by `Pelican <https://getpelican.com>`_
        and `m.css <http://mcss.mosra.cz>`_."""

If :py:`M_FINE_PRINT` is set to :py:`None` and none of :py:`M_LINKS_FOOTER1`,
:py:`M_LINKS_FOOTER2`, :py:`M_LINKS_FOOTER3`, :py:`M_LINKS_FOOTER4` is set, the
footer is not rendered at all.

Example configuration, again matching example markup from the
`CSS page layout <{filename}/css/page-layout.rst#footer-navigation>`__
documentation, populating the last column implicitly:

.. code:: py

    M_LINKS_FOOTER1 = [('Your Brand', '/'),
                       ('Features', 'features/'),
                       ('Showcase', 'showcase/')]

    M_LINKS_FOOTER2 = [('Download', 'download/'),
                       ('Packages', 'download/packages/'),
                       ('Source', 'download/source/')]

    M_LINKS_FOOTER3 = [('Contact', ''),
                       ('E-mail', 'mailto:you@your.brand'),
                       ('GitHub', 'https://github.com/your-brand')]

    M_FINE_PRINT = """
    Your Brand. Copyright © `You <mailto:you@your.brand>`_, 2017. All rights
    reserved.
    """

`Pages`_
========

Page content is simply put into :html:`<main>`, wrapped in an :html:`<article>`,
in the center 10 columns on large screens and spanning the full 12 columns
elsewhere; the container is marked as `inflatable <{filename}/css/grid.rst#inflatable-nested-grid>`_.
Page title is rendered in an :html:`<h1>` and there's nothing else apart from
the page content.

Pages can override which menu item in the `top navbar`_ will be highlighted
by specifying the corresponding menu item slug in the :rst:`:highlight:` field.
If the field is not present, page's own slug is used instead.

`Extra CSS`_
------------

The :rst:`:css:` field can be used to link additional CSS files in page header.
Put one URL per line, internal link targets are expanded. Example:

.. code:: rst

    Showcase
    ########

    :css:
        {filename}/static/webgl.css
        {filename}/static/canvas-controls.css

`Breadcrumb navigation`_
------------------------

It's common for pages to be organized in a hierarchy and the user should be
aware of it. m.css Pelican theme provides breadcrumb navigation, which is
rendered in main page heading (as described in the
`CSS page layout <{filename}/css/page-layout.rst#breadcrumb-navigation>`__
documentation) and also in page title. Breadcrumb links are taken from the
:rst:`:breadcrumb:` field, where every line is one level of hierarchy,
consisting of an internal target link (which gets properly expanded) and title
separated by whitespace.

Example usage:

.. code:: rst

    Steam engine
    ############

    :breadcrumb: {filename}/help.rst Help
                 {filename}/help/components.rst Components

.. note-info::

    You can see the breadcrumb in action on the top and bottom of this
    documentation page (and others).

`Landing pages`_
----------------

It's possible to override the default 10-column behavior for pages to make a
`landing page <{filename}/css/page-layout.rst#landing-pages>`__ with large
cover image spanning the whole window width. Put cover image URL into a
:rst:`:cover:` field, the :rst:`:landing:` field then contains
:abbr:`reST <reStructuredText>`-processed content that appears on top of the
cover image. Contents of the :rst:`:landing:` are put into a
:html:`<div class="m-container">`, you are expected to fully take care of rows
and columns in it. The :rst:`:hide_navbar_brand:` field controls visibility of
the navbar brand link. Set it to :py:`True` to hide it, default (if not
present) is :py:`False`.

.. block-warning:: Configuration

    Currently, in order to have the :rst:`:landing:` field properly parsed, you
    need to explicitly list it in :py:`FORMATTED_FIELDS`. Don't forget that
    :py:`'summary'` is already listed there.

    .. code:: py

        FORMATTED_FIELDS += ['landing']

Example of a fully custom index page that overrides the default theme index
page (which would just list all the articles) is below. Note the overriden save
destination and URL.

.. code:: rst

    Your Brand
    ##########

    :save_as: index.html
    :url:
    :cover: {filename}/static/cover.jpg
    :hide_navbar_brand: True
    :landing:
        .. container:: m-row

            .. container:: m-col-m-6 m-push-m-5

                .. raw:: html

                    <h1>Your Brand</h1>

                *This is the brand you need.*

.. block-warning:: Landing page title

    To give you full control over the landing page appearance, the page title
    is not rendered in :html:`<h1>` on top of the content as with usual pages.
    Instead you are expected to provide a heading inside the :rst:`:landing:`
    field. However, due to semantic restrictions of :abbr:`reST <reStructuredText>`,
    it's not possible to use section headers inside the :rst:`:landing:` field
    and you have to work around it using raw HTML blocks, as shown in the above
    example.

.. note-info::

    You can see the landing page in action on the `main project page <{filename}/index.rst>`_.

`Page header and footer`_
-------------------------

It's possible to add extra :abbr:`reST <reStructuredText>`-processed content
(such as page-specific navigation) before and after the page contents by
putting it into :rst:`:header:` / :rst:`:footer:` fields. Compared to having
these directly in page content, these will be put semantically outside the page
:html:`<article>` element (so even before the :html:`<h1>` heading and after
the last :html:`<section>` ends). The header / footer is put, equivalently to
page content, in the center 10 columns on large screens and spanning the full
12 columns elsewhere; the container is marked as `inflatable`_. Example of a
page-specific footer navigation, extending the breadcrumb navigation from
above:

.. code:: rst

    Steam engine
    ############

    :breadcrumb: {filename}/help.rst Help
                 {filename}/help/components.rst Components
    :footer:
        `« Water tank <{filename}/help/components/water-tank.rst>`_ |
        `Components <{filename}/help/components.rst>`_ |
        `Chimney » <{filename}/help/components/chimney.rst>`_

.. block-warning:: Configuration

    Similarly to landing page content, in order to have the :rst:`:header:` /
    :rst:`:footer:` fields properly parsed, you need to explicitly list them in
    :py:`FORMATTED_FIELDS`. Don't forget that :py:`'summary'` is already listed
    there.

    .. code:: py

        FORMATTED_FIELDS += ['header', 'footer']

.. note-warning::

    The :rst:`:header:` field is not supported on `landing pages`_. In case
    both :rst:`:landing:` and :rst:`:header:` is present, :rst:`:header:` is
    ignored.

`(Social) meta tags for pages`_
-------------------------------

You can use :rst:`:description:` field to populate :html:`<meta name="description">`,
which can be then shown in search engine results. Other than that, the field
does not appear anywhere on the rendered page. It's recommended to add it to
:py:`FORMATTED_FIELDS` so you can make use of the
`advanced typography features <{filename}/plugins/htmlsanity.rst#typography>`_
like smart quotes etc. in it:

.. code:: py

    FORMATTED_FIELDS += ['description']

For sharing pages on Twitter, Facebook and elsewhere, both `Open Graph <http://ogp.me/>`_
and `Twitter Card <https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary-card-with-large-image>`_
:html:`<meta>` tags are supported:

-   Page title is mapped to ``og:title`` / ``twitter:title``
-   Page URL is mapped to ``og:url``
-   The :rst:`:summary:` field is mapped to ``og:description`` /
    ``twitter:description``. Note that if the page doesn't have explicit
    summary, Pelican takes it from the first few sentences of the content and
    that may not be what you want. This is also different from the
    :rst:`:description:` field mentioned above and, unlike with articles,
    :rst:`:summary:` doesn't appear anywhere on the rendered page.
-   The :rst:`:cover:` field (e.g. the one used on `landing pages <#landing-pages>`_),
    if present, is mapped to ``og:image`` / ``twitter:image``. The exact same
    file is used without any resizing or cropping and is assumed to be in
    landscape.
-   ``twitter:card`` is set to ``summary_large_image`` if :rst:`:cover:` is
    present and to ``summary`` otherwise
-   ``og:type`` is set to ``page``

Example overriding the index page with essential properties for nice-looking
social links:

.. code:: rst

    Your Brand
    ##########

    :save_as: index.html
    :url:
    :cover: {filename}/static/cover.jpg
    :summary: This is the brand you need.

.. note-success::

    You can see how page links will display by pasting
    URL of the `index page <{filename}/index.rst>`_ into either
    `Facebook Debugger <https://developers.facebook.com/tools/debug/>`_ or
    `Twitter Card Validator <https://cards-dev.twitter.com/validator>`_.

`Articles`_
===========

Compared to pages, articles have additional metadata like :rst:`:date:`,
:rst:`:author:`, :rst:`:category:` and :rst:`tags` that order them and divide
them into various sections. Besides that, there's article :rst:`:summary:`,
that, unlike with pages, is displayed in the article header; other metadata are
displayed in article footer. The article can also optionally have a
:rst:`:modified:` date, which is shown as date of last update in the footer.

All article listing pages (archives, categories, tags, authors) are displaying
just the article summary and the full article content is available only on the
dedicated article page. An exception to this is the main index or archive page,
where the first article is fully expanded so the users are greeted with some
actual content instead of just a boring list of article summaries.

Article pages show a list of sections and tags in a right sidebar. By default,
list of authors is not displayed as there is usually just one author. If you
want to display the authors as well, enable it using the :py:`M_SHOW_AUTHOR_LIST`
option in the configuration:

.. code:: py

    M_SHOW_AUTHOR_LIST = True

`Jumbo articles`_
-----------------

`Jumbo articles <{filename}/css/page-layout.rst#jumbo-articles>`__ are made
by including the :rst:`:cover:` field containing URL of the cover image.
Besides that, if the title contains an em-dash (---), it gets split into a
title and subtitle that's then rendered in a different font size. Example:

.. code:: rst

    An article --- a jumbo one
    ##########################

    :cover: {filename}/static/ship.jpg
    :summary: Article summary paragraph.

    Article contents.

Sidebar with tag, category and author list shown in the classic article layout
on the right is moved to the bottom for jumbo articles. In case you need to
invert text color on cover, add a :rst:`:class:` field containing the
``m-inverted`` CSS class.

.. note-info::

    You can compare how an article with nearly the same contents looks as
    `a normal article <{filename}/examples/article.rst>`_ and a
    `jumbo article <{filename}/examples/jumbo-article.rst>`_.

`(Social) meta tags for articles`_
----------------------------------

Like with pages, you can use :rst:`:description:` field to populate
:html:`<meta name="description">`, which can be then shown in search engine
results. Other than that, the field doesn't appear anywhere in the rendered
article. `Open Graph`_ and `Twitter Card`_ :html:`<meta>` tags are also
supported in a similar way:

-   Article title is mapped to ``og:title`` / ``twitter:title``
-   Article URL is mapped to ``og:url``
-   The :rst:`:summary:` field is mapped to ``og:description`` /
    ``twitter:description``. Note that if the article doesn't have explicit
    summary, Pelican takes it from the first few sentences of the content and
    that may not be what you want. This is also different from the
    :rst:`:description:` field mentioned above.
-   The :rst:`:cover:` field from `jumbo articles <#jumbo-articles>`_, if
    present, is mapped to ``og:image`` / ``twitter:image``. The exact same
    file is used without any resizing or cropping and is assumed to be in
    landscape.
-   ``twitter:card`` is set to ``summary_large_image`` if :rst:`:cover:` is
    present and to ``summary`` otherwise
-   ``og:type`` is set to ``article``

.. note-success::

    You can see how article links will display by pasting
    URL of e.g. the `jumbo article`_ into either `Facebook Debugger`_ or
    `Twitter Card Validator`_.

`Controlling article appearance`_
---------------------------------

By default, the theme assumes that you provide an explicit :rst:`:summary:`
field for each article. The summary is then displayed on article listing page
and also prepended to fully expanded article. If your :rst:`:summary:` is
automatically generated by Pelican or for any other reason repeats article
content, it might not be desirable to show it in combination with article
content. This can be configured via the following setting:

.. code:: py

    M_HIDE_ARTICLE_SUMMARY = True

There's also a possibility to control this on a per-article basis by setting
:rst:`:hide_summary:` to either :py:`True` or :py:`False`. If both global and
per-article setting is present, article-specific setting has a precedence.
Example:

.. code:: rst

    An article without explicit summary
    ###################################

    :cover: {filename}/static/ship.jpg
    :hide_summary: True

    Implicit article summary paragraph.

    Article contents.

.. note-info::

    Here's the visual appearance of an `article without explicit summary <{filename}/examples/article-hide-summary.rst>`_
    and a corresponding `jumbo article <{filename}/examples/jumbo-article-hide-summary.rst>`__.

As noted above, the first article is by default fully expanded on index and
archive page. However, sometimes the article is maybe too long to be expanded
or you might want to not expand any article at all. This can be controlled
either globally using the following setting:

.. code:: py

    M_COLLAPSE_FIRST_ARTICLE = True

Or, again, on a per-article basis, by setting :rst:`:collapse_first:` to either
:py:`True` or :py:`False`. If both global and per-article setting is present,
article-specific setting has a precedence.

`Pre-defined pages`_
====================

With the default configuration above the index page is just a list of articles
with the first being expanded; the archives page is basically the same. If you
want to have a custom index page (for example a `landing page <#landing-pages>`_),
remove :py:`'index'` from the :py:`DIRECT_TEMPLATES` setting and keep just
:py:`'archives'` for the blog front page. Also you may want to enable
pagination for the archives, as that's not enabled by default:

.. code:: py

    # Defaults to ['index', 'categories', 'authors', 'archives']
    DIRECT_TEMPLATES = ['archives']

    # Defaults to ['index']
    PAGINATED_DIRECT_TEMPLATES = ['archives']

.. note-warning::

    The m.css Pelican theme doesn't provide per-year, per-month or per-day
    archive pages or category, tag, author *list* pages at the moment ---
    that's why the above :py:`DIRECT_TEMPLATES` setting omits them. List of
    categories and tags is available in a sidebar from any article or article
    listing page.

Every category, tag and author has its own page that lists corresponding
articles in a way similar to the index or archives page, but without the first
article expanded. On the top of the page there is a note stating what condition
the articles are filtered with.

.. note-info::

    See how an example `category page looks <{category}Examples>`_.

Index, archive and all category/tag/author pages are paginated based on the
:py:`DEFAULT_PAGINATION` setting --- on the bottom of each page there are link
to prev and next page, besides that there's :html:`<link rel="prev">` and
:html:`<link rel="next">` that provides the same as a hint to search engines.

`Theme properties`_
===================

The theme markup is designed to have readable, nicely indented output. The code
is valid HTML5 and should be parsable as XML.

.. note-danger::

    This is one of the main goals of this project. Please
    :gh:`report a bug <mosra/m.css/issues/new>` if it's not like that.
