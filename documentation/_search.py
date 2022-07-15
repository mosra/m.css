#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022
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

# Can't be in __init__.py because I can't say `from . import Trie` in
# doxygen.py. But `from _search import bla` works. Ugh.

import base64
import enum
import struct
from types import SimpleNamespace as Empty
from typing import List, Tuple, Union

# Version 0 was without the type map
searchdata_format_version = 2
search_filename = f'search-v{searchdata_format_version}.js'
searchdata_filename = f'{{search_filename_prefix}}-v{searchdata_format_version}.bin'
searchdata_filename_b85 = f'{{search_filename_prefix}}-v{searchdata_format_version}.js'

# In order to be both space-efficient and flexible enough to accommodate for
# larger projects, the bit counts for particular data types can vary in each
# file. There's the following categories:
#
# - NAME_SIZE_BITS, how many bits is needed to store name lengths (such as
#   prefix length). Can be either 8 or 16.
# - RESULT_ID_BITS, how many bits is needed for IDs pointing into the result
#   map. Can be either 16, 24 or 32.
# - FILE_OFFSET_BITS, how many bits is needed to store general offsets into
#   the file. Can be either 24 or 32.
#
# Whole file encoding
# ===================
#
# magic | version | type | not  | symbol | result | type   | trie | result | type
# 'MCS' | (0x02)  | data | used | count  |  map   |  map   | data |  map   | map
#       |         |      |      |        | offset | offset |      |  data  | data
#  24b  |   8b    |  8b  | 24b  |  32b   |  32b   |  32b   |  …   |   …    |  …
#
# The type data encode the NAME_SIZE_BITS, RESULT_ID_BITS and
# FILE_OFFSET_BITS:
#
# not  | NAME_SIZE_BITS | RESULT_ID_BITS | FILE_OFFSET_BITS
# used | 0b0 = 8b       | 0b00 = 16b     | 0b0 = 24b
#      | 0b1 = 16b      | 0b01 = 24b     | 0b1 = 32b
#      |                | 0b10 = 32b     |
#  4b  |     1b         |       2b       |       1b
#
# Trie encoding
# =============
#
# Because child tries are serialized first, the trie containing the initial
# characters is never the first, and instead the root offset points to it. If
# result count < 128:
#
#  root  |   |         header       |      results     | children
# offset | … | | result # | child # |         …        |  data
#  32b   |   |0|    7b    |   8b    | n*RESULT_ID_BITS |    …
#
# If result count > 127, it's instead this -- since entries with very large
# number of results (such as python __init__()) are rather rare, it doesn't
# make sense to have it globally configurable and then waste 8 bits in the
# majority of cases. Note that the 15-bit value is stored as Big-Endian,
# otherwise the leftmost bit couldn't be used to denote the size.
#
#  root  |   |         header       |      results     | children
# offset | … | | result # | child # |         …        |  data
#  32b   |   |1| 15b (BE) |   8b    | n*RESULT_ID_BITS |    …
#
# Trie children data encoding, the barrier is stored in the topmost offset bit:
#
# child 1 | child 2 |   |     child 1      |      child 2     |
#  char   |  char   | … | barrier + offset | barrier + offset | …
#   8b    |   8b    |   | FILE_OFFSET_BITS | FILE_OFFSET_BITS |
#
# Result map encoding
# ===================
#
# First all flags, then all offsets, so we don't need to have weird paddings or
# alignments. The "file size" is there so size of item N can be always
# retrieved as `offsets[N + 1] - offsets[N]`
#
#       item         |       file       | item  | item 1 | item 2 |
#      offsets       |       size       | flags |  data  |  data  | …
# n*FILE_OFFSET_BITS | FILE_OFFSET_BITS | n*8b  |        |        |
#
# Basic item data (flags & 0b11 == 0b00):
#
# name | \0 | URL
#      |    |
#      | 8b |
#
# Suffixed item data (flags & 0b11 == 0b01):
#
#     suffix     | name | \0 | URL
#     length     |      |    |
# NAME_SIZE_BITS |      | 8b |
#
# Prefixed item data (flags & 0xb11 == 0b10):
#
#     prefix     |     prefix     |  name  | \0 |  URL
#       id       |     length     | suffix |    | suffix
# RESULT_ID_BITS | NAME_SIZE_BITS |        | 8b |
#
# Prefixed & suffixed item (flags & 0xb11 == 0b11):
#
#     prefix     |     prefix     |     suffix     |  name  | \0 | URL
#       id       |     length     |     length     | suffix |    |
# RESULT_ID_BITS | NAME_SIZE_BITS | NAME_SIZE_BITS |        | 8b |
#
# Alias item (flags & 0xf0 == 0x00), flags & 0xb11 then denote what's in the
# `…` portion, alias have no URL so the alias name is in place of it:
#
#     alias      |   | alias
#       id       | … | name
# RESULT_ID_BITS |   |
#
# Type map encoding
# =================
#
# Again the "end offset" is here so size of type N can be always retrieved as
# `offsets[N + 1] - offsets[N]`. Type names are not expected to have more than
# 255 chars, so NAME_SIZE_BITS is not used here.
#
#     type 1     |     type 2     |   |         |        | type 1 |
# class |  name  | class |  name  | … | padding |  end   |  name  | …
#   ID  | offset |   ID  | offset |   |         | offset |  data  |
#   8b  |   8b   |   8b  |   8b   |   |    8b   |   8b   |        |

