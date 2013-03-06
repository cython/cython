# mode: run
# tag: global, nameerror

try:
    from heapq import *   # just to confuse the compiler
except ImportError:
    pass


def f(a):
    """
    >>> f(1)
    Traceback (most recent call last):
    NameError: name 'definitely_unknown_name' is not defined
    """
    a = f
    a = definitely_unknown_name
