# ticket: t232

cdef class MyExt:
    cdef object attr

def set_attr(value):
    """
    >>> set_attr(5)
    """
    MyExt().attr = value

def get_attr():
    """
    >>> get_attr()
    """
    return MyExt().attr
