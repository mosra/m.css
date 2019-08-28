"""This module has a *serious* docstring.

And module **details** as well."""

import enum

class Class:
    """This class has a *serious* docstring.
    With a multi-line summary.

    And class **details** as well."""

    @property
    def a_property(self) -> float:
        """This property has a *serious* docstring.

        And property **details** as well."""

class Enum(enum.Enum):
    """This enum has a *serious* docstring.

    And property **details** as well."""

    VALUE = 3

Enum.VALUE.__doc__ = "Tho enum value docs are unfortunately *not* processed."

def function(a: str, b: int) -> float:
    """This function has a *serious* docstring.

    :param a: And parameter docs.
        On multiple lines.
    :param b: *Wow.*
    :return: This too.

    And details.
    **Amazing**."""

def empty_docstring(): pass

def summary_only():
    """This is just a summary."""
