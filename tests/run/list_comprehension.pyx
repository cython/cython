
def foo():
    """
    >>> foo()
    [[], [-1], [-1, 0], [-1, 0, 1]]
    """
    result = [[a-1 for a in range(b)] for b in range(4)]
    return result
