# mode: error
# tag: cimport

from ..relative_cimport cimport some_name
from .e_relative_cimport cimport some_name
from ..cython cimport declare
from . cimport e_relative_cimport


_ERRORS="""
4:0: relative cimport beyond main package is not allowed
5:0: relative cimport beyond main package is not allowed
6:0: relative cimport beyond main package is not allowed
7:0: relative cimport beyond main package is not allowed
"""
