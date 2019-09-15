.. role:: label-success
    :class: m-label m-success
.. role:: label-info
    :class: m-label m-info

.. The actual correctness of relative references is tested in
    inspect_type_links in order to test both absolute -> relative and
    relative -> absolute direction at the same place. Here it's just verifying
    that scopes are correctly propagated to all places where it matters.

.. py:module:: content
    :summary: This overwrites the docstring for :ref:`content`.
    :data DATA_DOCUMENTED_INSIDE_MODULE: In-module summary for the data member
    :data ANOTHER_DOCUMENTED_INSIDE_MODULE: In-module summary for another data

    This is detailed module docs. I kinda *hate* how it needs to be indented,
    tho. Below is an included file to test file path is supplied somewhat
    correctly (relative to the input dir):

    .. include:: content/submodule.py
        :literal:

.. py:module:: content.docstring_summary

    And adds detailed docs.

.. py:module:: content.submodule
    :summary: This submodule has an external summary.

.. py:class:: content.Class
    :summary: This overwrites the docstring for :ref:`Class`.

    This is detailed class docs. Here I *also* hate how it needs to be
    indented.

.. py:function:: content.Class.class_method

    The :label-success:`classmethod` should be shown here.

.. py:function:: content.Class.static_method

    The :label-info:`staticmethod` should be shown here.

.. py:function:: content.Class.__init__

    A dunder method shown in the detailed view.

.. py:function:: content.Class.method
    :summary: This overwrites the docstring for :ref:`method()`, but doesn't
        add any detailed block.

.. py:function:: content.Class.method_with_details

    This one has a detailed block without any summary.

.. py:function:: content.Class.method_param_docs
    :param a: The first parameter
    :param b: The second parameter

    The ``self`` isn't documented and thus also not included in the list.

.. py:function:: content.Class.method_param_exception_return_docs
    :param a: The first parameter
    :param b: The second parameter
    :raise AttributeError: If you do bad things to it
    :return: If you don't do bad things to it

.. py:property:: content.Class.a_property
    :summary: This overwrites the docstring for :ref:`a_property`, but doesn't
        add any detailed block.

.. py:property:: content.Class.a_property_with_details
    :summary: This overwrites the docstring for :ref:`a_property_with_details`.

    Detailed property docs.

.. py:property:: content.Class.annotated_property

    Annotated property, using summary from the docstring.

.. py:property:: content.Class.property_exception_docs
    :raise AttributeError: If you do bad things to it

.. py:data:: content.Class.DATA_WITH_DETAILS

    Detailed docs for :ref:`DATA_WITH_DETAILS` in a class to check
    rendering.

.. py:class:: content.ClassWithSummary

    This class has external details but summary from the docstring.

.. py:property:: content.ClassWithSlots.hello
    :summary: This is a slot, another is :ref:`this_is_a_slot`

.. py:property:: content.ClassWithSlots.this_is_a_slot
    :summary: This the **other one**.

.. py:enum:: content.Enum
    :summary: This overwrites the docstring for :ref:`Enum`, but doesn't
        add any detailed block.

.. py:enum:: content.EnumWithSummary
    :value ANOTHER: This value is documented from within the ``enum``
        directive...

    And this is detailed docs added to the docstring summary. :ref:`VALUE`!!

.. py:enumvalue:: content.EnumWithSummary.THIRD

    ... while this comes from the ``enumvalue`` directive.

.. py:function:: content.foo
    :summary: This overwrites the docstring for :ref:`foo()`, but doesn't
        add any detailed block.

.. py:function:: content.foo_with_details
    :summary: This overwrites the docstring for :ref:`foo_with_details()`.

    .. container:: m-note m-info

        Detailed docs for this function

.. py:function:: content.function_with_summary

    This function has external details but summary from the docstring.

.. py:function:: content.param_docs
    :param a: First parameter
    :param b: The second one is different from :p:`a`
    :param c: And a ``float``
    :return: String, of course, it's all *stringly* typed

    Type annotations and param list in detailed docs.

.. py:function:: content.param_docs_wrong
    :param a: First
    :param c: Third

    The :p:`b` is not documented, while :p:`c` isn't in the signature.

Doing :p:`this` here is not good either.

.. py:function:: content.full_docstring
    :param a: First parameter
    :param b: Second

.. py:function:: content.exception_docs
    :raise ValueError: This thing fires
    :raise ValueError: This *same* thing fires *also* for this reason
    :raise RuntimeError: This another thing fires too

.. py:data:: content.CONSTANT
    :summary: This is finally a docstring for :ref:`CONSTANT`

.. py:data:: content.DATA_WITH_DETAILS
    :summary: This is finally a docstring for :ref:`DATA_WITH_DETAILS`

    Detailed docs for the data. **YAY.**

.. py:data:: content.DATA_WITH_DETAILS_BUT_NO_SUMMARY_NEITHER_TYPE

    Why it has to be yelling?!

.. py:class:: content.ClassDocumentingItsMembers
    :property property_documented_in_class: A property
    :property another: And the other property, documented inside
        :ref:`ClassDocumentingItsMembers`!
    :data DATA_DOCUMENTED_IN_CLASS: Documentation for the in-class data
    :data ANOTHER: And the other, :ref:`ANOTHER`!

.. This should check we handle reST parsing errors gracefully.
.. py:function:: content.this_function_has_bad_docs
    :summary: :nonexistentrole:`summary is all bad`
    :param a: :nonexistentrole:`param docs also blow`
    :return: :nonexistentrole:`return is terrible`

    :nonexistentrole:`this too`

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
