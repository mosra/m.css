"""..

:data _DATA_IN_MODULE: In-module documented underscored data. This won't be
    picked up by the initial crawl, unfortunately, as the docstrings are
    processed much later.
"""

import enum

from . import _submodule, _submodule_external, _submodule_undocumented

class _Class:
    """Documented underscored class"""

class _ClassExternal: pass

class _ClassUndocumented: pass

class _Enum(enum.Enum):
    """Documented underscored enum"""

class _EnumExternal(enum.Enum): pass

class _EnumUndocumented(enum.Enum): pass

def _function():
    """Documented undercored function"""

def _function_external(): pass

def _function_undocumented(): pass

_DATA_IN_MODULE: int = 0
_DATA_EXTERNAL: int = 1
_DATA_EXTERNAL_IN_MODULE: int = 2
_DATA_UNDOCUMENTED: int = 3

class Class:
    """..

    :property _property_in_class: In-class documented underscored property.
        This won't be picked up by the initial crawl, unfortunately, as the
        docstrings are processed much later.
    :data _DATA_IN_CLASS: In-class documented underscored data. This won't be
        picked up by the initial crawl, unfortunately, as the docstrings are
        processed much later.
    :data _DATA_DECLARATION_IN_CLASS: In-class documented underscored data.
        This won't be picked up by the initial crawl, unfortunately, as the
        docstrings are processed much later.
    """

    def _function(self):
        """Documented underscored function"""

    def _function_external(self): pass

    def _function_undocumented(self): pass

    @property
    def _property(self):
        """Documented underscored property"""

    @property
    def _property_in_class(self): pass

    @property
    def _property_external(self): pass

    @property
    def _property_external_in_class(self): pass

    @property
    def _property_undocumented(self): pass

    _DATA_IN_CLASS: int = 4
    _DATA_EXTERNAL: int = 5
    _DATA_EXTERNAL_IN_CLASS: int = 6
    _DATA_UNDOCUMENTED: int = 7

    _DATA_DECLARATION_IN_CLASS: float
    _DATA_DECLARATION_EXTERNAL: float
    _DATA_DECLARATION_EXTERNAL_IN_CLASS: float
    _DATA_DECLARATION_UNDOCUMENTED: float
