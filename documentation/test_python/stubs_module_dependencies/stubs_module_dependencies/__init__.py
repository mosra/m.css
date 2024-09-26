import unparsed_enum_module
import enum
from . import sub, pybind
import json
import logging
import email.mime.audio
import abc
import typing
import unittest

# The enum dependency is handled explitcitly in the code
class RootEnum(enum.Enum):
    A_VALUE = 3

class Root:
    # is a string as it'd lead to a circular import otherwise
    CLASS_VALUE_REFERENCING_MODULE_ITSELF: 'Root' = RootEnum.A_VALUE

    def method(self, library_type_alias: abc.ABC, builtin: float, external_enum_value = unparsed_enum_module.UnparsedEnumSubclass.UNPARSED_VALUE) -> json.decoder.JSONDecodeError:
        ...

    @property
    def prop(self) -> logging.Logger:
        ...

# The typing dependency is handled explitcitly in the code
VALUE_TYPE: typing.Optional[unittest.TestLoader] = None

def function(should_only_bring_import_sub: sub.Type.InnerClass) -> email.mime.audio.MIMEAudio:
    ...
