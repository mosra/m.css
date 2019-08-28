.. py:property:: inspect_attrs.MyClass.unannotated
    :summary: External docs for this property

.. py:property:: inspect_attrs.MyClassAutoAttribs.complex_annotation
    :summary: This is complex.

.. py:data:: inspect_attrs.MySlotClass.annotated
    :summary: This is a float slot.

.. py:data:: inspect_attrs.MyClass.plain_data
    :summary: This is plain data, not handled by attrs

.. py:function:: inspect_attrs.MyClass.__init__
    :summary: External docs for the init
    :param annotated: The first argument
    :param unannotated: This gets the default of four
    :param complex_annotation: Yes, a list
    :param complex_annotation_in_attr: Annotated using ``attr.ib(type=)``,
        should be shown as well
    :param hidden_property: Interesting, but I don't care.

    The :p:`hidden_property` isn't shown in the output as it's prefixed with
    an underscore.