class Serializer:
    # This is currently hardcoded
    result_map_flag_bytes = 1

    header_struct = struct.Struct('<3sBBxxxIII')
    result_map_flags_struct = struct.Struct('<B')
    trie_root_offset_struct = struct.Struct('<I')
    type_map_entry_struct = struct.Struct('<BB')

    def __init__(self, *, file_offset_bytes, result_id_bytes, name_size_bytes):
        assert file_offset_bytes in [3, 4]
        self.file_offset_bytes = file_offset_bytes

        assert result_id_bytes in [2, 3, 4]
        self.result_id_bytes = result_id_bytes

        assert name_size_bytes in [1, 2]
        self.name_size_bytes = name_size_bytes

    def pack_header(self, symbol_count, trie_size, result_map_size):
        return self.header_struct.pack(b'MCS', searchdata_format_version,
            (self.file_offset_bytes - 3) << 0 |
            (self.result_id_bytes - 2) << 1 |
            (self.name_size_bytes - 1) << 3,
            symbol_count,
            self.header_struct.size + trie_size,
            self.header_struct.size + trie_size + result_map_size)

    def pack_result_map_flags(self, flags: int):
        return self.result_map_flags_struct.pack(flags)
    def pack_result_map_offset(self, offset: int):
        if offset >= 256**self.file_offset_bytes:
            raise OverflowError("Result map offset too large to store in {} bits, set SEARCH_FILE_OFFSET_BYTES = {} in your conf.py.".format(self.file_offset_bytes*8, self.file_offset_bytes + 1))
        return offset.to_bytes(self.file_offset_bytes, byteorder='little')
    def pack_result_map_prefix(self, id: int, length: int):
        if id >= 256**self.result_id_bytes:
            raise OverflowError("Result map prefix ID too large to store in {} bits, set SEARCH_RESULT_ID_BYTES = {} in your conf.py.".format(self.result_id_bytes*8, self.result_id_bytes + 1))
        if length >= 256**self.name_size_bytes:
            raise OverflowError("Result map prefix length too large to store in {} bits, set SEARCH_NAME_SIZE_BYTES = {} in your conf.py.".format(self.name_size_bytes*8, self.name_size_bytes + 1))
        return id.to_bytes(self.result_id_bytes, byteorder='little') + \
           length.to_bytes(self.name_size_bytes, byteorder='little')
    def pack_result_map_suffix_length(self, length: int):
        if length >= 256**self.name_size_bytes:
            raise OverflowError("Result map suffix length too large to store in {} bits, set SEARCH_NAME_SIZE_BYTES = {} in your conf.py.".format(self.name_size_bytes*8, self.name_size_bytes + 1))
        return length.to_bytes(self.name_size_bytes, byteorder='little')
    def pack_result_map_alias(self, id: int):
        if id >= 256**self.result_id_bytes:
            raise OverflowError("Result map alias ID too large to store in {} bits, set SEARCH_RESULT_ID_BYTES = {} in your conf.py.".format(self.result_id_bytes*8, self.result_id_bytes + 1))
        return id.to_bytes(self.result_id_bytes, byteorder='little')

    def pack_trie_root_offset(self, offset: int):
        return self.trie_root_offset_struct.pack(offset)
    def pack_trie_node(self, result_ids: List[int], child_chars_offsets_barriers: List[Tuple[int, int, bool]]):
        out = bytearray()
        # If the result count fits into 7 bits, pack it into a single byte
        if len(result_ids) < 128:
            out += len(result_ids).to_bytes(1, byteorder='little')
        # Otherwise use the leftmost bit to denote it's two-byte, and store the
        # higher 8 bits in a second byte. Which is the same as storing the
        # value as Big-Endian.
        else:
            assert len(result_ids) < 32768
            out += (len(result_ids) | 0x8000).to_bytes(2, byteorder='big')
        out += len(child_chars_offsets_barriers).to_bytes(1, byteorder='little')
        for id in result_ids:
            if id >= 256**self.result_id_bytes:
                raise OverflowError("Trie result ID too large to store in {} bits, set SEARCH_RESULT_ID_BYTES = {} in your conf.py.".format(self.result_id_bytes*8, self.result_id_bytes + 1))
            out += id.to_bytes(self.result_id_bytes, byteorder='little')
        out += bytes([char for char, offset, barrier in child_chars_offsets_barriers])
        child_barrier_mask = 1 << (self.file_offset_bytes*8 - 1)
        for char, offset, barrier in child_chars_offsets_barriers:
            if offset >= child_barrier_mask:
                raise OverflowError("Trie child offset too large to store in {} bits, set SEARCH_FILE_OFFSET_BYTES = {} in your conf.py.".format(self.file_offset_bytes*8 - 1, self.file_offset_bytes + 1))
            out += (offset | (barrier*child_barrier_mask)).to_bytes(self.file_offset_bytes, byteorder='little')
        return out

    def pack_type_map_entry(self, class_: int, offset: int):
        return self.type_map_entry_struct.pack(class_, offset)

