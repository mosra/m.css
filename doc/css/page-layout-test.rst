Test
####

:save_as: css/page-layout/test/index.html
:breadcrumb: {filename}/css.rst CSS
             {filename}/css/page-layout.rst Page layout

`Components in highlighted sections`_
=====================================

Click on the section header above to see the effect. Left border radius on all
elements should be flattened and nothing should jump when highlighted.

.. note-default::

    Default note

.. note-primary::

    Primary note

.. note-success::

    Success note

.. note-warning::

    Warning note

.. note-danger::

    Danger note

.. note-info::

    Info note

.. note-dim::

    Dim note

`Subsections`_
--------------

.. code:: c++

    int main() { }

.. block-default:: Default block

    Blocks don't change their appearance much.

.. block-flat:: Flat block

    Flat blocks don't change their appearance at all.

.. frame:: Frame

    Frame will have its left border fattened.

`Nested components`_
--------------------

Shouldn't be any difference.

.. container:: m-row

    .. container:: m-col-m-4 m-col-s-6

        .. note-default::

            Default note.

    .. container:: m-col-m-4 m-col-s-6

        .. block-primary:: Primary block

            Text.

    .. container:: m-col-m-4 m-col-s-6

        .. frame::

            A frame.

    .. container:: m-clearfix-m

        ..

    .. container:: m-col-m-4 m-col-s-6

        .. code:: hs

            :: -> :: -> ::

    .. container:: m-col-m-4 m-col-s-6

        .. class:: m-inverted-highlight
        .. code:: c++
            :hl_lines: 2

            int main() {
                return 666;
            }
