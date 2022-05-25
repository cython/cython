
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

@cython.test_assert_path_exists(
    "//InlinedGeneratorExpressionNode",
    "//DictComprehensionAppendNode")
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
    def __richcmp__(one, other, int op): return one is other
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


# Copied from sre_compile.py in CPython 3.7.  Previously failed to detect variable initialisation.
_equivalences = (
    # LATIN SMALL LETTER I, LATIN SMALL LETTER DOTLESS I
    (0x69, 0x131), # iı
    # LATIN SMALL LETTER S, LATIN SMALL LETTER LONG S
    (0x73, 0x17f), # sſ
    # MICRO SIGN, GREEK SMALL LETTER MU
    (0xb5, 0x3bc), # µμ
    # COMBINING GREEK YPOGEGRAMMENI, GREEK SMALL LETTER IOTA, GREEK PROSGEGRAMMENI
    (0x345, 0x3b9, 0x1fbe), # \u0345ιι
    # ...
)

_ignorecase_fixes = {
    i: tuple(j for j in t if i != j)
    for t in _equivalences for i in t
}

def nested_tuple():
    """
    >>> modlevel, funclevel = nested_tuple()
    >>> modlevel == funclevel or (modlevel, funclevel)
    True
    """
    inner_ignorecase_fixes = {
        i: tuple(j for j in t if i != j)
        for t in _equivalences for i in t
    }

    return sorted(_ignorecase_fixes.items()), sorted(inner_ignorecase_fixes.items())
