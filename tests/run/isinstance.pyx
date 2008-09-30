__doc__ = u"""
>>> test_all()
True
"""
cdef class A:
    pass

def test_all():
    # Optimized tests.
    assert isinstance(type('a',(),{}), type)
    assert isinstance(bool(), bool)
    assert isinstance(int(), int)
    assert isinstance(long(), long)
    assert isinstance(float(), float)
    assert isinstance(complex(), complex)
    assert isinstance(bytes(), bytes)
    assert isinstance(str(), str)
    assert isinstance(unicode(), unicode)
    assert isinstance(tuple(), tuple)
    assert isinstance(list(), list)
    assert isinstance(dict(), dict)
#    if py_ver > (2, 3):
#        assert isinstance(set(), set)
    assert isinstance(slice(0), slice)
    assert isinstance(A, type)
    assert isinstance(A(), A)
    assert not isinstance("foo", int)
    
    # Non-optimized
    foo = A
    assert isinstance(A(), foo)
    assert isinstance(0, (int, long))
    assert not isinstance("xyz", (int, long))
    return True
    
