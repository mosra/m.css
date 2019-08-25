import enum

from . import pybind

def function(): pass

class Class:
    @classmethod
    def class_method(cls): pass

    @staticmethod
    def static_method(): pass

    def method(self): pass

    @property
    def a_property(self): pass

    CLASS_DATA = 3

class Enum(enum.Enum):
    ENUM_VALUE = 1

MODULE_DATA = {}

def _private_function(): pass
