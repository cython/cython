
ctypedef fused sequence:
    list
    tuple
    object

def unpack_one(sequence it):
    """
    >>> items = [1]
    >>> unpack_one(items)
    1
    >>> unpack_one(iter(items))
    1
    >>> unpack_one(list(items))
    1
    >>> unpack_one(tuple(items))
    1
    """
    a, = it
    return a

def unpack_two(sequence it):
    """
    >>> items = [1,2]
    >>> unpack_two(items)
    (1, 2)
    >>> unpack_two(iter(items))
    (1, 2)
    >>> unpack_two(list(items))
    (1, 2)
    >>> unpack_two(tuple(items))
    (1, 2)
    """
    a,b = it
    return a,b

def unpack_two_int(sequence it):
    """
    >>> items = [1,2]
    >>> unpack_two_int(items)
    (1, 2)
    >>> unpack_two_int(iter(items))
    (1, 2)
    >>> unpack_two_int(list(items))
    (1, 2)
    >>> unpack_two_int(tuple(items))
    (1, 2)

    >>> items = [1, object()]
    >>> unpack_two_int(items)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    >>> unpack_two_int(iter(items))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    >>> unpack_two_int(list(items))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    >>> unpack_two_int(tuple(items))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...int...
    """
    cdef int b
    a,b = it
    return a,b

def unpack_many(sequence it):
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

def unpack_many_int(sequence it):
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

    >>> items = range(1,10)
    >>> unpack_many_int(items)
    Traceback (most recent call last):
    ValueError: need more than 9 values to unpack
    >>> unpack_many_int(iter(items))
    Traceback (most recent call last):
    ValueError: need more than 9 values to unpack
    >>> unpack_many_int(list(items))
    Traceback (most recent call last):
    ValueError: need more than 9 values to unpack
    >>> unpack_many_int(tuple(items))
    Traceback (most recent call last):
    ValueError: need more than 9 values to unpack
    """
    cdef int b
    cdef long f
    cdef Py_ssize_t h
    a,b,c,d,e,f,g,h,i,j,k,l = it
    return a,b,c,d,e,f,g,h,i,j,k,l
