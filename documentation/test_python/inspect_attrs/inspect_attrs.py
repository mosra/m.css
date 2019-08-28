from typing import List, Tuple

import attr

@attr.s
class MyClass:
    """A class with attr-defined properties"""

    annotated: float = attr.ib()
    unannotated = attr.ib(4)
    complex_annotation: List[Tuple[int, float]] = attr.ib(default=[])

    # Shouldn't be shown
    _hidden_property: float = attr.ib(3)

@attr.s(auto_attribs=True)
class MyClassAutoAttribs:
    """A class with automatic attr-defined properties"""

    annotated: float
    unannotated = 4
    complex_annotation: List[Tuple[int, float]] = []

@attr.s(auto_attribs=True, slots=True)
class MySlotClass:
    """A class with attr-defined slots"""

    annotated: float
    complex_annotation: List[Tuple[int, float]] = []
