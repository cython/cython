# mode: run
# tag: sequence_unpacking

import cython


def _it(N):
    for i in range(N):
        yield i


cdef class ItCount(object):
    cdef object values
    cdef readonly count
    def __init__(self, values):
        self.values = iter(values)
        self.count = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.count += 1
        return next(self.values)

def kunterbunt(obj1, obj2, obj3, obj4, obj5):
    """
    >>> kunterbunt(1, (2,), (3,4,5), (6,(7,(8,9))), 0)
    (8, 9, (8, 9), (6, (7, (8, 9))), 0)
    """
    obj1, = obj2
    obj1, obj2 = obj2 + obj2
    obj1, obj2, obj3 = obj3
    obj1, (obj2, obj3) = obj4
    [obj1, obj2] = obj3
    return obj1, obj2, obj3, obj4, obj5

def unpack_tuple(tuple it):
    """
    >>> unpack_tuple((1,2,3))
    (1, 2, 3)

    >>> a,b,c = None   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> unpack_tuple(None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    a,b,c = it
    return a,b,c

def unpack_list(list it):
    """
    >>> unpack_list([1,2,3])
    (1, 2, 3)

    >>> a,b,c = None   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> unpack_list(None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    a,b,c = it
    return a,b,c

def unpack_to_itself(it):
    """
    >>> it = _it(2)
    >>> it, it = it
    >>> it
    1
    >>> unpack_to_itself([1,2])
    2
    >>> unpack_to_itself((1,2))
    2
    >>> unpack_to_itself(_it(2))
    1
    >>> unpack_to_itself((1,2,3))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 2)
    >>> unpack_to_itself(_it(3))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 2)
    """
    it, it = it
    return it

def unpack_partial(it):
    """
    >>> it = _it(2)
    >>> a = b = c = 0
    >>> try: a,b,c = it
    ... except ValueError: pass
    ... else: print("DID NOT FAIL!")
    >>> a, b, c
    (0, 0, 0)
    >>> unpack_partial([1,2])
    (0, 0, 0)
    >>> unpack_partial((1,2))
    (0, 0, 0)
    >>> unpack_partial(_it(2))
    (0, 0, 0)

    >>> it = ItCount([1,2])
    >>> a = b = c = 0
    >>> try: a,b,c = it
    ... except ValueError: pass
    ... else: print("DID NOT FAIL!")
    >>> a, b, c
    (0, 0, 0)
    >>> it.count
    3
    >>> it = ItCount([1,2])
    >>> unpack_partial(it)
    (0, 0, 0)
    >>> it.count
    3
    """
    a = b = c = 0
    try:
        a, b, c = it
    except ValueError:
        pass
    return a, b, c

def unpack_fail_assignment(it):
    """
    >>> it = ItCount([1, 2, 3])
    >>> a = b = c = 0
    >>> try: a, b[0], c = it
    ... except TypeError: pass
    >>> a,b,c
    (1, 0, 0)
    >>> it.count
    4
    >>> it = ItCount([1, 2, 3])
    >>> unpack_fail_assignment(it)
    (1, 0, 0)
    >>> it.count
    4
    """
    cdef object a,b,c
    a = b = c = 0
    try:
        a, b[0], c = it
    except TypeError:
        pass
    return a, b, c

def unpack_partial_typed(it):
    """
    >>> unpack_partial_typed([1, 2, 'abc'])
    (0, 0, 0)
    >>> unpack_partial_typed((1, 'abc', 3))
    (0, 0, 0)
    >>> unpack_partial_typed(set([1, 'abc', 3]))
    (0, 0, 0)

    >>> it = ItCount([1, 'abc', 3])
    >>> unpack_partial_typed(it)
    (0, 0, 0)
    >>> it.count
    4
    """
    cdef int a,b,c
    a = b = c = 0
    try:
        a, b, c = it
    except TypeError:
        pass
    return a, b, c

def unpack_typed(it):
    """
    >>> unpack_typed((1, 2.0, [1]))
    (1, 2.0, [1])
    >>> unpack_typed([1, 2.0, [1]])
    (1, 2.0, [1])
    >>> it = ItCount([1, 2.0, [1]])
    >>> unpack_typed(it)
    (1, 2.0, [1])
    >>> it.count
    4

    >>> try: unpack_typed((1, None, [1]))
    ... except TypeError: pass
    >>> try: unpack_typed([1, None, [1]])
    ... except TypeError: pass
    >>> it = ItCount([1, None, [1]])
    >>> try: unpack_typed(it)
    ... except TypeError: pass
    >>> it.count
    4

    >>> unpack_typed((1, 2.0, (1,)))
    Traceback (most recent call last):
    TypeError: Expected list, got tuple
    >>> it = ItCount([1, 2.0, (1,)])
    >>> unpack_typed(it)
    Traceback (most recent call last):
    TypeError: Expected list, got tuple
    >>> it.count
    4
    """
    cdef int a
    cdef float b
    cdef list c
    a,b,c = it
    return a,b,c

def failure_too_many(it):
    """
    >>> try: a,b,c = [1,2,3,4]
    ... except ValueError: pass
    >>> failure_too_many([1,2,3,4])
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)

    >>> try: a,b,c = [1,2,3,4]
    ... except ValueError: pass
    >>> failure_too_many((1,2,3,4))
    Traceback (most recent call last):
    ValueError: too many values to unpack (expected 3)

    >>> a,b,c = set([1,2,3,4])    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ValueError: too many values to unpack...
    >>> failure_too_many(set([1,2,3,4]))
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
    return a,b,c


def failure_too_few(it):
    """
    >>> try: a,b,c = [1,2]
    ... except ValueError: pass
    >>> failure_too_few([1,2])
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> try: a,b,c = (1,2)
    ... except ValueError: pass
    >>> failure_too_few((1,2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> try: a,b,c = set([1,2])
    ... except ValueError: pass
    ... else: print("DID NOT FAIL!")
    >>> failure_too_few(set([1,2]))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack

    >>> try: a,b,c = _it(2)
    ... except ValueError: pass
    ... else: print("DID NOT FAIL!")
    >>> failure_too_few(_it(2))
    Traceback (most recent call last):
    ValueError: need more than 2 values to unpack
    """
    a,b,c = it
    return a,b,c


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
    return a,b,c

def unpack_many(it):
    """
    >>> items = range(1,13)
    >>> unpack_many(items)
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many(iter(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many(list(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many(tuple(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    """
    a,b,c,d,e,f,g,h,i,j,k,l = it
    return a,b,c,d,e,f,g,h,i,j,k,l

def unpack_many_tuple(tuple it):
    """
    >>> items = range(1,13)
    >>> unpack_many_tuple(tuple(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    """
    a,b,c,d,e,f,g,h,i,j,k,l = it
    return a,b,c,d,e,f,g,h,i,j,k,l

def unpack_many_list(list it):
    """
    >>> items = range(1,13)
    >>> unpack_many_list(list(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    """
    a,b,c,d,e,f,g,h,i,j,k,l = it
    return a,b,c,d,e,f,g,h,i,j,k,l

def unpack_many_int(it):
    """
    >>> items = range(1,13)
    >>> unpack_many_int(items)
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many_int(iter(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many_int(list(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    >>> unpack_many_int(tuple(items))
    (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    """
    cdef int b
    cdef long f
    cdef Py_ssize_t h
    a,b,c,d,e,f,g,h,i,j,k,l = it
    return a,b,c,d,e,f,g,h,i,j,k,l


@cython.test_fail_if_path_exists('//PyTypeTestNode')
def unpack_literal_none_to_builtin_type():
    """
    >>> unpack_literal_none_to_builtin_type()
    (None, None, None, None)
    """
    cdef list a,b,c,d
    a, b = c, d = None, None
    return a,b,c,d


cdef class ExtType:
    pass


@cython.test_fail_if_path_exists('//PyTypeTestNode')
def unpack_literal_none_to_exttype():
    """
    >>> unpack_literal_none_to_exttype()
    (None, None, None, None)
    """
    cdef ExtType a,b,c,d
    a, b = c, d = None, None
    return a,b,c,d


# Github issue #1523
def test_unpack_resultref():
    """
    >>> test_unpack_resultref() == ((1, set()), 1, set())
    True
    """
    a = b, c = 1, set()
    return a, b, c
