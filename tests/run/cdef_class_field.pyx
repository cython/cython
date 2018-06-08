# mode: run
# tag: exttype
# ticket: 677

"""
>>> str(Foo(4))
'4'
>>> x
3
"""

x = 3
cdef int y

cdef class Foo:
    cdef int x
    cdef int y
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return str(self.x)
