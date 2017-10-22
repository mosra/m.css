Test
####

:save_as: plugins/components/test/index.html
:breadcrumb: {filename}/plugins.rst Pelican plugins
             {filename}/plugins/components.rst Components

Should match the rendering of
`CSS components test page <{filename}/css/components-test.rst>`_.

Blocks_
=======

.. container:: m-row

    .. container:: m-col-m-3 m-col-s-6

        .. block-default:: Default block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-primary:: Primary block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-success:: Success block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-warning:: Warning block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-danger:: Danger block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-info:: Info block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-dim:: Dim block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. block-flat:: Flat block

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

`Notes, frame`_
===============

.. container:: m-row

    .. container:: m-col-m-3 m-col-s-6

        .. note-default:: Default note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-primary:: Primary note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-success:: Success note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-warning:: Warning note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-danger:: Danger note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-info:: Info note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. note-dim:: Dim note

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

    .. container:: m-col-m-3 m-col-s-6

        .. frame:: Frame

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
            ultrices a erat eu suscipit. `Link. <#>`_

Note w/o title, with applied class:

.. note-default::
    :class: m-text-center

    Some center-aligned content.

Block, with applied class:

.. block-warning:: Warning block
    :class: m-text-right

    Aligned to the right

Frame, w/o title, with applied class:

.. frame::
    :class: m-text-center

    Centered frame content

Flat code figure:

.. code-figure::
    :class: m-flat

    ::

        Some
            code
        snippet

    And a resulting output.
