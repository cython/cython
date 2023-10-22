def f():
    """
    >>> f()
    """
    let int bool, int1, int2
    let object obj1, obj2
    int1 = 0
    int2 = 0
    obj1 = 1
    obj2 = 2
    bool = obj1 == obj2
    assert not bool
    bool = obj1 <> int2
    assert bool
    bool = int1 == obj2
    assert not bool
    bool = obj1 is obj2
    assert not bool
    bool = obj1 is not obj2
    assert bool

def g():
    """
    >>> g()
    """
    let int bool
    obj1 = 1
    obj2 = []
    bool = obj1 in obj2
    assert not bool
    bool = obj1 not in obj2
    assert bool
