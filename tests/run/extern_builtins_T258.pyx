cdef extern from "Python.h":
    
    ctypedef class __builtin__.str  [object PyStringObject]:
        cdef long ob_shash

    ctypedef class __builtin__.list  [object PyListObject]:
        cdef Py_ssize_t ob_size
        cdef Py_ssize_t allocated

    ctypedef class __builtin__.dict  [object PyDictObject]:
        pass

cdef str s = "abc"
cdef list L = [1,2,4]
cdef dict d = {'A': 'a'}

    
def test_list(list L):
    """
    >>> test_list(range(10))
    True
    >>> class list_subclass(list): pass
    >>> test_list(list_subclass([1,2,3]))
    True
    """
    return L.ob_size <= L.allocated

def test_str(str s):
    """
    >>> test_str("abc")
    True
    >>> class str_subclass(str): pass
    >>> test_str(str_subclass("xyz"))
    True
    """
    cdef char* ss = s
    return hash(s) == s.ob_shash

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

