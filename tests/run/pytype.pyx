from cpython.type cimport PyType_IsSubtype

class mylist(list): pass

def test_issubtype(a, b):
    """
    >>> test_issubtype(mylist, list)
    True
    >>> test_issubtype(mylist, dict)
    False

    >>> o = object()
    >>> test_issubtype(o, list)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert object to type
    """
    return PyType_IsSubtype(a, b)
