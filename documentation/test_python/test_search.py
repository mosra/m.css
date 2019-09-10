#!/usr/bin/env python3

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

import os

from _search import searchdata_filename, pretty_print
from python import EntryType

from test_python import BaseInspectTestCase

class Search(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'SEARCH_DISABLED': False,
            'SEARCH_DOWNLOAD_BINARY': True,
            'PYBIND11_COMPATIBILITY': True
        })

        with open(os.path.join(self.path, 'output', searchdata_filename), 'rb') as f:
            serialized = f.read()
            search_data_pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        #print(search_data_pretty)
        self.assertEqual(len(serialized), 2076)
        self.assertEqual(search_data_pretty, """
19 symbols
search [12]
||    .$
||     foo [7]
||     || .$
||     ||  enum [0]
||     ||  |   .$
||     ||  |    a_value [1]
||     ||  |     nother [2]
||     ||  a_method [3]
||     ||  | |     ($
||     ||  | |      ) [4]
||     ||  | property [5]
||     ||  data_declaration [6]
||     |unc_with_params [10]
||     ||              ($
||     ||               ) [11]
||     a_function [8]
||     |         ($
||     |          ) [9]
||     pybind [24]
||     |     .$
||     |      foo [19]
||     |       | .$
||     |       |  overloaded_method [15, 17, 13]
||     |       |                   ($
||     |       |                    ) [16, 18, 14]
||     |       unction [20]
||     |       |      ($
||     |       |       ) [21]
||     |       |      _with_params [22]
||     |       |      |           ($
||     |       |      |            ) [23]
||     sub [26]
||     |  .$
||     |   data_in_a_submodule [25]
|ub [26]
|| .$
||  data_in_a_submodule [25]
foo [7, 19]
|| .$
||  enum [0]
||  |   .$
||  |    a_value [1]
||  |     nother [2]
||  a_method [3]
||  | |     ($
||  | |      ) [4]
||  | property [5]
||  data_declaration [6]
||  overloaded_method [15, 17, 13]
||  |                ($
||  |                 ) [16, 18, 14]
|unc_with_params [10]
||  |           ($
||  |            ) [11]
||  tion [20]
||  |   ($
||  |    ) [21]
||  |   _with_params [22]
||  |   |           ($
||  |   |            ) [23]
enum [0]
|   .$
|    a_value [1]
|     nother [2]
a_value [1]
||method [3]
|||     ($
|||      ) [4]
||property [5]
||function [8]
|||       ($
|||        ) [9]
|nother [2]
data_declaration [6]
|    in_a_submodule [25]
pybind [24]
|     .$
|      foo [19]
|       | .$
|       |  overloaded_method [15, 17, 13]
|       |                   ($
|       |                    ) [16, 18, 14]
|       unction [20]
|       |      ($
|       |       ) [21]
|       |      _with_params [22]
|       |      |           ($
|       |      |            ) [23]
overloaded_method [15, 17, 13]
|                ($
|                 ) [16, 18, 14]
0: .Enum [prefix=7[:15], type=ENUM] -> #Enum
1: .A_VALUE [prefix=0[:20], type=ENUM_VALUE] -> -A_VALUE
2: .ANOTHER [prefix=0[:20], type=ENUM_VALUE] -> -ANOTHER
3: .a_method() [prefix=7[:15], suffix_length=2, type=FUNCTION] -> #a_method
4:  [prefix=3[:24], type=FUNCTION] ->
5: .a_property [prefix=7[:15], type=PROPERTY] -> #a_property
6: .DATA_DECLARATION [prefix=7[:15], type=DATA] -> #DATA_DECLARATION
7: .Foo [prefix=12[:7], type=CLASS] -> Foo.html
8: .a_function() [prefix=12[:11], suffix_length=2, type=FUNCTION] -> #a_function
9:  [prefix=8[:22], type=FUNCTION] ->
10: .func_with_params() [prefix=12[:11], suffix_length=2, type=FUNCTION] -> #func_with_params
11:  [prefix=10[:28], type=FUNCTION] ->
12: search [type=MODULE] -> search.html
13: .overloaded_method(self, first: int, second: float) [prefix=19[:22], suffix_length=33, type=FUNCTION] -> #overloaded_method-27269
14:  [prefix=13[:46], suffix_length=31, type=FUNCTION] ->
15: .overloaded_method(self, arg0: int) [prefix=19[:22], suffix_length=17, type=FUNCTION] -> #overloaded_method-745a3
16:  [prefix=15[:46], suffix_length=15, type=FUNCTION] ->
17: .overloaded_method(self, arg0: int, arg1: Foo) [prefix=19[:22], suffix_length=28, type=FUNCTION] -> #overloaded_method-41cfb
18:  [prefix=17[:46], suffix_length=26, type=FUNCTION] ->
19: .Foo [prefix=24[:14], type=CLASS] -> Foo.html
20: .function() [prefix=24[:18], suffix_length=2, type=FUNCTION] -> #function
21:  [prefix=20[:27], type=FUNCTION] ->
22: .function_with_params() [prefix=24[:18], suffix_length=2, type=FUNCTION] -> #function_with_params
23:  [prefix=22[:39], type=FUNCTION] ->
24: .pybind [prefix=12[:7], type=MODULE] -> pybind.html
25: .DATA_IN_A_SUBMODULE [prefix=26[:15], type=DATA] -> #DATA_IN_A_SUBMODULE
26: .sub [prefix=12[:7], type=MODULE] -> sub.html
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.MODULE, CssClass.PRIMARY, 'module'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.FUNCTION, CssClass.INFO, 'func'),
(EntryType.PROPERTY, CssClass.WARNING, 'property'),
(EntryType.ENUM, CssClass.PRIMARY, 'enum'),
(EntryType.ENUM_VALUE, CssClass.DEFAULT, 'enum val'),
(EntryType.DATA, CssClass.DEFAULT, 'data')
""".strip())

