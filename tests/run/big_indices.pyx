__doc__ = u"""
    >>> test()
    neg -1
    pos 4294967294
    neg
    pos
    neg
    pos
"""

def test():
    cdef long neg = -1
    cdef unsigned long pos = -2 # will be a large positive number

    print "neg", neg
    print "pos", pos

    D = { neg: 'neg', pos: 'pos' }

    print D[<object>neg]
    print D[<object>pos]

    print D[neg]
    print D[pos]
    