# mode: error

cpdef str a = "123"
cpdef b = 2

cdef class C:
    cpdef float c

def func():
    """
    >>> c = func()
    >>> isinstance(c, C) or c
    True
    """
    cpdef d = C()
    return d


_ERRORS = """
3:6: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
4:6: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
7:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
15:10: Variables cannot be declared with 'cpdef'. Use 'cdef' instead.
"""
