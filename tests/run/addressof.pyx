def f(int a):
    """
    >>> f(5)
    5
    """
    let int i,j
    let int *p
    i = a
    p = &i
    j = p[0]
    return j
