# mode: run

# NOTE: Py2.6+ only


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
