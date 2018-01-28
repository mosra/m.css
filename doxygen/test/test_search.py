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

import argparse
import os
import sys
import unittest
from types import SimpleNamespace as Empty

from dox2html5 import Trie, ResultMap, ResultFlag, serialize_search_data, search_data_header_struct

from test import IntegrationTestCase

def _pretty_print_trie(serialized: bytearray, hashtable, stats, base_offset, indent, draw_pipe, show_merged) -> str:
    # Visualize where the trees were merged
    if show_merged and base_offset in hashtable: return ' #'

    stats.node_count += 1

    out = ''
    size, value_count = Trie.header_struct.unpack_from(serialized, base_offset)
    stats.max_node_size = max(size, stats.max_node_size)
    stats.max_node_values = max(value_count, stats.max_node_values)
    offset = base_offset + Trie.header_struct.size

    # print values, if any
    if value_count:
        out += ' ['
        for i in range(value_count):
            if i: out += ', '
            value = Trie.value_struct.unpack_from(serialized, offset)[0]
            stats.max_node_value_index = max(value, stats.max_node_value_index)
            out += str(value)
            offset += Trie.value_struct.size
        out += ']'

    # print children
    if base_offset + size*2 - offset > 4: draw_pipe = True
    child_count = 0
    while offset < base_offset + size*2:
        if child_count or value_count:
            out += '\n'
            out += indent
        out += Trie.child_char_struct.unpack_from(serialized, offset + 3)[0].decode('utf-8')
        child_offset = Trie.child_struct.unpack_from(serialized, offset)[0] & 0x00ffffff
        stats.max_node_child_offset = max(child_offset, stats.max_node_child_offset)
        offset += Trie.child_struct.size
        out += _pretty_print_trie(serialized, hashtable, stats, child_offset, indent + ('|' if draw_pipe else ' '), draw_pipe=False, show_merged=show_merged)
        child_count += 1

    stats.max_node_children = max(child_count, stats.max_node_children)

    hashtable[base_offset] = True
    return out

def pretty_print_trie(serialized: bytes, show_merged=False):
    hashtable = {}

    stats = Empty()
    stats.node_count = 0
    stats.max_node_size = 0
    stats.max_node_values = 0
    stats.max_node_children = 0
    stats.max_node_value_index = 0
    stats.max_node_child_offset = 0

    out = _pretty_print_trie(serialized, hashtable, stats, Trie.root_offset_struct.unpack_from(serialized, 0)[0], '', draw_pipe=False, show_merged=show_merged)
    stats = """
node count:             {}
max node size:          {} bytes
max node values:        {}
max node children:      {}
max node value index:   {}
max node child offset:  {}""".lstrip().format(stats.node_count, stats.max_node_size*2, stats.max_node_values, stats.max_node_children, stats.max_node_value_index, stats.max_node_child_offset)
    return out, stats

def pretty_print_map(serialized: bytes):
    # The first item gives out offset of first value, which can be used to
    # calculate total value count
    offset = ResultMap.offset_struct.unpack_from(serialized, 0)[0] & 0x00ffffff
    size = int(offset/4 - 1)

    out = ''
    for i in range(size):
        if i: out += '\n'
        flags = ResultFlag(ResultMap.flags_struct.unpack_from(serialized, i*4 + 3)[0])
        extra = [str(int(flags.value))]
        if flags & ResultFlag.HAS_SUFFIX:
            extra += ['suffix_length={}'.format(ResultMap.suffix_length_struct.unpack_from(serialized, offset)[0])]
            offset += 1
        next_offset = ResultMap.offset_struct.unpack_from(serialized, (i + 1)*4)[0] & 0x00ffffff
        name, _, url = serialized[offset:next_offset].partition(b'\0')
        out += "{}: {} [{}] -> {}".format(i, name.decode('utf-8'), ', '.join(extra), url.decode('utf-8'))
        offset = next_offset
    return out

