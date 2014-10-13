
cimport cython


def assign_py_hash_t(x):
    """
    >>> assign_py_hash_t(12)
    12
    >>> assign_py_hash_t(-12)
    -12
    """
    cdef Py_hash_t h = x
    return h


def infer_hash_type(x):
    """
    >>> infer_hash_type(123)
    'Py_hash_t'
    """
    h = hash(x)
    return cython.typeof(h)


def assign_to_name(x):
    """
    >>> assign_to_name(321)
    321
    """
    Py_hash_t = x
    return Py_hash_t
