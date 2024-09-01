# coding=utf8
# mode: run
# tag: constant_folding

cimport cython


bstring = b'abc\xE9def'
ustring = u'abc\xE9def'
surrogates_ustring = u'abc\U00010000def'


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
    )
def bytes_slicing2():
    """
    >>> a,b,c,d = bytes_slicing2()
    >>> a == bstring[:]
    True
    >>> b == bstring[2:]
    True
    >>> c == bstring[:4]
    True
    >>> d == bstring[2:4]
    True
    """
    str0 = b'abc\xE9def'[:]
    str1 = b'abc\xE9def'[2:]
    str2 = b'abc\xE9def'[:4]
    str3 = b'abc\xE9def'[2:4]

    return str0, str1, str2, str3


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
    )
def unicode_slicing2():
    """
    >>> a,b,c,d = unicode_slicing2()
    >>> a == ustring[:]
    True
    >>> b == ustring[2:]
    True
    >>> c == ustring[:4]
    True
    >>> d == ustring[2:4]
    True
    """
    str0 = u'abc\xE9def'[:]
    str1 = u'abc\xE9def'[2:]
    str2 = u'abc\xE9def'[:4]
    str3 = u'abc\xE9def'[2:4]

    return str0, str1, str2, str3


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
    )
def unicode_slicing_unsafe_surrogates2():
    """
    >>> unicode_slicing_unsafe_surrogates2() == surrogates_ustring[2:]
    True
    """
    ustring = u'abc\U00010000def'[2:]
    return ustring


@cython.test_fail_if_path_exists(
    "//SliceIndexNode",
    )
def unicode_slicing_safe_surrogates2():
    """
    >>> unicode_slicing_safe_surrogates2() == surrogates_ustring[:2]
    True
    >>> print(unicode_slicing_safe_surrogates2())
    ab
    """
    ustring = u'abc\U00010000def'[:2]
    return ustring


@cython.test_fail_if_path_exists(
    "//ComprehensionNode",
    "//ForInStatNode",
)
@cython.test_assert_path_exists(
    "//SetNode",
)
def for_in_empty_setcomp():
    """
    >>> s = for_in_empty_setcomp()
    >>> isinstance(s, set)
    True
    >>> len(s)
    0
    """
    return {i for i in []}


@cython.test_fail_if_path_exists(
    "//ReturnStatNode//AddNode",
)
def add_strings():
    """
    >>> s, u, b = add_strings()
    >>> s == 'abcdef' or s
    True
    >>> u == 'abcdef' or u
    True
    >>> b == b'abcdef' or b
    True
    """
    # FIXME: test encodings and unicode escapes
    return "abc" + "def", u"abc" + u"def", b"abc" + b"def"
