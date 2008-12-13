__doc__ = u"""
>>> type(smoketest()) is not list
True
>>> type(smoketest()) is _set
True

>>> sorted(smoketest())
[0, 4, 8]
>>> list(typed())
[A, A, A]
>>> sorted(iterdict())
[1, 2, 3]
"""

# Py2.3 doesn't have the set type, but Cython does :)
_set = set

def smoketest():
    return {x*2 for x in range(5) if x % 2 == 0}

cdef class A:
    def __repr__(self): return u"A"
    def __richcmp__(one, other, op): return one is other
    def __hash__(self): return id(self) % 65536

def typed():
    cdef A obj
    return {obj for obj in {A(), A(), A()}}

def iterdict():
    cdef dict d = dict(a=1,b=2,c=3)
    return {d[key] for key in d}

def sorted(it):
    l = list(it)
    l.sort()
    return l
