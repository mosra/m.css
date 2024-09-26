import typing

@typing.overload
def overloaded(arg0: int, /) -> str:
    ...

@typing.overload
def overloaded(arg0: float, /) -> bool:
    ...
