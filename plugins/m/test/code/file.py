"""
`"Sphinx Gallery"-alike self-contained code file`_
--------------------------------------------------
"""

# Running sphx_glr_python_to_jupyter.py on this file will produce a ipynb
# version of the same (modulo bugs, which there's several of).

import math

#%%
# This is a reST markup explaining the following code, with the initial
# ``#<space>`` stripped, and on blank lines only the ``#`` stripped:
#
## However in this case both leading ``##`` will be kept.
#
# The ``math.sin()`` calculates a sin, *of course*, and the initial indentation
# of it is stripped also:
#

def foo():
# [yay-code]
    sin = math.sin(0.13587)
    two_sins = sin + sin
# [/yay-code]
