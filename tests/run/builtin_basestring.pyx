
cimport cython

ustring = u'abcdef'
sstring =  'abcdef'
bstring = b'abcdef'


def isinstance_basestring(obj):
    """
    >>> isinstance_basestring(ustring)
    True
    >>> isinstance_basestring(sstring)
    True
    >>> print(not isinstance_basestring(bstring))
    True
    """
    return isinstance(obj, basestring)


def basestring_is_unicode_in_py3():
    """
    >>> basestring_is_unicode_in_py3()
    True
    """
    object_type = basestring
    return object_type is unicode


def unicode_subtypes_basestring():
    """
    >>> unicode_subtypes_basestring()
    True
    """
    return issubclass(unicode, basestring)


def basestring_typed_variable(obj):
    """
    >>> basestring_typed_variable(None) is None
    True
    >>> basestring_typed_variable(ustring) is ustring
    True
    >>> basestring_typed_variable(sstring) is sstring
    True
    >>> class S(str): pass
    >>> basestring_typed_variable(S())   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...got ...S...
    """
    cdef basestring s
    s = u'abc'
    assert s
    s = 'abc'
    assert s
    # make sure coercion also works in conditional expressions
    s = u'abc' if obj else 'abc'
    assert s
    s = obj
    return s


def basestring_typed_argument(basestring obj):
    """
    >>> basestring_typed_argument(None) is None
    True
    >>> basestring_typed_argument(ustring) is ustring
    True
    >>> basestring_typed_argument(sstring) is sstring
    True
    >>> class S(str): pass
    >>> basestring_typed_argument(S())   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...got ...S...
    """
    return obj


@cython.test_fail_if_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def basestring_join(basestring s, *values):
    """
    >>> print(basestring_join(ustring, 'a', 'b', 'c'))
    aabcdefbabcdefc
    >>> print(basestring_join(sstring, 'a', 'b', 'c'))
    aabcdefbabcdefc
    >>> basestring_join(None, 'a', 'b', 'c')
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'join'
    """
    return s.join(values)
