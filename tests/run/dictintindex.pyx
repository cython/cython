def test_get_char_neg():
    """
    >>> test_get_char_neg()
    0
    """
    cdef char key = -1
    if <char>-1 < 0:
        d = {-1:0}
    else:
        d = {255:0}
    return d[key]
def test_get_char_zero():
    """
    >>> test_get_char_zero()
    1
    """
    cdef char key = 0
    d = {0:1}
    return d[key]
def test_get_char_pos():
    """
    >>> test_get_char_pos()
    2
    """
    cdef char key = 1
    d = {1:2}
    return d[key]


def test_get_uchar_zero():
    """
    >>> test_get_uchar_zero()
    1
    """
    cdef unsigned char key = 0
    d = {0:1}
    return d[key]
def test_get_uchar_pos():
    """
    >>> test_get_uchar_pos()
    2
    """
    cdef unsigned char key = 1
    d = {1:2}
    return d[key]


def test_get_int_neg():
    """
    >>> test_get_int_neg()
    0
    """
    cdef int key = -1
    d = {-1:0}
    return d[key]
def test_get_int_zero():
    """
    >>> test_get_int_zero()
    1
    """
    cdef int key = 0
    d = {0:1}
    return d[key]
def test_get_int_pos():
    """
    >>> test_get_int_pos()
    2
    """
    cdef int key = 1
    d = {1:2}
    return d[key]


def test_get_uint_zero():
    """
    >>> test_get_uint_zero()
    1
    """
    cdef unsigned int key = 0
    d = {0:1}
    return d[key]
def test_get_uint_pos():
    """
    >>> test_get_uint_pos()
    2
    """
    cdef unsigned int key = 1
    d = {1:2}
    return d[key]


def test_get_longlong_neg():
    """
    >>> test_get_longlong_neg()
    0
    """
    cdef long long key = -1
    d = {-1:0}
    return d[key]
def test_get_longlong_zero():
    """
    >>> test_get_longlong_zero()
    1
    """
    cdef long long key = 0
    d = {0:1}
    return d[key]
def test_get_longlong_pos():
    """
    >>> test_get_longlong_pos()
    2
    """
    cdef long long key = 1
    d = {1:2}
    return d[key]
def test_get_longlong_big():
    """
    >>> test_get_longlong_big()
    3
    """
    cdef unsigned int shift = sizeof(long)+2
    cdef long long big = 1
    cdef long long key = big<<shift
    d = {big<<shift:3}
    return d[key]

def test_get_ulonglong_zero():
    """
    >>> test_get_ulonglong_zero()
    1
    """
    cdef unsigned long long key = 0
    d = {0:1}
    return d[key]
def test_get_ulonglong_pos():
    """
    >>> test_get_ulonglong_pos()
    2
    """
    cdef unsigned long long key = 1
    d = {1:2}
    return d[key]
def test_get_ulonglong_big():
    """
    >>> test_get_ulonglong_big()
    3
    """
    cdef unsigned int shift = sizeof(long)+2
    cdef unsigned long long big = 1
    cdef unsigned long long key = big<<shift
    d = {big<<shift:3}
    return d[key]


def test_del_char():
    """
    >>> test_del_char()
    Traceback (most recent call last):
    KeyError: 0
    """
    cdef char key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_uchar():
    """
    >>> test_del_uchar()
    Traceback (most recent call last):
    KeyError: 0
    """
    cdef unsigned char key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_int():
    """
    >>> test_del_int()
    Traceback (most recent call last):
    KeyError: 0
    """
    cdef int key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_uint():
    """
    >>> test_del_uint()  #doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: 0...
    """
    cdef unsigned int key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_longlong():
    """
    >>> test_del_longlong() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: 0...
    """
    cdef long long key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_ulonglong():
    """
    >>> test_del_ulonglong() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: 0...
    """
    cdef unsigned long long key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_longlong_big():
    """
    >>> test_del_longlong_big() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: ...
    """
    cdef int shift = sizeof(long)+2
    cdef long long big = 1
    cdef long long key = big<<shift
    d = {big<<shift:1}
    del d[key]
    return d[key]

def test_del_ulonglong_big():
    """
    >>> test_del_ulonglong_big() #doctest: +ELLIPSIS
    Traceback (most recent call last):
    KeyError: ...
    """
    cdef unsigned int shift = sizeof(long)+2
    cdef unsigned long long big = 1
    cdef unsigned long long key = big<<shift
    d = {big<<shift:1}
    del d[key]
    return d[key]
