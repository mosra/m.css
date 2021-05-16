"""Value and default argument formatting"""

import enum

def basics(string_param = "string", tuple_param = (3, 5), float_param = 1.2):
    pass

def setup_callback(callback = basics):
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

# This value is too long and should be completely omitted
LARGE_VALUE_WILL_BE_AN_ELLIPSIS = """Lorem ipsum dolor sit amet, consectetur
    adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
    magna aliqua."""
