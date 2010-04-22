cimport cython

bytes_abc = b'abc'
bytes_ABC = b'ABC'
bytes_abc_null = b'a\0b\0c'
bytes_ABC_null = b'A\0B\0C'

unicode_abc = u'abc'
unicode_ABC = u'ABC'
unicode_abc_null = u'a\0b\0c'
unicode_ABC_null = u'A\0B\0C'


def for_in_bytes(bytes s):
    """
    >>> for_in_bytes(bytes_abc)
    'X'
    >>> for_in_bytes(bytes_ABC)
    'C'
    >>> for_in_bytes(bytes_abc_null)
    'X'
    >>> for_in_bytes(bytes_ABC_null)
    'C'
    """
    for c in s:
        # Py2/Py3
        if c == b'C' or c == c'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_char_in_bytes(bytes s):
    """
    >>> for_char_in_bytes(bytes_abc)
    'X'
    >>> for_char_in_bytes(bytes_ABC)
    'C'
    >>> for_char_in_bytes(bytes_abc_null)
    'X'
    >>> for_char_in_bytes(bytes_ABC_null)
    'C'
    """
    cdef char c
    for c in s:
        if c == b'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_char_in_enumerate_bytes(bytes s):
    """
    >>> for_char_in_enumerate_bytes(bytes_abc)
    'X'
    >>> for_char_in_enumerate_bytes(bytes_ABC)
    2
    >>> for_char_in_enumerate_bytes(bytes_abc_null)
    'X'
    >>> for_char_in_enumerate_bytes(bytes_ABC_null)
    4
    """
    cdef char c
    cdef Py_ssize_t i
    for i, c in enumerate(s):
        if c == b'C':
            return i
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_pyunicode_in_unicode(unicode s):
    """
    >>> for_pyunicode_in_unicode(unicode_abc)
    'X'
    >>> for_pyunicode_in_unicode(unicode_ABC)
    'C'
    >>> for_pyunicode_in_unicode(unicode_abc_null)
    'X'
    >>> for_pyunicode_in_unicode(unicode_ABC_null)
    'C'
    """
    cdef Py_UNICODE c
    for c in s:
        if c == u'C':
            return 'C'
    else:
        return 'X'

@cython.test_assert_path_exists("//ForFromStatNode")
@cython.test_fail_if_path_exists("//ForInStatNode")
def for_pyunicode_in_enumerate_unicode(unicode s):
    """
    >>> for_pyunicode_in_enumerate_unicode(unicode_abc)
    'X'
    >>> for_pyunicode_in_enumerate_unicode(unicode_ABC)
    2
    >>> for_pyunicode_in_enumerate_unicode(unicode_abc_null)
    'X'
    >>> for_pyunicode_in_enumerate_unicode(unicode_ABC_null)
    4
    """
    cdef Py_UNICODE c
    cdef Py_ssize_t i
    for i, c in enumerate(s):
        if c == u'C':
            return i
    else:
        return 'X'
