Test
####

:save_as: plugins/htmlsanity/test/index.html
:breadcrumb: {filename}/plugins.rst Pelican plugins
             {filename}/plugins/htmlsanity.rst HTML sanity

Inline preformatted blocks should be escaped: ``<hr>``

Inline preformatted blocks should have whitespace preserved: ``two  spaces  between  words``

Preformatted blocks should have sane rendering::

    helllo

      world

Inline code shouldn't be hyphenated or with smart quotes applied: ``"hello" --- isn't this working?"``.
