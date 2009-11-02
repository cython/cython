cdef class A:
    pass

import sys
IS_PY3 = sys.version_info[0] >= 3

def test_all():
    """
    >>> test_all()
    True
    """
    if IS_PY3:
        new_type = type(u'a',(),{})
    else:
        new_type = type('a',(),{})

    # Optimized tests.
    assert isinstance(new_type, type)
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
    assert not isinstance(u"foo", int)
    
    # Non-optimized
    cdef object foo = A
    assert isinstance(A(), foo)
    assert isinstance(0, (int, long))
    assert not isinstance(u"xyz", (int, long))
    return True
