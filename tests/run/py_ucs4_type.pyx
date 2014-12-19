# -*- coding: iso-8859-1 -*-

cimport cython

cdef Py_UCS4 char_ASCII = u'A'
cdef Py_UCS4 char_KLINGON = u'\uF8D2'

def compare_ASCII():
    """
    >>> compare_ASCII()
    True
    False
    False
    """
    print(char_ASCII == u'A')
    print(char_ASCII == u'B')
    print(char_ASCII == u'\uF8D2')


def compare_klingon():
    """
    >>> compare_klingon()
    True
    False
    False
    """
    print(char_KLINGON == u'\uF8D2')
    print(char_KLINGON == u'A')
    print(char_KLINGON == u'B')


def single_uchar_compare():
    """
    >>> single_uchar_compare()
    """
    assert u'\u0100' < u'\u0101'
    assert u'\u0101' > u'\u0100'


from cpython.unicode cimport PyUnicode_FromOrdinal
import sys

u0 = u'\x00'
u1 = u'\x01'
umax = PyUnicode_FromOrdinal(sys.maxunicode)

def unicode_ordinal(Py_UCS4 i):
    """
    >>> ord(unicode_ordinal(0)) == 0
    True
    >>> ord(unicode_ordinal(1)) == 1
    True
    >>> ord(unicode_ordinal(sys.maxunicode)) == sys.maxunicode
    True

    >>> ord(unicode_ordinal(u0)) == 0
    True
    >>> ord(unicode_ordinal(u1)) == 1
    True
    >>> ord(unicode_ordinal(umax)) == sys.maxunicode
    True

    Value too small:
    >>> unicode_ordinal(-1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    Value too large:
    >>> unicode_ordinal(1114111+1) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    OverflowError: ...

    Less than one character:
    >>> unicode_ordinal(u0[:0])
    Traceback (most recent call last):
    ...
    ValueError: only single character unicode strings can be converted to Py_UCS4, got length 0

    More than one character:
    >>> unicode_ordinal(u0+u1)
    Traceback (most recent call last):
    ...
    ValueError: only single character unicode strings can be converted to Py_UCS4, got length 2
    """
    return i

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_type_methods(Py_UCS4 uchar):
    """
    >>> unicode_type_methods(ord('A'))
    [True, True, False, False, False, False, False, True, True]
    >>> unicode_type_methods(ord('a'))
    [True, True, False, False, True, False, False, False, False]
    >>> unicode_type_methods(ord('8'))
    [True, False, True, True, False, True, False, False, False]
    >>> unicode_type_methods(ord('\\t'))
    [False, False, False, False, False, False, True, False, False]
    """
    return [
        # character types
        uchar.isalnum(),
        uchar.isalpha(),
        uchar.isdecimal(),
        uchar.isdigit(),
        uchar.islower(),
        uchar.isnumeric(),
        uchar.isspace(),
        uchar.istitle(),
        uchar.isupper(),
        ]

@cython.test_assert_path_exists('//PythonCapiCallNode')
@cython.test_fail_if_path_exists('//SimpleCallNode')
def unicode_methods(Py_UCS4 uchar):
    """
    >>> unicode_methods(ord('A')) == ['a', 'A', 'A']
    True
    >>> unicode_methods(ord('a')) == ['a', 'A', 'A']
    True
    """
    return [
        # character conversion
        uchar.lower(),
        uchar.upper(),
        uchar.title(),
        ]

@cython.test_assert_path_exists('//IntNode')
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//PythonCapiCallNode')
def len_uchar(Py_UCS4 uchar):
    """
    >>> len_uchar(ord('A'))
    1
    """
    return len(uchar)

def index_uchar(Py_UCS4 uchar, Py_ssize_t i):
    """
    >>> index_uchar(ord('A'), 0) == ('A', 'A', 'A')
    True
    >>> index_uchar(ord('A'), -1) == ('A', 'A', 'A')
    True
    >>> index_uchar(ord('A'), 1)
    Traceback (most recent call last):
    IndexError: string index out of range
    """
    return uchar[0], uchar[-1], uchar[i]

mixed_ustring = u'AbcDefGhIjKlmnoP'
lower_ustring = mixed_ustring.lower()
upper_ustring = mixed_ustring.lower()

