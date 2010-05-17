# -*- coding: utf-8 -*-

cimport cython

unicode_str = u'ab jd  üöä ôñ ÄÖ'
bytes_str   = b'ab jd  sdflk as sa  sadas asdas fsdf '

_frozenset = frozenset
_set = set

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_unicode(unicode s):
    """
    >>> len(unicode_str)
    16
    >>> len_unicode(unicode_str)
    16
    >>> len_unicode(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_bytes(bytes s):
    """
    >>> len(bytes_str)
    37
    >>> len_bytes(bytes_str)
    37
    >>> len_bytes(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

#@cython.test_assert_path_exists(
#    "//CoerceToPyTypeNode",
#    "//PythonCapiCallNode")
def len_str(str s):
    """
    >>> len('abcdefg')
    7
    >>> len_str('abcdefg')
    7
    >>> len_unicode(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_list(list s):
    """
    >>> l = [1,2,3,4]
    >>> len(l)
    4
    >>> len_list(l)
    4
    >>> len_list(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_tuple(tuple s):
    """
    >>> t = (1,2,3,4)
    >>> len(t)
    4
    >>> len_tuple(t)
    4
    >>> len_tuple(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_dict(dict s):
    """
    >>> d = dict(a=1, b=2, c=3, d=4)
    >>> len(d)
    4
    >>> len_dict(d)
    4
    >>> len_dict(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_set(set s):
    """
    >>> s = _set((1,2,3,4))
    >>> len(s)
    4
    >>> len_set(s)
    4
    >>> len_set(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)

@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def len_frozenset(frozenset s):
    """
    >>> s = _frozenset((1,2,3,4))
    >>> len(s)
    4
    >>> len_frozenset(s)
    4
    >>> len_set(None)
    Traceback (most recent call last):
    TypeError: object of type 'NoneType' has no len()
    """
    return len(s)
