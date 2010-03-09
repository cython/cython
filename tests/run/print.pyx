def f(a, b):
    """
    >>> f(1, 'test')
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
    """
    print
    print a
    print a,
    print b
    print a, b
    print a, b,
    print 42, u"spam"


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def s(stream, a, b):
    """
    >>> stream = StringIO()
    >>> s(stream, 1, 'test')
    >>> print(stream.getvalue())
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
    <BLANKLINE>
    """
    print >> stream
    print >> stream, a
    print >> stream, a,
    print >> stream, b
    print >> stream, a, b
    print >> stream, a, b,
    print >> stream, 42, u"spam"
