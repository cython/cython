# mode: run
# tag: cpp
# cython: c_string_encoding=ascii, c_string_type=unicode

cimport cython

from libcpp.string cimport string

b_asdf = b'asdf'
b_asdg = b'asdg'
b_s = b's'

u_asdf = u'asdf'
u_asdg = u'asdg'
u_s = u's'


def test_conversion(py_obj):
    """
    >>> test_conversion(b_asdf) == u_asdf or test_conversion(b_asdf)
    True
    >>> test_conversion(u_asdf) == u_asdf or test_conversion(u_asdf)
    True
    >>> test_conversion(123)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: expected ..., int found
    """
    cdef string s = py_obj
    assert <size_t>len(py_obj) == s.length(), '%d != %d' % (len(py_obj), s.length())
    return s


def test_empty(py_obj):
    """
    >>> test_empty('')
    True
    >>> test_empty('abc')
    False
    >>> test_empty(u_asdf[:0])
    True
    >>> test_empty(u_asdf)
    False
    """
    cdef string a = py_obj
    return a.empty()


def test_push_back(a):
    """
    >>> test_push_back(b_asdf) == u_asdf + u_s
    True
    >>> test_push_back(u_asdf) == u_asdf + u_s
    True
    """
    cdef string s = a
    s.push_back(<char>ord('s'))
    return s


def test_clear(a):
    """
    >>> test_clear(u_asdf) == u_s[:0]
    True
    >>> test_clear(b_asdf) == u_s[:0]
    True
    """
    cdef string s = a
    s.clear()
    return s

def test_assign(char *a):
    """
    >>> test_assign(b_asdf) == 'ggg'
    True
    """
    cdef string s = string(a)
    s.assign(<char *>"ggg")
    return s.c_str()
