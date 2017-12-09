import os

from test import MinimalTestCase, BaseTestCase

class Layout(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'SITENAME': 'Your Brand',
            'M_BLOG_NAME': 'Your Brand Blog',
            'M_SITE_LOGO_TEXT': 'Your.brand',
            'M_LINKS_NAVBAR1': [
                ('Features', 'features.html', 'features', []),
                ('Showcase', '#', 'showcase', [
                    ('Requirements', 'showcase-requirements.html', 'showcase-requirements'),
                    ('Live demo', 'http://demo.your.brand/', ''),
                    ('Get a quote', 'mailto:you@your.brand', '')]),
                ('Download', '#', 'download', [])],
            'M_LINKS_NAVBAR2': [('Blog', 'archives.html', '[blog]', [
                    ('News', '#', ''),
                    ('Archive', '#', ''),
                    ('Write a guest post', 'guest-post-howto.html', 'guest-post-howto')]),
                ('Contact', '#', 'contact', [])],
            'M_LINKS_FOOTER1': [('Your Brand', 'index.html'),
                   ('Mission', '#'),
                   ('', ''),
                   ('The People', '#')],
            'M_LINKS_FOOTER2':[('Features', 'features.html'),
                   ('', ''),
                   ('Live demo', 'http://demo.your.brand/'),
                   ('Requirements', 'showcase-requirements.html')],
            'M_LINKS_FOOTER3': [('Download', ''),
                   ('Packages', '#'),
                   ('', ''),
                   ('Source', '#')],
            'M_LINKS_FOOTER4':[('Contact', ''),
                   ('E-mail', 'mailto:you@your.brand'),
                   ('', ''),
                   ('GitHub', 'https://github.com/your-brand')],
            # multiline to test indentation
            'M_FINE_PRINT': """
Your Brand. Copyright © `You <mailto:you@your.brand>`_, 2017.
All rights reserved.
""",
            'PAGE_PATHS': ['.'],
            'PAGE_SAVE_AS': '{slug}.html',
            'PAGE_URL': '{slug}.html',
            'ARTICLE_PATHS': ['articles'] # doesn't exist
        })

        # - page title is M_BLOG_NAME for index, as it is a blog page
        # - the Blog entry should be highlighted
        # - mailto and external URL links should not have SITEURL prepended in
        #   both top navbar and bottom navigation
        # - footer spacers should put &nbsp; there
        # - again, the archives page and index page should be exactly the same
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertEqual(*self.actual_expected_contents('archives.html', 'index.html'))

        # - page title is SITENAME, as these are pages
        # - corresponding items in top navbar should be highlighted
        self.assertEqual(*self.actual_expected_contents('features.html'))
        self.assertEqual(*self.actual_expected_contents('showcase-requirements.html'))
        self.assertEqual(*self.actual_expected_contents('guest-post-howto.html'))

class Minimal(MinimalTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'minimal', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # This is the minimal that's required. Not even the M_THEME_COLOR
            # is required.
            'THEME': '.',
            'PLUGIN_PATHS': ['../pelican-plugins'],
            'PLUGINS': ['m.htmlsanity'],
            'THEME_STATIC_DIR': 'static',
            'M_CSS_FILES': ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i',
               'static/m-dark.css'],
            'M_THEME_COLOR': '#22272e'})

        # The archives and index page should be exactly the same
        self.assertEqual(*self.actual_expected_contents('index.html'))
        self.assertEqual(*self.actual_expected_contents('archives.html', 'index.html'))

        # Verify that we're *really* using the default setup and not disabling
        # any pages -- but don't verify the page content, as these are not
        # supported anyway
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/authors.html')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/categories.html')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/tags.html')))

        # The CSS files should be copied along
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/static/m-grid.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/static/m-components.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/static/m-dark.css')))
        self.assertTrue(os.path.exists(os.path.join(self.path, 'output/static/pygments-dark.css')))

class OneColumnNavbar(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'one_column_navbar', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'M_LINKS_NAVBAR1': [
                ('Features', '#', 'features', []),
                ('A long item caption that really should not wrap on small screen', '#', '', []),
                ('Blog', 'archives.html', '[blog]', [])]
        })

        # The navbar should be full 12 columns
        self.assertEqual(*self.actual_expected_contents('index.html'))

class NoFooter(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'no_footer', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'M_FINE_PRINT': None
        })

        # There should be no footer at all
        self.assertEqual(*self.actual_expected_contents('index.html'))

class DisableFinePrint(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'disable_fine_print', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'M_LINKS_FOOTER1': [('Your Brand', 'index.html')],
            'M_FINE_PRINT': None
        })

        # There should be footer with just the first and last column and no
        # fine print
        self.assertEqual(*self.actual_expected_contents('index.html'))

class DisableBlogLinks(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'disable_blog_links', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'M_LINKS_FOOTER1': [('Your Brand', 'index.html')],
            'M_LINKS_FOOTER4': None,
        })

        # There should be just the first column
        self.assertEqual(*self.actual_expected_contents('index.html'))
