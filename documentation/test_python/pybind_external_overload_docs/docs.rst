.. py:function:: pybind_external_overload_docs.foo(a: int, b: typing.Tuple[int, str])
    :param a: First parameter
    :param b: Second parameter

    Details for the first overload.

.. py:function:: pybind_external_overload_docs.foo(arg0: typing.Callable[[float, typing.List[float]], int])
    :param arg0: The caller

    Complex signatures in the second overload should be matched properly, too.

.. py:function:: pybind_external_overload_docs.foo
    :param name: Ha!

    This is a generic documentation and will be caught only by the third
    overload. Luckily we just document that exact parameter.

.. py:function:: pybind_external_overload_docs.foo(param: int)
    :param param: This has a default value of 4 but that shouldn't be part of
        the signature.

    Fourth overload has a default value.

.. py:function:: pybind_external_overload_docs.Class.foo(self, index: int)
    :return: Nothing at all.

    Class methods don't have type annotation on self.

.. py:function:: pybind_external_overload_docs.Class.foo

    And the fallback matching works there, too.

.. py:function:: pybind_external_overload_docs.Class26.foo(self, a: int, b: float, keyword: str)

    The ``/`` and ``*`` are excluded from matching.

.. py:function:: pybind_external_overload_docs.foo(first: int)
    :param second: But the second argument doesn't exist?!

.. py:function:: pybind_external_overload_docs.foo(terrible: wow)

    This docs can't match any overload and thus get unused.
