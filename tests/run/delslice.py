# mode: run
# tag: del, slicing

def del_constant_start_stop(x):
    """
    >>> l = [1,2,3,4]
    >>> del_constant_start_stop(l)
    [1, 2]

    >>> l = [1,2,3,4,5,6,7]
    >>> del_constant_start_stop(l)
    [1, 2, 7]
    """
    del x[2:6]
    return x


def del_start(x, start):
    """
    >>> l = [1,2,3,4]
    >>> del_start(l, 2)
    [1, 2]

    >>> l = [1,2,3,4,5,6,7]
    >>> del_start(l, 20)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_start(l, 8)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_start(l, 4)
    [1, 2, 3, 4]

    >>> del_start(l, -2)
    [1, 2]
    >>> l
    [1, 2]
    >>> del_start(l, -2)
    []
    >>> del_start(l, 2)
    []
    >>> del_start(l, -2)
    []
    >>> del_start(l, 20)
    []

    >>> del_start([1,2,3,4], -20)
    []
    >>> del_start([1,2,3,4], 0)
    []
    """
    del x[start:]
    return x


def del_stop(x, stop):
    """
    >>> l = [1,2,3,4]
    >>> del_stop(l, 2)
    [3, 4]

    >>> l = [1,2,3,4,5,6,7]
    >>> del_stop(l, -20)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_stop(l, -8)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_stop(l, -4)
    [4, 5, 6, 7]

    >>> del_stop(l, -2)
    [6, 7]
    >>> l
    [6, 7]
    >>> del_stop(l, -2)
    [6, 7]
    >>> del_stop(l, 2)
    []
    >>> del_stop(l, -2)
    []
    >>> del_stop(l, 20)
    []

    >>> del_stop([1,2,3,4], -20)
    [1, 2, 3, 4]
    >>> del_stop([1,2,3,4], 0)
    [1, 2, 3, 4]
    """
    del x[:stop]
    return x


def del_start_stop(x, start, stop):
    """
    >>> l = [1,2,3,4]
    >>> del_start_stop(l, 0, 2)
    [3, 4]
    >>> l
    [3, 4]

    >>> l = [1,2,3,4,5,6,7]
    >>> del_start_stop(l, -1, -20)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_start_stop(l, -20, -8)
    [1, 2, 3, 4, 5, 6, 7]
    >>> del_start_stop(l, -6, -4)
    [1, 4, 5, 6, 7]

    >>> del_start_stop(l, -20, -2)
    [6, 7]
    >>> l
    [6, 7]
    >>> del_start_stop(l, -2, 1)
    [7]
    >>> del_start_stop(l, -2, 3)
    []
    >>> del_start_stop(l, 2, 4)
    []

    >>> del_start_stop([1,2,3,4], 20, -20)
    [1, 2, 3, 4]
    >>> del_start_stop([1,2,3,4], 0, 0)
    [1, 2, 3, 4]
    """
    del x[start:stop]
    return x
