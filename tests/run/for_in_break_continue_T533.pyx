# mode: run
# ticket: t533
# ticket: gh1093

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


def for_in_break2(data, avoid):
    """
    >>> for_in_break2([1,2,3,None], avoid=[1,2,3])
    3
    >>> for_in_break2([1,2,3,None], avoid=[1])
    1
    >>> for_in_break2([1,2,3,None], avoid=[1])
    1
    """
    data_iter = iter(data)
    value = None
    while 1:
        match = next(data_iter)
        if match is None:
            break
        for value in avoid:
            if match == value:
                break
        else:
            break

    return value
