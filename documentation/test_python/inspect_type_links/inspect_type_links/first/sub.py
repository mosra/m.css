"""Submodule"""

from inspect_type_links import first

class Foo:
    """A class in the submodule"""

    def reference_self(a: 'inspect_type_links.first.sub.Foo'):
        """A method referencing a type in this submodule"""

    def reference_parent(a: first.Foo, b: first.Foo):
        """A method referencing a type in a parent module"""

def reference_self(a: Foo, b: 'inspect_type_links.first.sub.Foo'):
    """A function referencing a type in this submodule"""

def reference_parent(a: first.Foo, b: first.Foo):
    """A function referencing a type in a parent module"""
