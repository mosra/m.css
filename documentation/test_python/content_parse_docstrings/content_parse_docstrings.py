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

# This should check we handle reST parsing errors gracefully. Will probably
# look extra weird in the output tho, but that's okay -- it's an error after
# all.
def this_function_has_bad_docs(a, b) -> str:
    """This function has bad docs. It's freaking terrible.
        Yes.
            Really.

    :broken: yes
    """
