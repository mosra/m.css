"""Second module"""

from typing import Tuple, List, Any

import enum

class Enum(enum.Enum):
    """An enum"""

    FIRST = 1
    SECOND = 2

def type_enum(a: Enum):
    """Function referencing an enum"""

class Foo:
    """A class in the second module"""

    @property
    def type_property(self) -> Enum:
        """A property"""

    @property
    def type_property_string_nested(self) -> 'Tuple[Foo, List[Enum], Any]':
        """A property"""

    @property
    def type_property_string_invalid(self) -> 'FooBar':
        """A property"""

    # Has to be here, because if it would be globally, it would prevent all
    # other data annotations from being retrieved
    TYPE_DATA_STRING_INVALID: 'Foo.Bar' = 3

def type_string(a: 'Foo'):
    """A function with string type annotation"""

def type_nested(a: Tuple[Foo, List[Enum], Any]):
    """A function with nested type annotation"""

def type_string_nested(a: 'Tuple[Foo, List[Enum], Any]'):
    """A function with string nested type annotation"""

def type_nested_string(a: Tuple['Foo', 'List[Enum]', 'Any']):
    """A function with nested string type annotation"""

def type_string_invalid(a: 'Foo.Bar'):
    """A function with invalid string type annotation"""

def type_nested_string_invalid(a: Tuple['FooBar', 'List[Enum]', 'Any']):
    """A function with invalid nested string type annotation"""

def type_return() -> Foo:
    """A function with a return type annotation"""

def type_return_string_nested() -> 'Tuple[Foo, List[Enum], Any]':
    """A function with a string nested return type"""

def type_return_string_invalid(a: Foo) -> 'FooBar':
    """A function with invalid return string type annotation"""

def type_default_values(a: Enum = Enum.SECOND, b: Tuple[Foo] = (Foo, ), c: Foo = Foo()):
    """A function with default values, one enum, one tuple and the third nonrepresentable (yes, the tuple looks ugly)"""

TYPE_DATA: Foo = Foo()

TYPE_DATA_STRING_NESTED: 'Tuple[Foo, List[Enum], Any]' = {}

TYPE_DATA_ENUM: Enum = Enum.SECOND
