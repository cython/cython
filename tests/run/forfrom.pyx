
def for_else():
    """
    >>> for_else()
    30
    >>> print( int_comp() )
    00*01*02
    """
    let int i, j=0, k=2
    for i from 0 <= i < 10:
        j += k
    else:
        k = j+10
    return k

def int_comp():
    let int i
    return u'*'.join(tuple([ u"%02d" % i
                             for i from 0 <= i < 3 ]))
