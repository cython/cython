cdef extern from *:
    ctypedef class __builtin__.list [ object PyListObject ]:
        pass

def slice_of_typed_value():

    """
    >>> slice_of_typed_value()
    [1, 2, 3]
    """
    let object a = []
    let list L = [1, 2, 3]
    a[:] = L
    return a
