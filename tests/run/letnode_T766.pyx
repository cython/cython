# mode: run
# ticket: t766
# tag: letnode

def test_letnode_range(i32 n):
    """
    >>> [i() for i in test_letnode_range(5)]
    [0, 1, 2, 3, 4]
    """
    ret = []
    for i in range(n):
        def bar(x=i):
            return x
        ret.append(bar)
    return ret

def test_letnode_enumerate(a):
    """
    >>> [i() for i in test_letnode_enumerate("abc")]
    [0, 1, 2]
    """
    let i32 n
    ret = []
    for n, i in enumerate(a):
        def bar(x=n):
            return x
        ret.append(bar)
    return ret
