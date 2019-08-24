"""Second module"""

from typing import Tuple, List, Any, Callable

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

    def type_property_writeonly(self, a: Enum):
        """A writeonly property"""
    type_property_writeonly = property(None, type_property_writeonly)

    def type_property_writeonly_string_nested(self, a: 'Tuple[Foo, List[Enum], Any]'):
        """A writeonly property with a string nested type"""
    type_property_writeonly_string_nested = property(None, type_property_writeonly_string_nested)

    def type_property_writeonly_string_invalid(self, a: 'Foo.Bar'):
        """A writeonly property with invalid string type"""
    type_property_writeonly_string_invalid = property(None, type_property_writeonly_string_invalid)

    # Has to be here, because if it would be globally, it would prevent all
    # other data annotations from being retrieved
    TYPE_DATA_STRING_INVALID: 'Foo.Bar' = 3

class FooSlots:
    """A slot class"""

    __slots__ = ['type_slot', 'type_slot_string_nested']

    type_slot: Enum
    type_slot_string_nested: 'Tuple[Foo, List[Enum], Any]'

class FooSlotsInvalid:
    """A slot class with an invalid annotation. Has to be separate because otherwise it would invalidate all other slot annotations in FooSlots as well."""

    __slots__ = ['type_slot_string_invalid']

    type_slot_string_invalid: List['FooBar']

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

class _Hidden:
    pass

def type_cant_link(a: _Hidden):
    """Annotation linking to a type that's a part of INPUT_MODULES but not known"""

def type_default_values(a: Enum = Enum.SECOND, b: Tuple[Foo] = (Foo, ), c: Foo = Foo()):
    """A function with default values, one enum, one tuple and the third nonrepresentable (yes, the tuple looks ugly)"""

def returns_none(a: Callable[[], None]) -> None:
    """In order to disambiguate between a missing return annotation and an
    annotated none, the None return annotation is kept, converted from NoneType
    to None"""

def returns_none_type(a: Callable[[], type(None)]) -> type(None):
    """And it should behave the same when using None or type(None)"""

TYPE_DATA: Foo = Foo()

TYPE_DATA_STRING_NESTED: 'Tuple[Foo, List[Enum], Any]' = {}

TYPE_DATA_ENUM: Enum = Enum.SECOND
