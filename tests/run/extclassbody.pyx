__doc__ = u"""
>>> s = Spam()
>>> s.a
2
>>> s.c
3
>>> s.test(5)
13
>>> s.b
5
"""

cdef class Spam:
    a = 1
    def test(self, a):
        return a + self.b + self.c
    b = a + 2 # 3
    a = b - 1 # 2
    c = 3     # 3
    b = c + a # 5
