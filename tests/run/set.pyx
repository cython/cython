
# Py2.3 doesn't have the 'set' builtin type, but Cython does :)
_set = set

cimport cython

def cython_set():
    """
    >>> cython_set() is _set
    True
    """
    assert set is cython.set
    return cython.set

def cython_set_override():
    """
    >>> cython_set_override() is _set
    True
    """
    set = 1
    return cython.set

def test_set_literal():
    """
    >>> type(test_set_literal()) is _set
    True
    >>> sorted(test_set_literal())
    ['a', 'b', 1]
    """
    cdef set s1 = {1,'a',1,'b','a'}
    return s1

def test_set_add():
    """
    >>> type(test_set_add()) is _set
    True
    >>> sorted(test_set_add())
    ['a', 1]
    """
    cdef set s1
    s1 = set([1])
    s1.add(1)
    s1.add('a')
    s1.add(1)
    return s1

def test_set_clear():
    """
    >>> type(test_set_clear()) is _set
    True
    >>> list(test_set_clear())
    []
    """
    cdef set s1
    s1 = set([1])
    s1.clear()
    return s1

def test_set_clear_None():
    """
    >>> test_set_clear_None()
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'clear'
    """
    cdef set s1 = None
    s1.clear()

def test_set_list_comp():
    """
    >>> type(test_set_list_comp()) is _set
    True
    >>> sorted(test_set_list_comp())
    [0, 1, 2]
    """
    cdef set s1
    s1 = set([i%3 for i in range(5)])
    return s1

def test_set_pop():
    """
    >>> type(test_set_pop()) is _set
    True
    >>> list(test_set_pop())
    []
    """
    cdef set s1
    s1 = set()
    s1.add('2')
    two = s1.pop()
    return s1

@cython.test_fail_if_path_exists("//SimpleCallNode//NameNode")
def test_object_pop(s):
    """
    >>> s = _set([2])
    >>> test_object_pop(s)
    2
    >>> list(s)
    []
    """
    return s.pop()

def test_set_discard():
    """
    >>> type(test_set_discard()) is _set
    True
    >>> sorted(test_set_discard())
    ['12', 233]
    """
    cdef set s1
    s1 = set()
    s1.add('12')
    s1.add(3)
    s1.add(233)
    s1.discard('3')
    s1.discard(3)
    return s1

def test_set_sideeffect_unhashable_failure():
    """
    >>> test_set_sideeffect_unhashable_failure()
    [2, 4, 5]
    """
    L = []
    def sideeffect(x):
        L.append(x)
        return x
    def unhashable_value(x):
        L.append(x)
        return set()
    try:
        s = set([1,sideeffect(2),3,unhashable_value(4),sideeffect(5)])
    except TypeError: pass
    else: assert False, "expected exception not raised"
    return L

@cython.test_assert_path_exists("//SetNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_set_of_list():
    """
    >>> s = test_set_of_list()
    >>> isinstance(s, _set)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return set([1, 2, 3])

@cython.test_assert_path_exists("//SetNode")
@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_set_of_tuple():
    """
    >>> s = test_set_of_tuple()
    >>> isinstance(s, _set)
    True
    >>> sorted(s)
    [1, 2, 3]
    """
    return set((1, 2, 3))

def sorted(it):
    # Py3 can't compare strings to ints
    chars = []
    nums = []
    for item in it:
        if type(item) is int:
            nums.append(item)
        else:
            chars.append(item)
    nums.sort()
    chars.sort()
    return chars+nums
