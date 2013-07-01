# mode: run
# tag: global, nameerror

try:
    from heapq import *   # just to confuse the compiler
except ImportError:
    pass


def f(a):
    """
    Py<=3.3 gives 'global name ...', Py3.4+ only 'name ...'

    >>> f(1)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    NameError: ...name 'definitely_unknown_name' is not defined
    """
    a = f
    a = definitely_unknown_name
