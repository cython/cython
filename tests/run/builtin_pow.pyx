
def pow3(a,b,c):
    """
    >>> pow3(2,3,5)
    3
    >>> pow3(3,3,5)
    2
    """
    return pow(a,b,c)

def pow3_const():
    """
    >>> pow3_const()
    3
    """
    return pow(2,3,5)

def pow2(a,b):
    """
    >>> pow2(2,3)
    8
    >>> pow2(3,3)
    27
    """
    return pow(a,b)

def pow2_const():
    """
    >>> pow2_const()
    8
    """
    return pow(2,3)

def pow_args(*args):
    """
    >>> pow_args(2,3)
    8
    >>> pow_args(2,3,5)
    3
    """
    return pow(*args)
