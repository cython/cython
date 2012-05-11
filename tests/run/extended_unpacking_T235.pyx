# ticket: 235

__doc__ = u"""
    >>> class FakeSeq(object):
    ...     def __init__(self, length):
    ...         self._values = list(range(1,length+1))
    ...     def __getitem__(self, i):
    ...         return self._values[i]

    >>> unpack( FakeSeq(2) )
    (1, 2)
    >>> unpack_recursive( FakeSeq(4) )
    (1, [2, 3], 4)
"""

def unpack(l):
    """
    >>> unpack([1,2])
    (1, 2)
    >>> unpack('12')
    ('1', '2')
    """
    a, b = l
    return a,b

def unpack_list(list l):
    """
    >>> unpack_list([1,2])
    (1, 2)
    """
    a, b = l
    return a,b

def unpack_tuple(tuple t):
    """
    >>> unpack_tuple((1,2))
    (1, 2)
    """
    a, b = t
    return a,b

def unpack_single(l):
    """
    >>> unpack_single([1])
    [1]
    >>> unpack_single('1')
    ['1']
    """
    *a, = l
    return a

def unpack_tuple_single(tuple t):
    """
    >>> unpack_tuple_single((1,))
    [1]
    """
    *a, = t
    return a

def assign():
    """
    >>> assign()
    (1, [2, 3, 4], 5)
    """
    *a, b = 1,2,3,4,5
    assert a+[b] == [1,2,3,4,5], (a,b)
    a, *b = 1,2,3,4,5
    assert [a]+b == [1,2,3,4,5], (a,b)
    [a, *b, c] = 1,2,3,4,5
    return a,b,c

def unpack_into_list(l):
    """
    >>> unpack_into_list('123')
    ('1', ['2'], '3')
    """
    [*a, b] = l
    assert a+[b] == list(l), repr((a+[b],list(l)))
    [a, *b] = l
    assert [a]+b == list(l), repr(([a]+b,list(l)))
    [a, *b, c] = l
    return a,b,c

def unpack_into_tuple(t):
    """
    >>> unpack_into_tuple('123')
    ('1', ['2'], '3')
    """
    (*a, b) = t
    assert a+[b] == list(t), repr((a+[b],list(t)))
    (a, *b) = t
    assert [a]+b == list(t), repr(([a]+b,list(t)))
    (a, *b, c) = t
    return a,b,c

def unpack_in_loop(list_of_sequences):
    """
    >>> unpack_in_loop([(1,2), (1,2,3), (1,2,3,4)])
    1
    ([1], 2)
    ([1, 2], 3)
    ([1, 2, 3], 4)
    2
    (1, [2])
    (1, [2, 3])
    (1, [2, 3, 4])
    3
    (1, [], 2)
    (1, [2], 3)
    (1, [2, 3], 4)
    """
    print 1
    for *a,b in list_of_sequences:
        print((a,b))
    print 2
    for a,*b in list_of_sequences:
        print((a,b))
    print 3
    for a,*b, c in list_of_sequences:
        print((a,b,c))

def unpack_recursive(t):
    """
    >>> unpack_recursive((1,2,3,4))
    (1, [2, 3], 4)
    """
    *(a, *b), c  = t
    return a,b,c

def unpack_typed(t):
    """
    >>> unpack_typed((1,2))
    ([1], 2)
    """
    cdef list a
    *a, b  = t
    return a,b


def unpack_right(l):
    """
    >>> unpack_right('')
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_right('1')
    ('1', [])
    >>> unpack_right([1])
    (1, [])
    >>> unpack_right('12')
    ('1', ['2'])
    >>> unpack_right([1,2])
    (1, [2])
    >>> unpack_right('123')
    ('1', ['2', '3'])
    >>> unpack_right([1,2,3])
    (1, [2, 3])
    """
    a, *b = l
    return a,b

def unpack_right_list(list l):
    """
    >>> unpack_right_list([])
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_right_list([1])
    (1, [])
    >>> unpack_right_list([1,2])
    (1, [2])
    >>> unpack_right_list([1,2,3])
    (1, [2, 3])
    """
    a, *b = l
    return a,b

def unpack_right_tuple(tuple t):
    """
    >>> unpack_right_tuple(())
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_right_tuple((1,))
    (1, [])
    >>> unpack_right_tuple((1,2))
    (1, [2])
    >>> unpack_right_tuple((1,2,3))
    (1, [2, 3])
    """
    a, *b = t
    return a,b


