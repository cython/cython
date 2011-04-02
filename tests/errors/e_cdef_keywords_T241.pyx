# ticket: 241
# mode: error

cdef some_function(x, y):
    pass

cdef class A:
    cdef some_method(self, x, y=1):
        pass

some_function(1, 2)
some_function(1, y=2)

cdef A a = A()
a.some_method(1)
a.some_method(1, 2)
a.some_method(1, y=2)

_ERRORS = u"""
12:13: Keyword and starred arguments not allowed in cdef functions.
17:13: Keyword and starred arguments not allowed in cdef functions.
"""
