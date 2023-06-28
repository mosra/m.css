#
#   This file is part of m.css.
#
#   Copyright © 2017, 2018, 2019, 2020, 2021, 2022, 2023
#             Vladimír Vondruš <mosra@centrum.cz>
#   Copyright © 2020 Sergei Izmailov <sergei.a.izmailov@gmail.com>
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

import copy
import sys
import unittest

from python import State, parse_pybind_signature, default_config

from . import BaseInspectTestCase

class Signature(unittest.TestCase):
    # make_type_link() needs state.config['INPUT_MODULES'], simply supply
    # everything there
    state = State(copy.deepcopy(default_config))

    def test(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, a2: module.Thing) -> module.Thing3'),
            ('foo', '', [
                ('a', 'int', 'int', None),
                ('a2', 'module.Thing', 'module.Thing', None),
            ], 'module.Thing3', 'module.Thing3'))

    def test_newline(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, a2: module.Thing) -> module.Thing3\n'),
            ('foo', '', [
                ('a', 'int', 'int', None),
                ('a2', 'module.Thing', 'module.Thing', None),
            ], 'module.Thing3', 'module.Thing3'))

    def test_docs(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, a2: module.Thing) -> module.Thing3\n\nDocs here!!'),
            ('foo', 'Docs here!!', [
                ('a', 'int', 'int', None),
                ('a2', 'module.Thing', 'module.Thing', None),
            ], 'module.Thing3', 'module.Thing3'))

    def test_no_args(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'thingy() -> str'),
            ('thingy', '', [], 'str', 'str'))

    def test_no_return(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            '__init__(self: module.Thing)'),
            ('__init__', '', [
                ('self', 'module.Thing', 'module.Thing', None),
            ], None, None))

    def test_none_return(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            '__init__(self: module.Thing) -> None'),
            ('__init__', '', [
                ('self', 'module.Thing', 'module.Thing', None),
            ], 'None', 'None'))

    def test_no_arg_types(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'thingy(self, the_other_thing)'),
            ('thingy', '', [
                ('self', None, None, None),
                ('the_other_thing', None, None, None),
            ], None, None))

    def test_none_arg_types(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'thingy(self, the_other_thing: Callable[[], None])'),
            ('thingy', '', [
                ('self', None, None, None),
                ('the_other_thing', 'typing.Callable[[], None]', 'typing.Callable[[], None]', None),
            ], None, None))

    def test_square_brackets(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Tuple[int, str], no_really: str) -> List[str]'),
            ('foo', '', [
                ('a', 'typing.Tuple[int, str]', 'typing.Tuple[int, str]', None),
                ('no_really', 'str', 'str', None),
            ], 'typing.List[str]', 'typing.List[str]'))

    def test_nested_square_brackets(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Tuple[int, List[Tuple[int, int]]], another: float) -> Union[str, None]'),
            ('foo', '', [
                ('a', 'typing.Tuple[int, typing.List[typing.Tuple[int, int]]]', 'typing.Tuple[int, typing.List[typing.Tuple[int, int]]]', None),
                ('another', 'float', 'float', None),
            ], 'typing.Union[str, None]', 'typing.Union[str, None]'))

    def test_callable(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Callable[[int, Tuple[int, int]], float], another: float)'),
            ('foo', '', [
                ('a', 'typing.Callable[[int, typing.Tuple[int, int]], float]', 'typing.Callable[[int, typing.Tuple[int, int]], float]', None),
                ('another', 'float', 'float', None),
            ], None, None))

    def test_kwargs(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(*args, **kwargs)'),
            ('foo', '', [
                ('*args', None, None, None),
                ('**kwargs', None, None, None),
            ], None, None))

    def test_keyword_positional_only(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, /, b: float, *, keyword: str)'),
            ('foo', '', [
                ('a', 'int', 'int', None),
                ('/', None, None, None),
                ('b', 'float', 'float', None),
                ('*', None, None, None),
                ('keyword', 'str', 'str', None),
            ], None, None))

    def test_default_values(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: float = 1.0, b: str = \'hello\')'),
            ('foo', '', [
                ('a', 'float', 'float', '1.0'),
                ('b', 'str', 'str', '\'hello\''),
            ], None, None))

        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: float = libA.foo(libB.goo(123), libB.bar + 13) + 2, b = 3)'),
            ('foo', '', [
                ('a', 'float', 'float', 'libA.foo(libB.goo(123), libB.bar + 13) + 2'),
                ('b', None, None, '3'),
            ], None, None))

        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Tuple[int, ...] = (1,("hello", \'world\'),3,4))'),
            ('foo', '', [
                ('a', 'typing.Tuple[int, ...]',
                      'typing.Tuple[int, ...]',
                 '(1,("hello", \'world\'),3,4)')
            ], None, None))

        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: str = [dict(key="A", value=\'B\')["key"][0], None][0])'),
             ('foo', '', [
                 ('a', 'str', 'str', '[dict(key="A", value=\'B\')["key"][0], None][0]')
             ], None, None))

        bad_signature = ('foo', '', [('…', None, None, None)], None, None)

        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: float = [0][)'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: float = ()'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: float = (()'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: float = ))'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: float = ])'), bad_signature)

    # https://github.com/pybind/pybind11/pull/2126, extremely stupid and
    # annoying but what can I do. Want to support both this and the original
    # behavior in case they revert the insanity again, so test that both
    # variants give the same output.
    def test_default_enum_values_pybind26(self):
        # Before the insane change
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: bar.Enum = Enum.FOO_BAR)'),
            ('foo', '', [
                ('a', 'bar.Enum', 'bar.Enum', 'Enum.FOO_BAR')
            ], None, None))

        # After the insane change
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: bar.Enum = <Enum.FOO_BAR: -13376>)'),
            ('foo', '', [
                ('a', 'bar.Enum', 'bar.Enum', 'Enum.FOO_BAR')
            ], None, None))

        # Nested
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: bar.Enum = (4, [<Enum.FOO_BAR: -13376>], <Enum.FIZZ_PISS: 1>))'),
            ('foo', '', [
                ('a', 'bar.Enum', 'bar.Enum', '(4, [Enum.FOO_BAR], Enum.FIZZ_PISS)')
            ], None, None))

        # This isn't really expected to happen but yeah it still treats it as
        # an enum
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Enum = <Enum_MISSING_DOT:>)'),
            ('foo', '', [
                ('a', 'Enum', 'Enum', 'Enum_MISSING_DOT')
            ], None, None))

        # This is how pybind prints various objects, should be passed as-is.
        # It should not corrupt any parameters after.
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: FooBar = <FooBar object at 0xabcd>, b: int = 3)'),
            ('foo', '', [
                ('a', 'FooBar', 'FooBar', '<FooBar object at 0xabcd>'),
                ('b', 'int', 'int', '3')
            ], None, None))

        # This is weird and so will be passed as-is.
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: Enum = <Enum_MISSING_GT: -1)'),
            ('foo', '', [
                ('a', 'Enum', 'Enum', '<Enum_MISSING_GT: -1')
            ], None, None))

        # This will fail
        bad_signature = ('foo', '', [('…', None, None, None)], None, None)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: Enum = <Enum.CHARACTERS_AFTER: 17>a)'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo(a: Enum = <Enum.CHARACTERS_AFTER: 89><)'), bad_signature)

    def test_bad_return_type(self):
        bad_signature = ('foo', '', [('…', None, None, None)], None, None)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo() -> List[[]'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo() -> List]'), bad_signature)
        self.assertEqual(parse_pybind_signature(self.state, [], 'foo() -> ::std::vector<int>'), bad_signature)

    def test_crazy_stuff(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, b: Math::Vector<4, UnsignedInt>)'),
            ('foo', '', [('…', None, None, None)], None, None))

    def test_crazy_stuff_nested(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, b: List[Math::Vector<4, UnsignedInt>])'),
            ('foo', '', [('…', None, None, None)], None, None))

    def test_crazy_stuff_docs(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int, b: Math::Vector<4, UnsignedInt>)\n\nThis is text!!'),
            ('foo', 'This is text!!', [('…', None, None, None)], None, None))

    def test_crazy_return(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int) -> Math::Vector<4, UnsignedInt>'),
            ('foo', '', [('…', None, None, None)], None, None))

    def test_crazy_return_nested(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int) -> List[Math::Vector<4, UnsignedInt>]'),
            ('foo', '', [('…', None, None, None)], None, None))

    def test_crazy_return_docs(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            'foo(a: int) -> Math::Vector<4, UnsignedInt>\n\nThis returns!'),
            ('foo', 'This returns!', [('…', None, None, None)], None, None))

    def test_no_name(self):
        self.assertEqual(parse_pybind_signature(self.state, [],
            '(arg0: MyClass) -> float'),
            ('', '', [('arg0', 'MyClass', 'MyClass', None)], 'float', 'float'))

    def test_name_mapping(self):
        state = copy.deepcopy(self.state)
        state.name_mapping['module._module'] = 'module'

        self.assertEqual(parse_pybind_signature(state, [],
            'foo(a: module._module.Foo, b: typing.Tuple[int, module._module.Bar]) -> module._module.Baz'),
            ('foo', '', [('a', 'module.Foo', 'module.Foo', None),
                         ('b', 'typing.Tuple[int, module.Bar]', 'typing.Tuple[int, module.Bar]', None)], 'module.Baz', 'module.Baz'))

