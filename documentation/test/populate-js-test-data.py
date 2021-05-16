#!/usr/bin/env python3

#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020 Vladimír Vondruš <mosra@centrum.cz>
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

import base64
import os
import sys
import pathlib
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from _search_test_metadata import EntryType, search_type_map
from _search import Trie, ResultMap, ResultFlag, serialize_search_data, search_data_header_struct

basedir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))/'js-test-data'

# Basic error handling

with open(basedir/'short.bin', 'wb') as f:
    f.write(b'#'*(search_data_header_struct.size - 1))
with open(basedir/'wrong-magic.bin', 'wb') as f:
    f.write(b'MOS\1                      ')
with open(basedir/'wrong-version.bin', 'wb') as f:
    f.write(b'MCS\0                      ')
with open(basedir/'empty.bin', 'wb') as f:
    f.write(serialize_search_data(Trie(), ResultMap(), [], 0))

# General test

trie = Trie()
map = ResultMap()

trie.insert("math", map.add("Math", "namespaceMath.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)))
index = map.add("Math::min(int, int)", "namespaceMath.html#min", suffix_length=8, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC))
trie.insert("math::min()", index, lookahead_barriers=[4])
trie.insert("min()", index)
index = map.add("Math::Vector", "classMath_1_1Vector.html", flags=ResultFlag.from_type(ResultFlag.DEPRECATED, EntryType.CLASS))
trie.insert("math::vector", index)
trie.insert("vector", index)
index = map.add("Math::Vector::min() const", "classMath_1_1Vector.html#min", suffix_length=6, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC))
trie.insert("math::vector::min()", index, lookahead_barriers=[4, 12])
trie.insert("vector::min()", index, lookahead_barriers=[6])
trie.insert("min()", index)
range_index = map.add("Math::Range", "classMath_1_1Range.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))
trie.insert("math::range", range_index)
trie.insert("range", range_index)
index = map.add("Math::Range::min() const", "classMath_1_1Range.html#min", suffix_length=6, flags=ResultFlag.from_type(ResultFlag.DELETED, EntryType.FUNC))
trie.insert("math::range::min()", index, lookahead_barriers=[4, 11])
trie.insert("range::min()", index, lookahead_barriers=[5])
trie.insert("min()", index)
trie.insert("page", map.add("Page", "page.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.PAGE)))
index = map.add("Page » Subpage", "subpage.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.PAGE))
trie.insert("page » subpage", index, lookahead_barriers=[4])
trie.insert("subpage", index)

trie.insert("rectangle", map.add("Rectangle", "", alias=range_index))
trie.insert("rect", map.add("Rectangle::Rect()", "", suffix_length=2, alias=range_index))

with open(basedir/'searchdata.bin', 'wb') as f:
    f.write(serialize_search_data(trie, map, search_type_map, 7))
with open(basedir/'searchdata.b85', 'wb') as f:
    f.write(base64.b85encode(serialize_search_data(trie, map, search_type_map, 7), True))

# UTF-8 names

trie = Trie()
map = ResultMap()

trie.insert("hýždě", map.add("Hýždě", "#a", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.PAGE)))
trie.insert("hárá", map.add("Hárá", "#b", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.PAGE)))

with open(basedir/'unicode.bin', 'wb') as f:
    f.write(serialize_search_data(trie, map, search_type_map, 2))

# Heavy prefix nesting

trie = Trie()
map = ResultMap()

trie.insert("magnum", map.add("Magnum", "namespaceMagnum.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)))
trie.insert("math", map.add("Magnum::Math", "namespaceMagnum_1_1Math.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)))
trie.insert("geometry", map.add("Magnum::Math::Geometry", "namespaceMagnum_1_1Math_1_1Geometry.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)))
trie.insert("range", map.add("Magnum::Math::Range", "classMagnum_1_1Math_1_1Range.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)))

with open(basedir/'nested.bin', 'wb') as f:
    f.write(serialize_search_data(trie, map, search_type_map, 4))

# Extreme amount of search results (Python's __init__, usually)

trie = Trie()
map = ResultMap()

for i in range(128):
    trie.insert("__init__", map.add(f"Foo{i}.__init__(self)", f"Foo{i}.html#__init__", suffix_length=6, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC)))

# It's __init_subclass__, but here I want to trigger the case of both a high
# amount of results and some children as well.
for i in [3, 15, 67]:
    trie.insert("__init__subclass__", map.add(f"Foo{i}.__init__subclass__(self)", f"Foo{i}.html#__init__subclass__", suffix_length=6, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC)))

with open(basedir/'manyresults.bin', 'wb') as f:
    f.write(serialize_search_data(trie, map, search_type_map, 128 + 3))
