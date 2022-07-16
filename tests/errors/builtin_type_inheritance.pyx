# mode: error

# current restriction: cannot inherit from PyVarObject (see ticket #152)

cdef class MyTuple(tuple):
    pass

cdef class MyBytes(bytes):
    pass

# str is also included in this in Py2, but checked at runtime instead

_ERRORS = """
5:19: inheritance from PyVarObject types like 'tuple' is not currently supported
8:19: inheritance from PyVarObject types like 'bytes' is not currently supported
"""
