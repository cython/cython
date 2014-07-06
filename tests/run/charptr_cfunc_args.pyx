
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
    return cfunc(s[1])
