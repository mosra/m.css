import enum

class MyEnum(enum.Enum):
    YAY = 2

class Foo:
    ...

AN_UNREPRESENTABLE_VALUE: ...

A_FALSE_VALUE = False

A_NONE_VALUE = None

A_ZERO_VALUE = 0

ENUM_THING = MyEnum.YAY

LARGE_VALUE_WILL_BE_AN_ELLIPSIS = ...

def basics(string_param = 'string', tuple_param = (3, 5), float_param = 1.2, unrepresentable_param = ...):
    ...

def setup_callback(unknown_function_is_an_ellipsis = ..., builtin_function_is_an_ellipsis = ..., lambda_is_an_ellipsis = ...):
    ...