class Deserializer:
    def __init__(self, *, file_offset_bytes, result_id_bytes, name_size_bytes):
        assert file_offset_bytes in [3, 4]
        self.file_offset_bytes = file_offset_bytes

        assert result_id_bytes in [2, 3, 4]
        self.result_id_bytes = result_id_bytes

        assert name_size_bytes in [1, 2]
        self.name_size_bytes = name_size_bytes

    @classmethod
    def from_serialized(self, serialized: bytes):
        magic, version, type_data, symbol_count, map_offset, type_map_offset = Serializer.header_struct.unpack_from(serialized)
        assert magic == b'MCS'
        assert version == searchdata_format_version
        out = Deserializer(
            file_offset_bytes=[3, 4][(type_data & 0b0001) >> 0],
            result_id_bytes=[2, 3, 4][(type_data & 0b0110) >> 1],
            name_size_bytes=[1, 2][(type_data & 0b1000) >> 3])
        out.symbol_count = symbol_count
        out.map_offset = map_offset
        out.type_map_offset = type_map_offset
        return out

    # The last tuple item is number of bytes extracted
    def unpack_result_map_flags(self, serialized: bytes, offset: int) -> Tuple[int, int]:
        return Serializer.result_map_flags_struct.unpack_from(serialized, offset) + (Serializer.result_map_flags_struct.size, )
    def unpack_result_map_offset(self, serialized: bytes, offset: int) -> Tuple[int, int]:
        return int.from_bytes(serialized[offset:offset + self.file_offset_bytes], byteorder='little'), self.file_offset_bytes
    def unpack_result_map_prefix(self, serialized: bytes, offset: int) -> Tuple[int, int, int]:
        return int.from_bytes(serialized[offset:offset + self.result_id_bytes], byteorder='little'), int.from_bytes(serialized[offset + self.result_id_bytes:offset + self.result_id_bytes + self.name_size_bytes], byteorder='little'), self.result_id_bytes + self.name_size_bytes
    def unpack_result_map_suffix_length(self, serialized: bytes, offset: int) -> Tuple[int, int]:
        return int.from_bytes(serialized[offset:offset + self.name_size_bytes], byteorder='little'), self.name_size_bytes
    def unpack_result_map_alias(self, serialized: bytes, offset: int) -> Tuple[int, int]:
        return int.from_bytes(serialized[offset:offset + self.result_id_bytes], byteorder='little'), self.result_id_bytes

    def unpack_trie_root_offset(self, serialized: bytes, offset: int) -> Tuple[int, int]:
        return Serializer.trie_root_offset_struct.unpack_from(serialized, offset) + (Serializer.trie_root_offset_struct.size, )
    def unpack_trie_node(self, serialized: bytes, offset: int) -> Tuple[List[int], List[int], List[Tuple[int, int, bool]], int]:
        prev_offset = offset
        # Result count, first try 8-bit, if it has the highest bit set, extract
        # two bytes (as a BE) and then remove the highest bit
        result_count = int.from_bytes(serialized[offset:offset + 1], byteorder='little')
        if result_count & 0x80:
            result_count = int.from_bytes(serialized[offset:offset + 2], byteorder='big') & ~0x8000
            offset += 1
        offset += 1
        child_count = int.from_bytes(serialized[offset:offset + 1], byteorder='little')
        offset += 1

        # Unpack all result IDs
        result_ids = []
        for i in range(result_count):
            result_ids += [int.from_bytes(serialized[offset:offset + self.result_id_bytes], byteorder='little')]
            offset += self.result_id_bytes

        # Unpack all child chars
        child_chars = list(serialized[offset:offset + child_count])
        offset += child_count

        # Unpack all children offsets and lookahead barriers
        child_chars_offsets_barriers = []
        child_barrier_mask = 1 << (self.file_offset_bytes*8 - 1)
        for i in range(child_count):
            child_offset_barrier = int.from_bytes(serialized[offset:offset + self.file_offset_bytes], byteorder='little')
            child_chars_offsets_barriers += [(child_chars[i], child_offset_barrier & ~child_barrier_mask, bool(child_offset_barrier & child_barrier_mask))]
            offset += self.file_offset_bytes

        return result_ids, child_chars_offsets_barriers, offset - prev_offset

    def unpack_type_map_entry(self, serialized: bytes, offset: int) -> Tuple[int, int, int]:
        return Serializer.type_map_entry_struct.unpack_from(serialized, offset) + (Serializer.type_map_entry_struct.size, )