def unpack_left(l):
    """
    >>> unpack_left('')
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_left('1')
    ([], '1')
    >>> unpack_left([1])
    ([], 1)
    >>> unpack_left('12')
    (['1'], '2')
    >>> unpack_left([1,2])
    ([1], 2)
    >>> unpack_left('123')
    (['1', '2'], '3')
    >>> unpack_left([1,2,3])
    ([1, 2], 3)
    """
    *a, b = l
    return a,b

def unpack_left_list(list l):
    """
    >>> unpack_left_list([])
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_left_list([1])
    ([], 1)
    >>> unpack_left_list([1,2])
    ([1], 2)
    >>> unpack_left_list([1,2,3])
    ([1, 2], 3)
    """
    *a, b = l
    return a,b

def unpack_left_tuple(tuple t):
    """
    >>> unpack_left_tuple(())
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_left_tuple((1,))
    ([], 1)
    >>> unpack_left_tuple((1,2))
    ([1], 2)
    >>> unpack_left_tuple((1,2,3))
    ([1, 2], 3)
    """
    *a, b = t
    return a,b


def unpack_middle(l):
    """
    >>> unpack_middle('')
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_middle([])
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_middle(())
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_middle('1')
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> unpack_middle([1])
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> unpack_middle('12')
    ('1', [], '2')
    >>> unpack_middle([1,2])
    (1, [], 2)
    >>> unpack_middle('123')
    ('1', ['2'], '3')
    >>> unpack_middle([1,2,3])
    (1, [2], 3)
    """
    a, *b, c = l
    return a,b,c

def unpack_middle_list(list l):
    """
    >>> unpack_middle_list([])
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_middle_list([1])
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> unpack_middle_list([1,2])
    (1, [], 2)
    >>> unpack_middle_list([1,2,3])
    (1, [2], 3)
    """
    a, *b, c = l
    return a,b,c

def unpack_middle_tuple(tuple t):
    """
    >>> unpack_middle_tuple(())
    Traceback (most recent call last):
    ValueError: need more than 0 values to unpack
    >>> unpack_middle_tuple((1,))
    Traceback (most recent call last):
    ValueError: need more than 1 value to unpack
    >>> unpack_middle_tuple((1,2))
    (1, [], 2)
    >>> unpack_middle_tuple((1,2,3))
    (1, [2], 3)
    >>> a,b,c = unpack_middle(list(range(100)))
    >>> a, len(b), c
    (0, 98, 99)
    >>> a,b,c = unpack_middle_list(list(range(100)))
    >>> a, len(b), c
    (0, 98, 99)
    >>> a,b,c = unpack_middle_tuple(tuple(range(100)))
    >>> a, len(b), c
    (0, 98, 99)
    """
    a, *b, c = t
    return a,b,c

def unpack_many_middle(it):
    """
    >>> unpack_many_middle(list(range(14)))
    (0, 1, 2, 3, 4, [5, 6, 7, 8, 9], 10, 11, 12, 13)
    >>> unpack_many_middle(tuple(range(14)))
    (0, 1, 2, 3, 4, [5, 6, 7, 8, 9], 10, 11, 12, 13)
    >>> unpack_many_middle(iter(range(14)))
    (0, 1, 2, 3, 4, [5, 6, 7, 8, 9], 10, 11, 12, 13)
    """
    a,b,c,d,e,*f,g,h,i,j = it
    return a,b,c,d,e,f,g,h,i,j

def unpack_many_left(it):
    """
    >>> unpack_many_left(list(range(14)))
    (0, 1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11, 12, 13])
    >>> unpack_many_left(tuple(range(14)))
    (0, 1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11, 12, 13])
    >>> unpack_many_left(iter(range(14)))
    (0, 1, 2, 3, 4, 5, 6, 7, 8, [9, 10, 11, 12, 13])
    """
    a,b,c,d,e,f,g,h,i,*j = it
    return a,b,c,d,e,f,g,h,i,j

def unpack_many_right(it):
    """
    >>> unpack_many_right(list(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    >>> unpack_many_right(tuple(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    >>> unpack_many_right(iter(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    """
    *a,b,c,d,e,f,g,h,i,j = it
    return a,b,c,d,e,f,g,h,i,j

def unpack_many_right_loop(it):
    """
    >>> unpack_many_right_loop(list(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    >>> unpack_many_right_loop(tuple(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    >>> unpack_many_right_loop(iter(range(14)))
    ([0, 1, 2, 3, 4], 5, 6, 7, 8, 9, 10, 11, 12, 13)
    """
    cdef int i
    for i in range(1):
        *a,b,c,d,e,f,g,h,i,j = it
    return a,b,c,d,e,f,g,h,i,j
