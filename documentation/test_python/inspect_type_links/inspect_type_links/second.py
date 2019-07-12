"""Second module"""

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

def type_return() -> Foo:
    """A function with a return type annotation"""

TYPE_DATA: Foo = Foo()
