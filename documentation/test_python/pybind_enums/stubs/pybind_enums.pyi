import enum

class MyEnum(enum.Enum):
    First = 0
    Second = 1
    Third = 74
    CONSISTANTE = -5

class SixtyfourBitFlag(enum.Enum):
    Yes = 1000000000000
    No = 18446744073709551615
