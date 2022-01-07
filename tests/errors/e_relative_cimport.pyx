# mode: error
# tag: cimport

from ..relative_cimport cimport some_name
from ..cython cimport declare


_ERRORS="""
4:0: relative cimport beyond main package is not allowed
5:0: relative cimport beyond main package is not allowed
"""
