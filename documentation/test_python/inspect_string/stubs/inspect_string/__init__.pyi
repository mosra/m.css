import enum

class MyEnum(enum.Enum):
    VALUE = 0
    ANOTHER = 1
    YAY = 2

class UndocumentedEnum(enum.IntFlag):
    FLAG_ONE = 1
    FLAG_SIXTEEN = 16

class DerivedException:
    def add_note(self, *args):
        ...

    def with_traceback(self, *args):
        ...

    def __reduce__(self, *args):
        ...

    def __setstate__(self, *args):
        ...

    @property
    def __cause__(self):
        ...

    @property
    def __context__(self):
        ...

    @property
    def args(self):
        ...

class Foo:
    class InnerEnum(enum.Enum):
        VALUE = 0
        ANOTHER = 1
        YAY = 2

    class UndocumentedInnerEnum(enum.IntFlag):
        FLAG_ONE = 1
        FLAG_SIXTEEN = 16

    class Subclass:
        ...

    A_DATA = 'BOO'

    DATA_DECLARATION: int = None

    @staticmethod
    def static_func(a):
        ...

    @classmethod
    def func_on_class(a):
        ...

    def func(self, a, b):
        ...

    @property
    def a_property(self):
        ...

    @property
    def deletable_property(self):
        ...
    @deletable_property.deleter
    def deletable_property(self):
        ...

    @property
    def writable_property(self):
        ...
    @writable_property.setter
    def writable_property(self, value):
        ...

    @property
    def writeonly_property(self):
        ...
    @writeonly_property.setter
    def writeonly_property(self, value):
        ...

class FooSlots:
    @property
    def first(self):
        ...
    @first.setter
    def first(self, value):
        ...
    @first.deleter
    def first(self):
        ...

    @property
    def second(self):
        ...
    @second.setter
    def second(self, value):
        ...
    @second.deleter
    def second(self):
        ...

class Specials:
    def __add__(self, other):
        ...

    def __and__(self, other):
        ...

    def __init__(self):
        ...

A_CONSTANT = 3.24

foo: ...

def function():
    ...
