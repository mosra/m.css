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
import unittest
import sys
from types import SimpleNamespace as Empty

from dox2html5 import Trie

def _pretty_print(serialized: bytearray, hashtable, stats, base_offset, indent, draw_pipe, show_merged) -> str:
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
    if base_offset + size - offset > 4: draw_pipe = True
    child_count = 0
    while offset < base_offset + size:
        if child_count or value_count:
            out += '\n'
            out += indent
        out += Trie.child_char_struct.unpack_from(serialized, offset + 3)[0].decode('utf-8')
        child_offset = Trie.child_struct.unpack_from(serialized, offset)[0] & 0x00ffffff
        stats.max_node_child_offset = max(child_offset, stats.max_node_child_offset)
        offset += Trie.child_struct.size
        out += _pretty_print(serialized, hashtable, stats, child_offset, indent + ('|' if draw_pipe else ' '), draw_pipe=False, show_merged=show_merged)
        child_count += 1

    stats.max_node_children = max(child_count, stats.max_node_children)

    hashtable[base_offset] = True
    return out

def pretty_print(serialized: bytes, show_merged=False):
    hashtable = {}

    stats = Empty()
    stats.node_count = 0
    stats.max_node_size = 0
    stats.max_node_values = 0
    stats.max_node_children = 0
    stats.max_node_value_index = 0
    stats.max_node_child_offset = 0

    out = _pretty_print(serialized, hashtable, stats, Trie.root_offset_struct.unpack_from(serialized, 0)[0], '', draw_pipe=False, show_merged=show_merged)
    stats = """
node count:             {}
max node size:          {} bytes
max node values:        {}
max node children:      {}
max node value index:   {}
max node child offset:  {}""".lstrip().format(stats.node_count, stats.max_node_size, stats.max_node_values, stats.max_node_children, stats.max_node_value_index, stats.max_node_child_offset)
    return out, stats

class Serialization(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def compare(self, serialized: bytes, expected: str):
        pretty = pretty_print(serialized)[0]
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
