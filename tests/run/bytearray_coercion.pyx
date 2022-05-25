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


def infer_concatenation_types(bytearray b):
    """
    >>> b = bytearray(b'a\\xFEc')
    >>> b2, c, d, e, tb, tc, td, te = infer_concatenation_types(b)
    >>> tb, tc, td, te
    ('bytearray object', 'bytearray object', 'bytearray object', 'bytearray object')
    >>> b2, c, d, e
    (bytearray(b'a\\xfec'), bytearray(b'a\\xfeca\\xfec'), bytearray(b'a\\xfeca\\xfec'), bytearray(b'a\\xfeca\\xfec'))
    """
    c = b[:]
    c += b[:]

    d = b[:]
    d *= 2

    e = b + b

    return b, c, d, e, cython.typeof(b), cython.typeof(c), cython.typeof(d), cython.typeof(e)


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
    (bytearray(b'bc'), bytearray(b'bc'), bytearray(b'bc'), 'bytearray object', 'bytearray object', 'bytearray object', 'bytearray object')
    """
    c = b[1:]
    with cython.boundscheck(False):
        d = b[1:]
    with cython.boundscheck(False), cython.wraparound(False):
        e = b[1:]
    return c, d, e, cython.typeof(c), cython.typeof(d), cython.typeof(e), cython.typeof(b[1:])


def assign_to_index(bytearray b, value):
    """
    >>> b = bytearray(b'0abcdefg')
    >>> assign_to_index(b, 1)
    bytearray(b'xyzee\\x01h')
    >>> b
    bytearray(b'xyzee\\x01h')

    >>> assign_to_index(bytearray(b'0ABCDEFG'), 40)
    bytearray(b'xyzEE(o')

    >>> assign_to_index(bytearray(b'0abcdefg'), -1)
    Traceback (most recent call last):
    OverflowError: can't convert negative value to unsigned char

    >>> assign_to_index(bytearray(b'0abcdef\\x00'), 255)
    bytearray(b'xyzee\\xff\\xff')
    >>> assign_to_index(bytearray(b'0abcdef\\x01'), 255)
    Traceback (most recent call last):
    OverflowError: value too large to convert to unsigned char
    >>> assign_to_index(bytearray(b'0abcdef\\x00'), 256)
    Traceback (most recent call last):
    OverflowError: value too large to convert to unsigned char
    """
    b[1] = 'x'
    b[2] = b'y'
    b[3] = c'z'
    b[4] += 1
    b[5] |= 1
    b[6] = value
    b[7] += value
    del b[0]

    try:
        b[7] = 1
    except IndexError:
        pass
    else:
        assert False, "IndexError not raised"

    try:
        b[int(str(len(b)))] = 1   # test non-int-index assignment
    except IndexError:
        pass
    else:
        assert False, "IndexError not raised"

    return b


def check_bounds(int cvalue):
    """
    >>> check_bounds(0)
    0
    >>> check_bounds(255)
    255
    >>> check_bounds(256)
    Traceback (most recent call last):
    ValueError: byte must be in range(0, 256)
    >>> check_bounds(-1)
    Traceback (most recent call last):
    ValueError: byte must be in range(0, 256)
    """
    b = bytearray(b'x')

    try:
        b[0] = 256
    except ValueError:
        pass
    else:
        assert False, "ValueError not raised"

    try:
        b[0] = -1
    except ValueError:
        pass
    else:
        assert False, "ValueError not raised"

    b[0] = cvalue
    return b[0]


def nogil_assignment(bytearray x, int value):
    """
    >>> b = bytearray(b'abc')
    >>> nogil_assignment(b, ord('y'))
    >>> b
    bytearray(b'xyc')
    """
    with nogil:
        x[0] = 'x'
        x[1] = value
