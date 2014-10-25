
def from_int_array():
    """
    >>> from_int_array()
    [1, 2, 3]
    """
    cdef int[3] v
    v[0] = 1
    v[1] = 2
    v[2] = 3
    return v


cpdef tuple tuple_from_int_array():
    """
    >>> tuple_from_int_array()
    (1, 2, 3)
    """
    cdef int[3] v
    v[0] = 1
    v[1] = 2
    v[2] = 3
    assert isinstance(<tuple>v, tuple)
    return v


cdef extern from "stdint.h":
    ctypedef unsigned long uint32_t


def from_typedef_int_array():
    """
    >>> from_typedef_int_array()
    [1, 2, 3]
    """
    cdef uint32_t[3] v
    v[0] = 1
    v[1] = 2
    v[2] = 3
    return v


cpdef tuple tuple_from_typedef_int_array():
    """
    >>> tuple_from_typedef_int_array()
    (1, 2, 3)
    """
    cdef uint32_t[3] v
    v[0] = 1
    v[1] = 2
    v[2] = 3
    return v


ctypedef struct MyStructType:
    int x
    double y


cdef struct MyStruct:
    int x
    double y


def from_struct_array():
    """
    >>> a, b = from_struct_array()
    >>> a['x'], a['y']
    (1, 2.0)
    >>> b['x'], b['y']
    (3, 4.0)
    """
    cdef MyStructType[2] v
    cdef MyStruct[2] w
    v[0] = MyStructType(1, 2)
    v[1] = MyStructType(3, 4)
    assert isinstance(<tuple>v, tuple)
    assert isinstance(v, list)

    w[0] = MyStruct(1, 2)
    w[1] = MyStruct(3, 4)
    assert (<object>w) == v
    assert w == (<object>v)

    return v


def to_int_array(x):
    """
    >>> to_int_array([1, 2, 3])
    (1, 2, 3)
    >>> to_int_array([1, 2])
    Traceback (most recent call last):
    IndexError: not enough values found during array assignment, expected 3, got 2
    >>> to_int_array([1, 2, 3, 4])
    Traceback (most recent call last):
    IndexError: too many values found during array assignment, expected 3
    """
    cdef int[3] v
    v[:] = x[:3]
    assert v[0] == x[0]
    assert v[1] == x[1]
    assert v[2] == x[2]
    v[:3] = [0, 0, 0]
    assert v[0] == 0
    assert v[1] == 0
    assert v[2] == 0
    v[:] = x
    return v[0], v[1], v[2]


def iterable_to_int_array(x):
    """
    >>> iterable_to_int_array(iter([1, 2, 3]))
    (1, 2, 3)
    >>> iterable_to_int_array(iter([1, 2]))
    Traceback (most recent call last):
    IndexError: not enough values found during array assignment, expected 3, got 2
    >>> iterable_to_int_array(iter([1, 2, 3, 4]))
    Traceback (most recent call last):
    IndexError: too many values found during array assignment, expected 3
    """
    cdef int[3] v
    v[:] = x
    return v[0], v[1], v[2]


def to_struct_array(x):
    """
    >>> a, b = to_struct_array(({'x': 1, 'y': 2}, {'x': 3, 'y': 4}))
    >>> a['x'], a['y']
    (1, 2.0)
    >>> b['x'], b['y']
    (3, 4.0)
    """
    cdef MyStructType[2] v
    v[:] = x

    cdef MyStruct[2] w
    w[:] = x

    assert w[0].x == v[0].x
    assert w[0].y == v[0].y
    assert w[1].x == v[1].x
    assert w[1].y == v[1].y

    return v[0], w[1]
