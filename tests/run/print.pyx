__doc__ = u"""
    >>> f(1, 'test')
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
"""

def f(a, b):
    print
    print a
    print a,
    print b
    print a, b
    print a, b,
    print 42, u"spam"
