# mode: run

# NOTE: Py2.6+ only


cimport cython

cpdef bytearray coerce_to_charptr(char* b):
    """
    >>> b = bytearray(b'abc')
    >>> coerced = coerce_to_charptr(b)
    >>> coerced == b or coerced
    True
    >>> isinstance(coerced, bytearray) or type(coerced)
    True
    """
    return b

def coerce_to_charptrs(bytearray b):
    """
    >>> b = bytearray(b'abc')
    >>> coerce_to_charptrs(b)
    True
    """
    cdef char* cs = b
    cdef unsigned char* ucs = b
    cdef signed char* scs = b
    return b == <bytearray>cs == <bytearray> ucs == <bytearray>scs

cpdef bytearray coerce_charptr_slice(char* b):
    """
    >>> b = bytearray(b'abc')
    >>> coerced = coerce_charptr_slice(b)
    >>> coerced == b[:2] or coerced
    True
    >>> isinstance(coerced, bytearray) or type(coerced)
    True
    """
    return b[:2]

def infer_index_types(bytearray b):
    """
    >>> b = bytearray(b'a\\xFEc')
    >>> print(infer_index_types(b))
    (254, 254, 254, 'unsigned char', 'unsigned char', 'unsigned char', 'int')
    """
    c = b[1]
    with cython.wraparound(False):
        d = b[1]
    with cython.boundscheck(False):
        e = b[1]
    return c, d, e, cython.typeof(c), cython.typeof(d), cython.typeof(e), cython.typeof(b[1])

def infer_slice_types(bytearray b):
    """
    >>> b = bytearray(b'abc')
    >>> print(infer_slice_types(b))
    (bytearray(b'bc'), bytearray(b'bc'), bytearray(b'bc'), 'Python object', 'Python object', 'Python object', 'bytearray object')
    """
    c = b[1:]
    with cython.boundscheck(False):
        d = b[1:]
    with cython.boundscheck(False), cython.wraparound(False):
        e = b[1:]
    return c, d, e, cython.typeof(c), cython.typeof(d), cython.typeof(e), cython.typeof(b[1:])
