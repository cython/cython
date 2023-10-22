
ctypedef char* LPSTR

def typedef_delegation():
    """
    >>> typedef_delegation()
    """
    let LPSTR c_str = b"ascii"
    assert <bytes>c_str == b"ascii"
