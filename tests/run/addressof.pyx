def f(i32 a):
    """
    >>> f(5)
    5
    """
    let i32 i, j
    let i32 *p
    i = a
    p = &i
    j = p[0]
    return j
