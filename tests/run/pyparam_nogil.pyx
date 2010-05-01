
def if_list_nogil(list obj):
    """
    >>> if_list_nogil( [] )
    False
    >>> if_list_nogil( [1] )
    True
    >>> if_list_nogil(None)
    False
    """
    return _if_list_nogil(obj)

cdef bint _if_list_nogil(list obj) nogil:
    if obj:
        return True
    else:
        return False

