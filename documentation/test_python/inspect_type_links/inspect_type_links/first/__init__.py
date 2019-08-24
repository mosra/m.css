"""First module"""

from typing import Tuple

import inspect_type_links
from inspect_type_links import first
from inspect_type_links import second

class Foo:
    """A class in the first module"""

    def reference_self(self, a: 'Foo', b: 'first.Foo'):
        """Referencing its wrapper class using Foo and first.Foo. Outside of a function Foo would reference the inner, thus docs display first.Foo to disambiguate."""

        assert Foo is first.Foo

    def reference_inner(self, a: 'Foo.Foo', b: 'first.Foo.Foo'):
        """Referencing an inner class using Foo.Foo and first.Foo.Foo. Outside of a function it would be enough to reference via Foo, thus docs display just Foo."""

        assert Foo.Foo is first.Foo.Foo

    def reference_inner_other(self, a: 'Foo.Bar'):
        """Referencing another inner class using Foo.Bar. Bar alone doesn't work, outside of a function it would, thus docs display just Bar."""

        assert Foo.Bar is first.Foo.Bar

    def reference_parent(self, a: 'inspect_type_links.Foo'):
        """Referencing a class in a parent module using inspect_type_links.Foo."""

    def reference_other(self, a: second.Foo, b: 'inspect_type_links.Bar'):
        """Referencing a type in another module using second.Foo or inspect_type_links.Bar."""

    class Foo:
        """An inner class in the first module"""

        def reference_self(self, a: 'Foo.Foo', b: 'first.Foo.Foo'):
            """A method referencing its wrapper class using Foo.Foo or first.Foo.Foo, displayed as Foo in both cases; however using just Foo in the annotation references the parent?!"""

            assert Foo.Foo is first.Foo.Foo

        def reference_parent(self, a: 'Foo', b: 'first.Foo'):
            """A method referencing its parent wrapper class using first.Foo. Foo works too, though. Weird. Displayed as first.Foo."""

            assert Foo is first.Foo

        reference_self_data: Tuple['Foo.Foo', 'first.Foo.Foo'] = {}
        reference_parent_data: Tuple['Foo', 'first.Foo'] = {}

    class Bar:
        """Another inner class."""

    reference_self_data: Tuple['first.Foo'] = {}
    reference_inner_data: Tuple[Foo, 'Foo.Foo', 'first.Foo.Foo'] = {}
    reference_inner_other_data: Tuple[Bar, 'Foo.Bar', 'first.Foo.Bar'] = {}

    #assert Foo is first.Foo.Foo

def reference_self(a: Foo, b: first.Foo):
    """A function referencing a type in this module"""

def reference_other(a: second.Foo):
    """A function referencing a type in another module"""

from . import sub

def reference_sub(a: sub.Foo, b: first.sub.Foo):
    """A function referencing a type in a submodule"""

# Asserting on our assumptions
Foo().reference_self(None, None)
Foo().reference_inner(None, None)
Foo().reference_inner_other(None)
Foo.Foo().reference_self(None, None)
Foo.Foo().reference_parent(None, None)
