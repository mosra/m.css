import enum

class Enum(enum.Enum):
    VALUE_THAT_SHOULD_BE_ESCAPED = '<&>'

class Class:
    class ClassEnum(enum.Enum):
        VALUE_THAT_SHOULD_BE_ESCAPED = '<&>'

    DATA_THAT_SHOULD_BE_ESCAPED = '<&>'

    @staticmethod
    def staticmethod(default_string_that_should_be_escaped = '<&>'):
        ...

    @classmethod
    def classmethod(default_string_that_should_be_escaped = '<&>'):
        ...

    def method(self, default_string_that_should_be_escaped = '<&>'):
        ...

    def __dunder_method__(self, default_string_that_should_be_escaped = '<&>'):
        ...

DATA_THAT_SHOULD_BE_ESCAPED = '<&>'

def function(default_string_that_should_be_escaped = '<&>'):
    ...
