# ticket: t412

def f():
    """
    >>> f()
    True
    True
    """

    cdef char a
    a = 62
    print (a == '>')
    print (a == <char>'>')
