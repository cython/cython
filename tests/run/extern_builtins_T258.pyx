# ticket: t258

cdef extern from "Python.h":

    ctypedef class __builtin__.list  [object PyListObject]:
        cdef Py_ssize_t allocated

    ctypedef class __builtin__.dict  [object PyDictObject]:
        pass

    cdef Py_ssize_t Py_SIZE(object o)

cdef list L = [1,2,4]
cdef dict d = {'A': 'a'}


def test_list(list L):
    """
    >>> test_list(list(range(10)))
    True
    >>> class list_subclass(list): pass
    >>> test_list(list_subclass([1,2,3]))
    True
    """
    return Py_SIZE(L) <= L.allocated

def test_tuple(tuple t):
    """
    Actual builtin types are restrictive wrt subclassing so optimizations can be safely performed.

    >>> test_tuple((1,2))
    2
    >>> class tuple_subclass(tuple): pass
    >>> test_tuple(tuple_subclass((1,2)))
    Traceback (most recent call last):
    ...
    TypeError: Argument 't' has incorrect type (expected tuple, got tuple_subclass)
    """
    return len(t)

