"""Annotation parsing. For links inside annotations see test_inspect.TypeLinks."""

import sys

from typing import List, Tuple, Dict, Any, Union, Optional, Callable, TypeVar, Generic, Iterator

class Foo:
    """A class with properties"""

    @property
    def a_property(self) -> List[bool]:
        """A property with a type annotation"""
        pass

class FooSlots:
    """A class with slots"""

    __slots__ = ['unannotated', 'annotated']

    annotated: List[str]

_T = TypeVar('Tp')

# Triggers a corner case with _gorg on Py3.6 (the member has to be ignored).
# AContainer2 is not derived directly from Generic but has _gorg also.
# Additionally, on Py3.6 these classes will have a __next_in_mro__ member,
# which should be ignored as well
class AContainer(Generic[_T]):
    """A generic class. No parent class info extracted yet."""
class AContainer2(Iterator):
    """Another class derived from a typing thing."""

def annotation(param: List[int], another: bool, third: str = "hello") -> float:
    """An annotated function"""
    pass

def annotation_strings(param: 'List[int]', another: 'bool', third: 'str' = "hello") -> 'float':
    """Annotated using strings, should result in exactly the same as annotation()"""
    pass

def no_annotation(a, b, z):
    """Non-annotated function"""
    pass

def no_annotation_default_param(param, another, third = "hello"):
    """Non-annotated function with a default parameter"""
    pass

def partial_annotation(foo, param: Tuple[int, int], unannotated, cls: object):
    """Partially annotated function"""
    pass

def annotation_tuple_instead_of_tuple(a: (float, int)):
    """Annotation with a tuple instead of Tuple, ignored"""

def annotation_func_instead_of_type(a: open):
    """Annotation with a function instead of a type, ignored"""

def annotation_func_instead_of_type_nested(a: List[open], b: Callable[[open], str], c: Callable[[str], open]):
    """Annotations with nested problems, ignoring the whole thing"""

def annotation_any(a: Any):
    """Annotation with the Any type"""

def annotation_union(a: Union[float, int]):
    """Annotation with the Union type"""

def annotation_optional(a: Optional[float]):
    """Annotation with the Optional type"""

def annotation_union_second_bracketed(a: Union[float, List[int]]):
    """Annotation with the Union type and second type bracketed, where we can't use isinstance"""

def annotation_union_of_undefined(a: Union[int, 'something.Undefined']):
    """Annotation with an union that has an undefined type inside, where we can't use isinstance either"""

def annotation_list_noparam(a: List):
    """Annotation with the unparametrized List type. 3.7 and 3.8 adds an implicit TypeVar to it, 3.6, 3.9 and 3.10 not, so the output is different between the versions."""

def annotation_generic(a: List[_T]) -> _T:
    """Annotation with a generic type"""

def annotation_callable(a: Callable[[float, int], str]):
    """Annotation with the Callable type"""

def annotation_callable_no_args(a: Callable[[], Dict[int, float]]):
    """Annotation with the Callable type w/o arguments"""

def annotation_ellipsis(a: Callable[..., int], b: Tuple[str, ...]):
    """Annotation with ellipsis"""

# Only possible with native code now, https://www.python.org/dev/peps/pep-0570/
#def positionals_only(positional_only, /, positional_kw):
    #"""Function with explicitly delimited positional args"""
    #pass

def args_kwargs(a, b, *args, **kwargs):
    """Function with args and kwargs"""
    pass

def positional_keyword(positional_kw, *, kw_only):
    """Function with explicitly delimited keyword args"""
    pass

def annotated_positional_keyword(bar = False, *, foo: str, **kwargs):
    """Function with explicitly delimited keyword args and type annotations"""
    pass

def returns_none(a: Callable[[], None]) -> None:
    """In order to disambiguate between a missing return annotation and an
    annotated none, the None return annotation is kept, converted from NoneType
    to None"""

def returns_none_type(a: Callable[[], type(None)]) -> type(None):
    """And it should behave the same when using None or type(None)"""

UNANNOTATED_VAR = 3.45

ANNOTATED_VAR: Tuple[bool, str] = (False, 'No.')
