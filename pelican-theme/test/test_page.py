import unittest

import pelican

from distutils.version import LooseVersion

from test import PageTestCase

class Page(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'FORMATTED_FIELDS': ['summary', 'description']
        })

        # The content and summary meta tag shouldn't be there at all
        self.assertEqual(*self.actual_expected_contents('page.html'))

class Minimal(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'minimal', *args, **kwargs)

    def test(self):
        self.run_pelican({})

        # The content and summary meta tag shouldn't be there at all
        self.assertEqual(*self.actual_expected_contents('page.html'))

class Breadcrumb(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'breadcrumb', *args, **kwargs)

    def test(self):
        self.run_pelican({})

        # Internal links should work and guide the user from one page to
        # another
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('subpage.html'))

class ExtraCss(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'extra_css', *args, **kwargs)

    def test(self):
        self.run_pelican({})

        # The page should contain two extra CSS links
        self.assertEqual(*self.actual_expected_contents('page.html'))

class HeaderFooter(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'header_footer', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'FORMATTED_FIELDS': ['header', 'footer']
        })

        # The header and footer should have the links expanded
        self.assertEqual(*self.actual_expected_contents('page.html'))

class Landing(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'landing', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'STATIC_PATHS': ['ship.jpg'],
            'FORMATTED_FIELDS': ['landing']
        })

        # The landing field should have the links expanded, header should not
        # be shown, footer should be. Navbar brand should be hidden in the
        # second case.
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('hide-navbar-brand.html'))

class TitleSitenameAlias(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'title_sitename_alias', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'SITENAME': "Site name"
        })

        # The page title should be just one name, not both
        self.assertEqual(*self.actual_expected_contents('page.html'))

class HtmlEscape(PageTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'html_escape', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'SITENAME': "<&> in site name",
            'FORMATTED_FIELDS': ['summary', 'description', 'landing', 'header', 'footer'],
            'PAGE_URL': '{slug}.html?and&in&url=""',
        })

        # Verify that everything is properly escaped everywhere. The landing
        # page has the name same as site name and the title should contain just
        # one.
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('landing.html'))
        self.assertEqual(*self.actual_expected_contents('breadcrumb.html'))

    # This is broken in Pelican until https://github.com/getpelican/pelican/issues/2260
    # so we test in a separate xfail test case
    @unittest.skipUnless(LooseVersion(pelican.__version__) > LooseVersion("3.7.1"),
                         "Pelican doesn't produce expected results in this version")
    def test_content(self):
        self.run_pelican({
            'SITENAME': "<&> in site name",
            'FORMATTED_FIELDS': ['summary', 'description', 'landing', 'header', 'footer'],
            'PAGE_URL': '{slug}.html?and&in&url=""',
        })

        # Verify that also the Pelican-produced content has correctly escaped
        # everything.
        self.assertEqual(*self.actual_expected_contents('content.html'))
