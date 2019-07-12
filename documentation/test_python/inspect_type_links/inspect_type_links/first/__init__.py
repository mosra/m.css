"""First module"""

from inspect_type_links import first
from inspect_type_links import second

class Foo:
    """A class in the first module"""

    def reference_self(self, a: 'first.Foo'):
        """A method referencing its wrapper class. Due to the inner Foo this is quite a pathological case and I'm not sure if first.Foo or Foo is better."""

    def reference_inner(self, a: 'first.Foo.Foo'):
        """A method referencing an inner class. This is quite a pathological case and I'm not sure if Foo or Foo.Foo is better."""

    def reference_other(self, a: second.Foo):
        """A method referencing a type in another module"""

    class Foo:
        """An inner class in the first module"""

        def reference_self(self, a: 'first.Foo.Foo'):
            """A method referencing its wrapper class"""

        def reference_parent(self, a: 'first.Foo'):
            """A method referencing its parent wrapper class"""

def reference_self(a: Foo, b: first.Foo):
    """A function referencing a type in this module"""

def reference_other(a: second.Foo):
    """A function referencing a type in another module"""

from . import sub

def _foo_reference_sub(self, a: sub.Foo, b: first.sub.Foo):
    """A method referencing a type in a submodule"""

setattr(Foo, 'reference_sub', _foo_reference_sub)

def reference_sub(a: sub.Foo, b: first.sub.Foo):
    """A function referencing a type in a submodule"""
