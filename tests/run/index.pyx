__doc__ = u"""
    >>> index_object(100, 100)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: 'int' object ...
"""

import sys
if sys.version_info < (2,5):
    __doc__ = __doc__.replace(u"'int' object ...", u'unsubscriptable object')

import cython

def index_tuple(tuple t, int i):
    """
    >>> index_tuple((1,1,2,3,5), 0)
    1
    >>> index_tuple((1,1,2,3,5), 3)
    3
    >>> index_tuple((1,1,2,3,5), -1)
    5
    >>> index_tuple((1,1,2,3,5), 100)
    Traceback (most recent call last):
    IndexError: tuple index out of range
    >>> index_tuple(None, 0)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    return t[i]

def index_list(list L, int i):
    """
    >>> index_list([2,3,5,7,11,13,17,19], 0)
    2
    >>> index_list([2,3,5,7,11,13,17,19], 5)
    13
    >>> index_list([2,3,5,7,11,13,17,19], -1)
    19
    >>> index_list([2,3,5,7,11,13,17,19], 100)
    Traceback (most recent call last):
    IndexError: list index out of range
    >>> index_list(None, 0)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    return L[i]

def index_object(object o, int i):
    """
    >>> index_object([2,3,5,7,11,13,17,19], 1)
    3
    >>> index_object([2,3,5,7,11,13,17,19], -1)
    19
    >>> index_object((1,1,2,3,5), 2)
    2
    >>> index_object((1,1,2,3,5), -2)
    3
    >>> index_object("abcdef...z", 0)
    'a'
    >>> index_object("abcdef...z", -1)
    'z'
    >>> index_object("abcdef...z", 100)
    Traceback (most recent call last):
    IndexError: string index out of range
    >>> try: index_object(None, 0)
    ... except TypeError: pass
    """
    return o[i]


# These make sure that our fast indexing works with large and unsigned types.

def test_unsigned_long():
    """
    >>> test_unsigned_long()
    """
    cdef int i
    cdef unsigned long ix
    cdef D = {}
    for i from 0 <= i < <int>sizeof(unsigned long) * 8:
        ix = (<unsigned long>1) << i
        D[ix] = True
    for i from 0 <= i < <int>sizeof(unsigned long) * 8:
        ix = (<unsigned long>1) << i
        assert D[ix] is True
        del D[ix]
    assert len(D) == 0

def test_unsigned_short():
    """
    >>> test_unsigned_short()
    """
    cdef int i
    cdef unsigned short ix
    cdef D = {}
    for i from 0 <= i < <int>sizeof(unsigned short) * 8:
        ix = (<unsigned short>1) << i
        D[ix] = True
    for i from 0 <= i < <int>sizeof(unsigned short) * 8:
        ix = (<unsigned short>1) << i
        assert D[ix] is True
        del D[ix]
    assert len(D) == 0

def test_long_long():
    """
    >>> test_long_long()
    """
    cdef int i
    cdef long long ix
    cdef D = {}
    for i from 0 <= i < <int>sizeof(long long) * 8:
        ix = (<long long>1) << i
        D[ix] = True
    for i from 0 <= i < <int>sizeof(long long) * 8:
        ix = (<long long>1) << i
        assert D[ix] is True
        del D[ix]
    assert len(D) == 0

@cython.boundscheck(False)
def test_boundscheck_unsigned(list L, tuple t, object o, unsigned long ix):
    """
    >>> test_boundscheck_unsigned([1, 2, 4], (1, 2, 4), [1, 2, 4], 2)
    (4, 4, 4)
    >>> test_boundscheck_unsigned([1, 2, 4], (1, 2, 4), "", 2)
    Traceback (most recent call last):
    ...
    IndexError: string index out of range
    """
    return L[ix], t[ix], o[ix]

@cython.boundscheck(False)
def test_boundscheck_signed(list L, tuple t, object o, long ix):
    """
    >>> test_boundscheck_signed([1, 2, 4], (1, 2, 4), [1, 2, 4], 2)
    (4, 4, 4)
    >>> test_boundscheck_signed([1, 2, 4], (1, 2, 4), "", 2)
    Traceback (most recent call last):
    ...
    IndexError: string index out of range
    """
    return L[ix], t[ix], o[ix]

@cython.wraparound(False)
def test_wraparound_signed(list L, tuple t, object o, long ix):
    """
    >>> test_wraparound_signed([1, 2, 4], (1, 2, 4), [1, 2, 4], 2)
    (4, 4, 4)
    >>> test_wraparound_signed([1, 2, 4], (1, 2, 4), "", 2)
    Traceback (most recent call last):
    ...
    IndexError: string index out of range
    """
    return L[ix], t[ix], o[ix]

def large_literal_index(object o):
    """
    >>> large_literal_index({1000000000000000000000000000000: True})
    True
    """
    return o[1000000000000000000000000000000]
