from . import hidden
from . import _private_but_exposed

class HiddenClass:
    """A documented class not exposed in __all__"""
    pass

class _PrivateButExposedClass:
    # An undocumented class but exposed to
    pass

def hidden_func(a, b, c):
    """A documented function not exposed in __all__"""
    pass

def _private_but_exposed_func():
    # A private thing but exposed in __all__
    pass

hidden_data = 34

_private_data = 'Hey!'

__all__ = ['_private_but_exposed', '_PrivateButExposedClass', '_private_but_exposed_func', '_private_data']
