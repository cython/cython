
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

fn bint _if_list_nogil(list obj) nogil:
    if obj:
        return true
    else:
        return false

