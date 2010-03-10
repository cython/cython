
# Py2.6 and later only!
from __future__ import print_function

def print_to_stdout(a, b):
    """
    >>> print_to_stdout(1, 'test')
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
    """
    print()
    print(a)
    print(a, end=' ')
    print(b)
    print(a, b)
    print(a, b, end=' ')
    print(42, u"spam")

def print_assign(a, b):
    """
    >>> print_assign(1, 'test')
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
    """
    x = print
    x()
    x(a)
    x(a, end=' ')
    x(b)
    x(a, b)
    x(a, b, end=' ')
    x(42, u"spam")


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def print_to_stringio(stream, a, b):
    """
    >>> stream = StringIO()
    >>> print_to_stringio(stream, 1, 'test')
    >>> print(stream.getvalue())
    <BLANKLINE>
    1
    1 test
    1 test
    1 test 42 spam
    <BLANKLINE>
    """
    print(file=stream)
    print(a, file=stream)
    print(a, end=' ', file=stream)
    print(b, file=stream)
    print(a, b, file=stream)
    print(a, b, end=' ', file=stream)
    print(42, u"spam", file=stream)
