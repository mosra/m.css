"""This module has a *serious* docstring. And a :ref:`Class`.

And module **details** as well."""

import enum

class Class:
    """This class has a *serious* docstring.
    With a multi-line summary. Relative reference to :ref:`a_property` works
    even from a summary.

    :property another_property: This property is documented in the class

    And class **details** as well."""

    @property
    def a_property(self) -> float:
        """The :ref:`a_property` has a *serious* docstring.

        And property **details** as well."""

    @property
    def another_property():
        pass

class Enum(enum.Enum):
    """This enum has a *serious* docstring. :ref:`VALUE` works from a summary.

    :value ANOTHER: Values can be documented from a docstring, too.

    And enum **details** as well."""

    VALUE = 3
    ANOTHER = 4

Enum.VALUE.__doc__ = """Enum value docstrings are *processed* as well.

The :ref:`ANOTHER` value is documented from within the :ref:`Enum` itself.
"""

def function(a: str, b: int) -> float:
    """This :ref:`function()` has a *serious* docstring.

    :param a: And parameter docs, referring to :ref:`function()` as well.
        On multiple lines.
    :param b: *Wow.*
    :return: This too. In the :ref:`function()`.

    And details.
    **Amazing**."""

def empty_docstring(): pass

def summary_only():
    """This is just a summary."""

# This should check we handle reST parsing errors gracefully. Will probably
# look extra weird in the output tho, but that's okay -- it's an error after
# all.
def this_function_has_bad_docs(a, b) -> str:
    """This function has bad docs. It's freaking terrible.
        Yes.
            Really.

    :broken: yes
    """
