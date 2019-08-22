.. role:: label-success
    :class: m-label m-success
.. role:: label-info
    :class: m-label m-info

.. py:module:: content
    :summary: This overwrites the docstring for ``content``.

    This is detailed module docs. I kinda *hate* how it needs to be indented,
    tho.

.. py:module:: content.docstring_summary

    And adds detailed docs.

.. py:class:: content.Class
    :summary: This overwrites the docstring for ``content.Class``.

    This is detailed class docs. Here I *also* hate how it needs to be
    indented.

.. py:function:: content.Class.class_method

    The :label-success:`classmethod` should be shown here.

.. py:function:: content.Class.static_method

    The :label-info:`staticmethod` should be shown here.

.. py:function:: content.Class.__init__

    A dunder method shown in the detailed view.

.. py:function:: content.Class.method
    :summary: This overwrites the docstring for ``content.Class.method``, but
        doesn't add any detailed block.

.. py:function:: content.Class.method_with_details

    This one has a detailed block without any summary.

.. py:function:: content.Class.method_param_docs
    :param a: The first parameter
    :param b: The second parameter

    The ``self`` isn't documented and thus also not included in the list.

.. py:property:: content.Class.a_property
    :summary: This overwrites the docstring for ``content.Class.a_property``,
        but doesn't add any detailed block.

.. py:property:: content.Class.a_property_with_details
    :summary: This overwrites the docstring for ``content.Class.a_property_with_details``.

    Detailed property docs.

.. py:property:: content.Class.annotated_property

    Annotated property, using summary from the docstring.

.. py:data:: content.Class.DATA_WITH_DETAILS

    Detailed docs for ``data`` in a class to check rendering.

.. py:class:: content.ClassWithSummary

    This class has external details but summary from the docstring.

.. py:enum:: content.Enum
    :summary: This overwrites the docstring for ``content.Enum``, but
        doesn't add any detailed block.

.. py:enum:: content.EnumWithSummary

    And this is detailed docs added to the docstring summary.

.. py:function:: content.foo
    :summary: This overwrites the docstring for ``content.foo``, but
        doesn't add any detailed block.

.. py:function:: content.foo_with_details
    :summary: This overwrites the docstring for ``content.foo_with_details()``.

    .. container:: m-note m-info

        Detailed docs for this function

.. py:function:: content.function_with_summary

    This function has external details but summary from the docstring.

.. py:function:: content.param_docs
    :param a: First parameter
    :param b: The second one
    :param c: And a ``float``
    :return: String, of course, it's all *stringly* typed

    Type annotations and param list in detailed docs.

.. py:function:: content.param_docs_wrong
    :param a: First
    :param c: Third

    The ``b`` is not documented, while ``c`` isn't in the signature.

.. py:data:: content.CONSTANT
    :summary: This is finally a docstring for ``content.CONSTANT``

.. py:data:: content.DATA_WITH_DETAILS
    :summary: This is finally a docstring for ``content.CONSTANT``

    Detailed docs for the data. **YAY.**

.. py:data:: content.DATA_WITH_DETAILS_BUT_NO_SUMMARY_NEITHER_TYPE

    Why it has to be yelling?!

.. py:function: content.foo

    Details for this function

.. py:module:: thismoduledoesnotexist
    :summary: This docs get unused and produce a warning

.. py:class:: content.ThisDoesNotExist
    :summary: This docs get unused and produce a warning

.. py:enum:: content.ThisEnumDoesNotExist
    :summary: This docs get unused and produce a warning

.. py:function:: content.this_function_does_not_exist
    :summary: This docs get unused and produce a warning

.. py:property:: content.Class.this_property_does_not_exist
    :summary: This docs get unused and produce a warning

.. py:data:: content.THIS_DOES_NOT_EXIST
    :summary: This docs get unused and produce a warning
