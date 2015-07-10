
cimport cython

# Py2.3 doesn't have the set type, but Cython does :)
_set = set

def setcomp():
    """
    >>> type(setcomp()) is not list
    True
    >>> type(setcomp()) is _set
    True
    >>> sorted(setcomp())
    [0, 4, 8]
    """
    x = 'abc'
    result = { x*2
             for x in range(5)
             if x % 2 == 0 }
    assert x == 'abc' # do not leak
    return result

@cython.test_assert_path_exists(
    "//InlinedGeneratorExpressionNode",
    "//ComprehensionAppendNode")
def genexp_set():
    """
    >>> type(genexp_set()) is _set
    True
    >>> sorted(genexp_set())
    [0, 4, 8]
    """
    x = 'abc'
    result = set( x*2
                  for x in range(5)
                  if x % 2 == 0 )
    assert x == 'abc' # do not leak
    return result

cdef class A:
    def __repr__(self): return u"A"
    def __richcmp__(one, other, int op): return one is other
    def __hash__(self): return id(self) % 65536

def typed():
    """
    >>> list(typed())
    [A, A, A]
    """
    cdef A obj
    return {obj for obj in {A(), A(), A()}}

def iterdict():
    """
    >>> sorted(iterdict())
    [1, 2, 3]
    """
    cdef dict d = dict(a=1,b=2,c=3)
    return {d[key] for key in d}

def sorted(it):
    l = list(it)
    l.sort()
    return l