class Signatures(BaseInspectTestCase):
    def test_positional_args(self):
        sys.path.append(self.path)
        import pybind_signatures

        # Verify that the assumptions are correct -- not using py::arg() makes
        # the parameters positional-only, while py::arg() makes them
        # positional-or-keyword
        self.assertEqual(pybind_signatures.scale(14, 0.3), 4)
        with self.assertRaises(TypeError):
            pybind_signatures.scale(arg0=1, arg1=3.0)
        self.assertEqual(pybind_signatures.scale_kwargs(14, 0.3), 4)
        self.assertEqual(pybind_signatures.scale_kwargs(a=14, argument=0.3), 4)

        # Verify the same for classes
        a = pybind_signatures.MyClass()
        self.assertEqual(pybind_signatures.MyClass.instance_function(a, 3, 'bla'), (0.5, 42))
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass.instance_function(self=a, arg0=3, arg1='bla')
        self.assertEqual(pybind_signatures.MyClass.instance_function_kwargs(a, 3, 'bla'), (0.5, 42))
        self.assertEqual(pybind_signatures.MyClass.instance_function_kwargs(self=a, hey=3, what='bla'), (0.5, 42))

        # In particular, the 'self' parameter is positional-only if there are
        # no arguments to use py::arg() for
        self.assertEqual(pybind_signatures.MyClass.another(a), 42)
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass.another(self=a)

    def test_explicit_positional_args(self):
        sys.path.append(self.path)
        import pybind_signatures

        # Similar to above, but these functions have explicit py::pos_only and
        # py::kw_only placeholders

        if not pybind_signatures.MyClass26.is_pybind26:
            self.skipTest("only on pybind 2.6+")

        # The a: int argument is always before the / and thus shouldn't be
        # callable with a keyword
        self.assertEqual(pybind_signatures.MyClass26.positional_only(1, 3.0), 1)
        self.assertEqual(pybind_signatures.MyClass26.positional_keyword_only(1, 3.0), 3)
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass26.positional_only(a=1, b=3.0)
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass26.positional_keyword_only(a=1, b=3.0)

        # The b argument is always between / and * and thus should be callable
        # both without (done above/below) and with
        self.assertEqual(pybind_signatures.MyClass26.positional_only(1, b=3.0), 1)
        self.assertEqual(pybind_signatures.MyClass26.keyword_only(b=3.0), 2)
        self.assertEqual(pybind_signatures.MyClass26.positional_keyword_only(1, b=3.0), 3)

        # The keyword: str argument is always after the / and thus shouldn't be
        # callable without a keyword
        self.assertEqual(pybind_signatures.MyClass26.keyword_only(3.0, keyword='yes'), 2)
        self.assertEqual(pybind_signatures.MyClass26.positional_keyword_only(1, 3.0, keyword='yes'), 3)
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass26.keyword_only(3.0, 'yes')
        with self.assertRaises(TypeError):
            pybind_signatures.MyClass26.positional_keyword_only(1, 3.0, 'yes')

    def test(self):
        sys.path.append(self.path)
        import pybind_signatures
        self.run_python({
            'INPUT_MODULES': [pybind_signatures, 'false_positives'],
            'PYBIND11_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_signatures.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_signatures.MyClass.html'))
        self.assertEqual(*self.actual_expected_contents('false_positives.html'))

        if pybind_signatures.MyClass23.is_pybind23:
            self.assertEqual(*self.actual_expected_contents('pybind_signatures.MyClass23.html'))
        if pybind_signatures.MyClass26.is_pybind26:
            self.assertEqual(*self.actual_expected_contents('pybind_signatures.MyClass26.html'))

