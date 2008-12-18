__doc__ = u"""
>>> smoketest()
[0, 4, 8]
>>> int_runvar()
[0, 4, 8]
>>> typed()
[A, A, A]
>>> iterdict()
[1, 2, 3]
"""

def smoketest():
    print [x*2 for x in range(5) if x % 2 == 0]

def int_runvar():
    cdef int x
    print [x*2 for x in range(5) if x % 2 == 0]

cdef class A:
    def __repr__(self): return u"A"

def typed():
    cdef A obj
    print [obj for obj in [A(), A(), A()]]

def iterdict():
    cdef dict d = dict(a=1,b=2,c=3)
    l = [d[key] for key in d]
    l.sort()
    print l
