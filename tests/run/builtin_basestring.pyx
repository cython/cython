
import sys
IS_PY3 = sys.version_info[0] >= 3

ustring = u'abcdef'
sstring =  'abcdef'
bstring = b'abcdef'


def isinstance_basestring(obj):
    """
    >>> isinstance_basestring(ustring)
    True
    >>> isinstance_basestring(sstring)
    True
    >>> if IS_PY3: print(not isinstance_basestring(bstring))
    ... else: print(isinstance_basestring(bstring))
    True
    """
    return isinstance(obj, basestring)


def basestring_is_unicode_in_py3():
    """
    >>> basestring_is_unicode_in_py3()
    True
    """
    if IS_PY3:
        return basestring is unicode
    else:
        return basestring is not unicode


def unicode_subtypes_basestring():
    """
    >>> unicode_subtypes_basestring()
    True
    """
    return issubclass(unicode, basestring)
