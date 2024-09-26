import typing

class MyClass:
    plain_data: float = 35

    def __init__(self, annotated: float, unannotated = 4, complex_annotation: typing.List[typing.Tuple[int, float]] = [], complex_annotation_in_attr: typing.List[typing.Tuple[int, float]] = [], hidden_property: float = 3) -> None:
        ...

    @property
    def annotated(self) -> float:
        ...
    @annotated.setter
    def annotated(self, value: float):
        ...
    @annotated.deleter
    def annotated(self):
        ...

    @property
    def complex_annotation(self) -> typing.List[typing.Tuple[int, float]]:
        ...
    @complex_annotation.setter
    def complex_annotation(self, value: typing.List[typing.Tuple[int, float]]):
        ...
    @complex_annotation.deleter
    def complex_annotation(self):
        ...

    @property
    def unannotated(self):
        ...
    @unannotated.setter
    def unannotated(self, value):
        ...
    @unannotated.deleter
    def unannotated(self):
        ...

    @property
    def complex_annotation_in_attr(self) -> typing.List[typing.Tuple[int, float]]:
        ...
    @complex_annotation_in_attr.setter
    def complex_annotation_in_attr(self, value: typing.List[typing.Tuple[int, float]]):
        ...
    @complex_annotation_in_attr.deleter
    def complex_annotation_in_attr(self):
        ...

class MyClassAutoAttribs:
    unannotated = 4

    def __init__(self, annotated: float, complex_annotation: typing.List[typing.Tuple[int, float]] = []) -> None:
        ...

    @property
    def annotated(self) -> float:
        ...
    @annotated.setter
    def annotated(self, value: float):
        ...
    @annotated.deleter
    def annotated(self):
        ...

    @property
    def complex_annotation(self) -> typing.List[typing.Tuple[int, float]]:
        ...
    @complex_annotation.setter
    def complex_annotation(self, value: typing.List[typing.Tuple[int, float]]):
        ...
    @complex_annotation.deleter
    def complex_annotation(self):
        ...

class MySlotClass:
    def __init__(self, annotated: float, complex_annotation: typing.List[typing.Tuple[int, float]] = [], complex_annotation_in_attr: typing.List[typing.Tuple[int, float]] = []) -> None:
        ...

    @property
    def annotated(self) -> float:
        ...
    @annotated.setter
    def annotated(self, value: float):
        ...
    @annotated.deleter
    def annotated(self):
        ...

    @property
    def complex_annotation(self) -> typing.List[typing.Tuple[int, float]]:
        ...
    @complex_annotation.setter
    def complex_annotation(self, value: typing.List[typing.Tuple[int, float]]):
        ...
    @complex_annotation.deleter
    def complex_annotation(self):
        ...

    @property
    def complex_annotation_in_attr(self) -> typing.List[typing.Tuple[int, float]]:
        ...
    @complex_annotation_in_attr.setter
    def complex_annotation_in_attr(self, value: typing.List[typing.Tuple[int, float]]):
        ...
    @complex_annotation_in_attr.deleter
    def complex_annotation_in_attr(self):
        ...
