
cimport cython

bstring1 = b"abcdefg"
bstring2 = b"1234567"

string1 = "abcdefg"
string2 = "1234567"

ustring1 = u"abcdefg"
ustring2 = u"1234567"

# unicode

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_eq(unicode s1, unicode s2):
    """
    >>> unicode_eq(ustring1, ustring1)
    True
    >>> unicode_eq(ustring1+ustring2, ustring1+ustring2)
    True
    >>> unicode_eq(ustring1, ustring2)
    False
    """
    return s1 == s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_neq(unicode s1, unicode s2):
    """
    >>> unicode_neq(ustring1, ustring1)
    False
    >>> unicode_neq(ustring1+ustring2, ustring1+ustring2)
    False
    >>> unicode_neq(ustring1, ustring2)
    True
    """
    return s1 != s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_literal_eq(unicode s):
    """
    >>> unicode_literal_eq(ustring1)
    True
    >>> unicode_literal_eq((ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_literal_eq(ustring2)
    False
    """
    return s == u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_literal_neq(unicode s):
    """
    >>> unicode_literal_neq(ustring1)
    False
    >>> unicode_literal_neq((ustring1+ustring2)[:len(ustring1)])
    False
    >>> unicode_literal_neq(ustring2)
    True
    """
    return s != u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
    "//CascadedCmpNode"
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def unicode_cascade(unicode s1, unicode s2):
    """
    >>> unicode_cascade(ustring1, ustring1)
    True
    >>> unicode_cascade(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_cascade(ustring1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_cascade_untyped_end(unicode s1, unicode s2):
    """
    >>> unicode_cascade_untyped_end(ustring1, ustring1)
    True
    >>> unicode_cascade_untyped_end(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_cascade_untyped_end(ustring1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg" == (<object>ustring1) == ustring1

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def unicode_cascade_untyped_end_bool(unicode s1, unicode s2):
    """
    >>> unicode_cascade_untyped_end_bool(ustring1, ustring1)
    True
    >>> unicode_cascade_untyped_end_bool(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> unicode_cascade_untyped_end_bool(ustring1, ustring2)
    False
    """
    if s1 == s2 == u"abcdefg" == (<object>ustring1) == ustring1:
        return True
    else:
        return False


# str

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def str_eq(str s1, str s2):
    """
    >>> str_eq(string1, string1)
    True
    >>> str_eq(string1+string2, string1+string2)
    True
    >>> str_eq(string1, string2)
    False
    """
    return s1 == s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def str_neq(str s1, str s2):
    """
    >>> str_neq(string1, string1)
    False
    >>> str_neq(string1+string2, string1+string2)
    False
    >>> str_neq(string1, string2)
    True
    """
    return s1 != s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def str_literal_eq(str s):
    """
    >>> str_literal_eq(string1)
    True
    >>> str_literal_eq((string1+string2)[:len(string1)])
    True
    >>> str_literal_eq(string2)
    False
    """
    return s == "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def str_literal_neq(str s):
    """
    >>> str_literal_neq(string1)
    False
    >>> str_literal_neq((string1+string2)[:len(string1)])
    False
    >>> str_literal_neq(string2)
    True
    """
    return s != "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def str_cascade(str s1, str s2):
    """
    >>> str_cascade(string1, string1)
    True
    >>> str_cascade(string1, (string1+string2)[:len(string1)])
    True
    >>> str_cascade(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def str_cascade_untyped_end(str s1, str s2):
    """
    >>> str_cascade_untyped_end(string1, string1)
    True
    >>> str_cascade_untyped_end(string1, (string1+string2)[:len(string1)])
    True
    >>> str_cascade_untyped_end(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg" == (<object>string1) == string1

# bytes

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def bytes_eq(bytes s1, bytes s2):
    """
    >>> bytes_eq(bstring1, bstring1)
    True
    >>> bytes_eq(bstring1+bstring2, bstring1+bstring2)
    True
    >>> bytes_eq(bstring1, bstring2)
    False
    """
    return s1 == s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def bytes_neq(bytes s1, bytes s2):
    """
    >>> bytes_neq(bstring1, bstring1)
    False
    >>> bytes_neq(bstring1+bstring2, bstring1+bstring2)
    False
    >>> bytes_neq(bstring1, bstring2)
    True
    """
    return s1 != s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def bytes_literal_eq(bytes s):
    """
    >>> bytes_literal_eq(bstring1)
    True
    >>> bytes_literal_eq((bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_literal_eq(bstring2)
    False
    """
    return s == b"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def bytes_literal_neq(bytes s):
    """
    >>> bytes_literal_neq(bstring1)
    False
    >>> bytes_literal_neq((bstring1+bstring2)[:len(bstring1)])
    False
    >>> bytes_literal_neq(bstring2)
    True
    """
    return s != b"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def bytes_cascade(bytes s1, bytes s2):
    """
    >>> bytes_cascade(bstring1, bstring1)
    True
    >>> bytes_cascade(bstring1, (bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_cascade(bstring1, bstring2)
    False
    """
    return s1 == s2 == b"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def bytes_cascade_untyped_end(bytes s1, bytes s2):
    """
    >>> bytes_cascade_untyped_end(bstring1, bstring1)
    True
    >>> bytes_cascade_untyped_end(bstring1, (bstring1+bstring2)[:len(bstring1)])
    True
    >>> bytes_cascade_untyped_end(bstring1, bstring2)
    False
    """
    return s1 == s2 == b"abcdefg" == (<object>bstring1) == bstring1


# basestring

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_eq(basestring s1, basestring s2):
    """
    >>> basestring_eq(string1, string1)
    True
    >>> basestring_eq(string1, ustring1)
    True
    >>> basestring_eq(string1+string2, string1+string2)
    True
    >>> basestring_eq(string1+ustring2, ustring1+string2)
    True
    >>> basestring_eq(string1, string2)
    False
    >>> basestring_eq(string1, ustring2)
    False
    >>> basestring_eq(ustring1, string2)
    False
    """
    return s1 == s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_neq(basestring s1, basestring s2):
    """
    >>> basestring_neq(string1, string1)
    False
    >>> basestring_neq(string1+string2, string1+string2)
    False
    >>> basestring_neq(string1+ustring2, ustring1+string2)
    False
    >>> basestring_neq(string1, string2)
    True
    >>> basestring_neq(string1, ustring2)
    True
    >>> basestring_neq(ustring1, string2)
    True
    """
    return s1 != s2

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_str_literal_eq(basestring s):
    """
    >>> basestring_str_literal_eq(string1)
    True
    >>> basestring_str_literal_eq((string1+string2)[:len(string1)])
    True
    >>> basestring_str_literal_eq(string2)
    False
    """
    return s == "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_unicode_literal_eq(basestring s):
    """
    >>> basestring_unicode_literal_eq(string1)
    True
    >>> basestring_unicode_literal_eq((string1+string2)[:len(string1)])
    True
    >>> basestring_unicode_literal_eq(string2)
    False
    """
    return s == u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_str_literal_neq(basestring s):
    """
    >>> basestring_str_literal_neq(string1)
    False
    >>> basestring_str_literal_neq((string1+string2)[:len(string1)])
    False
    >>> basestring_str_literal_neq(string2)
    True
    """
    return s != "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_unicode_literal_neq(basestring s):
    """
    >>> basestring_unicode_literal_neq(string1)
    False
    >>> basestring_unicode_literal_neq((string1+string2)[:len(string1)])
    False
    >>> basestring_unicode_literal_neq(string2)
    True
    """
    return s != u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
    "//CascadedCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def basestring_cascade_str(basestring s1, basestring s2):
    """
    >>> basestring_cascade_str(string1, string1)
    True
    >>> basestring_cascade_str(string1, (string1+string2)[:len(string1)])
    True
    >>> basestring_cascade_str(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
    "//CascadedCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def basestring_cascade_unicode(basestring s1, basestring s2):
    """
    >>> basestring_cascade_unicode(string1, string1)
    True
    >>> basestring_cascade_unicode(ustring1, string1)
    True
    >>> basestring_cascade_unicode(string1, ustring1)
    True
    >>> basestring_cascade_unicode(string1, (string1+string2)[:len(string1)])
    True
    >>> basestring_cascade_unicode(string1, string2)
    False
    >>> basestring_cascade_unicode(ustring1, string2)
    False
    >>> basestring_cascade_unicode(string1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def basestring_cascade_untyped_end(basestring s1, basestring s2):
    """
    >>> basestring_cascade_untyped_end(string1, string1)
    True
    >>> basestring_cascade_untyped_end(string1, (string1+string2)[:len(string1)])
    True
    >>> basestring_cascade_untyped_end(string1, string2)
    False
    """
    return s1 == s2 == "abcdefg" == (<object>string1) == string1


# untyped/literal comparison

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def untyped_unicode_literal_eq_bool(s):
    """
    >>> untyped_unicode_literal_eq_bool(string1)
    True
    >>> untyped_unicode_literal_eq_bool(ustring1)
    True
    >>> untyped_unicode_literal_eq_bool((string1+string2)[:len(string1)])
    True
    >>> untyped_unicode_literal_eq_bool(string2)
    False
    >>> untyped_unicode_literal_eq_bool(ustring2)
    False
    """
    return True if s == u"abcdefg" else False

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def untyped_str_literal_eq_bool(s):
    """
    >>> untyped_str_literal_eq_bool(string1)
    True
    >>> untyped_str_literal_eq_bool(ustring1)
    True
    >>> untyped_str_literal_eq_bool((string1+string2)[:len(string1)])
    True
    >>> untyped_str_literal_eq_bool(string2)
    False
    >>> untyped_str_literal_eq_bool(ustring2)
    False
    """
    return True if s == "abcdefg" else False

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = True]",
    "//CascadedCmpNode",
    "//CascadedCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def untyped_unicode_cascade(s1, unicode s2):
    """
    >>> untyped_unicode_cascade(ustring1, ustring1)
    True
    >>> untyped_unicode_cascade(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> untyped_unicode_cascade(ustring1, ustring2)
    False
    """
    return s1 == s2 == u"abcdefg"

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = False]",
    "//CascadedCmpNode",
    "//CascadedCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = True]",
)
def untyped_unicode_cascade_bool(s1, unicode s2):
    """
    >>> untyped_unicode_cascade_bool(ustring1, ustring1)
    True
    >>> untyped_unicode_cascade_bool(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> untyped_unicode_cascade_bool(ustring1, ustring2)
    False
    """
    return True if s1 == s2 == u"abcdefg" else False

@cython.test_assert_path_exists(
    "//PrimaryCmpNode",
    "//PrimaryCmpNode[@is_pycmp = True]",
    "//CascadedCmpNode",
#    "//CascadedCmpNode[@is_pycmp = False]",
)
@cython.test_fail_if_path_exists(
    "//CascadedCmpNode[@is_pycmp = True]",
    "//PrimaryCmpNode[@is_pycmp = False]",
)
def untyped_untyped_unicode_cascade_bool(s1, s2):
    """
    >>> untyped_untyped_unicode_cascade_bool(ustring1, ustring1)
    True
    >>> untyped_untyped_unicode_cascade_bool(ustring1, (ustring1+ustring2)[:len(ustring1)])
    True
    >>> untyped_untyped_unicode_cascade_bool(ustring1, ustring2)
    False
    >>> untyped_untyped_unicode_cascade_bool(string1, string2)
    False
    >>> untyped_untyped_unicode_cascade_bool(1, 2)
    False
    >>> untyped_untyped_unicode_cascade_bool(1, 1)
    False
    """
    return True if s1 == s2 == u"abcdefg" else False


# bytes/str comparison

@cython.test_assert_path_exists(
    '//PrimaryCmpNode',
    '//PrimaryCmpNode[@operator = "!="]',
)
def literal_compare_bytes_str():
    """
    >>> literal_compare_bytes_str()
    True
    """
    # we must not constant fold the subexpressions as the result is Py2/3 sensitive
    return b'abc' != 'abc'
