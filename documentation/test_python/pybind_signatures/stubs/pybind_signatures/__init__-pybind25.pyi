import datetime
import typing

class MyClass:
    @staticmethod
    def static_function(arg0: int, arg1: float, /) -> MyClass:
        ...

    def another(self, /) -> int:
        ...

    def instance_function(self, arg0: int, arg1: str, /) -> tuple[float, int]:
        ...

    def instance_function_kwargs(self, hey: int, what: str = '<eh?>') -> tuple[float, int]:
        ...

    def __init__(self, /) -> None:
        ...

    @property
    def bar(self) -> float:
        ...

    @property
    def foo(self) -> float:
        ...
    @foo.setter
    def foo(self, value: float):
        ...

class Pybind23:
    is_pybind23 = True

    @property
    def writeonly(self) -> float:
        ...
    @writeonly.setter
    def writeonly(self, value: float):
        ...

    @property
    def writeonly_crazy(self):
        ...
    @writeonly_crazy.setter
    def writeonly_crazy(self, value):
        ...

class Pybind26:
    is_pybind26 = False

class Pybind27:
    is_pybind27 = False

def crazy_signature(*args):
    ...

def date_time(arg0: datetime.datetime, arg1: datetime.timedelta, /) -> None:
    ...

def default_unrepresentable_argument(a: MyClass = ...) -> None:
    ...

def duck(*args, **kwargs) -> None:
    ...

def escape_docstring(arg0: int, /) -> None:
    ...

def failed_parse_docstring(*args):
    ...

def full_docstring(arg0: int, /) -> None:
    ...

@typing.overload
def full_docstring_overloaded(arg0: int, arg1: int, /) -> None:
    ...

@typing.overload
def full_docstring_overloaded(arg0: float, arg1: float, /) -> None:
    ...

@typing.overload
def overloaded(arg0: int, /) -> str:
    ...

@typing.overload
def overloaded(arg0: float, /) -> bool:
    ...

def scale(arg0: int, arg1: float, /) -> int:
    ...

def scale_kwargs(a: int, argument: float) -> int:
    ...

def takes_a_function(arg0: typing.Callable[[float, list[float]], int], /) -> None:
    ...

def takes_a_function_returning_none(arg0: typing.Callable[[], None], /) -> None:
    ...

def taking_a_list_returning_a_tuple(arg0: list[float], /) -> tuple[int, int, int]:
    ...

@typing.overload
def tenOverloads(arg0: float, arg1: float, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: int, arg1: float, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: bool, arg1: float, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: float, arg1: int, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: int, arg1: int, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: bool, arg1: int, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: float, arg1: bool, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: int, arg1: bool, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: bool, arg1: bool, /) -> None:
    ...

@typing.overload
def tenOverloads(arg0: str, arg1: str, /) -> None:
    ...

def void_function(arg0: int, /) -> None:
    ...
