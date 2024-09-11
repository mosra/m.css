#!/usr/bin/env python3

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

import argparse
import os
import sys

from doxygen import EntryType
from _search import pretty_print, searchdata_filename

from test_doxygen import IntegrationTestCase

class Search(IntegrationTestCase):
    def test(self):
        self.run_doxygen(index_pages=[], wildcard='*.xml')

        with open(os.path.join(self.path, 'html', searchdata_filename.format(search_filename_prefix='secretblob')), 'rb') as f:
            serialized = f.read()
            search_data_pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        #print(search_data_pretty)
        self.assertEqual(len(serialized), 4841)
        self.assertEqual(search_data_pretty, """
53 symbols
deprecated_macro [0]
||        |     ($
||        |      ) [1]
||        dir [23]
||        |  /$
||        |   deprecatedfile.h [2]
||        file.h [2]
||        |oo [37]
||        || ($
||        ||  ) [38]
||         list [22]
||        namespace [39]
||        |        :$
||        |         :deprecatedenum [32]
||        |          |         |   :$
||        |          |         |    :value [31]
||        |          |         typedef [35]
||        |          |         variable [36]
||        |          |         foo [37]
||        |          |         |  ($
||        |          |         |   ) [38]
||        |          |         class [53]
||        |          |         struct [54]
||        |          |         union [58]
||        |          enum [34]
||        |          |   :$
||        |          |    :deprecatedvalue [33]
||        enum [32]
||        |   :$
||        |    :value [31]
||        value [33]
||        | riable [36]
||        typedef [35]
||        class [53]
||        struct [54]
||        union [58]
|ir [24]
|| /$
||  file.h [9]
macro [3]
||   _function [5]
||            ($
||             ) [6]
||            _with_params [7]
||            |           ($
||            |            ) [8]
|in() [49]
glmacro() [4]
| file() [10]
| |oo() [13]
| class() [21]
| directory() [25]
| |  () [26]
| _dir [27]
| |group [30]
| |enum [45]
| ||   _value [43]
| ||         _ext [42]
| |typedef [47]
| namespace() [51]
| struct() [56]
| union() [60]
file.h [9]
|oo [11, 14, 18, 16]
|| ($
||  ) [12, 15, 19, 17]
namespace [50]
|        :$
|         :class [20]
|          |    :$
|          |     :foo [11, 14, 18, 16]
|          |         ($
|          |          ) [12, 15, 19, 17]
|          enum [44]
|          |   :$
|          |    :onlyabrief [40]
|          |     value [41]
|          typedef [46]
|          variable [48]
|          struct [55]
|          union [59]
class [20]
|    :$
|     :foo [11, 14, 18, 16]
|         ($
|          ) [12, 15, 19, 17]
a group [29, 28]
| page [52]
| |    $
| |    0xc2
| |     0xbb
| |       subpage [57]
value [41, 31]
| riable [48]
enum [44, 34]
|   :$
|    :deprecatedvalue [33]
|     onlyabrief [40]
|     value [41]
onlyabrief [40]
typedef [46]
struct [55]
|ubpage [57]
union [59]
0: DEPRECATED_MACRO(a, b, c) [suffix_length=9, deprecated, type=DEFINE] -> DeprecatedFile_8h.html#a7f8376730349fef9ff7d103b0245a13e
1:  [prefix=0[:56], suffix_length=7, deprecated, type=DEFINE] ->
2: /DeprecatedFile.h [prefix=23[:0], deprecated, type=FILE] -> DeprecatedFile_8h.html
3: MACRO [type=DEFINE] -> File_8h.html#a824c99cb152a3c2e9111a2cb9c34891e
4: glMacro() [alias=3] ->
5: _FUNCTION() [prefix=3[:14], suffix_length=2, type=DEFINE] -> 025158d6007b306645a8eb7c7a9237c1
6:  [prefix=5[:46], type=DEFINE] ->
7: _FUNCTION_WITH_PARAMS(params) [prefix=3[:15], suffix_length=8, type=DEFINE] -> 8602bba5a72becb4f2dc544ce12c420
8:  [prefix=7[:46], suffix_length=6, type=DEFINE] ->
9: /File.h [prefix=24[:0], type=FILE] -> File_8h.html
10: glFile() [alias=9] ->
11: ::foo() [prefix=20[:28], suffix_length=2, type=FUNC] -> #aaeba4096356215868370d6ea476bf5d9
12:  [prefix=11[:62], type=FUNC] ->
13: glFoo() [alias=11] ->
14:  const [prefix=11[:30], suffix_length=8, type=FUNC] -> c03c5b93907dda16763eabd26b25500a
15:  [prefix=14[:62], suffix_length=6, type=FUNC] ->
16:  && [prefix=11[:30], suffix_length=5, deleted, type=FUNC] -> 77803233441965cad057a6619e9a75fd
17:  [prefix=16[:62], suffix_length=3, deleted, type=FUNC] ->
18: ::foo(const Enum&, Typedef) [prefix=20[:28], suffix_length=22, type=FUNC] -> #aba8d57a830d4d79f86d58d92298677fa
19:  [prefix=18[:62], suffix_length=20, type=FUNC] ->
20: ::Class [prefix=50[:0], type=CLASS] -> classNamespace_1_1Class.html
21: glClass() [alias=20] ->
22: Deprecated List [type=PAGE] -> deprecated.html
23: DeprecatedDir [deprecated, type=DIR] -> dir_c6c97faf5a6cbd0f62c27843ce3af4d0.html
24: Dir [type=DIR] -> dir_da5033def2d0db76e9883b31b76b3d0c.html
25: glDirectory() [alias=24] ->
26: glDir() [alias=24] ->
27: GL_DIR [alias=24] ->
28: A group [deprecated, type=GROUP] -> group__deprecated-group.html
29: A group [type=GROUP] -> group__group.html
30: GL_GROUP [alias=29] ->
31: ::Value [prefix=32[:67], type=ENUM_VALUE] -> a689202409e48743b914713f96d93947c
32: ::DeprecatedEnum [prefix=39[:33], deprecated, type=ENUM] -> #ab1e37ddc1d65765f2a48485df4af7b47
33: ::DeprecatedValue [prefix=34[:67], deprecated, type=ENUM_VALUE] -> a4b5b0e9709902228c33df7e5e377e596
34: ::Enum [prefix=39[:33], type=ENUM] -> #ac59010e983270c330b8625b5433961b9
35: ::DeprecatedTypedef [prefix=39[:33], deprecated, type=TYPEDEF] -> #af503ad3ff194a4c2512aff16df771164
36: ::DeprecatedVariable [prefix=39[:33], deprecated, type=VAR] -> #ae934297fc39624409333eefbfeabf5e5
37: ::deprecatedFoo(int, bool, double) [prefix=39[:33], suffix_length=19, deprecated, type=FUNC] -> #a9a1b3fc71d294b548095985acc0d5092
38:  [prefix=37[:67], suffix_length=17, deprecated, type=FUNC] ->
39: DeprecatedNamespace [deprecated, type=NAMESPACE] -> namespaceDeprecatedNamespace.html
40: ::OnlyABrief [prefix=44[:57], type=ENUM_VALUE] -> a9b0246417d89d650ed429f1b784805eb
41: ::Value [prefix=44[:57], type=ENUM_VALUE] -> a689202409e48743b914713f96d93947c
42: _EXT [alias=41, prefix=43[:0]] ->
43: _VALUE [alias=41, prefix=45[:0]] ->
44: ::Enum [prefix=50[:23], type=ENUM] -> #add172b93283b1ab7612c3ca6cc5dcfea
45: GL_ENUM [alias=44] ->
46: ::Typedef [prefix=50[:23], type=TYPEDEF] -> #abe2a245304bc2234927ef33175646e08
47: GL_TYPEDEF [alias=46] ->
48: ::Variable [prefix=50[:23], type=VAR] -> #ad3121960d8665ab045ca1bfa1480a86d
49: GLSL: min() [alias=48, suffix_length=2] ->
50: Namespace [type=NAMESPACE] -> namespaceNamespace.html
51: glNamespace() [alias=50] ->
52: A page [type=PAGE] -> page.html
53: ::DeprecatedClass [prefix=39[:0], deprecated, type=STRUCT] -> structDeprecatedNamespace_1_1DeprecatedClass.html
54: ::DeprecatedStruct [prefix=39[:0], deprecated, type=STRUCT] -> structDeprecatedNamespace_1_1DeprecatedStruct.html
55: ::Struct [prefix=50[:0], type=STRUCT] -> structNamespace_1_1Struct.html
56: glStruct() [alias=55] ->
57:  » Subpage [prefix=52[:0], type=PAGE] -> subpage.html
58: ::DeprecatedUnion [prefix=39[:0], deprecated, type=UNION] -> unionDeprecatedNamespace_1_1DeprecatedUnion.html
59: ::Union [prefix=50[:0], type=UNION] -> unionNamespace_1_1Union.html
60: glUnion() [alias=59] ->
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.NAMESPACE, CssClass.PRIMARY, 'namespace'),
(EntryType.GROUP, CssClass.SUCCESS, 'group'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.STRUCT, CssClass.PRIMARY, 'struct'),
(EntryType.UNION, CssClass.PRIMARY, 'union'),
(EntryType.TYPEDEF, CssClass.PRIMARY, 'typedef'),
(EntryType.DIR, CssClass.WARNING, 'dir'),
(EntryType.FILE, CssClass.WARNING, 'file'),
(EntryType.FUNC, CssClass.INFO, 'func'),
(EntryType.DEFINE, CssClass.INFO, 'define'),
(EntryType.ENUM, CssClass.PRIMARY, 'enum'),
(EntryType.ENUM_VALUE, CssClass.DEFAULT, 'enum val'),
(EntryType.VAR, CssClass.DEFAULT, 'var')
""".strip())

    def test_byte_sizes(self):
        for config, bytes, size in [
            ('SEARCH_RESULT_ID_BYTES', 3, 4959),
            ('SEARCH_RESULT_ID_BYTES', 4, 5077),
            ('SEARCH_FILE_OFFSET_BYTES', 4, 5302),
            ('SEARCH_NAME_SIZE_BYTES', 2, 4893)
        ]:
            with self.subTest(config=config, bytes=bytes, size=size):
                self.run_doxygen(index_pages=[], wildcard='*.xml', config={
                    config: bytes
                })

                with open(os.path.join(self.path, 'html', searchdata_filename.format(search_filename_prefix='secretblob')), 'rb') as f:
                    serialized = f.read()
                self.assertEqual(len(serialized), size)

