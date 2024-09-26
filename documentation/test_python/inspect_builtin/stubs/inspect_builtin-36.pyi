class BaseException:
    def with_traceback(self, *args):
        ...

    def __reduce__(self, *args):
        ...

    def __setstate__(self, *args):
        ...

    @property
    def __cause__(self):
        ...

    @property
    def __context__(self):
        ...

    @property
    def args(self):
        ...

def log(*args):
    ...
