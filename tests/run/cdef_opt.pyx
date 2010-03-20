__doc__ = u"""
    >>> a = A()
    >>> a.foo()
    (True, 'yo')
    >>> a.foo(False)
    (False, 'yo')
    >>> a.foo(10, 'yes')
    (True, 'yes')

"""

cdef class A:
    cpdef foo(self, bint a=True, b="yo"):
        return a, b

def call0():
    """
    >>> call0()
    (True, 'yo')
    """
    cdef A a = A()
    return a.foo()

def call1():
    """
    >>> call1()
    (False, 'yo')
    """
    cdef A a = A()
    return a.foo(False)

def call2():
    """
    >>> call2()
    (False, 'go')
    """
    cdef A a = A()
    return a.foo(False, "go")
