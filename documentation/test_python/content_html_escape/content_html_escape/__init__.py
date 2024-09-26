"""
Summary that should be <&> escaped <&>

Details that *aren't* rST-processed and thus should only be <&> escaped <&>.
"""

import enum

from . import pybind

# TODO page names can be escaped!

class Class:
    class ClassEnum(enum.Enum):
        VALUE_THAT_SHOULD_BE_ESCAPED = "<&>"

    @staticmethod
    def staticmethod(default_string_that_should_be_escaped = "<&>"):
        pass

    @classmethod
    def classmethod(cls, default_string_that_should_be_escaped = "<&>"):
        pass

    def __dunder_method__(self, default_string_that_should_be_escaped = "<&>"):
        pass

    def method(self, default_string_that_should_be_escaped = "<&>"):
        pass

    DATA_THAT_SHOULD_BE_ESCAPED = "<&>"

class Enum(enum.Enum):
    VALUE_THAT_SHOULD_BE_ESCAPED = "<&>"

def function(default_string_that_should_be_escaped = "<&>"):
    pass

DATA_THAT_SHOULD_BE_ESCAPED = "<&>"
