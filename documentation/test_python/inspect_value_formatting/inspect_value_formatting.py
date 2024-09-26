"""Value and default argument formatting"""

import enum
import math
import os

class Foo:
    ...

def basics(string_param = "string", tuple_param = (3, 5), float_param = 1.2, unrepresentable_param = Foo()):
    pass

def setup_callback(unknown_function_is_an_ellipsis = os.path.join,
                   builtin_function_is_an_ellipsis = math.log,
                   lambda_is_an_ellipsis = lambda a: a):
    """Should produce a deterministic output."""
    pass

# TODO: not visible ATM, need to figure out interaction with __all__
DATA_DECLARATION: int

class MyEnum(enum.Enum):
    YAY = 2

ENUM_THING = MyEnum.YAY

# These should have their value shown in the docs as well, even though they are
# not true-ish
A_ZERO_VALUE = 0
A_FALSE_VALUE = False
A_NONE_VALUE = None
AN_UNREPRESENTABLE_VALUE = Foo()

# This value is too long and should be completely omitted
LARGE_VALUE_WILL_BE_AN_ELLIPSIS = """Lorem ipsum dolor sit amet, consectetur
    adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
    magna aliqua."""
