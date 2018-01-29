#!/usr/bin/env python

#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>
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
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from dox2html5 import Trie, ResultMap, serialize_search_data

basedir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))/'js-test-data'

with open(basedir/'short.bin', 'wb') as f:
    f.write(b'')
with open(basedir/'wrong-magic.bin', 'wb') as f:
    f.write(b'MOS\0              ')
with open(basedir/'wrong-version.bin', 'wb') as f:
    f.write(b'MCS\1              ')
with open(basedir/'empty.bin', 'wb') as f:
    f.write(serialize_search_data(Trie(), ResultMap()))

trie = Trie()
map = ResultMap()

trie.insert("math", map.add("Math", "namespaceMath.html"))
index = map.add("Math::min(int, int)", "namespaceMath.html#min", suffix_length=8)
trie.insert("math::min()", index, lookahead_barriers=[4])
trie.insert("min()", index)
index = map.add("Math::Vector", "classMath_1_1Vector.html")
trie.insert("math::vector", index)
trie.insert("vector", index)
index = map.add("Math::Vector::min() const", "classMath_1_1Vector.html#min", suffix_length=6)
trie.insert("math::vector::min()", index, lookahead_barriers=[4, 12])
trie.insert("vector::min()", index, lookahead_barriers=[6])
trie.insert("min()", index)
index = map.add("Math::Range", "classMath_1_1Range.html")
trie.insert("math::range", index)
trie.insert("range", index)
index = map.add("Math::Range::min() const", "classMath_1_1Range.html#min", suffix_length=6)
trie.insert("math::range::min()", index, lookahead_barriers=[4, 11])
trie.insert("range::min()", index, lookahead_barriers=[5])
trie.insert("min()", index)
trie.insert("subpage", map.add("Page » Subpage", "subpage.html"))

with open(basedir/'searchdata.bin', 'wb') as f:
    f.write(serialize_search_data(trie, map))
with open(basedir/'searchdata.b85', 'wb') as f:
    f.write(base64.b85encode(serialize_search_data(trie, map), True))
