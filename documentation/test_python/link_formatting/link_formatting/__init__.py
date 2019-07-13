"""This is a module."""

import enum

from . import sub, pybind

class Enum(enum.Enum):
    """An enum"""

    FIRST_VALUE = 1
    SECOND_VALUE = 2

SOME_DATA: Enum = Enum.FIRST_VALUE

class Class:
    """This is a nice class."""

    class Sub:
        """And a nice subclass, oh."""

    @property
    def property(self) -> Enum:
        """A property."""

def function(a: Enum = Enum.SECOND_VALUE) -> Class:
    """A function."""
