# mode: run

import cython


def calls():
    """
    >>> calls()
    """
    r1 = range(3)
    assert cython.typeof(r1) == 'range object', cython.typeof(r1)

    r2 = range(1, 3)
    assert cython.typeof(r2) == 'range object', cython.typeof(r2)

    r3 = range(1, 3, 1)
    assert cython.typeof(r3) == 'range object', cython.typeof(r3)


def arg_type(r: range):
    """
    >>> arg_type(range(3))
    0
    1
    2
    >>> arg_type([])
    Traceback (most recent call last):
    TypeError: Argument 'r' has incorrect type (expected range, got list)
    """
    for i in r:
        print(i)


def attributes(r: range):
    """
    >>> attributes(range(2))
    (0, 2, 1)
    >>> attributes(range(1,2))
    (1, 2, 1)
    >>> attributes(range(1,2,3))
    (1, 2, 3)
    """
    return r.start, r.stop, r.step


def isinstance_range(x):
    """
    >>> isinstance_range(range(20))
    True
    >>> isinstance_range([])
    False
    >>> isinstance_range(2)
    False
    """
    return isinstance(x, range)
