import sys
from math import log, pow

__all__ = ['pow', 'log']

# Signature with / for pow() is not present in 3.6 so it makes no sense to have
# it there.
if sys.version_info < (3, 7):
    __all__ = __all__[1:]
