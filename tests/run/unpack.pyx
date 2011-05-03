# mode: run
# tag: sequence_unpacking

_set = set

def _it(N):
    for i in range(N):
        yield i

def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1, (2,), (3,4,5), (6,(7,(8,9))), 0)
    (8, 9, (8, 9), (6, (7, (8, 9))), 0)
    """
    obj1, = obj2
    obj1, obj2 = obj2 + obj2
    obj1, obj2, obj3 = obj3
    obj1, (obj2, obj3) = obj4
    [obj1, obj2] = obj3
    return obj1, obj2, obj3, obj4, obj5

def unpack_typed(it):
    """
    >>> unpack_typed((1, 2.0, [1]))
    (1, 2.0, [1])
    >>> unpack_typed((1, None, [1]))
    Traceback (most recent call last):
    TypeError: a float is required
    >>> unpack_typed((1, 2.0, (1,)))
    Traceback (most recent call last):
    TypeError: Expected list, got tuple
    """
    cdef int a
    cdef float b
    cdef list c
    a,b,c = it
    return a,b,c

def failure_too_many(it):
    """
    >>> a,b,c = [1,2,3,4]    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_too_many([1,2,3,4])
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)

    >>> a,b,c = [1,2,3,4]    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_too_many((1,2,3,4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)

    >>> a,b,c = _set([1,2,3,4])    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_too_many(_set([1,2,3,4]))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)

    >>> a,b,c = _it(4)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_too_many(_it(4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)
    """
    a,b,c = it

def failure_too_few(it):
    """
    >>> a,b,c = [1,2]
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> failure_too_few([1,2])
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> a,b,c = (1,2)
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> failure_too_few((1,2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> a,b,c = _set([1,2])
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> failure_too_few(_set([1,2]))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> a,b,c = _it(2)
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    >>> failure_too_few(_it(2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    """
    a,b,c = it

def _it_failure(N):
    for i in range(N):
        yield i
    raise ValueError("huhu")

def failure_while_unpacking(it):
    """
    >>> a,b,c = _it_failure(0)
    Traceback (most recent call last):
    ValueError: huhu
    >>> failure_while_unpacking(_it_failure(0))
    Traceback (most recent call last):
    ValueError: huhu

    >>> a,b,c = _it_failure(1)
    Traceback (most recent call last):
    ValueError: huhu
    >>> failure_while_unpacking(_it_failure(1))
    Traceback (most recent call last):
    ValueError: huhu

    >>> a,b,c = _it_failure(2)
    Traceback (most recent call last):
    ValueError: huhu
    >>> failure_while_unpacking(_it_failure(2))
    Traceback (most recent call last):
    ValueError: huhu

    >>> a,b,c = _it_failure(3)
    Traceback (most recent call last):
    ValueError: huhu
    >>> failure_while_unpacking(_it_failure(3))
    Traceback (most recent call last):
    ValueError: huhu

    >>> a,b,c = _it_failure(4)    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_while_unpacking(_it_failure(4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)
    """
    a,b,c = it
