# This file isn't included in m.css parsing, so its types are unknown, but it's
# still imported as a dependency and the type is correctly recognized as an
# enum type

import enum

class UnparsedEnumClass(enum.Enum):
    ...

class UnparsedEnumSubclass(enum.Enum):
    UNPARSED_VALUE = 1337