class CssClass(enum.Enum):
    DEFAULT = 0
    PRIMARY = 1
    SUCCESS = 2
    WARNING = 3
    DANGER = 4
    INFO = 5
    DIM = 6

class ResultFlag(enum.Flag):
    @staticmethod
    def from_type(flag: 'ResultFlag', type) -> 'ResultFlag':
        assert not flag & ResultFlag._TYPE
        assert type.value > 0 and type.value <= 0xf
        return flag|ResultFlag(type.value << 4)

    @property
    def type(self):
        return (int(self.value) >> 4) & 0xf

    NONE = 0

    HAS_SUFFIX = 1 << 0
    HAS_PREFIX = 1 << 3
    DEPRECATED = 1 << 1
    DELETED = 1 << 2 # TODO: this is C++-specific, put aside as well?

    # Result type. Order defines order in which equally-named symbols appear in
    # search results, every backend supplies its own, ranging from 1 << 4 to
    # 15 << 4.
    _TYPE = 0xf << 4
    ALIAS = 0 << 4 # This one gets the type from the referenced result

    # Otherwise it says "32 is not a valid ResultFlag"
    _TYPE01 = 1 << 4
    _TYPE02 = 2 << 4
    _TYPE03 = 3 << 4
    _TYPE04 = 4 << 4
    _TYPE05 = 5 << 4
    _TYPE06 = 6 << 4
    _TYPE07 = 7 << 4
    _TYPE08 = 8 << 4
    _TYPE09 = 9 << 4
    _TYPE10 = 10 << 4
    _TYPE11 = 11 << 4
    _TYPE12 = 12 << 4
    _TYPE13 = 13 << 4
    _TYPE14 = 14 << 4
    _TYPE15 = 15 << 4

