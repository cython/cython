# ticket: 237
#def add_large_c():
#    cdef unsigned long long val = 2**30 + 2**30
#    return val

def add_large():
    """
    >>> add_large() == 2147483647 + 2147483647
    True

    #>>> add_large_c() == 2147483647 + 2147483647
    #True
    """
    return 2147483647 + 2147483647

def add_large_pow():
    """
    >>> add_large_pow() == 2**31 + 2**31
    True
    >>> add_large_pow() == 2**32
    True
    """
    return 2**31 + 2**31
