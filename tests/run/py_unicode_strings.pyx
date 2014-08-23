# tag: py_unicode_strings

import sys

cimport cython
from libc.string cimport memcpy, strcpy

cdef bint Py_UNICODE_equal(const Py_UNICODE* u1, const Py_UNICODE* u2):
    while u1[0] != 0 and u2[0] != 0 and u1[0] == u2[0]:
        u1 += 1
        u2 += 1
    return u1[0] == u2[0]


ctypedef Py_UNICODE* LPWSTR

cdef unicode uobj = u'unicode\u1234'
cdef unicode uobj1 = u'u'
cdef Py_UNICODE* c_pu_str = u"unicode\u1234"
cdef Py_UNICODE[42] c_pu_arr
cdef LPWSTR c_wstr = u"unicode\u1234"
cdef Py_UNICODE* c_pu_empty = u""
cdef char* c_empty = ""
cdef unicode uwide_literal = u'\U00020000\U00020001'
cdef Py_UNICODE* c_pu_wide_literal = u'\U00020000\U00020001'

memcpy(c_pu_arr, c_pu_str, sizeof(Py_UNICODE) * (len(uobj) + 1))


def test_c_to_python():
    """
    >>> test_c_to_python()
    """
    assert c_pu_arr == uobj
    assert c_pu_str == uobj
    assert c_wstr == uobj

    assert c_pu_arr[1:] == uobj[1:]
    assert c_pu_str[1:] == uobj[1:]
    assert c_wstr[1:] == uobj[1:]

    assert c_pu_arr[:1] == uobj[:1]
    assert c_pu_arr[:1] == uobj[:1]
    assert c_pu_str[:1] == uobj[:1]
    assert c_wstr[:1] == uobj[:1]

    assert c_pu_arr[1:7] == uobj[1:7]
    assert c_pu_str[1:7] == uobj[1:7]
    assert c_wstr[1:7] == uobj[1:7]

    assert c_pu_arr[1] == uobj[1]
    assert c_pu_str[1] == uobj[1]
    assert c_wstr[1] == uobj[1]

    assert len(c_pu_str) == 8
    assert len(c_pu_arr) == 8
    assert len(c_wstr) == 8

    assert sizeof(c_pu_arr) == sizeof(Py_UNICODE) * 42
    assert sizeof(c_pu_str) == sizeof(void*)

    assert c_pu_wide_literal == uwide_literal
    if sizeof(Py_UNICODE) >= 4:
        assert len(c_pu_wide_literal) == 2
    else:
        assert len(c_pu_wide_literal) == 4

    if sys.version_info >= (3, 3):
        # Make sure len(unicode) is not reverted to pre-3.3 behavior
        assert len(uwide_literal) == 2

    assert u'unicode'
    assert not u''
    assert c_pu_str
    assert c_pu_empty


def test_python_to_c():
    """
    >>> test_python_to_c()
    """
    cdef unicode u

    assert Py_UNICODE_equal(c_pu_arr, uobj)
    assert Py_UNICODE_equal(c_pu_str, uobj)
    assert Py_UNICODE_equal(c_pu_str, <LPWSTR>uobj)
    u = uobj[1:]
    assert Py_UNICODE_equal(c_pu_str + 1, u)
    assert Py_UNICODE_equal(c_wstr + 1, u)
    u = uobj[:1]
    assert Py_UNICODE_equal(<Py_UNICODE*>u"u", u)
    u = uobj[1:7]
    assert Py_UNICODE_equal(<Py_UNICODE*>u"nicode", u)
    u = uobj[1]
    assert Py_UNICODE_equal(<Py_UNICODE*>u"n", u)

    assert Py_UNICODE_equal(uwide_literal, <Py_UNICODE*>c_pu_wide_literal)

    assert len(u"abc\0") == 4
    assert len(<Py_UNICODE*>u"abc\0") == 3