class ResultMap:
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

    def serialize(self, serializer: Serializer, merge_prefixes=True) -> bytearray:
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

        # Write the offset array. Starting offset for items is after the
        # (aligned) flag array and (aligned) offset + file size array.
        output = bytearray()
        offset = len(self.entries)*serializer.result_map_flag_bytes + (len(self.entries) + 1)*serializer.file_offset_bytes
        for e in self.entries:
            output += serializer.pack_result_map_offset(offset)

            # The entry is an alias, extra field for alias index
            if e.flags & ResultFlag._TYPE == ResultFlag.ALIAS:
                offset += serializer.result_id_bytes

            # Extra field for prefix index and length
            if e.flags & ResultFlag.HAS_PREFIX:
                offset += serializer.result_id_bytes + serializer.name_size_bytes

            # Extra field for suffix length
            if e.flags & ResultFlag.HAS_SUFFIX:
                offset += serializer.name_size_bytes

            # Length of the name
            offset += len(e.name.encode('utf-8'))

            # Length of the URL and 0-delimiter. If URL is empty, it's not
            # added at all, then the 0-delimiter is also not needed.
            if e.name and e.url:
                 offset += len(e.url.encode('utf-8')) + 1

        # Write file size
        output += serializer.pack_result_map_offset(offset)

        # Write the flag array
        for e in self.entries:
            output += serializer.pack_result_map_flags(e.flags.value)

        # Write the entries themselves
        for e in self.entries:
            if e.flags & ResultFlag._TYPE == ResultFlag.ALIAS:
                assert not e.alias is None
                assert not e.url
                output += serializer.pack_result_map_alias(e.alias)
            if e.flags & ResultFlag.HAS_PREFIX:
                output += serializer.pack_result_map_prefix(e.prefix, e.prefix_length)
            if e.flags & ResultFlag.HAS_SUFFIX:
                output += serializer.pack_result_map_suffix_length(e.suffix_length)
            output += e.name.encode('utf-8')
            if e.url:
                output += b'\0'
                output += e.url.encode('utf-8')

        assert len(output) == offset
        return output

class Trie:
    def __init__(self):
        self.results = []
        self.children = {}

    def _insert(self, path: bytes, result: Union[int, List[int]], lookahead_barriers):
        if not path:
            # Inserting a list is mainly used by the
            # TrieSerialization.test_23bit_file_offset_too_small() test, as
            # otherwise it'd be WAY too slow.
            # TODO this whole thing needs optimizing with less recursion
            if type(result) is list:
                self.results += result
            else:
                self.results += [result]
            return

        char = path[0]
        if not char in self.children:
            self.children[char] = (False, Trie())
        if lookahead_barriers and lookahead_barriers[0] == 0:
            lookahead_barriers = lookahead_barriers[1:]
            self.children[char] = (True, self.children[char][1])
        self.children[char][1]._insert(path[1:], result, [b - 1 for b in lookahead_barriers])

    def insert(self, path: str, result: Union[int, List[int]], lookahead_barriers=[]):
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
    def _serialize(self, serializer: Serializer, hashtable, output: bytearray, merge_subtrees) -> int:
        # Serialize all children first
        child_chars_offsets_barriers = []
        for char, child in self.children.items():
            offset = child[1]._serialize(serializer, hashtable, output, merge_subtrees=merge_subtrees)
            child_chars_offsets_barriers += [(char, offset, child[0])]

        # Serialize this node
        serialized = serializer.pack_trie_node(self.results, child_chars_offsets_barriers)

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

    def serialize(self, serializer: Serializer, merge_subtrees=True) -> bytearray:
        output = bytearray(b'\x00\x00\x00\x00')
        hashtable = {}
        output[0:4] = serializer.pack_trie_root_offset(self._serialize(serializer, hashtable, output, merge_subtrees=merge_subtrees))
        return output

def serialize_type_map(serializer: Serializer, map: List[Tuple[CssClass, str]]) -> bytearray:
    serialized = bytearray()
    names = bytearray()

    # There's just 16 bits for the type and we're using one for aliases, so
    # that makes at most 15 values left. See ResultFlag for details.
    assert len(map) <= 15

    # Initial name offset is after all the offset entries plus the final one
    initial_name_offset = (len(map) + 1)*serializer.type_map_entry_struct.size

    # Add all entries (and the final offset), encode the names separately,
    # concatenate at the end
    for css_class, name in map:
        serialized += serializer.pack_type_map_entry(css_class.value, initial_name_offset + len(names))
        names += name.encode('utf-8')
    serialized += serializer.pack_type_map_entry(0, initial_name_offset + len(names))
    assert len(serialized) == initial_name_offset

    return serialized + names

