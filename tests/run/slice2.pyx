# mode: run
# tag: list, slice, slicing

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
    >>> l = [1,2,3,4]
    >>> test_start(l, 2)
    [3, 4]
    >>> test_start(l, 3)
    [4]
    >>> test_start(l, 4)
    []
    >>> test_start(l, 8)
    []
    >>> test_start(l, -3)
    [2, 3, 4]
    >>> test_start(l, -4)
    [1, 2, 3, 4]
    >>> test_start(l, -8)
    [1, 2, 3, 4]
    >>> test_start(l, 0)
    [1, 2, 3, 4]
    >>> test_start(l, None)
    [1, 2, 3, 4]
    >>> try: test_start(42, 2, 3)
    ... except TypeError: pass
    """
    obj = seq[start:]
    return obj

def test_stop(seq, stop):
    """
    >>> l = [1,2,3,4]
    >>> test_stop(l, 3)
    [1, 2, 3]
    >>> test_stop(l, -1)
    [1, 2, 3]
    >>> test_stop(l, -3)
    [1]
    >>> test_stop(l, -4)
    []
    >>> test_stop(l, -8)
    []
    >>> test_stop(l, 0)
    []
    >>> test_stop(l, None)
    [1, 2, 3, 4]
    >>> try: test_stop(42, 3)
    ... except TypeError: pass
    """
    obj = seq[:stop]
    return obj

def test_step(seq, step):
    """
    >>> l = [1,2,3,4]
    >>> test_step(l, -1)
    [4, 3, 2, 1]
    >>> test_step(l, 1)
    [1, 2, 3, 4]
    >>> test_step(l, 2)
    [1, 3]
    >>> test_step(l, 3)
    [1, 4]
    >>> test_step(l, -3)
    [4, 1]
    >>> test_step(l, None)
    [1, 2, 3, 4]
    >>> try: test_step(l, 0)
    ... except ValueError: pass
    ...
    >>> try: test_step(42, 0)
    ... except TypeError: pass
    ...
    """
    obj = seq[::step]
    return obj

def test_start_and_stop(seq, start, stop):
    """
    >>> l = [1,2,3,4]
    >>> test_start_and_stop(l, 2, 3)
    [3]
    >>> test_start_and_stop(l, -3, -1)
    [2, 3]
    >>> test_start_and_stop(l, None, None)
    [1, 2, 3, 4]
    >>> try: test_start_and_stop(42, 2, 3)
    ... except TypeError: pass
    """
    obj = seq[start:stop]
    return obj

def test_start_stop_and_step(seq, start, stop, step):
    """
    >>> l = [1,2,3,4,5]
    >>> test_start_stop_and_step(l, 0, 5, 1)
    [1, 2, 3, 4, 5]
    >>> test_start_stop_and_step(l, 5, -1, -1)
    []
    >>> test_start_stop_and_step(l, 5, None, -1)
    [5, 4, 3, 2, 1]
    >>> test_start_stop_and_step(l, 2, 5, 2)
    [3, 5]
    >>> test_start_stop_and_step(l, -100, 100, 1)
    [1, 2, 3, 4, 5]
    >>> test_start_stop_and_step(l, None, None, None)
    [1, 2, 3, 4, 5]
    >>> try: test_start_stop_and_step(l, None, None, 0)
    ... except ValueError: pass
    ... 
    >>> try: test_start_stop_and_step(42, 1, 2, 3)
    ... except TypeError: pass
    """
    obj = seq[start:stop:step]
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
