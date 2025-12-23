# mode: error

cimport cython

cdef takes_a_lock(cython.pymutex l):
    pass

cdef cython.pymutex uncopyable():
    cdef cython.pymutex l
    cdef object o
    takes_a_lock(l)
    l2 = l
    o = l
    return l

_ERRORS = """
11:17: cython.pymutex cannot be copied
12:9: cython.pymutex cannot be copied
13:8: Cannot convert 'cython.pymutex' to Python object
14:11: cython.pymutex cannot be copied
"""
