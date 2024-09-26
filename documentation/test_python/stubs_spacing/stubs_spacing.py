# This file is both an input and output, i.e. the generated stub should have
# exactly the same spacing as the input.

import enum

class Enum1(enum.Enum):
    VALUE1 = 0
    VALUE2 = 1

class Enum2(enum.Enum):
    VALUE1 = 10
    VALUE2 = 20
    VALUE3 = 30

class EnumEmpty(enum.Enum):
    ...

class Class1:
    @staticmethod
    def staticmethod1():
        ...

    @staticmethod
    def staticmethod2():
        ...

    @staticmethod
    def staticmethod3():
        ...

    @classmethod
    def classmethod1(*args):
        ...

    @classmethod
    def classmethod2(*args):
        ...

    @classmethod
    def classmethod3(*args):
        ...

    def method1(self):
        ...

    def method2(self):
        ...

    def method3(self):
        ...

    def __dunder_method1__(self):
        ...

    def __dunder_method2__(self):
        ...

    def __dunder_method3__(self):
        ...

    @property
    def property1(self):
        ...

    @property
    def property2(self):
        ...
    @property2.setter
    def property2(self, value):
        ...

    @property
    def property3(self):
        ...
    @property3.deleter
    def property3(self):
        ...

    @property
    def property4(self):
        ...
    @property4.setter
    def property4(self, value):
        ...
    @property4.deleter
    def property4(self):
        ...

class Class2:
    class InnerEnum1(enum.Enum):
        VALUE1 = 0
        VALUE2 = 1

    class InnerEnum2(enum.Enum):
        ...

    class InnerClass1:
        ...

    class InnerClass2:
        ...

    INNER_DATA1: str = 'a'

    INNER_DATA2: int = 3

    INNER_DATA3: None = None

class Class3:
    class InnerClass:
        class InnerInnerClass:
            ...

class ClassEmpty:
    ...

DATA1: str = 'b'

DATA2: int = 7

DATA3: float = 15.6

def function1():
    ...

def function2():
    ...
