__doc__ = u"""
>>> test_get_char_neg()
0
>>> test_get_char_zero()
1
>>> test_get_char_pos()
2
>>> test_get_uchar_zero()
1
>>> test_get_uchar_pos()
2
>>> test_get_int_neg()
0
>>> test_get_int_zero()
1
>>> test_get_int_pos()
2
>>> test_get_uint_zero()
1
>>> test_get_uint_pos()
2
>>> test_get_longlong_neg()
0
>>> test_get_longlong_zero()
1
>>> test_get_longlong_pos()
2
>>> test_get_longlong_big()
3
>>> test_get_ulonglong_zero()
1
>>> test_get_ulonglong_pos()
2
>>> test_get_ulonglong_big()
3
>>> test_del_char()
Traceback (most recent call last):
KeyError: 0
>>> test_del_uchar()
Traceback (most recent call last):
KeyError: 0
>>> test_del_int()
Traceback (most recent call last):
KeyError: 0
>>> test_del_uint()  #doctest: +ELLIPSIS
Traceback (most recent call last):
KeyError: 0...
>>> test_del_longlong() #doctest: +ELLIPSIS
Traceback (most recent call last):
KeyError: 0...
>>> test_del_longlong_big() #doctest: +ELLIPSIS
Traceback (most recent call last):
KeyError: ...
>>> test_del_ulonglong() #doctest: +ELLIPSIS
Traceback (most recent call last):
KeyError: 0...
>>> test_del_ulonglong_big() #doctest: +ELLIPSIS
Traceback (most recent call last):
KeyError: ...
"""

def test_get_char_neg():
    cdef char key = -1
    d = {-1:0}
    return d[key]
def test_get_char_zero():
    cdef char key = 0
    d = {0:1}
    return d[key]
def test_get_char_pos():
    cdef char key = 1
    d = {1:2}
    return d[key]


def test_get_uchar_zero():
    cdef unsigned char key = 0
    d = {0:1}
    return d[key]
def test_get_uchar_pos():
    cdef unsigned char key = 1
    d = {1:2}
    return d[key]


def test_get_int_neg():
    cdef int key = -1
    d = {-1:0}
    return d[key]
def test_get_int_zero():
    cdef int key = 0
    d = {0:1}
    return d[key]
def test_get_int_pos():
    cdef int key = 1
    d = {1:2}
    return d[key]


def test_get_uint_zero():
    cdef unsigned int key = 0
    d = {0:1}
    return d[key]
def test_get_uint_pos():
    cdef unsigned int key = 1
    d = {1:2}
    return d[key]


def test_get_longlong_neg():
    cdef long long key = -1
    d = {-1:0}
    return d[key]
def test_get_longlong_zero():
    cdef long long key = 0
    d = {0:1}
    return d[key]
def test_get_longlong_pos():
    cdef long long key = 1
    d = {1:2}
    return d[key]
def test_get_longlong_big():
    cdef unsigned int shift = sizeof(long)+2
    cdef long long big = 1
    cdef long long key = big<<shift
    d = {big<<shift:3}
    return d[key]

def test_get_ulonglong_zero():
    cdef unsigned long long key = 0
    d = {0:1}
    return d[key]
def test_get_ulonglong_pos():
    cdef unsigned long long key = 1
    d = {1:2}
    return d[key]
def test_get_ulonglong_big():
    cdef unsigned int shift = sizeof(long)+2
    cdef unsigned long long big = 1
    cdef unsigned long long key = big<<shift
    d = {big<<shift:3}
    return d[key]


def test_del_char():
    cdef char key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_uchar():
    cdef unsigned char key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_int():
    cdef int key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_uint():
    cdef unsigned int key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_longlong():
    cdef long long key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_ulonglong():
    cdef unsigned long long key = 0
    d = {0:1}
    del d[key]
    return d[key]

def test_del_longlong_big():
    cdef int shift = sizeof(long)+2
    cdef long long big = 1
    cdef long long key = big<<shift
    d = {big<<shift:1}
    del d[key]
    return d[key]

def test_del_ulonglong_big():
    cdef unsigned int shift = sizeof(long)+2
    cdef unsigned long long big = 1
    cdef unsigned long long key = big<<shift
    d = {big<<shift:1}
    del d[key]
    return d[key]
