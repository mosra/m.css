"""A module"""

# This one is a module that shouldn't be exposed
import enum

# This one is a package that shouldn't be exposed
import xml

# These are descendant packages / modules that should be exposed
from . import subpackage, another_module

# These are variables from an external modules, shouldn't be exposed either
from re import I

# TODO: there's no way to tell where a variable of a builtin type comes from,
#   so this would be exposed. The only solution is requiring a presence of an
#   external docstring I'm afraid.
#from math import pi

class Foo:
    """The foo class"""

    A_DATA = 'BOO'

    DATA_DECLARATION: int

    class InnerEnum(enum.Enum):
        """Inner enum"""

        VALUE = 0
        ANOTHER = 1
        YAY = 2

    InnerEnum.VALUE.__doc__ = "A value"
    InnerEnum.ANOTHER.__doc__ = "Another value"

    class UndocumentedInnerEnum(enum.IntFlag):
        FLAG_ONE = 1
        FLAG_SEVENTEEN = 17

    class Subclass:
        """A subclass of Foo"""
        pass

    def func(self, a, b):
        """A method"""
        pass

    @classmethod
    def func_on_class(cls, a):
        """A class method"""
        pass

    @staticmethod
    def static_func(a):
        """A static method"""
        pass

    @property
    def a_property(self):
        """A property"""
        pass

    @property
    def writable_property(self):
        """Writable property"""
        pass

    @writable_property.setter
    def writable_property(self, a):
        pass

    @property
    def deletable_property(self):
        """Deletable property"""
        pass

    @deletable_property.deleter
    def deletable_property(self):
        pass

    def writeonly_property(self, a):
        """Write-only property"""
        pass

    writeonly_property = property(None, writeonly_property)

class FooSlots:
    """A class with slots. Can't have docstrings for these."""

    __slots__ = ['first', 'second']

class DerivedException(BaseException):
    """A class deriving from BaseException, which has the weird args getset_descriptor"""

    # Note: once we properly handle properties of base classes, we might want
    # to import BaseException and add it to __all__ so it gets parsed directly

class Specials:
    """Special class members"""

    def __init__(self):
        """The constructor"""
        pass

    def __add__(self, other):
        """Add a thing"""
        pass

    def __and__(self, other):
        # Undocumented, but should be present
        pass

class MyEnum(enum.Enum):
    """An enum"""

    VALUE = 0
    ANOTHER = 1
    YAY = 2

MyEnum.VALUE.__doc__ = "A value"
MyEnum.ANOTHER.__doc__ = "Another value"

class UndocumentedEnum(enum.IntFlag):
    FLAG_ONE = 1
    FLAG_SEVENTEEN = 17

def function():
    """A function"""
    pass

A_CONSTANT = 3.24

_PRIVATE_CONSTANT = -3

foo = Foo()
