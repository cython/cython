__doc__ = """
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
