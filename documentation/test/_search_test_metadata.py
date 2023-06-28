#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023
#             Vladimír Vondruš <mosra@centrum.cz>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included
#   in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#   THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#

import enum

from _search import CssClass

# Taken from doxygen.py, with stuff that's unused in the generic tests removed.
# It's C++-specific but the implementation doesn't really care, actually ;)

class EntryType(enum.Enum):
    # Order must match the search_type_map below; first value is reserved for
    # ResultFlag.ALIAS
    PAGE = 1
    NAMESPACE = 2
    CLASS = 3
    FUNC = 4

# Order must match the EntryType above
search_type_map = [
    (CssClass.SUCCESS, "page"),
    (CssClass.PRIMARY, "namespace"),
    (CssClass.PRIMARY, "class"),
    (CssClass.INFO, "func")
]

# Tries don't store any strings, so name_size_bytes can be whatever
trie_type_sizes = [
    {'file_offset_bytes': 3,
     'result_id_bytes': 2,
     'name_size_bytes': 1},
    {'file_offset_bytes': 3,
     'result_id_bytes': 3,
     'name_size_bytes': 1},
    {'file_offset_bytes': 3,
     'result_id_bytes': 4,
     'name_size_bytes': 1},

    {'file_offset_bytes': 4,
     'result_id_bytes': 2,
     'name_size_bytes': 1},
    {'file_offset_bytes': 4,
     'result_id_bytes': 3,
     'name_size_bytes': 1},
    {'file_offset_bytes': 4,
     'result_id_bytes': 4,
     'name_size_bytes': 1},
]

type_sizes = trie_type_sizes + [
    {'file_offset_bytes': 3,
     'result_id_bytes': 2,
     'name_size_bytes': 2},
    {'file_offset_bytes': 3,
     'result_id_bytes': 3,
     'name_size_bytes': 2},
    {'file_offset_bytes': 3,
     'result_id_bytes': 4,
     'name_size_bytes': 2},

    {'file_offset_bytes': 4,
     'result_id_bytes': 2,
     'name_size_bytes': 2},
    {'file_offset_bytes': 4,
     'result_id_bytes': 3,
     'name_size_bytes': 2},
    {'file_offset_bytes': 4,
     'result_id_bytes': 4,
     'name_size_bytes': 2},
]
