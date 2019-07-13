"""Second module, imported as inspect_recursive.a, with no contents"""

import inspect_recursive.first as a

import sys

if sys.version_info >= (3, 7):
    # For some reason 3.6 says second doesn't exist yet. I get that, it's a
    # cyclic reference, but that works in 3.7.
    import inspect_recursive.second as b

from inspect_recursive import Foo as Bar
