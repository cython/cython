u"""
>>> smoketest()
[0, 4, 8]
>>> typed()
[A, A, A]
"""

def smoketest():
    print [x*2 for x in range(5) if x % 2 == 0]

cdef class A:
    def __repr__(self): return "A"

def typed():
    cdef A obj
    print [obj for obj in [A(), A(), A()]]