import typing

def log(*args):
    ...

@typing.overload
def overload(arg0: int, /) -> None:
    ...

@typing.overload
def overload(*args):
    ...

@typing.overload
def overload(*args):
    ...

@typing.overload
def overload2(arg0: int, /) -> None:
    ...

@typing.overload
def overload2(*args):
    ...

@typing.overload
def overload2(*args):
    ...
