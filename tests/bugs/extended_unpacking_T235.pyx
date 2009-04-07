__doc__ = u"""
>>> unpack([1,2])
(1, 2)
>>> unpack_list([1,2])
(1, 2)
>>> unpack_tuple((1,2))
(1, 2)

>>> unpack('12')
('1', '2')

>>> unpack_into_list('123')
('1', ['2'], '3')
>>> unpack_into_tuple('123')
('1', ['2'], '3')

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
(1, [2])
(1, [2], 3)
(1, [2, 3], 4)

>>> assign()
(1, [2, 3, 4], 5)

>>> unpack_right('')
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_right_list([])
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_right_tuple(())
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

>>> unpack_right_list([1])
(1, [])
>>> unpack_right_list([1,2])
(1, [2])
>>> unpack_right_list([1,2,3])
(1, [2, 3])
>>> unpack_right_tuple((1,))
(1, [])
>>> unpack_right_tuple((1,2))
(1, [2])
>>> unpack_right_tuple((1,2,3))
(1, [2, 3])

>>> unpack_left('')
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_left_list([])
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_left_tuple(())
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

>>> unpack_left_list([1])
([], 1)
>>> unpack_left_list([1,2])
([1], 2)
>>> unpack_left_list([1,2])
([1, 2], 3)
>>> unpack_left_tuple((1,))
([], 1)
>>> unpack_left_tuple((1,2))
([1], 2)
>>> unpack_left_tuple((1,2,3))
([1, 2], 3)

>>> unpack_middle('')
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_middle([])
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_middle(())
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_middle_list([])
Traceback (most recent call last):
ValueError: need more than 0 values to unpack
>>> unpack_middle_tuple(())
Traceback (most recent call last):
ValueError: need more than 0 values to unpack

>>> unpack_middle('1')
Traceback (most recent call last):
ValueError: need more than 1 value to unpack
>>> unpack_middle([1])
Traceback (most recent call last):
ValueError: need more than 1 value to unpack
>>> unpack_middle_list([1])
Traceback (most recent call last):
ValueError: need more than 1 value to unpack
>>> unpack_middle_tuple((1,))
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

>>> unpack_middle_list([1,2])
(1, [], 2)
>>> unpack_middle_list([1,2,3])
(1, [2], 3)
>>> unpack_middle_tuple((1,2))
(1, [], 2)
>>> unpack_middle_tuple((1,2,3))
(1, [2], 3)

>>> a,b,c = unpack_middle(range(100))
>>> a, len(b), c
0, 98, 99
>>> a,b,c = unpack_middle_list(range(100))
>>> a, len(b), c
0, 98, 99
>>> a,b,c = unpack_middle_tuple(tuple(range(100)))
>>> a, len(b), c
0, 98, 99

"""

def unpack(l):
    a, b = l
    return a,b

def unpack_list(list l):
    a, b = l
    return a,b

def unpack_tuple(tuple t):
    a, b = t
    return a,b

def assign():
    *a, b = 1,2,3,4,5
    assert a+[b] == (1,2,3,4,5)
    a, *b = 1,2,3,4,5
    assert [a]+b == (1,2,3,4,5)
    [a, *b, c] = 1,2,3,4,5
    return a,b,c

def unpack_into_list(l):
    [*a, b] = l
    assert a+[b] == l
    [a, *b] = l
    assert [a]+b == l
    [a, *b, c] = l
    return a,b,c

def unpack_into_tuple(t):
    (*a, b) = t
    assert a+(b,) == t
    (a, *b) = t
    assert (a,)+b == t
    (a, *b, c) = t
    return a,b,c

def unpack_in_loop(list_of_sequences):
    print 1
    for *a,b in list_of_sequences:
        print a,b
    print 2
    for a,*b in list_of_sequences:
        print a,b
    print 3
    for a,*b, c in list_of_sequences:
        print a,b,c

def unpack_right(l):
    a, *b = l
    return a,b

def unpack_right_list(list l):
    a, *b = l
    return a,b

def unpack_right_tuple(tuple t):
    a, *b = t
    return a,b


def unpack_left(l):
    *a, b = l
    return a,b

def unpack_left_list(list l):
    *a, b = l
    return a,b

def unpack_left_tuple(tuple t):
    *a, b = t
    return a,b


def unpack_middle(l):
    a, *b, c = l
    return a,b,c

def unpack_middle_list(list l):
    a, *b, c = l
    return a,b,c

def unpack_middle_tuple(tuple t):
    a, *b, c = t
    return a,b,c
