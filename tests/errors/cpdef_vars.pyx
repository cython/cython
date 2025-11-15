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
3:0: Variables cannot be declared with 'cpdef'. Use 'cdef' or 'cdef public' instead.
4:0: Variables cannot be declared with 'cpdef'. Use 'cdef' or 'cdef public' instead.
7:4: Variables cannot be declared with 'cpdef'. Use 'cdef' or 'cdef public' instead.
15:4: Variables cannot be declared with 'cpdef'. Use 'cdef' or 'cdef public' instead.
"""
