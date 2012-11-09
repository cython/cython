# mode: run
# tag: generators, lambda

def genexpr():
    """
    >>> genexpr()
    [0, 2, 4, 6, 8]
    """
    x = 'abc'
    result = list( x*2 for x in range(5) )
    assert x == 'abc' # don't leak
    return result

def genexpr_if():
    """
    >>> genexpr_if()
    [0, 4, 8]
    """
    x = 'abc'
    result = list( x*2 for x in range(5) if x % 2 == 0 )
    assert x == 'abc' # don't leak
    return result

def genexpr_if_false():
    """
    >>> genexpr_if_false()
    []
    """
    x = 'abc'
    result = list( x*2 for x in range(5) if False )
    assert x == 'abc' # don't leak
    return result

def genexpr_with_lambda():
    """
    >>> genexpr_with_lambda()
    [0, 4, 8]
    """
    x = 'abc'
    result = list( x*2 for x in range(5) if (lambda x:x % 2)(x) == 0 )
    assert x == 'abc' # don't leak
    return result

def genexpr_of_lambdas(int N):
    """
    >>> [ (f(), g()) for f,g in genexpr_of_lambdas(5) ]
    [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)]
    """
    return ( ((lambda : x), (lambda : x*2)) for x in range(N) )
