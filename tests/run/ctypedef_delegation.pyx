
ctypedef char* LPSTR

def typedef_delegation():
    """
    >>> typedef_delegation()
    """
    cdef LPSTR c_str = b"ascii"
    assert <bytes>c_str == b"ascii"
