import typing

class AContainer:
    def __new__(cls, *args, **kwds):
        ...

class AContainer2:
    def __iter__(self):
        ...

    def __new__(cls, *args, **kwds):
        ...

    def __next__(self):
        ...

    @classmethod
    def __subclasshook__(C):
        ...

class Foo:
    @property
    def a_property(self) -> typing.List[bool]:
        ...

class FooSlots:
    @property
    def annotated(self) -> typing.List[str]:
        ...
    @annotated.setter
    def annotated(self, value: typing.List[str]):
        ...
    @annotated.deleter
    def annotated(self):
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

ANNOTATED_VAR: typing.Tuple[bool, str] = (False, 'No.')

UNANNOTATED_VAR = 3.45

def annotated_positional_keyword(bar = False, *, foo: str, **kwargs):
    ...

def annotation(param: typing.List[int], another: bool, third: str = 'hello') -> float:
    ...

def annotation_any(a: typing.Any):
    ...

def annotation_callable(a: typing.Callable[[float, int], str]):
    ...

def annotation_callable_no_args(a: typing.Callable[[], typing.Dict[int, float]]):
    ...

def annotation_ellipsis(a: typing.Callable[[...], int], b: typing.Tuple[str, ...]):
    ...

def annotation_func_instead_of_type(a):
    ...

def annotation_func_instead_of_type_nested(a, b, c):
    ...

def annotation_generic(a: typing.List['Tp']) -> 'Tp':
    ...

def annotation_invalid() -> 'Foo.Bar':
    ...

def annotation_list_noparam(a: typing.List['T']):
    ...

def annotation_optional(a: typing.Optional[float]):
    ...

def annotation_strings(param: typing.List[int], another: bool, third: str = 'hello') -> float:
    ...

def annotation_tuple_instead_of_tuple(a):
    ...

def annotation_union(a: typing.Union[float, int]):
    ...

def annotation_union_of_forward_reference(a: typing.Union[int, 'something.Undefined']):
    ...

def annotation_union_second_bracketed(a: typing.Union[float, typing.List[int]]):
    ...

def args_kwargs(a, b, *args, **kwargs):
    ...

def no_annotation(a, b, z):
    ...

def no_annotation_default_param(param, another, third = 'hello'):
    ...

def partial_annotation(foo, param: typing.Tuple[int, int], unannotated, cls: object):
    ...

def positional_keyword(positional_kw, *, kw_only):
    ...

def returns_none(a: typing.Callable[[], None]) -> None:
    ...

def returns_none_type(a: typing.Callable[[], None]) -> None:
    ...
