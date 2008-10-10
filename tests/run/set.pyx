__doc__ = u"""
>>> test_set_add()
set(['a', 1])
>>> test_set_clear()
set([])
>>> test_set_pop()
set([])
>>> test_set_discard()
set([233, '12'])
"""

def test_set_add():
    cdef set s1
    s1 = set([1])
    s1.add(1)
    s1.add('a')
    s1.add(1)
    return s1

def test_set_clear():
    cdef set s1
    s1 = set([1])
    s1.clear()
    return s1

def test_set_pop():
    cdef set s1
    s1 = set()
    s1.add('2')
    two = s1.pop()
    return s1

def test_set_discard():
    cdef set s1
    s1 = set()
    s1.add('12')
    s1.add(3)
    s1.add(233)
    s1.discard('3')
    s1.discard(3)
    return s1
    