class LongSuffixLength(IntegrationTestCase):
    def test(self):
        self.run_doxygen(index_pages=[], wildcard='*.xml')

        with open(os.path.join(self.path, 'html', searchdata_filename.format(search_filename_prefix='searchdata')), 'rb') as f:
            serialized = f.read()
            search_data_pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        #print(search_data_pretty)
        self.assertEqual(len(serialized), 478)
        # The parameters get cut off with an ellipsis
        self.assertEqual(search_data_pretty, """
2 symbols
file.h [2]
|     :$
|      :averylongfunctionname [0]
|                            ($
|                             ) [1]
averylongfunctionname [0]
|                    ($
|                     ) [1]
0: ::aVeryLongFunctionName(const std::reference_wrapper<const std::vector<s…) [prefix=2[:12], suffix_length=53, type=FUNC] -> #a1e9a11887275938ef5541070955c9d9c
1:  [prefix=0[:46], suffix_length=51, type=FUNC] ->
2: File.h [type=FILE] -> File_8h.html
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.NAMESPACE, CssClass.PRIMARY, 'namespace'),
(EntryType.GROUP, CssClass.SUCCESS, 'group'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.STRUCT, CssClass.PRIMARY, 'struct'),
(EntryType.UNION, CssClass.PRIMARY, 'union'),
(EntryType.TYPEDEF, CssClass.PRIMARY, 'typedef'),
(EntryType.DIR, CssClass.WARNING, 'dir'),
(EntryType.FILE, CssClass.WARNING, 'file'),
(EntryType.FUNC, CssClass.INFO, 'func'),
(EntryType.DEFINE, CssClass.INFO, 'define'),
(EntryType.ENUM, CssClass.PRIMARY, 'enum'),
(EntryType.ENUM_VALUE, CssClass.DEFAULT, 'enum val'),
(EntryType.VAR, CssClass.DEFAULT, 'var')
""".strip())

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="file to pretty-print")
    parser.add_argument('--show-merged', help="show merged subtrees", action='store_true')
    parser.add_argument('--show-lookahead-barriers', help="show lookahead barriers", action='store_true')
    parser.add_argument('--colors', help="colored output", action='store_true')
    parser.add_argument('--show-stats', help="show stats", action='store_true')
    args = parser.parse_args()

    with open(args.file, 'rb') as f:
        out, stats = pretty_print(f.read(), entryTypeClass=EntryType, show_merged=args.show_merged, show_lookahead_barriers=args.show_lookahead_barriers, colors=args.colors)
        print(out)
        if args.show_stats: print(stats, file=sys.stderr)
