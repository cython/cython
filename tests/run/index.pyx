__doc__ = u"""
    >>> index_object(100, 100)       # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: 'int' object ...
"""

import sys
cdef Py_ssize_t maxsize = sys.maxsize

py_maxsize = maxsize

import cython

def index_tuple(tuple t, int i):
    """
    (minor PyPy error formatting bug here, hence ELLIPSIS)

    >>> index_tuple((1,1,2,3,5), 0)
    1
    >>> index_tuple((1,1,2,3,5), 3)
    3
    >>> index_tuple((1,1,2,3,5), -1)
    5
    >>> index_tuple((1,1,2,3,5), 100)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: ... index out of range
    >>> index_tuple((1,1,2,3,5), -7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: ... index out of range
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
    >>> index_list([2,3,5,7,11,13,17,19], 100)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: ... index out of range
    >>> index_list([2,3,5,7,11,13,17,19], -10)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: ... index out of range
    >>> index_list(None, 0)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    """
    return L[i]

def index_object(object o, int i):
    """
    (minor PyPy error formatting bug here, hence ELLIPSIS)

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


def del_index_list(list L, Py_ssize_t index):
    """
    >>> del_index_list(list(range(4)), 0)
    [1, 2, 3]
    >>> del_index_list(list(range(4)), 1)
    [0, 2, 3]
    >>> del_index_list(list(range(4)), -1)
    [0, 1, 2]
    >>> del_index_list(list(range(4)), py_maxsize)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: list... index out of range
    >>> del_index_list(list(range(4)), -py_maxsize)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: list... index out of range
    """
    del L[index]
    return L


def set_index_list(list L, Py_ssize_t index):
    """
    >>> set_index_list(list(range(4)), 0)
    [5, 1, 2, 3]
    >>> set_index_list(list(range(4)), 1)
    [0, 5, 2, 3]
    >>> set_index_list(list(range(4)), -1)
    [0, 1, 2, 5]
    >>> set_index_list(list(range(4)), py_maxsize)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: list... index out of range
    >>> set_index_list(list(range(4)), -py_maxsize)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    IndexError: list... index out of range
    """
    L[index] = 5
    return L


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

    L = [1, 2, 3]
    try:
        ix = py_maxsize + 1
    except OverflowError:
        pass  # can't test this here
    else:
        try: L[ix] = 5
        except IndexError: pass
        else: assert False, "setting large index failed to raise IndexError"

        try: del L[ix]
        except IndexError: pass
        else: assert False, "deleting large index failed to raise IndexError"

    try:
        ix = -py_maxsize - 2
    except OverflowError:
        pass  # can't test this here
    else:
        try: L[ix] = 5
        except IndexError: pass
        else: assert False, "setting large index failed to raise IndexError"

        try: del L[ix]
        except IndexError: pass
        else: assert False, "deleting large index failed to raise IndexError"

    assert len(D) == 0


def test_ulong_long():
    """
    >>> test_ulong_long()
    """
    cdef unsigned long long ix

    L = [1, 2, 3]
    try:
        ix = py_maxsize + 1
    except OverflowError:
        pass  # can't test this here
    else:
        try: L[ix] = 5
        except IndexError: pass
        else: assert False, "setting large index failed to raise IndexError"

        try: del L[ix]
        except IndexError: pass
        else: assert False, "deleting large index failed to raise IndexError"


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


class LargeIndexable(object):
    expected = None

    def __len__(self):
        raise OverflowError

    def __getitem__(self, index):
        return index

    def __setitem__(self, index, value):
        assert index == value == self.expected
        self.expected = None

    def __delitem__(self, index):
        assert self.expected == index
        self.expected = None


def test_large_indexing(obj):
    """
    >>> obj = LargeIndexable()
    >>> zero, pone, none, pmaxsize, nmaxsize = test_large_indexing(obj)
    >>> # , p2maxsize, n2maxsize
    >>> zero
    0
    >>> pone
    1
    >>> none
    -1
    >>> pmaxsize == py_maxsize
    True
    >>> nmaxsize == -py_maxsize
    True

    #>>> p2maxsize == py_maxsize*2
    #True
    #>>> n2maxsize == -py_maxsize*2
    #True
    """
    return (
        obj[0], obj[1], obj[-1],
        obj[maxsize], obj[-maxsize],
        #obj[maxsize*2], obj[-maxsize*2]     # FIXME!
    )


def del_large_index(obj, Py_ssize_t index):
    """
    >>> obj = LargeIndexable()
    >>> del_large_index(obj, 0)
    >>> del_large_index(obj, 1)
    >>> del_large_index(obj, -1)
    >>> del_large_index(obj, py_maxsize)
    >>> del_large_index(obj, -py_maxsize)
    """
    obj.expected = index
    del obj[index]
    assert obj.expected is None


def set_large_index(obj, Py_ssize_t index):
    """
    >>> obj = LargeIndexable()
    >>> set_large_index(obj, 0)
    >>> set_large_index(obj, 1)
    >>> set_large_index(obj, -1)
    >>> set_large_index(obj, py_maxsize)
    >>> set_large_index(obj, -py_maxsize)
    """
    obj.expected = index
    obj[index] = index
    assert obj.expected is None


class DoesntLikePositiveIndices(object):
    def __getitem__(self, idx):
        if idx >= 0:
            raise RuntimeError("Positive index")
        return "Good"

    def __setitem__(self, idx, value):
        if idx >= 0:
            raise RuntimeError("Positive index")

    def __delitem__(self, idx):
        if idx >= 0:
            raise RuntimeError("Positive index")

    def __len__(self):
        return 500

def test_call_with_negative_numbers():
    """
    The key point is that Cython shouldn't default to PySequence_*Item
    since that invisibly adjusts negative numbers to be len(o)-idx.
    >>> test_call_with_negative_numbers()
    'Good'
    """
    cdef int idx = -5
    indexme = DoesntLikePositiveIndices()
    del indexme[idx]
    indexme[idx] = "something"
    return indexme[idx]
