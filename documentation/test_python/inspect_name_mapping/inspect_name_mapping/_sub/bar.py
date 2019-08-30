"""This submodule is renamed from bar to submodule and should have a function member."""

from . import Foo

class _NameThatGetsOverridenExternally:
    pass

def foo(a: Foo, b: int) -> _NameThatGetsOverridenExternally:
    """A function"""
    return b*2
