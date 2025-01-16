from math import log
from .pybind import *

# log() is like in inspect_builtin, but here testing behavior with the missing
# signatures affecting search data
__all__ = ['log', 'overload', 'overload2']
