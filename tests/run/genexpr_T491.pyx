# ticket: t491

def test_genexpr():
    """
    >>> gen = test_genexpr()
    >>> list(gen)
    [0, 1, 2, 3, 4]
    """
    return (i for i in range(5))

def test_genexpr_typed():
    """
    >>> gen = test_genexpr_typed()
    >>> list(gen)
    [0, 1, 2, 3, 4]
    """
    cdef int i
    return (i for i in range(5))

def test_genexpr_funccall():
    """
    >>> test_genexpr_funccall()
    [0, 1, 2, 3, 4]
    """
    return list(i for i in range(5))

def test_genexpr_scope():
    """
    >>> test_genexpr_scope()
    ([0, 1, 2, 3, 4], 'abc')
    """
    i = 'abc'
    gen = (i for i in range(5))
    lst = list(gen)
    return lst, i

def test_genexpr_closure():
    """
    >>> gen = test_genexpr_closure()
    >>> list(gen)
    ['a', 'b', 'c']
    """
    abc = 'a' + 'b' + 'c'
    return (c for c in abc)
