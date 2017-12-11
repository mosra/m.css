from m.test import PluginTestCase

class Content(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'content', *args, **kwargs)

    def test(self):
        self.run_pelican({
            'PLUGINS': ['m.htmlsanity']
        })

        # Verify there's no superfluous markup or useless classes
        self.assertEqual(*self.actual_expected_contents('page.html'))

class Typography(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'typography', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # Need extended Latin characters for Czech text
            'M_CSS_FILES': ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i&subset=latin-ext',
                            'static/m-dark.css'],
            'PLUGINS': ['m.htmlsanity'],
            'M_HTMLSANITY_HYPHENATION': True,
            'M_HTMLSANITY_SMART_QUOTES': True,
            'M_FINE_PRINT': "The footer should be hyphenated as well. \"And with smart quotes.\"",
            'M_SHOW_AUTHOR_LIST': True,
            'DATE_FORMATS': {'en': ('en_US.UTF-8', '%b %d, %Y'),
                             'cs': ('en_US.UTF-8', '%b %d, %Y')},
            'PAGE_LANG_SAVE_AS': '{slug}.html',
            'ARTICLE_SAVE_AS': 'article-{slug}.html',
            'ARTICLE_URL': 'article-{slug}.html',
            'ARTICLE_LANG_SAVE_AS': 'article-{slug}.html',
            'ARTICLE_LANG_URL': 'article-{slug}.html',
            'CATEGORY_SAVE_AS': 'category-{slug}.html',
            'CATEGORY_URL': 'category-{slug}.html',
            'AUTHOR_SAVE_AS': 'author-{slug}.html',
            'AUTHOR_URL': 'author-{slug}.html',
            'TAG_SAVE_AS': 'tag-{slug}.html',
            'TAG_URL': 'tag-{slug}.html',
            'FORMATTED_FIELDS': ['summary', 'description', 'header', 'footer'],

            # Disable unneeded stuff
            'TRANSLATION_FEED_ATOM': None,
            'CATEGORY_FEED_ATOM': None,
            'AUTHOR_FEED_ATOM': None,
            'AUTHOR_FEED_RSS': None,
        })

        # The &shy; should be at proper places and not where it shouldn't be.
        # The <html> lang element should be set correctly as well. Verify that
        # hyphenation and smart quotes are correctly used across the whole
        # theme.
        self.assertEqual(*self.actual_expected_contents('page.html'))
        self.assertEqual(*self.actual_expected_contents('page-lang.html'))
        self.assertEqual(*self.actual_expected_contents('article-lang.html'))
        self.assertEqual(*self.actual_expected_contents('article-jumbo.html'))
        self.assertEqual(*self.actual_expected_contents('author-an-author.html'))
        self.assertEqual(*self.actual_expected_contents('category-a-category.html'))
        self.assertEqual(*self.actual_expected_contents('tag-tagging-a-name.html'))

class TypographyGlobalLang(PluginTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, 'typography_global_lang', *args, **kwargs)

    def test(self):
        self.run_pelican({
            # Need extended Latin characters for Czech text
            'M_CSS_FILES': ['https://fonts.googleapis.com/css?family=Source+Code+Pro:400,400i,600%7CSource+Sans+Pro:400,400i,600,600i&subset=latin-ext',
                            'static/m-dark.css'],
            'PLUGINS': ['m.htmlsanity'],
            'DEFAULT_LANG': 'cs',
            'M_HTMLSANITY_HYPHENATION': True,
            'M_HTMLSANITY_SMART_QUOTES': True,
            'M_FINE_PRINT': "Patička má dělení slov také. \"A chytré uvozovky.\""
        })

        # The <html> lang element should be set correctly and the &shy; should
        # be at proper places and not where it shouldn't be.
        self.assertEqual(*self.actual_expected_contents('page.html'))
