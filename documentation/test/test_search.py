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

import os
import sys
import unittest
from types import SimpleNamespace as Empty

from ._search_test_metadata import EntryType, search_type_map, trie_type_sizes, type_sizes
from _search import Trie, ResultMap, ResultFlag, Serializer, Deserializer, serialize_search_data, pretty_print_trie, pretty_print_map, pretty_print

from test_doxygen import IntegrationTestCase

class TrieSerialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, deserializer: Deserializer, serialized: bytes, expected: str):
        pretty = pretty_print_trie(deserializer, serialized)[0]
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test_empty(self):
        trie = Trie()

        for i in trie_type_sizes:
            with self.subTest(**i):
                serialized = trie.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, "")
                self.assertEqual(len(serialized), 6)

    def test_single(self):
        trie = Trie()
        trie.insert("magnum", 1337)
        trie.insert("magnum", 21)

        for i in trie_type_sizes:
            with self.subTest(**i):
                serialized = trie.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, """
magnum [1337, 21]
""")
                # Verify just the smallest and largest size, everything else
                # should fit in between
                if i['file_offset_bytes'] == 3 and i['result_id_bytes'] == 2:
                    self.assertEqual(len(serialized), 46)
                elif i['file_offset_bytes'] == 4 and i['result_id_bytes'] == 4:
                    self.assertEqual(len(serialized), 56)
                else:
                    self.assertGreater(len(serialized), 46)
                    self.assertLess(len(serialized), 56)

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

        for i in trie_type_sizes:
            with self.subTest(**i):
                serialized = trie.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, """
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
                # Verify just the smallest and largest size, everything else
                # should fit in between
                if i['file_offset_bytes'] == 3 and i['result_id_bytes'] == 2:
                    self.assertEqual(len(serialized), 340)
                elif i['file_offset_bytes'] == 4 and i['result_id_bytes'] == 4:
                    self.assertEqual(len(serialized), 428)
                else:
                    self.assertGreater(len(serialized), 340)
                    self.assertLess(len(serialized), 428)

    def test_unicode(self):
        trie = Trie()

        trie.insert("hýždě", 0)
        trie.insert("hárá", 1)

        serialized = trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))
        self.compare(Deserializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1), serialized, """
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

    def test_16bit_result_count(self):
        trie = Trie()

        for i in range(128):
            trie.insert("__init__", i)
        # It's __init_subclass__ (one underscore, not two), but here I want to
        # trigger the case of both a high amount of results and some children
        # as well.
        for i in [203, 215, 267]:
            trie.insert("__init__subclass__", i)

        for i in trie_type_sizes:
            with self.subTest(**i):
                serialized = trie.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, """
__init__ [{}]
        subclass__ [203, 215, 267]
""".format(', '.join([str(i) for i in range(128)])))
                # Verify just the smallest and largest size, everything else
                # should fit in between
                if i['file_offset_bytes'] == 3 and i['result_id_bytes'] == 2:
                    self.assertEqual(len(serialized), 377)
                elif i['file_offset_bytes'] == 4 and i['result_id_bytes'] == 4:
                    self.assertEqual(len(serialized), 657)
                else:
                    self.assertGreater(len(serialized), 377)
                    self.assertLess(len(serialized), 657)

    def test_16bit_result_id_too_small(self):
        trie = Trie()
        trie.insert("a", 65536)
        with self.assertRaisesRegex(OverflowError, "Trie result ID too large to store in 16 bits, set SEARCH_RESULT_ID_BYTES = 3 in your conf.py."):
            trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=3, name_size_bytes=1))

    def test_24bit_result_id_too_small(self):
        trie = Trie()
        trie.insert("a", 16*1024*1024)
        with self.assertRaisesRegex(OverflowError, "Trie result ID too large to store in 24 bits, set SEARCH_RESULT_ID_BYTES = 4 in your conf.py."):
            trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=3, name_size_bytes=1))

        # This should work
        trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=4, name_size_bytes=1))

    def test_23bit_file_offset_too_small(self):
        trie = Trie()

        # The high bit of the child offset stores a lookahead barrier, so the
        # file has to be smaller than 8M, not 16. Python has a recursion limit
        # of 1000, so we can't really insert a 8M character long string.
        # Instead, insert one 130-character string where each char has 32k
        # 16bit result IDs. 129 isn't enough to overflow the offsets.
        results_32k = [j for j in range(32767)]
        for i in range(130):
            trie.insert('a'*i, results_32k)

        with self.assertRaisesRegex(OverflowError, "Trie child offset too large to store in 23 bits, set SEARCH_FILE_OFFSET_BYTES = 4 in your conf.py."):
            trie.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        trie.serialize(Serializer(file_offset_bytes=4, result_id_bytes=2, name_size_bytes=1))

class MapSerialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, deserializer: Deserializer, serialized: bytes, expected: str):
        pretty = pretty_print_map(deserializer, serialized, entryTypeClass=EntryType)
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test_empty(self):
        map = ResultMap()

        for i in type_sizes:
            with self.subTest(**i):
                serialized = map.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, "")
                self.assertEqual(len(serialized), i['file_offset_bytes'])

    def test_single(self):
        map = ResultMap()

        self.assertEqual(map.add("Magnum", "namespaceMagnum.html", suffix_length=11, flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)), 0)

        for i in type_sizes:
            with self.subTest(**i):
                serialized = map.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, """
0: Magnum [suffix_length=11, type=NAMESPACE] -> namespaceMagnum.html
""")
                # Verify just the smallest and largest size, everything else
                # should fit in between. The `result_id_bytes` don't affect
                # this case.
                if i['file_offset_bytes'] == 3 and i['name_size_bytes'] == 1:
                    self.assertEqual(len(serialized), 35)
                elif i['file_offset_bytes'] == 4 and i['name_size_bytes'] == 2:
                    self.assertEqual(len(serialized), 38)
                else:
                    self.assertGreater(len(serialized), 35)
                    self.assertLess(len(serialized), 38)

    def test_multiple(self):
        map = ResultMap()

        self.assertEqual(map.add("Math", "namespaceMath.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.NAMESPACE)), 0)
        self.assertEqual(map.add("Math::Vector", "classMath_1_1Vector.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)), 1)
        self.assertEqual(map.add("Math::Range", "classMath_1_1Range.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)), 2)
        self.assertEqual(map.add("Math::min()", "namespaceMath.html#abcdef2875", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC)), 3)
        self.assertEqual(map.add("Math::max(int, int)", "namespaceMath.html#abcdef1234", suffix_length=8, flags=ResultFlag.from_type(ResultFlag.DEPRECATED|ResultFlag.DELETED, EntryType.FUNC)), 4)
        self.assertEqual(map.add("Rectangle", "", alias=2), 5)
        self.assertEqual(map.add("Rectangle::Rect()", "", suffix_length=2, alias=2), 6)

        for i in type_sizes:
            with self.subTest(**i):
                serialized = map.serialize(Serializer(**i))
                self.compare(Deserializer(**i), serialized, """
0: Math [type=NAMESPACE] -> namespaceMath.html
1: ::Vector [prefix=0[:0], type=CLASS] -> classMath_1_1Vector.html
2: ::Range [prefix=0[:0], type=CLASS] -> classMath_1_1Range.html
3: ::min() [prefix=0[:18], type=FUNC] -> #abcdef2875
4: ::max(int, int) [prefix=0[:18], suffix_length=8, deprecated, deleted, type=FUNC] -> #abcdef1234
5: Rectangle [alias=2] ->
6: ::Rect() [alias=2, prefix=5[:0], suffix_length=2] ->
""")
                # Verify just the smallest and largest size, everything else
                # should fit in between
                if i['file_offset_bytes'] == 3 and i['result_id_bytes'] == 2 and i['name_size_bytes'] == 1:
                    self.assertEqual(len(serialized), 202)
                elif i['file_offset_bytes'] == 4 and i['result_id_bytes'] == 4 and i['name_size_bytes'] == 2:
                    self.assertEqual(len(serialized), 231)
                else:
                    self.assertGreater(len(serialized), 202)
                    self.assertLess(len(serialized), 231)

    def test_24bit_file_offset_too_small(self):
        map = ResultMap()
        # 3 bytes for the initial offset, 3 bytes for file size, 1 byte for the
        # flags, 1 byte for the null terminator, 6 bytes for the URL
        map.add('F'*(16*1024*1024 - 14), 'f.html', flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))

        with self.assertRaisesRegex(OverflowError, "Result map offset too large to store in 24 bits, set SEARCH_FILE_OFFSET_BYTES = 4 in your conf.py."):
            # Disabling prefix merging otherwise memory usage goes to hell
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1), merge_prefixes=False)

        # This should work. Disabling prefix merging otherwise memory usage
        # goes to hell.
        map.serialize(Serializer(file_offset_bytes=4, result_id_bytes=2, name_size_bytes=1), merge_prefixes=False)

    def test_8bit_suffix_length_too_small(self):
        map = ResultMap()
        map.add("F()" + ';'*256, "f.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC), suffix_length=256)

        with self.assertRaisesRegex(OverflowError, "Result map suffix length too large to store in 8 bits, set SEARCH_NAME_SIZE_BYTES = 2 in your conf.py."):
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=2))

    def test_8bit_prefix_length_too_small(self):
        map = ResultMap()
        map.add("A", 'a'*251 + ".html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))
        map.add("A::foo()", 'a'*251 + ".html#foo", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC))

        with self.assertRaisesRegex(OverflowError, "Result map prefix length too large to store in 8 bits, set SEARCH_NAME_SIZE_BYTES = 2 in your conf.py."):
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=2))

    def test_16bit_prefix_id_too_small(self):
        map = ResultMap()

        # Adding A0 to A65535 would be too slow due to the recursive Trie
        # population during prefix merging (SIGH) so trying this instead. It's
        # still hella slow, but at least not TWO MINUTES.
        for i in range(128):
            for j in range(128):
                for k in range(4):
                    map.add(bytes([i, j, k]).decode('utf-8'), "a.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS))

        self.assertEqual(map.add("B", "b.html", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.CLASS)), 65536)
        map.add("B::foo()", "b.html#foo", flags=ResultFlag.from_type(ResultFlag.NONE, EntryType.FUNC))

        with self.assertRaisesRegex(OverflowError, "Result map prefix ID too large to store in 16 bits, set SEARCH_RESULT_ID_BYTES = 3 in your conf.py."):
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=3, name_size_bytes=1))

        # Testing this error for a 24bit prefix seems infeasibly slow, not
        # doing that

    def test_16bit_alias_id_too_small(self):
        map = ResultMap()

        # The alias doesn't exist of course, hopefully that's fine in this case
        map.add("B", "", alias=65536)

        with self.assertRaisesRegex(OverflowError, "Result map alias ID too large to store in 16 bits, set SEARCH_RESULT_ID_BYTES = 3 in your conf.py."):
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=2, name_size_bytes=1))

        # This should work
        map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=3, name_size_bytes=1))

    def test_24bit_alias_id_too_small(self):
        map = ResultMap()

        # The alias doesn't exist of course, hopefully that's fine in this case
        map.add("B", "", alias=16*1024*1024)

        with self.assertRaisesRegex(OverflowError, "Result map alias ID too large to store in 24 bits, set SEARCH_RESULT_ID_BYTES = 4 in your conf.py."):
            map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=3, name_size_bytes=1))

        # This should work
        map.serialize(Serializer(file_offset_bytes=3, result_id_bytes=4, name_size_bytes=1))

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

        for i in type_sizes:
            with self.subTest(**i):
                serialized = serialize_search_data(Serializer(**i), trie, map, search_type_map, 3)
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
                # Verify just the smallest and largest size, everything else
                # should fit in between
                if i['file_offset_bytes'] == 3 and i['result_id_bytes'] == 2 and i['name_size_bytes'] == 1:
                    self.assertEqual(len(serialized), 282)
                elif i['file_offset_bytes'] == 4 and i['result_id_bytes'] == 4 and i['name_size_bytes'] == 2:
                    self.assertEqual(len(serialized), 317)
                else:
                    self.assertGreater(len(serialized), 282)
                    self.assertLess(len(serialized), 317)