@cython.test_assert_path_exists('//PythonCapiCallNode',
                                '//ForFromStatNode')
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def count_lower_case_characters(unicode ustring):
    """
    >>> count_lower_case_characters(mixed_ustring)
    10
    >>> count_lower_case_characters(lower_ustring)
    16
    """
    cdef Py_ssize_t count = 0
    for uchar in ustring:
         if uchar.islower():
             count += 1
    return count

@cython.test_assert_path_exists('//PythonCapiCallNode',
                                '//ForFromStatNode')
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def count_lower_case_characters_slice(unicode ustring):
    """
    >>> count_lower_case_characters_slice(mixed_ustring)
    10
    >>> count_lower_case_characters_slice(lower_ustring)
    14
    >>> sum([ 1 for uchar in lower_ustring[1:-1] if uchar.islower() ])
    14
    """
    cdef Py_ssize_t count = 0
    for uchar in ustring[1:-1]:
         if uchar.islower():
             count += 1
    return count

@cython.test_assert_path_exists('//PythonCapiCallNode',
                                '//ForFromStatNode')
@cython.test_fail_if_path_exists('//SimpleCallNode',
                                 '//ForInStatNode')
def count_lower_case_characters_slice_reversed(unicode ustring):
    """
    >>> count_lower_case_characters_slice_reversed(mixed_ustring)
    10
    >>> count_lower_case_characters_slice_reversed(lower_ustring)
    14
    >>> sum([ 1 for uchar in lower_ustring[-2:0:-1] if uchar.islower() ])
    14
    """
    cdef Py_ssize_t count = 0
    for uchar in ustring[-2:0:-1]:
         if uchar.islower():
             count += 1
    return count

def loop_object_over_latin1_unicode_literal():
    """
    >>> result = loop_object_over_latin1_unicode_literal()
    >>> print(result[:-1])
    abcdefg
    >>> ord(result[-1]) == 0xD7
    True
    """
    cdef object uchar
    chars = []
    for uchar in u'abcdefg\xD7':
        chars.append(uchar)
    return u''.join(chars)

def loop_object_over_unicode_literal():
    """
    >>> result = loop_object_over_unicode_literal()
    >>> print(result[:-1])
    abcdefg
    >>> ord(result[-1]) == 0xF8FD
    True
    """
    cdef object uchar
    chars = []
    for uchar in u'abcdefg\uF8FD':
        chars.append(uchar)
    return u''.join(chars)

@cython.test_assert_path_exists('//SwitchStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def iter_and_in():
    """
    >>> iter_and_in()
    a
    b
    e
    f
    h
    """
    for c in u'abcdefgh':
        if c in u'abCDefGh':
            print c


@cython.test_fail_if_path_exists('//ForInStatNode')
def iter_inferred():
    """
    >>> iter_inferred()
    a
    b
    c
    d
    e
    """
    uchars = list(u"abcde")
    uchars = u''.join(uchars)
    for c in uchars:
        print c


@cython.test_assert_path_exists('//SwitchStatNode',
                                '//ForFromStatNode')
@cython.test_fail_if_path_exists('//ForInStatNode')
def index_and_in():
    """
    >>> index_and_in()
    1
    3
    4
    7
    8
    """
    cdef int i
    for i in range(1,9):
        if u'abcdefgh'[-i] in u'abCDefGh':
            print i

# special test for narrow builds

high_uchar = u'\U00012345'
high_ustring0 = u'\U00012345\U00012346abc'
high_ustring1 = u'\U00012346\U00012345abc'
high_ustring_end = u'\U00012346abc\U00012344\U00012345'
high_ustring_no = u'\U00012346\U00012346abc'

def uchar_in(Py_UCS4 uchar, unicode ustring):
    """
    >>> uchar_in(high_uchar, high_ustring0)
    True
    >>> uchar_in(high_uchar, high_ustring1)
    True
    >>> uchar_in(high_uchar, high_ustring_end)
    True
    >>> uchar_in(high_uchar, high_ustring_no)
    False
    """
    assert uchar == 0x12345, ('%X' % uchar)
    return uchar in ustring
