from ._sub import Foo as Class
from ._sub import bar as submodule

# This test is almost the same as pybind_name_mapping, only pure Python

"""This module should have a `submodule`, a `Class` and `foo()`"""

__all__ = ['submodule', 'Class', 'foo']

def foo() -> Class:
    """This function returns Class, *not* _sub.Foo"""
