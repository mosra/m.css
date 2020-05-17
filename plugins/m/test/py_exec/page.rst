m.py_exec
#########

First context, no output:

.. py-exec::
    :context-id: ctx1

    from typing import List
    a = 12

Second context, no output:

.. py-exec::
    :context-id: ctx2

    List = [1,2,3]

Anon context, expect top-level ``RuntimeError``:

.. py-exec::
    :hl_lines: 2
    :raises: RuntimeError

    def f():
        raise RuntimeError()
    f()

First context, print to stdout:

.. py-exec::
    :context-id: ctx1

    print(a + 2)

Second context:

.. py-exec::
    :context-id: ctx2

    assert List + [4] == [1,2,3,4]

Anon context, suppressed output:

.. py-exec::
    :hide-stdout:

    print(4 + 2 / 2)

Anon context, suppressed stderr:

.. py-exec::
    :hide-stderr:

    import sys
    print(4 + 2 / 2, file=sys.stderr)


First context, print and destroy context:

.. py-exec::
    :context-id: ctx1
    :discard-context:

    print(List)

Second context, print and destroy context:

.. py-exec::
    :context-id: ctx2
    :discard-context:

    print(List)

Both contexts are destroyed now, variable access results to expected ``NameError``:

.. py-exec::
    :context-id: ctx1
    :raises: NameError
    :discard-context:

    print(List)


.. py-exec::
    :context-id: ctx2
    :raises: NameError
    :discard-context:

    print(List)

List comprehension:

.. py-exec::

    def foo(a):
        return a * 2 + 2
    print([ foo(i) for i in [1,2] ])