def serialize_search_data(serializer: Serializer, trie: Trie, map: ResultMap, type_map: List[Tuple[CssClass, str]], symbol_count, *, merge_subtrees=True, merge_prefixes=True) -> bytearray:
    serialized_trie = trie.serialize(serializer, merge_subtrees=merge_subtrees)
    serialized_map = map.serialize(serializer, merge_prefixes=merge_prefixes)
    serialized_type_map = serialize_type_map(serializer, type_map)

    preamble = serializer.pack_header(symbol_count, len(serialized_trie), len(serialized_map))
    return preamble + serialized_trie + serialized_map + serialized_type_map

def base85encode_search_data(data: bytearray) -> bytearray:
    return (b"/* Generated by https://mcss.mosra.cz/documentation/doxygen/. Do not edit. */\n" +
            b"Search.load('" + base64.b85encode(data, True) + b"');\n")

def _pretty_print_trie(deserializer: Deserializer, serialized: bytearray, hashtable, stats, base_offset, indent, *, show_merged, show_lookahead_barriers, color_map) -> str:
    # Visualize where the trees were merged
    if show_merged and base_offset in hashtable:
        return color_map['red'] + '#' + color_map['reset']

    stats.node_count += 1

    out = ''
    result_ids, child_chars_offsets_barriers, offset = deserializer.unpack_trie_node(serialized, base_offset)

    stats.max_node_results = max(len(result_ids), stats.max_node_results)
    stats.max_node_children = max(len(child_chars_offsets_barriers), stats.max_node_children)

    # print results, if any
    if result_ids:
        out += color_map['blue'] + ' ['
        for i, result in enumerate(result_ids):
            if i: out += color_map['blue']+', '
            stats.max_node_result_index = max(result, stats.max_node_result_index)
            out += color_map['cyan'] + str(result)
        out += color_map['blue'] + ']'

    # print children, if any
    for i, (char, offset, barrier) in enumerate(child_chars_offsets_barriers):
        if len(result_ids) or i:
            out += color_map['reset'] + '\n'
            out += color_map['blue'] + indent + color_map['white']
        if char <= 127:
            out += chr(char)
        else:
            out += color_map['reset'] + hex(char)
        if (show_lookahead_barriers and barrier):
            out += color_map['green'] + '$'
        if char > 127 or (show_lookahead_barriers and barrier):
            out += color_map['reset'] + '\n' + color_map['blue'] + indent + ' ' + color_map['white']
        stats.max_node_child_offset = max(offset, stats.max_node_child_offset)
        out += _pretty_print_trie(deserializer, serialized, hashtable, stats, offset, indent + ('|' if len(child_chars_offsets_barriers) > 1 else ' '), show_merged=show_merged, show_lookahead_barriers=show_lookahead_barriers, color_map=color_map)

    hashtable[base_offset] = True
    return out

color_map_colors = {'blue': '\033[0;34m',
                    'white': '\033[1;39m',
                    'red': '\033[1;31m',
                    'green': '\033[1;32m',
                    'cyan': '\033[1;36m',
                    'yellow': '\033[1;33m',
                    'reset': '\033[0m'}

color_map_dummy = {'blue': '',
                   'white': '',
                   'red': '',
                   'green': '',
                   'cyan': '',
                   'yellow': '',
                   'reset': ''}

def pretty_print_trie(deserializer: Deserializer, serialized: bytes, *, show_merged=False, show_lookahead_barriers=True, colors=False):
    color_map = color_map_colors if colors else color_map_dummy

    hashtable = {}

    stats = Empty()
    stats.node_count = 0
    stats.max_node_results = 0
    stats.max_node_children = 0
    stats.max_node_result_index = 0
    stats.max_node_child_offset = 0

    out = _pretty_print_trie(deserializer, serialized, hashtable, stats, deserializer.unpack_trie_root_offset(serialized, 0)[0], '', show_merged=show_merged, show_lookahead_barriers=show_lookahead_barriers, color_map=color_map)
    if out: out = color_map['white'] + out
    stats = """
node count:             {}
max node results:       {}
max node children:      {}
max node result index:  {}
max node child offset:  {}""".lstrip().format(stats.node_count, stats.max_node_results, stats.max_node_children, stats.max_node_result_index, stats.max_node_child_offset)
    return out, stats

