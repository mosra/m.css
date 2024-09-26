import abc
import email.mime.audio
import enum
import json.decoder
import logging
import typing
import unittest.loader
import unparsed_enum_module
from . import sub

class RootEnum(enum.Enum):
    A_VALUE = 3

class Root:
    CLASS_VALUE_REFERENCING_MODULE_ITSELF: Root = RootEnum.A_VALUE

    def method(self, library_type_alias: abc.ABC, builtin: float, external_enum_value = unparsed_enum_module.UnparsedEnumSubclass.UNPARSED_VALUE) -> json.decoder.JSONDecodeError:
        ...

    @property
    def prop(self) -> logging.Logger:
        ...

VALUE_TYPE: typing.Optional[unittest.loader.TestLoader] = None

def function(should_only_bring_import_sub: sub.Type.InnerClass) -> email.mime.audio.MIMEAudio:
    ...
