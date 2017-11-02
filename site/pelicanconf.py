#
#   This file is part of m.css.
#
#   Copyright © 2017 Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

AUTHOR = 'Vladimír Vondruš'

SITE_LOGO_TEXT = 'm.css'

SITENAME = 'm.css'
SITEURL = ''

BLOGNAME = 'm.css example articles'
BLOGURL = 'examples/'

STATIC_URL = '{path}'

PATH = 'content'
ARTICLE_PATHS = ['examples']
PAGE_PATHS = ['']

TIMEZONE = 'Europe/Prague'

DEFAULT_LANG = 'en'
DATE_FORMATS = {'en': ('en_US', '%b %d %Y')}

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS_NAVBAR1 = [('Why?', 'why/', 'why', []),
                 ('CSS', 'css/', 'css', [
                    ('Grid system', 'css/grid/', 'css/grid'),
                    ('Typography', 'css/typography/', 'css/typography'),
                    ('Components', 'css/components/', 'css/components'),
                    ('Page layout', 'css/page-layout/', 'css/page-layout'),
                    ('Themes', 'css/themes/', 'css/themes')]),
                 ('Pelican', 'pelican/', 'pelican', [
                    ('Writing content', 'pelican/writing-content/', 'pelican/writing-content'),
                    ('Theme', 'pelican/theme/', 'pelican/theme')])]

LINKS_NAVBAR2 = [('Pelican plugins', 'plugins/', 'plugins', [
                    ('HTML sanity', 'plugins/htmlsanity/', 'plugins/htmlsanity'),
                    ('Components', 'plugins/components/', 'plugins/components'),
                    ('Images', 'plugins/images/', 'plugins/images'),
                    ('Math and code', 'plugins/math-and-code/', 'plugins/math-and-code'),
                    ('Links', 'plugins/links/', 'plugins/links')]),
                 ('GitHub', 'https://github.com/mosra/m.css', '', [])]

LINKS_FOOTER1 = [('m.css', '/'),
                 ('Why?', 'why/'),
                 ('GitHub', 'https://github.com/mosra/m.css'),
                 ('Gitter', 'https://gitter.im/mosra/m.css'),
                 ('E-mail', 'mailto:mosra@centrum.cz'),
                 ('Twitter', 'https://twitter.com/czmosra')]

LINKS_FOOTER2 = [('CSS', 'css/'),
                 ('Grid system', 'css/grid/'),
                 ('Typography', 'css/typography/'),
                 ('Components', 'css/components/'),
                 ('Page layout', 'css/page-layout/'),
                 ('Themes', 'css/themes/')]

LINKS_FOOTER3 = [('Pelican', 'pelican/'),
                 ('Writing content', 'pelican/writing-content/'),
                 ('Theme', 'pelican/theme/')]

LINKS_FOOTER4 = [('Pelican plugins', 'plugins/'),
                 ('HTML sanity', 'plugins/htmlsanity/'),
                 ('Components', 'plugins/components/'),
                 ('Images', 'plugins/images/'),
                 ('Math and code', 'plugins/math-and-code/'),
                 ('Links', 'plugins/links/')]

FINE_PRINT = """
m.css. Copyright © Vladimír Vondruš 2017. Site powered by `Pelican <https://getpelican.com>`_
and m.css (yes, I am eating my own dog food). Both the code and site content is
`available on GitHub under MIT <https://github.com/mosra/m.css>`_. Contact the
author via `e-mail <mosra@centrum.cz>`_, :abbr:`Jabber <mosra@jabbim.cz>`,
`Twitter <https://twitter.com/czmosra>`_ or smoke signals.
"""

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['static']

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['m.abbr',
           'm.code',
           'm.components',
           'm.dox',
           'm.filesize',
           'm.gl',
           'm.gh',
           'm.htmlsanity',
           'm.images',
           'm.math']

THEME = '../pelican-theme'
THEME_STATIC_DIR = 'static'
THEME_COLOR = '#22272e'
CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i&amp;subset=latin-ext',
             '/static/m-dark.css',
             #'/static/m-debug.css'
             ]
#CSS_FILES = ['https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700,700i%7CSource+Code+Pro:400,400i,600',
             #'/static/m-light.css']

FORMATTED_FIELDS = ['summary', 'landing', 'header', 'footer']

M_HTMLSANITY_SMART_QUOTES = True
M_HTMLSANITY_HYPHENATION = True
M_DOX_TAGFILES = [
    ('../doc/doxygen/corrade.tag', 'http://doc.magnum.graphics/corrade/', ['Corrade::'])]

DIRECT_TEMPLATES = []

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

AUTHORS_SAVE_AS = None # Not used
CATEGORIES_SAVE_AS = None # Not used
TAGS_SAVE_AS = None # Not used

SLUGIFY_SOURCE = 'basename'
PATH_METADATA = '(?P<slug>.+).rst'
