# mode: run
# tag: generator

def yield_from_gen(values):
    """
    >>> def yf(x): yield from x
    >>> list(yf(yield_from_gen([1, 2, 3, 4])))
    [1, 2, 3, 4]
    """
    for value in values:
        yield value


def yield_from_gen_return(values):
    """
    >>> def yf(x): yield from x
    >>> list(yf(yield_from_gen_return([1, 2, 3, 4])))
    [1, 2, 3, 4]
    """
    for value in values:
        yield value
    return 5
