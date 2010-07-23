
cimport cython

def dictcomp():
    """
    >>> sorted(dictcomp().items())
    [(2, 0), (4, 4), (6, 8)]
    >>> sorted(dictcomp().items())
    [(2, 0), (4, 4), (6, 8)]
    """
    x = 'abc'
    result = { x+2:x*2
               for x in range(5)
               if x % 2 == 0 }
    assert x == 'abc' # do not leak!
    return result

@cython.test_fail_if_path_exists(
    "//GeneratorExpressionNode",
    "//SimpleCallNode")
@cython.test_assert_path_exists(
    "//ComprehensionNode",
    "//ComprehensionNode//DictComprehensionAppendNode")
def genexpr():
    """
    >>> type(genexpr()) is dict
    True
    >>> type(genexpr()) is dict
    True
    """
    x = 'abc'
    result = dict( (x+2,x*2)
                   for x in range(5)
                   if x % 2 == 0 )
    assert x == 'abc'
    return result

cdef class A:
    def __repr__(self): return u"A"
    def __richcmp__(one, other, op): return one is other
    def __hash__(self): return id(self) % 65536

def typed_dictcomp():
    """
    >>> list(typed_dictcomp().items())
    [(A, 1), (A, 1), (A, 1)]
    """
    cdef A obj
    return {obj:1 for obj in [A(), A(), A()]}

def iterdict_dictcomp():
    """
    >>> sorted(iterdict_dictcomp().items())
    [(1, 'a'), (2, 'b'), (3, 'c')]
    """
    cdef dict d = dict(a=1,b=2,c=3)
    return {d[key]:key for key in d}

def sorted(it):
    l = list(it)
    l.sort()
    return l
