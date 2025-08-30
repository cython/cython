# mode: run
# tag: special_method

cimport cython

text = u'ab jd  sdflk as sa  sadas asdas fsdf '


@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//AttributeNode",
    "//AttributeNode[@entry.cname = 'PyUnicode_Contains']")
def unicode_contains(unicode s, substring):
    """
    >>> unicode_contains(text, u'fl')
    True
    >>> unicode_contains(text, u'XYZ')
    False
    >>> unicode_contains(None, u'XYZ')
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute '__contains__'
    """
    return s.__contains__(substring)


@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode")
@cython.test_assert_path_exists(
#    "//CoerceToPyTypeNode",
    "//NameNode[@entry.cname = 'PyUnicode_Contains']")
def unicode_contains_unbound(unicode s, substring):
    """
    >>> unicode_contains_unbound(text, u'fl')
    True
    >>> unicode_contains_unbound(text, u'XYZ')
    False
    >>> unicode_contains_unbound(None, u'XYZ')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: descriptor '__contains__' requires a '...' object but received a 'NoneType'
    """
    return unicode.__contains__(s, substring)


cdef class UnicodeSubclass(unicode):
    """
    >>> u = UnicodeSubclass(text)
    >>> u'fl' in u
    False
    >>> u'XYZ' in u
    True
    >>> u.method(u'fl')
    False
    >>> u.method(u'XYZ')
    True
    >>> u.operator(u'fl')
    False
    >>> u.operator(u'XYZ')
    True
    """
    def __contains__(self, substring):
        return substring not in (self + u'x')

    def method(self, other):
        return self.__contains__(other)

    def operator(self, other):
        return other in self
