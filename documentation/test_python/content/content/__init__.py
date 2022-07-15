"""Yes so this is module summary, not shown in the output"""

import enum
from . import docstring_summary, submodule

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
        """This summary will get overridden from the docs"""

    def method_with_details(self):
        pass

    def method_param_docs(self, a, b):
        """This method gets its params except self documented"""

    def method_param_exception_return_docs(self, a, b):
        """This one documents params and raised exceptions"""

    @property
    def a_property(self):
        """This summary is not shown either"""

    @property
    def a_property_with_details(self):
        """This summary is not shown either"""

    @property
    def annotated_property(self) -> float:
        """This is an annotated property"""

    @property
    def property_exception_docs(self):
        """This one documents raised exceptions in an (otherwise unneeded)
        detail view"""

    DATA_WITH_DETAILS: str = 'this blows'

class ClassWithSummary:
    """This class has summary from the docstring"""

class ClassWithSlots:
    """This class has slots and those have to be documented externally"""

    __slots__ = ['hello', 'this_is_a_slot']

class ClassDocumentingItsMembers:
    """This class documents its members directly in its own directive"""

    DATA_DOCUMENTED_IN_CLASS: int = 3
    ANOTHER = 1

    @property
    def property_documented_in_class(self) -> float: pass

    @property
    def another(self): pass

class Enum(enum.Enum):
    """This summary gets ignored"""

class EnumWithSummary(enum.Enum):
    """This summary is preserved"""

    VALUE = 0
    ANOTHER = 1
    THIRD = 3

EnumWithSummary.VALUE.__doc__ = """Value docs where this is treated as summary.

And this as detailed docs by the raw docstring parser, but the theme doesn't
distinguish between them so they get merged together.
"""

def foo(a, b):
    """This summary is not shown either"""

def foo_with_details(a, b):
    """This summary is not shown either"""

def function_with_summary():
    """This function has summary from the docstring"""

def param_docs(a: int, b, c: float) -> str:
    """Detailed param docs and annotations"""

def param_docs_wrong(a, b):
    """Should give warnings"""

def full_docstring(a, b) -> str:
    """This function has a full docstring.

    It takes one parameter and also another, which are documented externally,
    but not overwriting the in-source docstring. The details are in two
    paragraphs, each wrapped in its own `<p>`, but not additionally formatted
    or parsed in any way.

    Like this.
    """

def exception_docs():
    """This one documents raised exceptions in an (otherwise unneeded) detail
    view
    """

# This should check we handle reST parsing errors in external docs gracefully.
# Will probably look extra weird in the output tho, but that's okay -- it's an
# error after all.
def this_function_has_bad_docs(a, b): pass

CONSTANT: float = 3.14

DATA_WITH_DETAILS: str = 'heyoo'

DATA_WITH_DETAILS_BUT_NO_SUMMARY_NEITHER_TYPE = None

DATA_DOCUMENTED_INSIDE_MODULE: float = 6.28
ANOTHER_DOCUMENTED_INSIDE_MODULE = 3
