A page
######

:summary: no.

.. contents::
    :class: m-block m-default

.. contents:: TOC title, to catch wrong assumptions in ``topic`` processing
    :class: m-block m-primary

.. topic:: A topic that's not a TOC
    :class: m-block m-dim

    To catch even more wrong assumptions about ``topic`` nodes.

A paragraph.

    A block quote.

| Hand
| wrapped
| content

::

    Code with <all> the & "things" escaped and
                                           weird whitespace
                                           preserved

-   An unordered list
-   Another item

    1.  Sub-list, ordered
    2.  Another item

-   Third item of the top-level list

.. class:: m-table

========= ============
Heading 1 Heading 2
========= ============
Cell 1    Table cell 2
Row 2     Row 2 cell 2
========= ============

Term 1
    Description
Term 2
    Description of term 2

Section title
=============

An *emphasised text*, **strong text** and a ``literal``. Link to
`Google <https://google.com>`_, `the heading below <#a-heading>`_ or just an
URL as-is: https://mcss.mosra.cz/. `E-mail <mosra@centrum.cz>`_. A footnote
reference on a single thing [1]_ and more things [1]_ [2]_

.. [1] A footnote description
.. [2] Second thing description

.. container:: m-row

    .. container:: m-col-m-4 m-push-m-4 m-col-t-6 m-push-t-3 m-nopady

        A link that gets auto-wrapped:

        http://llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk

        A link that doesn't, because the title is different:

        `llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk <http://llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk>`_

        A link that also doesn't, because the title is the same, but specified explicitly:

        `http://llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk <http://llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch.co.uk>`_

`Section title with link`_
--------------------------

A line in the middle of a section, stays inside the section node:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A line at the end of a section, gets extracted outside of the section node.
Clicking on the section header will not include it in the highlight.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Section after
=============

Docutils says "Document may not end with a transition", eh.
