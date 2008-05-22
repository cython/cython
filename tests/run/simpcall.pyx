__doc__ = u"""
    >>> z(1,9.2, b'test')
    >>> failtype()
    Traceback (most recent call last):
    TypeError: an integer is required

    >>> fail0(1,2) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: function takes exactly 2 arguments (0 given)

    >>> fail1(1,2) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: function takes exactly 2 arguments (1 given)
"""

import sys, re
if sys.version_info >= (2,6):
    __doc__ = re.sub(u"Error: .*exactly.*", u"Error: ...", __doc__)

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")

def f(x, y):
    x = y

cdef void g(int i, float f, char *p):
    f = i

cdef h(int i, obj):
    i = obj

def z(a, b, c):
    f(a, b)
    f(a, b,)
    g(1, 2.0, "spam")
    g(a, b, c)
    
def fail0(a, b):
    f()
    
def fail1(a, b):
    f(a)

def failtype():
    h(42, "eggs")
