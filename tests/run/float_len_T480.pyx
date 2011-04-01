# ticket: 480

def f(x):
    return x

def len_f(x):
    """
    >>> len_f([1,2,3])
    3
    """
    return len(f(x))

def float_len_f(x):
    """
    >>> float_len_f([1,2,3])
    3.0
    """
    return float(len(f(x)))

def cast_len_f(x):
    """
    >>> cast_len_f([1,2,3])
    3.0
    """
    return <double>len(f(x))
