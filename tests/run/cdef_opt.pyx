__doc__ = u"""
    >>> a = A()
    >>> a.foo()
    (True, u'yo')
    >>> a.foo(False)
    (False, u'yo')
    >>> a.foo(10, u'yes')
    (True, u'yes')

"""

import sys

if sys.version_info[0] >= 3:
    __doc__ = __doc__.replace(u"u'", u"'")

cdef class A:
    cpdef foo(self, bint a=True, b=u"yo"):
        return a, b

def call0():
    """
    >>> call0()
    (True, u'yo')
    """
    a = A()
    return a.foo()

def call1():
    """
    >>> call1()
    (False, u'yo')
    """
    a = A()
    return a.foo(False)

def call2():
    """
    >>> call2()
    (False, u'go')
    """
    a = A()
    return a.foo(False, u"go")