def pretty_print_map(deserializer: Deserializer, serialized: bytes, *, entryTypeClass, colors=False):
    color_map = color_map_colors if colors else color_map_dummy

    # The first item gives out offset of first value, which can be used to
    # calculate total value count
    offset, offset_size = deserializer.unpack_result_map_offset(serialized, 0)
    size = int((offset - offset_size)/(offset_size + Serializer.result_map_flag_bytes))
    flags_offset = (size + 1)*offset_size

    out = ''
    for i in range(size):
        if i: out += '\n'
        flags = ResultFlag(deserializer.unpack_result_map_flags(serialized, flags_offset + i*Serializer.result_map_flag_bytes)[0])
        extra = []
        if flags & ResultFlag._TYPE == ResultFlag.ALIAS:
            alias, alias_bytes = deserializer.unpack_result_map_alias(serialized, offset)
            extra += ['alias={}'.format(alias)]
            offset += alias_bytes
        if flags & ResultFlag.HAS_PREFIX:
            prefix_id, prefix_length, prefix_bytes = deserializer.unpack_result_map_prefix(serialized, offset)
            extra += ['prefix={}[:{}]'.format(prefix_id, prefix_length)]
            offset += prefix_bytes
        if flags & ResultFlag.HAS_SUFFIX:
            suffix_length, suffix_bytes = deserializer.unpack_result_map_suffix_length(serialized, offset)
            extra += ['suffix_length={}'.format(suffix_length)]
            offset += suffix_bytes
        if flags & ResultFlag.DEPRECATED:
            extra += ['deprecated']
        if flags & ResultFlag.DELETED:
            extra += ['deleted']
        if flags & ResultFlag._TYPE:
            extra += ['type={}'.format(entryTypeClass(flags.type).name)]
        next_offset = deserializer.unpack_result_map_offset(serialized, (i + 1)*offset_size)[0]
        name, _, url = serialized[offset:next_offset].partition(b'\0')
        out += color_map['cyan'] + str(i) + color_map['blue'] + ': ' + color_map['white'] + name.decode('utf-8') + color_map['blue'] + ' [' + color_map['yellow'] + (color_map['blue'] + ', ' + color_map['yellow']).join(extra) + color_map['blue'] + '] ->' + (' ' + color_map['reset'] + url.decode('utf-8') if url else '')
        offset = next_offset
    return out

def pretty_print_type_map(deserializer: Deserializer, serialized: bytes, *, entryTypeClass):
    # Unpack until we aren't at EOF
    i = 0
    out = ''
    class_id, name_offset, type_map_bytes = deserializer.unpack_type_map_entry(serialized, 0)
    while name_offset < len(serialized):
        if i: out += ',\n'
        next_class_id, next_name_offset = deserializer.unpack_type_map_entry(serialized, (i + 1)*type_map_bytes)[:2]
        out += "({}, {}, '{}')".format(entryTypeClass(i + 1), CssClass(class_id), serialized[name_offset:next_name_offset].decode('utf-8'))
        i += 1
        class_id, name_offset = next_class_id, next_name_offset
    return out

def pretty_print(serialized: bytes, *, entryTypeClass, show_merged=False, show_lookahead_barriers=True, colors=False):
    deserializer = Deserializer.from_serialized(serialized)

    pretty_trie, stats = pretty_print_trie(deserializer, serialized[Serializer.header_struct.size:deserializer.map_offset], show_merged=show_merged, show_lookahead_barriers=show_lookahead_barriers, colors=colors)
    pretty_map = pretty_print_map(deserializer, serialized[deserializer.map_offset:deserializer.type_map_offset], entryTypeClass=entryTypeClass, colors=colors)
    pretty_type_map = pretty_print_type_map(deserializer, serialized[deserializer.type_map_offset:], entryTypeClass=entryTypeClass)
    return '{} symbols\n'.format(deserializer.symbol_count) + pretty_trie + '\n' + pretty_map + '\n' + pretty_type_map, stats
