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
    >>> unicode_contains(text, 'fl')
    True
    >>> unicode_contains(text, 'XYZ')
    False
    >>> unicode_contains(None, 'XYZ')
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
    >>> unicode_contains_unbound(text, 'fl')
    True
    >>> unicode_contains_unbound(text, 'XYZ')
    False
    >>> unicode_contains_unbound(None, 'XYZ')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: descriptor '__contains__' requires a '...' object but received a 'NoneType'
    """
    return unicode.__contains__(s, substring)


cdef class UnicodeSubclass(unicode):
    """
    >>> u = UnicodeSubclass(text)
    >>> 'fl' in u
    False
    >>> 'XYZ' in u
    True
    >>> u.method('fl')
    False
    >>> u.method('XYZ')
    True
    >>> u.operator('fl')
    False
    >>> u.operator('XYZ')
    True
    """
    def __contains__(self, substring):
        return substring not in (self + u'x')

    def method(self, other):
        return self.__contains__(other)

    def operator(self, other):
        return other in self
