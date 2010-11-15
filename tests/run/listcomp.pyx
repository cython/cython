def smoketest():
    """
    >>> smoketest()
    [0, 4, 8]
    """
    x = 'abc'
    result = [x*2 for x in range(5) if x % 2 == 0]
    assert x != 'abc'
    return result

def list_genexp():
    """
    >>> list_genexp()
    [0, 4, 8]
    """
    x = 'abc'
    result = list(x*2 for x in range(5) if x % 2 == 0)
    assert x == 'abc'
    return result

def int_runvar():
    """
    >>> int_runvar()
    [0, 4, 8]
    """
    cdef int x
    print [x*2 for x in range(5) if x % 2 == 0]

cdef class A:
    def __repr__(self): return u"A"

def typed():
    """
    >>> typed()
    [A, A, A]
    """
    cdef A obj
    print [obj for obj in [A(), A(), A()]]

def iterdict():
    """
    >>> iterdict()
    [1, 2, 3]
    """
    cdef dict d = dict(a=1,b=2,c=3)
    l = [d[key] for key in d]
    l.sort()
    print l

listcomp_result = [ i*i for i in range(5) ]
def global_listcomp():
    """
    >>> [ i*i for i in range(5) ]
    [0, 1, 4, 9, 16]
    >>> listcomp_result
    [0, 1, 4, 9, 16]
    """

def nested_result():
    """
    >>> nested_result()
    [[], [-1], [-1, 0], [-1, 0, 1]]
    """
    result = [[a-1 for a in range(b)] for b in range(4)]
    return result

def listcomp_as_condition(sequence):
    """
    >>> listcomp_as_condition(['a', 'b', '+'])
    True
    >>> listcomp_as_condition('ab+')
    True
    >>> listcomp_as_condition('abc')
    False
    """
    if [1 for c in sequence if c in '+-*/<=>!%&|([^~,']:
        return True
    return False
