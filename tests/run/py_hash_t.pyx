
cimport cython


class IntLike(object):
  def __init__(self, value):
    self.value = value
  def __index__(self):
    return self.value


def assign_py_hash_t(x):
    """
    >>> assign_py_hash_t(12)
    12
    >>> assign_py_hash_t(-12)
    -12

    >>> assign_py_hash_t(IntLike(-3))
    -3
    >>> assign_py_hash_t(IntLike(1 << 100))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...
    >>> assign_py_hash_t(IntLike(1.5))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: __index__ ... (type ...float...)
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
