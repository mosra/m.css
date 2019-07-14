#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019 Vladimír Vondruš <mosra@centrum.cz>
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

# Can't be in __init__.py because I can't say `from . import Trie` in
# doxygen.py. But `from _search import bla` works. Ugh.

import base64
import struct
from enum import Flag
from types import SimpleNamespace as Empty

class ResultFlag(Flag):
    HAS_SUFFIX = 1 << 0
    HAS_PREFIX = 1 << 3
    DEPRECATED = 1 << 1
    DELETED = 1 << 2

    # Result type. Order defines order in which equally-named symbols appear in
    # search results. Keep in sync with search.js.
    _TYPE = 0xf << 4
    ALIAS = 0 << 4 # This one gets the type from the referenced result
    PAGE = 1 << 4
    NAMESPACE = 2 << 4
    GROUP = 3 << 4
    CLASS = 4 << 4
    STRUCT = 5 << 4
    UNION = 6 << 4
    TYPEDEF = 7 << 4
    DIR = 8 << 4
    FILE = 9 << 4
    FUNC = 10 << 4
    DEFINE = 11 << 4
    ENUM = 12 << 4
    ENUM_VALUE = 13 << 4
    VAR = 14 << 4

class ResultMap:
    # item 1 flags | item 2 flags |     | item N flags | file | item 1 |
    #   + offset   |   + offset   | ... |   + offset   | size |  data  | ...
    #    8 + 24b   |    8 + 24b   |     |    8 + 24b   |  32b |        |
    #
    # basic item (flags & 0b11 == 0b00):
    #
    # name | \0 | URL
    #      |    |
    #      | 8b |
    #
    # suffixed item (flags & 0b11 == 0b01):
    #
    # suffix | name | \0 | URL
    # length |      |    |
    #   8b   |      | 8b |
    #
    # prefixed item (flags & 0xb11 == 0b10):
    #
    #  prefix  |  name  | \0 |  URL
    # id + len | suffix |    | suffix
    # 16b + 8b |        | 8b |
    #
    # prefixed & suffixed item (flags & 0xb11 == 0b11):
    #
    #  prefix  | suffix |  name  | \0 | URL
    # id + len | length | suffix |    |
    # 16b + 8b |   8b   |        | 8b |
    #
    # alias item (flags & 0xf0 == 0x00):
    #
    # alias |     | alias
    #  id   | ... | name
    #  16b  |     |
    #
    offset_struct = struct.Struct('<I')
    flags_struct = struct.Struct('<B')
    prefix_struct = struct.Struct('<HB')
    suffix_length_struct = struct.Struct('<B')
    alias_struct = struct.Struct('<H')

    def __init__(self):
        self.entries = []

    def add(self, name, url, alias=None, suffix_length=0, flags=ResultFlag(0)) -> int:
        if suffix_length: flags |= ResultFlag.HAS_SUFFIX
        if alias is not None:
            assert flags & ResultFlag._TYPE == ResultFlag.ALIAS

        entry = Empty()
        entry.name = name
        entry.url = url
        entry.flags = flags
        entry.alias = alias
        entry.prefix = 0
        entry.prefix_length = 0
        entry.suffix_length = suffix_length

        self.entries += [entry]
        return len(self.entries) - 1

    def serialize(self, merge_prefixes=True) -> bytearray:
        output = bytearray()

        if merge_prefixes:
            # Put all entry names into a trie to discover common prefixes
            trie = Trie()
            for index, e in enumerate(self.entries):
                trie.insert(e.name, index)

            # Create a new list with merged prefixes
            merged = []
            for index, e in enumerate(self.entries):
                # Search in the trie and get the longest shared name prefix
                # that is already fully contained in some other entry
                current = trie
                longest_prefix = None
                for c in e.name.encode('utf-8'):
                    for candidate, child in current.children.items():
                        if c == candidate:
                            current = child[1]
                            break
                    else: assert False # pragma: no cover

                    # Allow self-reference only when referenced result suffix
                    # is longer (otherwise cycles happen). This is for
                    # functions that should appear when searching for foo (so
                    # they get ordered properly based on the name length) and
                    # also when searching for foo() (so everything that's not
                    # a function gets filtered out). Such entries are
                    # completely the same except for a different suffix length.
                    if index in current.results:
                        for i in current.results:
                            if self.entries[i].suffix_length > self.entries[index].suffix_length:
                                longest_prefix = current
                                break
                    elif current.results:
                        longest_prefix = current

                # Name prefix found, for all possible URLs find the one that
                # shares the longest prefix
                if longest_prefix:
                    max_prefix = (0, -1)
                    for longest_index in longest_prefix.results:
                        # Ignore self (function self-reference, see above)
                        if longest_index == index: continue

                        prefix_length = 0
                        for i in range(min(len(e.url), len(self.entries[longest_index].url))):
                            if e.url[i] != self.entries[longest_index].url[i]: break
                            prefix_length += 1
                        if max_prefix[1] < prefix_length:
                            max_prefix = (longest_index, prefix_length)

                    # Expect we found something
                    assert max_prefix[1] != -1

                    # Save the entry with reference to the prefix
                    entry = Empty()
                    assert e.name.startswith(self.entries[longest_prefix.results[0]].name)
                    entry.name = e.name[len(self.entries[longest_prefix.results[0]].name):]
                    entry.url = e.url[max_prefix[1]:]
                    entry.flags = e.flags|ResultFlag.HAS_PREFIX
                    entry.alias = e.alias
                    entry.prefix = max_prefix[0]
                    entry.prefix_length = max_prefix[1]
                    entry.suffix_length = e.suffix_length
                    merged += [entry]

                # No prefix found, copy the entry verbatim
                else: merged += [e]

            # Everything merged, replace the original list
            self.entries = merged

        # Write the offset array. Starting offset for items is after the offset
        # array and the file size
        offset = (len(self.entries) + 1)*4
        for e in self.entries:
            assert offset < 2**24
            output += self.offset_struct.pack(offset)
            self.flags_struct.pack_into(output, len(output) - 1, e.flags.value)

            # The entry is an alias, extra field for alias index
            if e.flags & ResultFlag._TYPE == ResultFlag.ALIAS:
                offset += 2

            # Extra field for prefix index and length
            if e.flags & ResultFlag.HAS_PREFIX:
                offset += 3

            # Extra field for suffix length
            if e.flags & ResultFlag.HAS_SUFFIX:
                offset += 1

            # Length of the name
            offset += len(e.name.encode('utf-8'))

            # Length of the URL and 0-delimiter. If URL is empty, it's not
            # added at all, then the 0-delimiter is also not needed.
            if e.name and e.url:
                 offset += len(e.url.encode('utf-8')) + 1

        # Write file size
        output += self.offset_struct.pack(offset)

        # Write the entries themselves
        for e in self.entries:
            if e.flags & ResultFlag._TYPE == ResultFlag.ALIAS:
                assert not e.alias is None
                assert not e.url
                output += self.alias_struct.pack(e.alias)
            if e.flags & ResultFlag.HAS_PREFIX:
                output += self.prefix_struct.pack(e.prefix, e.prefix_length)
            if e.flags & ResultFlag.HAS_SUFFIX:
                output += self.suffix_length_struct.pack(e.suffix_length)
            output += e.name.encode('utf-8')
            if e.url:
                output += b'\0'
                output += e.url.encode('utf-8')

        assert len(output) == offset
        return output