class LongSuffixLength(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'SEARCH_DISABLED': False,
            'SEARCH_DOWNLOAD_BINARY': True,
            'PYBIND11_COMPATIBILITY': True
        })

        with open(os.path.join(self.path, 'output', searchdata_filename), 'rb') as f:
            serialized = f.read()
            search_data_pretty = pretty_print(serialized, entryTypeClass=EntryType)[0]
        #print(search_data_pretty)
        self.assertEqual(len(serialized), 633)
        # The parameters get cut off with an ellipsis
        self.assertEqual(search_data_pretty, """
3 symbols
search_long_suffix_length [4]
|                        .$
|                         many_parameters [0, 2]
|                                        ($
|                                         ) [1, 3]
many_parameters [0, 2]
|              ($
|               ) [1, 3]
0: .many_parameters(arg0: typing.Tuple[float, int, str, typing.List[…) [prefix=4[:30], suffix_length=53, type=FUNCTION] -> #many_parameters-06151
1:  [prefix=0[:52], suffix_length=51, type=FUNCTION] ->
2: .many_parameters(arg0: typing.Tuple[int, float, str, typing.List[…) [prefix=4[:30], suffix_length=53, type=FUNCTION] -> #many_parameters-31300
3:  [prefix=2[:52], suffix_length=51, type=FUNCTION] ->
4: search_long_suffix_length [type=MODULE] -> search_long_suffix_length.html
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.MODULE, CssClass.PRIMARY, 'module'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.FUNCTION, CssClass.INFO, 'func'),
(EntryType.PROPERTY, CssClass.WARNING, 'property'),
(EntryType.ENUM, CssClass.PRIMARY, 'enum'),
(EntryType.ENUM_VALUE, CssClass.DEFAULT, 'enum val'),
(EntryType.DATA, CssClass.DEFAULT, 'data')
""".strip())
