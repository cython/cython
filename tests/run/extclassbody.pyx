__doc__ = u"""
>>> s = Spam()
>>> s.a
1
>>> s.c
3
>>> s.test(5)
8
>>> s.b
3
"""

cdef class Spam:
    a = 1
    def test(self, a):
        return a + self.c
    b = a + 2
    c = 3
