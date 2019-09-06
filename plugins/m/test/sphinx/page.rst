m.sphinx
########

:ref-prefix:
    typing
    unittest.mock

.. role:: ref-small(ref)
    :class: m-text m-small

-   Module link:

    -   :ref:`argparse`
    -   explicit type: :ref:`py:module:argparse`

-   Function link:

    -   :ref:`open()`
    -   without a ``()``: :ref:`open`
    -   explicit type: :ref:`py:function:open()`,
    -   explicit without a ``()``: :ref:`py:function:open`

-   Class link:

    -   :ref:`xml.etree.ElementTree.Element`
    -   explicit type: :ref:`py:class:xml.etree.ElementTree.Element`

-   Classmethod link:

    -   :ref:`bytearray.fromhex()`
    -   without a ``()``: :ref:`bytearray.fromhex`
    -   explicit type: :ref:`py:classmethod:bytearray.fromhex()`
    -   explicit without a ``()``: :ref:`py:classmethod:bytearray.fromhex`

-   Staticmethod link:

    -   :ref:`bytes.maketrans()`
    -   without a ``()``: :ref:`bytes.maketrans`
    -   explicit type :ref:`py:staticmethod:bytes.maketrans()`
    -   explicit without a ``()``: :ref:`py:staticmethod:bytes.maketrans`

-   Method link:

    -   :ref:`str.rstrip()`
    -   without a ``()``: :ref:`str.rstrip`
    -   explicit type: :ref:`py:method:str.rstrip()`
    -   explicit type without a ``()``: :ref:`py:method:str.rstrip()`

-   Property link:

    -   :ref:`datetime.date.year`
    -   explicit type :ref:`py:attribute:datetime.date.year`

-   Data link:

    -   :ref:`re.X`
    -   explicit type: :ref:`py:data:re.X`

-   Explicitly typed page link with automatic title: :ref:`std:doc:using/cmdline`
-   :ref:`Page link with custom link title <std:doc:using/cmdline>`,
    :ref:`Function link with a custom title <os.path.join()>`
-   Custom CSS class: :ref-small:`str.join()`
-   Omitting a prefix: :ref:`etree.ElementTree`, :ref:`ElementTree`
-   Omitting a page-specific prefix defined in ``:ref-prefix:``:
    :ref:`Tuple`, :ref:`NonCallableMagicMock`
-   Custom query string: :ref:`os.path <os.path?q=the meaning of life>`

These should produce warnings:

-   Link to nonexistent name will be rendered as code: :ref:`nonexistent()`
-   :ref:`Link to nonexistent name with custom title will be just text <nonexistent()>`