def pretty_print(serialized: bytes, show_merged=False):
    magic, version, map_offset = search_data_header_struct.unpack_from(serialized)
    assert magic == b'MCS'
    assert version == 0
    assert not search_data_header_struct.size % 4

    pretty_trie, stats = pretty_print_trie(serialized[search_data_header_struct.size:map_offset], show_merged=show_merged)
    pretty_map = pretty_print_map(serialized[map_offset:])
    return pretty_trie + '\n' + pretty_map, stats

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
        trie.insert("math::vector", 1)
        trie.insert("vector", 1)
        trie.insert("math::range", 2)
        trie.insert("range", 2)

        trie.insert("math::min", 3)
        trie.insert("min", 3)
        trie.insert("math::max", 4)
        trie.insert("max", 4)
        trie.insert("math::minmax", 5)
        trie.insert("minmax", 5)

        trie.insert("math::vector::minmax", 6)
        trie.insert("vector::minmax", 6)
        trie.insert("minmax", 6)
        trie.insert("math::vector::min", 7)
        trie.insert("vector::min", 7)
        trie.insert("min", 7)
        trie.insert("math::vector::max", 8)
        trie.insert("vector::max", 8)
        trie.insert("max", 8)

        trie.insert("math::range::min", 9)
        trie.insert("range::min", 9)
        trie.insert("min", 9)

        trie.insert("math::range::max", 10)
        trie.insert("range::max", 10)
        trie.insert("max", 10)

        serialized = trie.serialize()
        self.compare(serialized, """
math [0]
||| ::vector [1]
|||   |     ::min [7]
|||   |        | max [6]
|||   |        ax [8]
|||   range [2]
|||   |    ::min [9]
|||   |       ax [10]
|||   min [3]
|||   || max [5]
|||   |ax [4]
||x [4, 8, 10]
|in [3, 7, 9]
|| max [5, 6]
vector [1]
|     ::min [7]
|        | max [6]
|        ax [8]
range [2]
|    ::min [9]
|       ax [10]
""")
        self.assertEqual(len(serialized), 340)

class MapSerialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print_map(serialized)
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test_empty(self):
        map = ResultMap()

        serialized = map.serialize()
        self.compare(serialized, "")
        self.assertEqual(len(serialized), 4)

    def test_single(self):
        map = ResultMap()
        self.assertEqual(map.add("Magnum", "namespaceMagnum.html", suffix_length=11), 0)

        serialized = map.serialize()
        self.compare(serialized, """
0: Magnum [1, suffix_length=11] -> namespaceMagnum.html
""")
        self.assertEqual(len(serialized), 36)

    def test_multiple(self):
        map = ResultMap()

        self.assertEqual(map.add("Math", "namespaceMath.html"), 0)
        self.assertEqual(map.add("Math::Vector", "classMath_1_1Vector.html"), 1)
        self.assertEqual(map.add("Math::Range", "classMath_1_1Range.html"), 2)
        self.assertEqual(map.add("Math::min()", "namespaceMath.html#abcdef2875"), 3)
        self.assertEqual(map.add("Math::max(int, int)", "namespaceMath.html#abcdef2875", suffix_length=8), 4)

        serialized = map.serialize()
        self.compare(serialized, """
0: Math [0] -> namespaceMath.html
1: Math::Vector [0] -> classMath_1_1Vector.html
2: Math::Range [0] -> classMath_1_1Range.html
3: Math::min() [0] -> namespaceMath.html#abcdef2875
4: Math::max(int, int) [1, suffix_length=8] -> namespaceMath.html#abcdef2875
""")
        self.assertEqual(len(serialized), 210)

class Serialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print(serialized)[0]
        #print(pretty)
        self.assertEqual(pretty, expected.strip())

    def test(self):
        trie = Trie()
        map = ResultMap()

        trie.insert("math", map.add("Math", "namespaceMath.html"))
        index = map.add("Math::Vector", "classMath_1_1Vector.html")
        trie.insert("math::vector", index)
        trie.insert("vector", index)
        index = map.add("Math::Range", "classMath_1_1Range.html")
        trie.insert("math::range", index)
        trie.insert("range", index)

        serialized = serialize_search_data(trie, map)
        self.compare(serialized, """
math [0]
|   ::vector [1]
|     range [2]
vector [1]
range [2]
0: Math [0] -> namespaceMath.html
1: Math::Vector [0] -> classMath_1_1Vector.html
2: Math::Range [0] -> classMath_1_1Range.html
""")
        self.assertEqual(len(serialized), 241)

class Search(IntegrationTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(__file__, '', *args, **kwargs)

    def test(self):
        self.run_dox2html5(index_pages=[], wildcard='*.xml')

        with open(os.path.join(self.path, 'html', 'searchdata.bin'), 'rb') as f:
            search_data_pretty = pretty_print(f.read())[0]
        #print(search_data_pretty)
        self.assertEqual(search_data_pretty, """
namespace [0]
|        ::class [1]
|          |    ::foo() [6, 7, 8, 9]
|          enum [11]
|          |   ::value [10]
|          typedef [12]
|          variable [13]
class [1]
|    ::foo() [6, 7, 8, 9]
a page [2]
subpage [3]
dir [4]
|  /file.h [5]
file.h [5]
|oo() [6, 7, 8, 9]
enum [11]
|   ::value [10]
value [10]
| riable [13]
typedef [12]
macro [14]
|    _function() [15]
|             _with_params() [16]
0: Namespace [0] -> namespaceNamespace.html
1: Namespace::Class [0] -> classNamespace_1_1Class.html
2: A page [0] -> page.html
3: A page » Subpage [0] -> subpage.html
4: Dir/ [1, suffix_length=1] -> dir_da5033def2d0db76e9883b31b76b3d0c.html
5: Dir/File.h [0] -> File_8h.html
6: Namespace::Class::foo() [0] -> classNamespace_1_1Class.html#aaeba4096356215868370d6ea476bf5d9
7: Namespace::Class::foo() const [1, suffix_length=6] -> classNamespace_1_1Class.html#ac03c5b93907dda16763eabd26b25500a
8: Namespace::Class::foo() && [1, suffix_length=3] -> classNamespace_1_1Class.html#ac9e7e80d06281e30cfcc13171d117ade
9: Namespace::Class::foo(const Enum&, Typedef) [1, suffix_length=20] -> classNamespace_1_1Class.html#aba8d57a830d4d79f86d58d92298677fa
10: Namespace::Enum::Value [0] -> namespaceNamespace.html#add172b93283b1ab7612c3ca6cc5dcfeaa689202409e48743b914713f96d93947c
11: Namespace::Enum [0] -> namespaceNamespace.html#add172b93283b1ab7612c3ca6cc5dcfea
12: Namespace::Typedef [0] -> namespaceNamespace.html#abe2a245304bc2234927ef33175646e08
13: Namespace::Variable [0] -> namespaceNamespace.html#ad3121960d8665ab045ca1bfa1480a86d
14: MACRO [0] -> File_8h.html#a824c99cb152a3c2e9111a2cb9c34891e
15: MACRO_FUNCTION() [0] -> File_8h.html#a025158d6007b306645a8eb7c7a9237c1
16: MACRO_FUNCTION_WITH_PARAMS(params) [1, suffix_length=6] -> File_8h.html#a88602bba5a72becb4f2dc544ce12c420
""".strip())

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="file to pretty-print")
    parser.add_argument('--show-merged', help="show merged subtrees", action='store_true')
    parser.add_argument('--show-stats', help="show stats", action='store_true')
    args = parser.parse_args()

    with open(args.file, 'rb') as f:
        out, stats = pretty_print(f.read(), show_merged=args.show_merged)
        print(out)
        if args.show_stats: print(stats, file=sys.stderr)
