"""Yes so this is module summary, not shown in the output"""

import enum
from . import docstring_summary

class Class:
    """And this class summary, not shown either"""

    @classmethod
    def class_method(a, b):
        """This function is a class method"""

    @staticmethod
    def static_method(cls, a):
        """This function is a static method"""

    def __init__(self):
        """A dunder method"""

    def method(self):
        """This summary will get overriden from the docs"""

    def method_with_details(self):
        pass

    @property
    def a_property(self):
        """This summary is not shown either"""

    @property
    def a_property_with_details(self):
        """This summary is not shown either"""

    @property
    def annotated_property(self) -> float:
        """This is an annotated property"""

    DATA_WITH_DETAILS: str = 'this blows'

class ClassWithSummary:
    """This class has summary from the docstring"""

class Enum(enum.Enum):
    """This summary gets ignored"""

class EnumWithSummary(enum.Enum):
    """This summary is preserved"""

    VALUE = 0
    ANOTHER = 1

EnumWithSummary.VALUE.__doc__ = "A value"

def foo(a, b):
    """This summary is not shown either"""

def foo_with_details(a, b):
    """This summary is not shown either"""

def function_with_summary():
    """This function has summary from the docstring"""

def annotations(a: int, b, c: float) -> str:
    """No annotations shown for this"""

CONSTANT: float = 3.14

DATA_WITH_DETAILS: str = 'heyoo'

DATA_WITH_DETAILS_BUT_NO_SUMMARY_NEITHER_TYPE = None
