import another_module
import unparsed_enum_module
import unparsed_module
from . import *
from .. import *

class EnumSubclass(unparsed_enum_module.UnparsedEnumClass):
    A_VALUE = 36

def all_should_be_the_same_relative_type(a: Type, b: Type, c: Type):
    ...

def foo(type_three_levels_up: Root, unparsed_type: unparsed_module.UnparsedName, enum = RootEnum.A_VALUE) -> another_module.Another:
    ...
