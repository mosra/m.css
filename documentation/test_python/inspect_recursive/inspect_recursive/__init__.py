"""Recursive imports"""

import inspect_recursive # Importing self, should get ignored

class Foo:
    """A class"""

from . import first

# Importing a module twice, only one of them should be picked
from . import second as b
from . import second as a

def foo() -> b.Bar:
    """Function that returns Foo"""

def bar() -> a.Bar:
    """Function that also returns Foo"""
