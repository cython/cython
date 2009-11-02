
def for_else():
    """
    >>> for_else()
    30
    >>> print( int_comp() )
    00*01*02
    """
    cdef int i, j=0, k=2
    for i from 0 <= i < 10:
        j += k
    else:
        k = j+10
    return k

def int_comp():
    cdef int i
    return u'*'.join(tuple([ u"%02d" % i
                             for i from 0 <= i < 3 ]))