class Trie:
    #  root  |     |     header         | results | child 1 | child 1 | child 1 |
    # offset | ... | result # | value # |   ...   |  char   | barrier | offset  | ...
    #  32b   |     |    8b    |   8b    |  n*16b  |   8b    |    1b   |   23b   |
    root_offset_struct = struct.Struct('<I')
    header_struct = struct.Struct('<BB')
    result_struct = struct.Struct('<H')
    child_struct = struct.Struct('<I')
    child_char_struct = struct.Struct('<B')

    def __init__(self):
        self.results = []
        self.children = {}

    def _insert(self, path: bytes, result, lookahead_barriers):
        if not path:
            self.results += [result]
            return

        char = path[0]
        if not char in self.children:
            self.children[char] = (False, Trie())
        if lookahead_barriers and lookahead_barriers[0] == 0:
            lookahead_barriers = lookahead_barriers[1:]
            self.children[char] = (True, self.children[char][1])
        self.children[char][1]._insert(path[1:], result, [b - 1 for b in lookahead_barriers])

    def insert(self, path: str, result, lookahead_barriers=[]):
        self._insert(path.encode('utf-8'), result, lookahead_barriers)

    def _sort(self, key):
        self.results.sort(key=key)
        for _, child in self.children.items():
            child[1]._sort(key)

    def sort(self, result_map: ResultMap):
        # What the shit, why can't I just take two elements and say which one
        # is in front of which, this is awful
        def key(item: int):
            entry = result_map.entries[item]
            return [
                # First order based on deprecation/deletion status, deprecated
                # always last, deleted in front of them, usable stuff on top
                2 if entry.flags & ResultFlag.DEPRECATED else 1 if entry.flags & ResultFlag.DELETED else 0,

                # Second order based on type (pages, then namespaces/classes,
                # later functions, values last)
                (entry.flags & ResultFlag._TYPE).value,

                # Third on suffix length (shortest first)
                entry.suffix_length,

                # Lastly on full name length (or prefix length, also shortest
                # first)
                len(entry.name)
            ]

        self._sort(key)

    # Returns offset of the serialized thing in `output`
    def _serialize(self, hashtable, output: bytearray, merge_subtrees) -> int:
        # Serialize all children first
        child_offsets = []
        for char, child in self.children.items():
            offset = child[1]._serialize(hashtable, output, merge_subtrees=merge_subtrees)
            child_offsets += [(char, child[0], offset)]

        # Serialize this node
        serialized = bytearray()
        serialized += self.header_struct.pack(len(self.results), len(self.children))
        for v in self.results:
            serialized += self.result_struct.pack(v)

        # Serialize child offsets
        for char, lookahead_barrier, abs_offset in child_offsets:
            assert abs_offset < 2**23

            # write them over each other because that's the only way to pack
            # a 24 bit field
            offset = len(serialized)
            serialized += self.child_struct.pack(abs_offset | ((1 if lookahead_barrier else 0) << 23))
            self.child_char_struct.pack_into(serialized, offset + 3, char)

        # Subtree merging: if this exact tree is already in the table, return
        # its offset. Otherwise add it and return the new offset.
        # TODO: why hashable = bytes(output[base_offset:] + serialized) didn't work?
        hashable = bytes(serialized)
        if merge_subtrees and hashable in hashtable:
            return hashtable[hashable]
        else:
            offset = len(output)
            output += serialized
            if merge_subtrees: hashtable[hashable] = offset
            return offset

    def serialize(self, merge_subtrees=True) -> bytearray:
        output = bytearray(b'\x00\x00\x00\x00')
        hashtable = {}
        self.root_offset_struct.pack_into(output, 0, self._serialize(hashtable, output, merge_subtrees=merge_subtrees))
        return output

search_data_header_struct = struct.Struct('<3sBHI')

def serialize_search_data(trie: Trie, map: ResultMap, symbol_count, merge_subtrees=True, merge_prefixes=True) -> bytearray:
    serialized_trie = trie.serialize(merge_subtrees=merge_subtrees)
    serialized_map = map.serialize(merge_prefixes=merge_prefixes)
    # magic header, version, symbol count, offset of result map
    return search_data_header_struct.pack(b'MCS', 0, symbol_count, len(serialized_trie) + 10) + serialized_trie + serialized_map

def base85encode_search_data(data: bytearray) -> bytearray:
    return (b"/* Generated by https://mcss.mosra.cz/documentation/doxygen/. Do not edit. */\n" +
            b"Search.load('" + base64.b85encode(data, True) + b"');\n")
