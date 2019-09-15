.. py:module:: inspect_type_links

    :ref:`first.Foo` and :ref:`inspect_type_links.first.Foo` should lead to the
    same class.

    :ref:`open()` should lead to the Python builtin, for the local
    function we need to say :ref:`inspect_type_links.open()`. If it would be
    the other way around, there would be no simple way to link to builtins.

.. py:function:: inspect_type_links.open
    :raise ValueError: If this is not a can, crosslinking to :ref:`ValueError`
        of course.

.. py:property:: inspect_type_links.Foo.prop
    :raise SystemError: If you look at it wrong, crosslinking to
        :ref:`SystemError` of course.

.. py:module:: inspect_type_links.first

    :ref:`Foo`, :ref:`first.Foo` and :ref:`inspect_type_links.first.Foo` should
    lead to the same class.

.. py:class:: inspect_type_links.first.Foo

    :ref:`first.Foo` and :ref:`inspect_type_links.first.Foo` should
    lead to self; referencing the subclass via :ref:`Foo`, :ref:`Foo.Foo`,
    :ref:`first.Foo.Foo` or :ref:`Bar`. :ref:`second.Foo` and
    :ref:`inspect_type_links.Bar` lead to other classes.

    This is consistent with how Python type annotations inside *a class* are
    interpreted -- see :ref:`reference_self_data`, :ref:`reference_inner_data`
    and :ref:`reference_inner_other_data`. Inside *function definitions* the
    rules are different as per https://docs.python.org/3/reference/executionmodel.html#resolution-of-names:

        The scope of names defined in a class block is limited to the class
        block; it does not extend to the code blocks of methods

    This means relative annotations in :ref:`reference_self()`,
    :ref:`reference_inner()` and :ref:`reference_inner_other()` are parsed
    differently -- but in the documentation, these are shown with the same
    rules as for data themselves.

.. py:data:: inspect_type_links.first.Foo.reference_self_data
    :summary: Referencing its wrapper class using ``first.Foo``, displayed
        as ``first.Foo`` as well. ``Foo`` alone would reference the inner. This
        is different from :ref:`reference_self()`.

.. py:data:: inspect_type_links.first.Foo.reference_inner_data
    :summary: Referencing the inner class using ``Foo``, ``Foo.Foo`` or
        ``first.Foo.Foo``, displayed as just ``Foo``. This is different from
        :ref:`reference_inner()`.

.. py:data:: inspect_type_links.first.Foo.reference_inner_other_data
    :summary: Referencing another inner class using ``Bar``, ``Foo.Bar`` or
        ``first.Foo.Bar``, displayed as just ``Bar``. This is different from
        :ref:`reference_inner_other()`.

.. py:class:: inspect_type_links.first.Foo.Foo

    Referencing self as :ref:`Foo` or :ref:`Foo.Foo`, parent as
    :ref:`first.Foo`, other as :ref:`second.Foo`. However inside annotations
    ``Foo`` references the parent, consistently in a function and in data?
    Am I doing something wrong?

.. py:class:: inspect_type_links.first.sub.Foo

    Referencing self as :ref:`Foo` or :ref:`sub.Foo`, parent as
    :ref:`first.Foo`, other as :ref:`second.Foo`.
