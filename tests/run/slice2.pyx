# mode: run
# tag: slicing

def test_full(seq):
    """
    >>> l = [1,2,3,4]
    >>> test_full(l)
    [1, 2, 3, 4]
    >>> l == test_full(l)
    True
    >>> l is test_full(l)
    False
    >>> try: test_full(42)
    ... except TypeError: pass
    """
    obj = seq[:]
    return obj

def test_start(seq, start):
    """
    >>> test_start([1,2,3,4], 2)
    [3, 4]
    >>> test_start([1,2,3,4], 3)
    [4]
    >>> test_start([1,2,3,4], 4)
    []
    >>> test_start([1,2,3,4], 8)
    []
    >>> test_start([1,2,3,4], -3)
    [2, 3, 4]
    >>> test_start([1,2,3,4], -4)
    [1, 2, 3, 4]
    >>> test_start([1,2,3,4], -8)
    [1, 2, 3, 4]
    >>> test_start([1,2,3,4], 0)
    [1, 2, 3, 4]
    >>> try: test_start(42, 2, 3)
    ... except TypeError: pass
    """
    obj = seq[start:]
    return obj

def test_stop(seq, stop):
    """
    >>> test_stop([1,2,3,4], 3)
    [1, 2, 3]
    >>> test_stop([1,2,3,4], -1)
    [1, 2, 3]
    >>> test_stop([1,2,3,4], -3)
    [1]
    >>> test_stop([1,2,3,4], -4)
    []
    >>> test_stop([1,2,3,4], -8)
    []
    >>> test_stop([1,2,3,4], 0)
    []
    >>> try: test_stop(42, 3)
    ... except TypeError: pass
    """
    obj = seq[:stop]
    return obj

def test_start_and_stop(seq, start, stop):
    """
    >>> l = [1,2,3,4]
    >>> test_start_and_stop(l, 2, 3)
    [3]
    >>> test_start_and_stop(l, -3, -1)
    [2, 3]
    >>> try: test_start_and_stop(42, 2, 3)
    ... except TypeError: pass
    """
    obj = seq[start:stop]
    return obj

class A(object):
    pass

def slice_of_temporary_smoketest():
    """
    >>> slice_of_temporary_smoketest()
    [3, 2]
    """
    x = A()
    x.a = [1, 2]
    x.a[:] = [3,2]
    return x.a
