__doc__ = u"""
    >>> a = A()
    >>> a.foo()
    (True, u'yo')
    >>> a.foo(False)
    (False, u'yo')
    >>> a.foo(10, u'yes')
    (True, u'yes')

    >>> call0()
    (True, u'yo')
    >>> call1()
    (False, u'yo')
    >>> call2()
    (False, u'go')
"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'")

cdef class A:
    cpdef foo(self, bint a=True, b=u"yo"):
        return a, b

def call0():
    a = A()
    return a.foo()

def call1():
    a = A()
    return a.foo(False)

def call2():
    a = A()
    return a.foo(False, u"go")
