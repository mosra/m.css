#!/usr/bin/env python3

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
        self.assertEqual(len(serialized), 2585)
        self.assertEqual(search_data_pretty, """
21 symbols
search [14]
||    .$
||     foo [7]
||     || .$
||     ||  enum [0]
||     || ||   .$
||     || ||    a_value [1]
||     || ||     nother [2]
||     || |a_method [3]
||     || || |     ($
||     || || |      ) [4]
||     || || property [5]
||     || |data_declaration [6]
||     || withslots [9]
||     || |        .$
||     || |         im_a_sloth [8]
||     |unc_with_params [12]
||     ||              ($
||     ||               ) [13]
||     a_function [10]
||     |         ($
||     |          ) [11]
||     pybind [26]
||     |     .$
||     |      foo [21]
||     |       | .$
||     |       |  overloaded_method [17, 19, 15]
||     |       |                   ($
||     |       |                    ) [18, 20, 16]
||     |       unction [22]
||     |       |      ($
||     |       |       ) [23]
||     |       |      _with_params [24]
||     |       |      |           ($
||     |       |      |            ) [25]
||     sub [28]
||     |  .$
||     |   data_in_a_submodule [27]
|loth [8]
||  s [9]
|ub [28]
|| .$
||  data_in_a_submodule [27]
|| module [27]
foo [7, 21]
|| .$
||  enum [0]
|| ||   .$
|| ||    a_value [1]
|| ||     nother [2]
|| |a_method [3]
|| || |     ($
|| || |      ) [4]
|| || property [5]
|| |data_declaration [6]
|| |overloaded_method [17, 19, 15]
|| ||                ($
|| ||                 ) [18, 20, 16]
|| withslots [9]
|| |        .$
|| |         im_a_sloth [8]
|unction [10, 22]
||  |   ($
||  |    ) [11, 23]
||  |   _with_params [24]
||  |   |           ($
||  |   |            ) [25]
||  _with_params [12]
||  |           ($
||  |            ) [13]
enum [0]
|   .$
|    a_value [1]
|     nother [2]
a_value [1]
||method [3]
|||     ($
|||      ) [4]
||property [5]
||sloth [8]
|||ubmodule [27]
||function [10]
|||       ($
|||        ) [11]
|nother [2]
value [1]
method [3, 17, 19, 15]
|     ($
|      ) [4, 18, 20, 16]
property [5]
|arams [12, 24]
||    ($
||     ) [13, 25]
|ybind [26]
||    .$
||     foo [21]
||      | .$
||      |  overloaded_method [17, 19, 15]
||      |                   ($
||      |                    ) [18, 20, 16]
||      unction [22]
||      |      ($
||      |       ) [23]
||      |      _with_params [24]
||      |      |           ($
||      |      |            ) [25]
data_declaration [6]
||   in_a_submodule [27]
|eclaration [6]
im_a_sloth [8]
|n_a_submodule [27]
withslots [9]
|   _params [12, 24]
|   |      ($
|   |       ) [13, 25]
overloaded_method [17, 19, 15]
|                ($
|                 ) [18, 20, 16]
0: .Enum [prefix=7[:15], type=ENUM] -> #Enum
1: .A_VALUE [prefix=0[:20], type=ENUM_VALUE] -> -A_VALUE
2: .ANOTHER [prefix=0[:20], type=ENUM_VALUE] -> -ANOTHER
3: .a_method() [prefix=7[:15], suffix_length=2, type=FUNCTION] -> #a_method
4:  [prefix=3[:24], type=FUNCTION] ->
5: .a_property [prefix=7[:15], type=PROPERTY] -> #a_property
6: .DATA_DECLARATION [prefix=7[:15], type=DATA] -> #DATA_DECLARATION
7: .Foo [prefix=14[:7], type=CLASS] -> Foo.html
8: .im_a_sloth [prefix=9[:24], type=PROPERTY] -> #im_a_sloth
9: WithSlots [prefix=7[:10], type=CLASS] -> WithSlots.html
10: .a_function() [prefix=14[:11], suffix_length=2, type=FUNCTION] -> #a_function
11:  [prefix=10[:22], type=FUNCTION] ->
12: .func_with_params() [prefix=14[:11], suffix_length=2, type=FUNCTION] -> #func_with_params
13:  [prefix=12[:28], type=FUNCTION] ->
14: search [type=MODULE] -> search.html
15: .overloaded_method(self, first: int, second: float) [prefix=21[:22], suffix_length=33, type=FUNCTION] -> #overloaded_method-27269
16:  [prefix=15[:46], suffix_length=31, type=FUNCTION] ->
17: .overloaded_method(self, arg0: int) [prefix=21[:22], suffix_length=17, type=FUNCTION] -> #overloaded_method-745a3
18:  [prefix=17[:46], suffix_length=15, type=FUNCTION] ->
19: .overloaded_method(self, arg0: int, arg1: Foo) [prefix=21[:22], suffix_length=28, type=FUNCTION] -> #overloaded_method-41cfb
20:  [prefix=19[:46], suffix_length=26, type=FUNCTION] ->
21: .Foo [prefix=26[:14], type=CLASS] -> Foo.html
22: .function() [prefix=26[:18], suffix_length=2, type=FUNCTION] -> #function
23:  [prefix=22[:27], type=FUNCTION] ->
24: .function_with_params() [prefix=26[:18], suffix_length=2, type=FUNCTION] -> #function_with_params
25:  [prefix=24[:39], type=FUNCTION] ->
26: .pybind [prefix=14[:7], type=MODULE] -> pybind.html
27: .DATA_IN_A_SUBMODULE [prefix=28[:15], type=DATA] -> #DATA_IN_A_SUBMODULE
28: .sub [prefix=14[:7], type=MODULE] -> sub.html
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
        self.assertEqual(len(serialized), 755)
        # The parameters get cut off with an ellipsis
        self.assertEqual(search_data_pretty, """
3 symbols
search_long_suffix_length [4]
||                       .$
||                        many_parameters [0, 2]
||                                       ($
||                                        ) [1, 3]
|uffix_length [4]
many_parameters [0, 2]
|              ($
|               ) [1, 3]
parameters [0, 2]
|         ($
|          ) [1, 3]
long_suffix_length [4]
|ength [4]
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
