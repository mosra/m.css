"""This submodule is renamed from bar to submodule and should have a function member."""

from . import Foo

def foo(a: Foo, b: int) -> int:
    """A function"""
    return b*2
