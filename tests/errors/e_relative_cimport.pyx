# mode: error
# tag: cimport

from ..relative_cimport cimport some_name

from ..cython cimport declare


_ERRORS="""
4:0: 'relative_cimport.pxd' not found
4:0: 'some_name.pxd' not found
4:0: relative cimport beyond main package is not allowed
4:32: Name 'some_name' not declared in module 'relative_cimport'
6:0: 'declare.pxd' not found
6:0: relative cimport beyond main package is not allowed
6:22: Name 'declare' not declared in module 'cython'
"""