class Enums(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'PYBIND11_COMPATIBILITY': True,
        })
        self.assertEqual(*self.actual_expected_contents('pybind_enums.html'))

class Submodules(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PYBIND11_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_submodules.html'))

class SubmodulesPackage(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PYBIND11_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_submodules_package.sub.html'))

class NameMapping(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PYBIND11_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_name_mapping.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_name_mapping.Class.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_name_mapping.submodule.html'))

class TypeLinks(BaseInspectTestCase):
    def test(self):
        sys.path.append(self.path)
        import pybind_type_links
        # Annotate the type of TYPE_DATA (TODO: can this be done from pybind?)
        pybind_type_links.__annotations__ = {}
        pybind_type_links.__annotations__['TYPE_DATA'] = pybind_type_links.Foo
        pybind_type_links.Foo.__annotations__ = {}
        pybind_type_links.Foo.__annotations__['TYPE_DATA'] = pybind_type_links.Enum
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_MODULES': [pybind_type_links],
            'PYBIND11_COMPATIBILITY': True,
            'M_SPHINX_INVENTORIES': [
                ('../../../doc/documentation/python.inv', 'https://docs.python.org/3/', [], ['m-doc-external'])]
        })
        self.assertEqual(*self.actual_expected_contents('pybind_type_links.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_type_links.Foo.html'))

class ExternalOverloadDocs(BaseInspectTestCase):
    def test(self):
        self.run_python({
            'PLUGINS': ['m.sphinx'],
            'INPUT_DOCS': ['docs.rst'],
            'PYBIND11_COMPATIBILITY': True
        })
        self.assertEqual(*self.actual_expected_contents('pybind_external_overload_docs.html'))
        self.assertEqual(*self.actual_expected_contents('pybind_external_overload_docs.Class.html'))

        sys.path.append(self.path)
        import pybind_external_overload_docs
        if pybind_external_overload_docs.Class26.is_pybind26:
            self.assertEqual(*self.actual_expected_contents('pybind_external_overload_docs.Class26.html'))
