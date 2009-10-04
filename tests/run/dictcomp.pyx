__doc__ = u"""
>>> type(smoketest_dict()) is dict
True
>>> type(smoketest_list()) is dict
True

>>> sorted(smoketest_dict().items())
[(2, 0), (4, 4), (6, 8)]
>>> sorted(smoketest_list().items())
[(2, 0), (4, 4), (6, 8)]

>>> list(typed().items())
[(A, 1), (A, 1), (A, 1)]
>>> sorted(iterdict().items())
[(1, 'a'), (2, 'b'), (3, 'c')]
"""

cimport cython

def smoketest_dict():
    return { x+2:x*2
             for x in range(5)
             if x % 2 == 0 }

@cython.test_fail_if_path_exists(
    "//ComprehensionNode//ComprehensionAppendNode",
    "//SimpleCallNode//ComprehensionNode")
@cython.test_assert_path_exists(
    "//ComprehensionNode",
    "//ComprehensionNode//DictComprehensionAppendNode")
def smoketest_list():
    return dict([ (x+2,x*2)
                  for x in range(5)
                  if x % 2 == 0 ])

cdef class A:
    def __repr__(self): return u"A"
    def __richcmp__(one, other, op): return one is other
    def __hash__(self): return id(self) % 65536

def typed():
    cdef A obj
    return {obj:1 for obj in [A(), A(), A()]}

def iterdict():
    cdef dict d = dict(a=1,b=2,c=3)
    return {d[key]:key for key in d}

def sorted(it):
    l = list(it)
    l.sort()
    return l
