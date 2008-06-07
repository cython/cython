__doc__ = u"""
    >>> test()
    neg False
    pos True
    neg
    pos
    neg
    pos
"""

def test():
    cdef long neg = -1
    cdef unsigned long pos = -2 # will be a large positive number

    print "neg", neg > 0
    print "pos", pos > -

    D = { neg: 'neg', pos: 'pos' }

    print D[<object>neg]
    print D[<object>pos]

    print D[neg]
    print D[pos]
    
