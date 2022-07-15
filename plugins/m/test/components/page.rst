m.components
############

.. block-default:: Default block

    Text.

.. block-success:: Success block
    :class: m-text-right

    First paragraph, aligned to the right.

    *Second* paragraph, also.

.. note-default:: Default note

    Text.

.. note-danger:: Danger note

    First paragraph.

    *Second* paragraph.

.. note-warning::
    :class: m-text-center

    Warning note without title, centered.

.. frame:: Frame with title

    Text.

.. frame::
    :class: m-text-left

    Frame *without* title, on the left.

.. code-figure::
    :class: m-flat

    ::

        Some
            code
        snippet

    And a resulting output.

.. console-figure:: Figure caption

    .. class:: m-console

    ::

        Console

    And text.

.. math-figure::

    .. raw:: html

        <svg class="m-math" style="width: 5rem; height: 5rem;"></svg>

    Math figure contents.

.. graph-figure:: Caption

    .. raw:: html

        <svg class="m-graph" style="width: 5rem; height: 5rem;"></svg>

    Graph figure contents.

.. text-dim::

    Dim text.

.. transition:: ~ ~ ~

.. button-warning:: {filename}/page.rst

    Button text.

.. button-success:: #

    First text.

    Second text.

.. button-flat:: #

    Flat button

Inline elements: :label-primary:`Primary label`,
:label-flat-warning:`Flat warning label`.

`Transitions, builtin`_
=======================

Builtin transition in the middle of a section, stays inside the section node:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Builtin transition at the end of a section, gets extracted outside of the
section node. Clicking on the section header will not include it in the
highlight.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Transitions, m.css`_
=====================

M.css transition in the middle of a section, stays inside the section node:

.. transition:: ~ * ~ * ~

M.css transition at the end of a section, gets extracted outside of the section
node the same as a builtin transition. Clicking on the section header will not
include it in the highlight.

.. transition:: ~ * ~ * ~

Section after
=============

Docutils says "Document may not end with a transition", eh.
