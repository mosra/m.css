import enum
from .sub import Foo as Bar

class AnEnum(enum.Enum):
    """An enum which is earlier than Bar, and with values that shouldn't be
    checked for duplicates because they don't have the .object property"""
    AAA = 3

__all__ = ['AnEnum', 'sub', 'Bar']
