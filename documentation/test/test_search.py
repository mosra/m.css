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

import os
import sys
import unittest
from types import SimpleNamespace as Empty

from ._search_test_metadata import EntryType, search_type_map
from _search import Trie, ResultMap, ResultFlag, serialize_search_data, pretty_print_trie, pretty_print_map, pretty_print, searchdata_filename

from test_doxygen import IntegrationTestCase

class TrieSerialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print_trie(serialized)[0]
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test_empty(self):
        trie = Trie()

        serialized = trie.serialize()
        self.compare(serialized, "")
        self.assertEqual(len(serialized), 6)

    def test_single(self):
        trie = Trie()
        trie.insert("magnum", 1337)
        trie.insert("magnum", 21)

        serialized = trie.serialize()
        self.compare(serialized, """
magnum [1337, 21]
""")
        self.assertEqual(len(serialized), 46)

    def test_multiple(self):
        trie = Trie()

        trie.insert("math", 0)
        trie.insert("math::vector", 1, lookahead_barriers=[4])
        trie.insert("vector", 1)
        trie.insert("math::range", 2)
        trie.insert("range", 2)

        trie.insert("math::min", 3)
        trie.insert("min", 3)
        trie.insert("math::max", 4)
        trie.insert("max", 4)
        trie.insert("math::minmax", 5)
        trie.insert("minmax", 5)

        trie.insert("math::vector::minmax", 6, lookahead_barriers=[4, 12])
        trie.insert("vector::minmax", 6, lookahead_barriers=[6])
        trie.insert("minmax", 6)
        trie.insert("math::vector::min", 7)
        trie.insert("vector::min", 7)
        trie.insert("min", 7)
        trie.insert("math::vector::max", 8)
        trie.insert("vector::max", 8)
        trie.insert("max", 8)

        trie.insert("math::range::min", 9, lookahead_barriers=[4, 11])
        trie.insert("range::min", 9, lookahead_barriers=[5])
        trie.insert("min", 9)

        trie.insert("math::range::max", 10)
        trie.insert("range::max", 10)
        trie.insert("max", 10)

        serialized = trie.serialize()
        self.compare(serialized, """
math [0]
||| :$
|||  :vector [1]
|||   |     :$
|||   |      :min [7]
|||   |        | max [6]
|||   |        ax [8]
|||   range [2]
|||   |    :$
|||   |     :min [9]
|||   |       ax [10]
|||   min [3]
|||   || max [5]
|||   |ax [4]
||x [4, 8, 10]
|in [3, 7, 9]
|| max [5, 6]
vector [1]
|     :$
|      :min [7]
|        | max [6]
|        ax [8]
range [2]
|    :$
|     :min [9]
|       ax [10]
""")
        self.assertEqual(len(serialized), 340)

    def test_unicode(self):
        trie = Trie()

        trie.insert("hýždě", 0)
        trie.insert("hárá", 1)

        serialized = trie.serialize()
        self.compare(serialized, """
h0xc3
  0xbd
   0xc5
  | 0xbe
  |  d0xc4
  |    0x9b
  |      [0]
  0xa1
   r0xc3
  |  0xa1
  |    [1]
""")
        self.assertEqual(len(serialized), 82)

class MapSerialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print_map(serialized, entryTypeClass=EntryType)
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test_empty(self):
        map = ResultMap()

        serialized = map.serialize()
        self.compare(serialized, "")
        self.assertEqual(len(serialized), 4)

    def test_single(self):
        map = ResultMap()
        self.assertEqual(map.add("Magnum", "namespaceMagnum.html", suffix_length=11, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)), 0)

        serialized = map.serialize()
        self.compare(serialized, """
0: Magnum [suffix_length=11, type=NAMESPACE] -> namespaceMagnum.html
""")
        self.assertEqual(len(serialized), 36)

    def test_multiple(self):
        map = ResultMap()

        self.assertEqual(map.add("Math", "namespaceMath.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)), 0)
        self.assertEqual(map.add("Math::Vector", "classMath_1_1Vector.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)), 1)
        self.assertEqual(map.add("Math::Range", "classMath_1_1Range.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)), 2)
        self.assertEqual(map.add("Math::min()", "namespaceMath.html#abcdef2875", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC)), 3)
        self.assertEqual(map.add("Math::max(int, int)", "namespaceMath.html#abcdef1234", suffix_length=8, flags=ResultFlag.from_type(ResultFlag.DEPRECATED|ResultFlag.DELETED, EntryType.FUNC)), 4)
        self.assertEqual(map.add("Rectangle", "", alias=2), 5)
        self.assertEqual(map.add("Rectangle::Rect()", "", suffix_length=2, alias=2), 6)

        serialized = map.serialize()
        self.compare(serialized, """
0: Math [type=NAMESPACE] -> namespaceMath.html
1: ::Vector [prefix=0[:0], type=CLASS] -> classMath_1_1Vector.html
2: ::Range [prefix=0[:0], type=CLASS] -> classMath_1_1Range.html
3: ::min() [prefix=0[:18], type=FUNC] -> #abcdef2875
4: ::max(int, int) [prefix=0[:18], suffix_length=8, deprecated, deleted, type=FUNC] -> #abcdef1234
5: Rectangle [alias=2] ->
6: ::Rect() [alias=2, prefix=5[:0], suffix_length=2] ->
""")
        self.assertEqual(len(serialized), 203)

class Serialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test(self):
        trie = Trie()
        map = ResultMap()

        trie.insert("math", map.add("Math", "namespaceMath.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)))
        index = map.add("Math::Vector", "classMath_1_1Vector.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))
        trie.insert("math::vector", index)
        trie.insert("vector", index)
        index = map.add("Math::Range", "classMath_1_1Range.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))
        trie.insert("math::range", index)
        trie.insert("range", index)

        serialized = serialize_search_data(trie, map, search_type_map, 3)
        self.compare(serialized, """
3 symbols
math [0]
|   ::vector [1]
|     range [2]
vector [1]
range [2]
0: Math [type=NAMESPACE] -> namespaceMath.html
1: ::Vector [prefix=0[:0], type=CLASS] -> classMath_1_1Vector.html
2: ::Range [prefix=0[:0], type=CLASS] -> classMath_1_1Range.html
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.NAMESPACE, CssClass.PRIMARY, 'namespace'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.FUNC, CssClass.INFO, 'func')
""")
        self.assertEqual(len(serialized), 277)
