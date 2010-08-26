
class test(object):
    a = 1
t = test()

def getattr2_literal_unicode(a):
    """
    >>> getattr2_literal_unicode(t)
    1
    >>> getattr2_literal_unicode(object())
    Traceback (most recent call last):
    AttributeError: 'object' object has no attribute 'a'
    """
    return getattr(a, u"a")

def getattr3_literal_unicode(a, b):
    """
    >>> getattr3_literal_unicode(t, 2)
    (1, 2)
    """
    return getattr(a, u"a", b), getattr(a, u"b", b)

def getattr2_simple(a, b):
    """
    >>> getattr2_simple(t, 'a')
    1
    >>> getattr2_simple(t, 'b')
    Traceback (most recent call last):
    AttributeError: 'test' object has no attribute 'b'
    """
    return getattr(a, b)

def getattr3_explicit(a, b, c):
    """
    >>> getattr3_explicit(t, 'a', 2)
    1
    >>> getattr3_explicit(t, 'b', 2)
    2
    """
    return getattr3(a, b, c)

def getattr3_args(a, b, c):
    """
    >>> getattr3_args(t, 'a', 2)
    1
    >>> getattr3_args(t, 'b', 2)
    2
    """
    return getattr(a, b, c)
