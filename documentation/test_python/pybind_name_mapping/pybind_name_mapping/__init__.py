from ._sub import Foo as Class
from ._sub import bar as submodule

# This test is almost the same as inspect_name_mapping, only natively

"""This module should have a bar submodule and a Foo class"""

__all__ = ['submodule', 'Class', 'foo']

def foo() -> Class:
    """This function returns Class, *not* _sub.Foo"""
