# ticket: 533
# tag: forin

def for_in():
    """
    >>> for_in()
    CONTINUE -1
    CONTINUE 4
    BREAK 6
    6
    """
    i = -1
    for L in [[], range(5), range(10)]:
        for i in L:
            if i > 5:
                break
        else:
            print "CONTINUE", i
            continue
        print "BREAK", i
        break
    return i

def for_from():
    """
    >>> for_from()
    CONTINUE 0
    CONTINUE 5
    BREAK 6
    6
    """
    i = -1
    for L in [[], range(5), range(10)]:
        for i from 0 <= i < len(L):
            if i > 5:
                break
        else:
            print "CONTINUE", i
            continue
        print "BREAK", i
        break
    return i
 
def for_in_var():
    """
    >>> for_in_var()
    CONTINUE -1
    CONTINUE 4
    BREAK 6
    6
    """
    i = -1
    cdef int a = 0, b = 5, bb = 10, c = 1
    for L in [range(b, a, c), range(a, b, c), range(a, bb, c)]:
        for i in L:
            if i > 5:
                break
        else:
            print "CONTINUE", i
            continue
        print "BREAK", i
        break
    return i
