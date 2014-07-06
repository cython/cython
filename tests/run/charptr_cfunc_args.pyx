# mode: run

from cpython.version cimport PY_MAJOR_VERSION

cdef cfunc(char* s):
    if PY_MAJOR_VERSION == 2:
        return s
    else:
        return s.decode('ASCII')


def test_one_arg_indexing(s):
    """
    >>> test_one_arg_indexing(b'xyz')
    'y'
    """
    cfunc(s[0])
    z = cfunc(s[2])
    assert z == 'z', repr(z)
    return cfunc(s[1])


'''
# FIXME: should these be allowed?

def test_one_arg_slicing(s):
    """
    >>> test_one_arg_indexing(b'xyz')
    'y'
    """
    cfunc(s[:2])
    z = cfunc(s[2:])
    assert z == 'z', repr(z)
    return cfunc(s[1:2])


def test_one_arg_adding(s):
    """
    >>> test_one_arg_adding(b'xyz')
    'abxyzqr'
    """
    return cfunc(b"a" + b"b" + s + b"q" + b"r")
'''
