from typing import List, Tuple

import attr

@attr.s
class MyClass:
    """A class with attr-defined properties"""

    annotated: float = attr.ib()
    unannotated = attr.ib(4)
    complex_annotation: List[Tuple[int, float]] = attr.ib(default=[])
    complex_annotation_in_attr = attr.ib(default=[], type=List[Tuple[int, float]])

    # This is just data
    plain_data: float = 35

    # Shouldn't be shown
    _hidden_property: float = attr.ib(3)

@attr.s(auto_attribs=True)
class MyClassAutoAttribs:
    """A class with automatic attr-defined properties"""

    annotated: float
    unannotated = 4
    complex_annotation: List[Tuple[int, float]] = []

@attr.s(slots=True)
class MySlotClass:
    """A class with attr-defined slots"""

    annotated: float = attr.ib()
    complex_annotation: List[Tuple[int, float]] = attr.ib(default=[])
    complex_annotation_in_attr = attr.ib(default=[], type=List[Tuple[int, float]])
