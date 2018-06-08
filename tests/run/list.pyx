
cimport cython

def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1, 2, 3, 4, 5)
    []
    """
    obj1 = []
    return obj1

def g(obj1, obj2, obj3, obj4, obj5):
    """
    >>> g(1, 2, 3, 4, 5)
    [2]
    """
    obj1 = [obj2]
    return obj1

def h(obj1, obj2, obj3, obj4, obj5):
    """
    >>> h(1, 2, 3, 4, 5)
    [2, 3]
    """
    obj1 = [obj2, obj3]
    return obj1

def j(obj1, obj2, obj3, obj4, obj5):
    """
    >>> j(1, 2, 3, 4, 5)
    [2, 3, 4]
    """
    obj1 = [obj2, obj3, obj4]
    return obj1

def k(obj1, obj2, obj3, obj4, obj5):
    """
    >>> k(1, 2, 3, 4, 5)
    [17, 42, 88]
    """
    obj1 = [17, 42, 88]
    return obj1

@cython.test_fail_if_path_exists("//SimpleCallNode")
def test_list_call(ob):
    """
    >>> def f():
    ...     yield 1
    ...     yield 2
    ...
    >>> list(f())
    [1, 2]
    """
    return list(ob)

def test_list_sort():
    """
    >>> test_list_sort()
    [1, 2, 3, 4]
    """
    cdef list l1
    l1 = [2,3,1,4]
    l1.sort()
    return l1

def test_list_sort_reversed():
    cdef list l1
    l1 = [2,3,1,4]
    l1.sort(reversed=True)
    return l1

def test_list_reverse():
    """
    >>> test_list_reverse()
    [1, 2, 3, 4]
    """
    cdef list l1
    l1 = [4,3,2,1]
    l1.reverse()
    return l1


@cython.test_assert_path_exists(
    '//SimpleCallNode//AttributeNode[@entry.cname = "__Pyx_PyList_Append"]',
)
def test_list_append():
    """
    >>> test_list_append()
    [1, 2, 3, 4]
    """
    cdef list l1 = [1,2]
    l1.append(3)
    l1.append(4)
    return l1


@cython.test_assert_path_exists(
    '//SimpleCallNode//NameNode[@entry.cname = "__Pyx_PyList_Append"]',
)
def test_list_append_unbound():
    """
    >>> test_list_append_unbound()
    [1, 2, 3, 4]
    """
    cdef list l1 = [1,2]
    list.append(l1, 3)
    list.append(l1, 4)
    return l1


@cython.test_assert_path_exists(
    '//SimpleCallNode//NameNode[@entry.cname = "__Pyx_PyList_Append"]',
)
def test_list_append_unbound_assigned():
    """
    >>> test_list_append_unbound_assigned()
    [1, 2, 3, 4]
    """
    append = list.append
    cdef list l1 = [1,2]
    append(l1, 3)
    append(l1, 4)
    return l1


def test_list_append_insert():
    """
    >>> test_list_append_insert()
    ['first', 'second']
    """
    cdef list l = []
    l.append("second")
    l.insert(0, "first")
    return l

def test_list_pop():
    """
    >>> test_list_pop()
    (2, [1])
    """
    cdef list l1
    l1 = [1,2]
    two = l1.pop()
    return two, l1

def test_list_pop0():
    """
    >>> test_list_pop0()
    (1, [2])
    """
    cdef list l1
    l1 = [1,2]
    one = l1.pop(0)
    return one, l1

def test_list_pop_all():
    """
    >>> test_list_pop_all()
    True
    """
    cdef list l1
    l1 = [1,2]
    i = 0
    try:
        l1.pop()
        i = 1
        l1.pop(-1)
        i = 2
        l1.pop(0)
        i = 3
    except IndexError:
        return i == 2
    return False


@cython.test_assert_path_exists(
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_ListComp_Append"]',
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_PyList_Append"]',
)
def test_list_extend(seq=None, x=4):
    """
    >>> test_list_extend()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> test_list_extend([])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> test_list_extend([1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1]
    >>> test_list_extend([1, 2])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2]
    """
    cdef list l = [1,2,3]
    l.extend([])
    l.extend(())
    l.extend(set())  # not currently optimised (not worth the trouble)
    assert l == [1,2,3]
    assert len(l) == 3
    l.extend([4,x+1,6])
    l.extend([7,8,9,10,11,12,13,14,15,16])
    if seq is not None:
        l.extend(seq)
    return l


@cython.test_assert_path_exists(
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_ListComp_Append"]',
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_PyList_Append"]',
)
def test_list_extend_unbound(seq=None, x=4):
    """
    >>> test_list_extend_unbound()
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> test_list_extend_unbound([])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    >>> test_list_extend_unbound([1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1]
    >>> test_list_extend_unbound([1, 2])
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2]
    """
    cdef list l = [1,2,3]
    list.extend(l, [])
    list.extend(l, ())
    try:
        list.extend((), ())
    except TypeError:
        pass
    else:
        assert False, "TypeError not raised!"
    list.extend(l, set())  # not currently optimised (not worth the trouble)
    assert l == [1,2,3]
    assert len(l) == 3
    list.extend(l, [4,x+1,6])
    list.extend(l, [7,8,9,10,11,12,13,14,15,16])
    if seq is not None:
        list.extend(l, seq)
    return l

@cython.test_assert_path_exists(
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_ListComp_Append"]',
    '//PythonCapiCallNode//PythonCapiFunctionNode[@cname = "__Pyx_PyList_Append"]',
)
def test_list_extend_sideeffect(seq=None, exc=False):
    """
    >>> test_list_extend_sideeffect()
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], [4, 6, 7, 8])
    >>> test_list_extend_sideeffect([])
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], [4, 6, 7, 8])
    >>> test_list_extend_sideeffect([], exc=True)
    ([1, 2, 3, 10, 11, 12, 13, 14, 15, 16], [4, 7, 8])
    >>> test_list_extend_sideeffect([1])
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1], [4, 6, 7, 8])
    >>> test_list_extend_sideeffect([1], exc=True)
    ([1, 2, 3, 10, 11, 12, 13, 14, 15, 16, 1], [4, 7, 8])
    >>> test_list_extend_sideeffect([1, 2])
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 1, 2], [4, 6, 7, 8])
    """
    calls = []
    def sideeffect(value):
        calls.append(value)
        return value
    def fail(value):
        if exc:
            raise TypeError("HUHU")
        return value

    cdef list l = [1,2,3]
    l.extend([])
    l.extend(())
    l.extend(set())  # not currently optimised (not worth the trouble)
    assert l == [1,2,3]
    assert len(l) == 3

    # Must first build all items, then append them in order.
    # If building one value fails, none of them must be appended.
    try:
        l.extend([sideeffect(4), fail(5), sideeffect(6)])
    except TypeError as e:
        assert exc
        assert "HUHU" in str(e)
    else:
        assert not exc

    try:
        l.extend([sideeffect(7), sideeffect(8), fail(9)])
    except TypeError as e:
        assert exc
        assert "HUHU" in str(e)
    else:
        assert not exc

    l.extend([10,11,12,13,14,15,16])
    if seq is not None:
        l.extend(seq)
    return l, calls


def test_none_list_extend(list l):
    """
    >>> test_none_list_extend([])
    [1, 2, 3]
    >>> test_none_list_extend([0, 0, 0])
    [0, 0, 0, 1, 2, 3]
    >>> test_none_list_extend(None)
    123
    """
    try:
        l.extend([1,2,3])
    except AttributeError:
        return 123
    return l
