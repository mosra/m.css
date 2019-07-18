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
        self.assertEqual(len(serialized), 1918)
        self.assertEqual(search_data_pretty, """
18 symbols
search [11]
||    .$
||     foo [6]
||     || .$
||     ||  enum [0]
||     ||  |   .$
||     ||  |    a_value [1]
||     ||  |     nother [2]
||     ||  a_method [3]
||     ||  | |     ($
||     ||  | |      ) [4]
||     ||  | property [5]
||     |unc_with_params [9]
||     ||              ($
||     ||               ) [10]
||     a_function [7]
||     |         ($
||     |          ) [8]
||     pybind [23]
||     |     .$
||     |      foo [16]
||     |      |  .$
||     |      |   method [12]
||     |      |         ($
||     |      |          ) [13]
||     |      |         _with_params [14]
||     |      |         |           ($
||     |      |         |            ) [15]
||     |      overloaded_function [19, 21, 17]
||     |      |                  ($
||     |      |                   ) [20, 22, 18]
||     sub [25]
||     |  .$
||     |   data_in_a_submodule [24]
|ub [25]
|| .$
||  data_in_a_submodule [24]
foo [6, 16]
|| .$
||  enum [0]
||  |   .$
||  |    a_value [1]
||  |     nother [2]
||  a_method [3]
||  | |     ($
||  | |      ) [4]
||  | property [5]
||  method [12]
||  |     ($
||  |      ) [13]
||  |     _with_params [14]
||  |     |           ($
||  |     |            ) [15]
|unc_with_params [9]
||              ($
||               ) [10]
enum [0]
|   .$
|    a_value [1]
|     nother [2]
a_value [1]
||method [3]
|||     ($
|||      ) [4]
||property [5]
||function [7]
|||       ($
|||        ) [8]
|nother [2]
pybind [23]
|     .$
|      foo [16]
|      |  .$
|      |   method [12]
|      |         ($
|      |          ) [13]
|      |         _with_params [14]
|      |         |           ($
|      |         |            ) [15]
|      overloaded_function [19, 21, 17]
|      |                  ($
|      |                   ) [20, 22, 18]
method [12]
|     ($
|      ) [13]
|     _with_params [14]
|     |           ($
|     |            ) [15]
overloaded_function [19, 21, 17]
|                  ($
|                   ) [20, 22, 18]
data_in_a_submodule [24]
0: .Enum [prefix=6[:15], type=ENUM] -> #Enum
1: .A_VALUE [prefix=0[:20], type=ENUM_VALUE] -> -A_VALUE
2: .ANOTHER [prefix=0[:20], type=ENUM_VALUE] -> -ANOTHER
3: .a_method() [prefix=6[:15], suffix_length=2, type=FUNCTION] -> #a_method
4:  [prefix=3[:24], type=FUNCTION] ->
5: .a_property [prefix=6[:15], type=PROPERTY] -> #a_property
6: .Foo [prefix=11[:7], type=CLASS] -> Foo.html
7: .a_function() [prefix=11[:11], suffix_length=2, type=FUNCTION] -> #a_function
8:  [prefix=7[:22], type=FUNCTION] ->
9: .func_with_params() [prefix=11[:11], suffix_length=2, type=FUNCTION] -> #func_with_params
10:  [prefix=9[:28], type=FUNCTION] ->
11: search [type=MODULE] -> search.html
12: .method(self) [prefix=16[:22], suffix_length=6, type=FUNCTION] -> #method-6eef6
13:  [prefix=12[:35], suffix_length=4, type=FUNCTION] ->
14: .method_with_params(self, first: int, second: float) [prefix=16[:22], suffix_length=33, type=FUNCTION] -> #method_with_params-27269
15:  [prefix=14[:47], suffix_length=31, type=FUNCTION] ->
16: .Foo [prefix=23[:14], type=CLASS] -> Foo.html
17: .overloaded_function(arg0: int, arg1: float) [prefix=23[:18], suffix_length=24, type=FUNCTION] -> #overloaded_function-8f19c
18:  [prefix=17[:44], suffix_length=22, type=FUNCTION] ->
19: .overloaded_function(arg0: int) [prefix=23[:18], suffix_length=11, type=FUNCTION] -> #overloaded_function-46f8a
20:  [prefix=19[:44], suffix_length=9, type=FUNCTION] ->
21: .overloaded_function(arg0: int, arg1: Foo) [prefix=23[:18], suffix_length=22, type=FUNCTION] -> #overloaded_function-0cacd
22:  [prefix=21[:44], suffix_length=20, type=FUNCTION] ->
23: .pybind [prefix=11[:7], type=MODULE] -> pybind.html
24: .DATA_IN_A_SUBMODULE [prefix=25[:15], type=DATA] -> #DATA_IN_A_SUBMODULE
25: .sub [prefix=11[:7], type=MODULE] -> sub.html
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
        self.assertEqual(len(serialized), 521)
        # The parameters get cut off with an ellipsis
        self.assertEqual(search_data_pretty, """
2 symbols
search_long_suffix_length [2]
|                        .$
|                         many_parameters [0]
|                                        ($
|                                         ) [1]
many_parameters [0]
|              ($
|               ) [1]
0: .many_parameters(arg0: Tuple[int, float, str, List[Tuple[int, int…) [prefix=2[:30], suffix_length=53, type=FUNCTION] -> #many_parameters-5ce5b
1:  [prefix=0[:52], suffix_length=51, type=FUNCTION] ->
2: search_long_suffix_length [type=MODULE] -> search_long_suffix_length.html
(EntryType.PAGE, CssClass.SUCCESS, 'page'),
(EntryType.MODULE, CssClass.PRIMARY, 'module'),
(EntryType.CLASS, CssClass.PRIMARY, 'class'),
(EntryType.FUNCTION, CssClass.INFO, 'func'),
(EntryType.PROPERTY, CssClass.WARNING, 'property'),
(EntryType.ENUM, CssClass.PRIMARY, 'enum'),
(EntryType.ENUM_VALUE, CssClass.DEFAULT, 'enum val'),
(EntryType.DATA, CssClass.DEFAULT, 'data')
""".strip())
