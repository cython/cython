# mode: error

# current restriction: cannot inherit from PyVarObject if C structure changes (see ticket #152)

cdef class MyTuple(tuple):
    cdef object attr

cdef class MyBytes(bytes):
    cdef object attr

cdef class MyStr(str): # only in Py2, but can't know that during compilation
    cdef object attr

cdef class MyTuple2(tuple):
    cdef meth(self): pass

cdef class MyBytes2(bytes):
    cdef meth(self): pass

cdef class MyStr2(str): # only in Py2, but can't know that during compilation
    cdef meth(self): pass

_ERRORS = """
5:19: inheritance from PyVarObject types 'tuple' with C-level attributes is not currently supported
8:19: inheritance from PyVarObject types 'bytes' with C-level attributes is not currently supported
11:17: inheritance from PyVarObject types 'str' with C-level attributes is not currently supported
14:20: inheritance from PyVarObject types 'tuple' with C-level vtable is not currently supported
17:20: inheritance from PyVarObject types 'bytes' with C-level vtable is not currently supported
20:18: inheritance from PyVarObject types 'str' with C-level vtable is not currently supported
"""
