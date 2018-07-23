# mode: run
# tag: list, tuple, slice, slicing

def slice_list(list l, int start, int stop):
    """
    >>> slice_list([1,2,3,4], 1, 3)
    [2, 3]
    >>> slice_list([1,2,3,4], 1, 7)
    [2, 3, 4]
    >>> slice_list([], 1, 3)
    []
    >>> slice_list([1], 1, 3)
    []
    >>> slice_list([1,2,3,4], -3, -1)
    [2, 3]
    >>> slice_list([1,2,3,4], -10, -1)
    [1, 2, 3]
    >>> slice_list([], -3, -1)
    []
    >>> slice_list([1], -3, -1)
    []
    """
    return l[start:stop]

def slice_list_start(list l, int start):
    """
    >>> slice_list_start([1,2,3,4], 1)
    [2, 3, 4]
    >>> slice_list_start([], 1)
    []
    >>> slice_list_start([1], 1)
    []
    >>> slice_list_start([1], 2)
    []
    >>> slice_list_start([1,2,3,4], -3)
    [2, 3, 4]
    >>> slice_list_start([1,2,3,4], -10)
    [1, 2, 3, 4]
    >>> slice_list_start([], -3)
    []
    >>> slice_list_start([1], -3)
    [1]
    """
    return l[start:]


def slice_list_stop(list l, int stop):
    """
    >>> slice_list_stop([1,2,3,4], 3)
    [1, 2, 3]
    >>> slice_list_stop([1,2,3,4], 7)
    [1, 2, 3, 4]
    >>> slice_list_stop([], 3)
    []
    >>> slice_list_stop([1], 3)
    [1]
    >>> slice_list_stop([1,2,3,4], -3)
    [1]
    >>> slice_list_stop([1,2,3,4], -10)
    []
    >>> slice_list_stop([], -1)
    []
    >>> slice_list_stop([1], -1)
    []
    >>> slice_list_stop([1, 2], -3)
    []
    """
    return l[:stop]


def slice_list_copy(list l):
    """
    >>> slice_list_copy([])
    []
    >>> slice_list_copy([1,2,3])
    [1, 2, 3]
    """
    return l[:]


def slice_tuple_copy(tuple l):
    """
    >>> slice_tuple_copy(())
    ()
    >>> slice_tuple_copy((1,2,3))
    (1, 2, 3)
    """
    return l[:]


def slice_tuple(tuple t, int start, int stop):
    """
    >>> slice_tuple((1,2,3,4), 1, 3)
    (2, 3)
    >>> slice_tuple((1,2,3,4), 1, 7)
    (2, 3, 4)
    >>> slice_tuple((), 1, 3)
    ()
    >>> slice_tuple((1,), 1, 3)
    ()
    >>> slice_tuple((1,2,3,4), -3, -1)
    (2, 3)
    >>> slice_tuple((1,2,3,4), -10, -1)
    (1, 2, 3)
    >>> slice_tuple((), -3, -1)
    ()
    >>> slice_tuple((1,), -3, -1)
    ()
    """
    return t[start:stop]


def slice_tuple_start(tuple t, int start):
    """
    >>> slice_tuple_start((1,2,3,4), 1)
    (2, 3, 4)
    >>> slice_tuple_start((), 1)
    ()
    >>> slice_tuple_start((1,), 1)
    ()
    >>> slice_tuple_start((1,2,3,4), -3)
    (2, 3, 4)
    >>> slice_tuple_start((1,2,3,4), -10)
    (1, 2, 3, 4)
    >>> slice_tuple_start((), -3)
    ()
    >>> slice_tuple_start((1,), -3)
    (1,)
    """
    return t[start:]

def slice_tuple_stop(tuple t, int stop):
    """
    >>> slice_tuple_stop((1,2,3,4), 3)
    (1, 2, 3)
    >>> slice_tuple_stop((1,2,3,4), 7)
    (1, 2, 3, 4)
    >>> slice_tuple_stop((), 3)
    ()
    >>> slice_tuple_stop((1,), 3)
    (1,)
    >>> slice_tuple_stop((1,2,3,4), -1)
    (1, 2, 3)
    >>> slice_tuple_stop((), -1)
    ()
    """
    return t[:stop]


def slice_list_assign_list(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_list(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = [1,2,3,4]
    return l


def slice_list_assign_tuple(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_tuple(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = (1,2,3,4)
    return l


def slice_list_assign(list l, value):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign(l2, (1,2,3,4))
    [1, 1, 2, 3, 4, 4]
    >>> l2 = l[:]
    >>> slice_list_assign(l2, dict(zip(l,l)))
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = value
    return l


def slice_charp(py_string_arg):
    """
    >>> print("%s" % slice_charp('abcdefg'))
    bc
    """
    cdef bytes py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    return s[1:3].decode(u'ASCII')


def slice_charp_repeat(py_string_arg):
    """
    >>> print("%s" % slice_charp_repeat('abcdefg'))
    cd
    """
    cdef bytes py_string = py_string_arg.encode(u'ASCII')
    cdef char* s = py_string
    cdef bytes slice_val = s[1:6]
    s = slice_val
    return s[1:3].decode(u'ASCII')

ctypedef fused slicable:
    list
    tuple
    bytes
    unicode

def slice_fused_type_start(slicable seq, start):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for s in (0, 4, 5, -5):
    ...         print(p(slice_fused_type_start(o, s)))
    ... 
    [1, 2, 3, 4, 5]
    [5]
    []
    [1, 2, 3, 4, 5]
    (1, 2, 3, 4, 5)
    (5,)
    ()
    (1, 2, 3, 4, 5)
    12345
    5
    <BLANKLINE>
    12345
    12345
    5
    <BLANKLINE>
    12345
    """
    obj = seq[start:]
    return obj

def slice_fused_type_stop(slicable seq, stop):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for s in (0, 4, 5, -5, None):
    ...         print(p(slice_fused_type_stop(o, s)))
    ... 
    []
    [1, 2, 3, 4]
    [1, 2, 3, 4, 5]
    []
    [1, 2, 3, 4, 5]
    ()
    (1, 2, 3, 4)
    (1, 2, 3, 4, 5)
    ()
    (1, 2, 3, 4, 5)
    <BLANKLINE>
    1234
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    1234
    12345
    <BLANKLINE>
    12345
    """
    obj = seq[:stop]
    return obj

def slice_fused_type_start_and_stop(slicable seq, start, stop):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for start in (0, 1, 4, 5, -5, None):
    ...         for stop in (0, 4, 5, 10, -10, None):
    ...             print(p(slice_fused_type_start_and_stop(o, start, stop)))
    ... 
    []
    [1, 2, 3, 4]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    []
    [1, 2, 3, 4, 5]
    []
    [2, 3, 4]
    [2, 3, 4, 5]
    [2, 3, 4, 5]
    []
    [2, 3, 4, 5]
    []
    []
    [5]
    [5]
    []
    [5]
    []
    []
    []
    []
    []
    []
    []
    [1, 2, 3, 4]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    []
    [1, 2, 3, 4, 5]
    []
    [1, 2, 3, 4]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    []
    [1, 2, 3, 4, 5]
    ()
    (1, 2, 3, 4)
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    ()
    (1, 2, 3, 4, 5)
    ()
    (2, 3, 4)
    (2, 3, 4, 5)
    (2, 3, 4, 5)
    ()
    (2, 3, 4, 5)
    ()
    ()
    (5,)
    (5,)
    ()
    (5,)
    ()
    ()
    ()
    ()
    ()
    ()
    ()
    (1, 2, 3, 4)
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    ()
    (1, 2, 3, 4, 5)
    ()
    (1, 2, 3, 4)
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    ()
    (1, 2, 3, 4, 5)
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    234
    2345
    2345
    <BLANKLINE>
    2345
    <BLANKLINE>
    <BLANKLINE>
    5
    5
    <BLANKLINE>
    5
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    234
    2345
    2345
    <BLANKLINE>
    2345
    <BLANKLINE>
    <BLANKLINE>
    5
    5
    <BLANKLINE>
    5
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    <BLANKLINE>
    1234
    12345
    12345
    <BLANKLINE>
    12345
    """
    obj = seq[start:stop]
    return obj

def slice_fused_type_step(slicable seq, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for s in (1, -1, 2, -3, 10, -10, None):
    ...         print(p(slice_fused_type_step(o, s)))
    ... 
    [1, 2, 3, 4, 5]
    [5, 4, 3, 2, 1]
    [1, 3, 5]
    [5, 2]
    [1]
    [5]
    [1, 2, 3, 4, 5]
    (1, 2, 3, 4, 5)
    (5, 4, 3, 2, 1)
    (1, 3, 5)
    (5, 2)
    (1,)
    (5,)
    (1, 2, 3, 4, 5)
    12345
    54321
    135
    52
    1
    5
    12345
    12345
    54321
    135
    52
    1
    5
    12345
    >>> for o in (l, t, b):
    ...     try: slice_fused_type_step(o, 0)
    ...     except ValueError: pass
    """
    obj = seq[::step]
    return obj

def slice_fused_type_start_and_step(slicable seq, start, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for start in (0, 2, 5, -5, None):
    ...         for step in (1, -1, 2, -3, None):
    ...             print(p(slice_fused_type_start_and_step(o, start, step)))
    ... 
    [1, 2, 3, 4, 5]
    [1]
    [1, 3, 5]
    [1]
    [1, 2, 3, 4, 5]
    [3, 4, 5]
    [3, 2, 1]
    [3, 5]
    [3]
    [3, 4, 5]
    []
    [5, 4, 3, 2, 1]
    []
    [5, 2]
    []
    [1, 2, 3, 4, 5]
    [1]
    [1, 3, 5]
    [1]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    [5, 4, 3, 2, 1]
    [1, 3, 5]
    [5, 2]
    [1, 2, 3, 4, 5]
    (1, 2, 3, 4, 5)
    (1,)
    (1, 3, 5)
    (1,)
    (1, 2, 3, 4, 5)
    (3, 4, 5)
    (3, 2, 1)
    (3, 5)
    (3,)
    (3, 4, 5)
    ()
    (5, 4, 3, 2, 1)
    ()
    (5, 2)
    ()
    (1, 2, 3, 4, 5)
    (1,)
    (1, 3, 5)
    (1,)
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    (5, 4, 3, 2, 1)
    (1, 3, 5)
    (5, 2)
    (1, 2, 3, 4, 5)
    12345
    1
    135
    1
    12345
    345
    321
    35
    3
    345
    <BLANKLINE>
    54321
    <BLANKLINE>
    52
    <BLANKLINE>
    12345
    1
    135
    1
    12345
    12345
    54321
    135
    52
    12345
    12345
    1
    135
    1
    12345
    345
    321
    35
    3
    345
    <BLANKLINE>
    54321
    <BLANKLINE>
    52
    <BLANKLINE>
    12345
    1
    135
    1
    12345
    12345
    54321
    135
    52
    12345
    >>> for o in (l, t, b):
    ...     try: slice_fused_type_start_and_step(o, 0, 0)
    ...     except ValueError: pass
    """
    obj = seq[start::step]
    return obj

def slice_fused_type_stop_and_step(slicable seq, stop, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for stop in (5, 10, 3, -10, None):
    ...         for step in (1, -1, 2, -3, None):
    ...             print(p(slice_fused_type_stop_and_step(o, stop, step)))
    ... 
    [1, 2, 3, 4, 5]
    []
    [1, 3, 5]
    []
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    []
    [1, 3, 5]
    []
    [1, 2, 3, 4, 5]
    [1, 2, 3]
    [5]
    [1, 3]
    [5]
    [1, 2, 3]
    []
    [5, 4, 3, 2, 1]
    []
    [5, 2]
    []
    [1, 2, 3, 4, 5]
    [5, 4, 3, 2, 1]
    [1, 3, 5]
    [5, 2]
    [1, 2, 3, 4, 5]
    (1, 2, 3, 4, 5)
    ()
    (1, 3, 5)
    ()
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    ()
    (1, 3, 5)
    ()
    (1, 2, 3, 4, 5)
    (1, 2, 3)
    (5,)
    (1, 3)
    (5,)
    (1, 2, 3)
    ()
    (5, 4, 3, 2, 1)
    ()
    (5, 2)
    ()
    (1, 2, 3, 4, 5)
    (5, 4, 3, 2, 1)
    (1, 3, 5)
    (5, 2)
    (1, 2, 3, 4, 5)
    12345
    <BLANKLINE>
    135
    <BLANKLINE>
    12345
    12345
    <BLANKLINE>
    135
    <BLANKLINE>
    12345
    123
    5
    13
    5
    123
    <BLANKLINE>
    54321
    <BLANKLINE>
    52
    <BLANKLINE>
    12345
    54321
    135
    52
    12345
    12345
    <BLANKLINE>
    135
    <BLANKLINE>
    12345
    12345
    <BLANKLINE>
    135
    <BLANKLINE>
    12345
    123
    5
    13
    5
    123
    <BLANKLINE>
    54321
    <BLANKLINE>
    52
    <BLANKLINE>
    12345
    54321
    135
    52
    12345
    >>> for o in (l, t, b):
    ...     try: slice_fused_type_stop_and_step(o, 5, 0)
    ...     except ValueError: pass
    """
    obj = seq[:stop:step]
    return obj

def slice_fused_type_all(slicable seq, start, stop, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> for o in (l, t, b, u):
    ...     for args in ((0, 5, 1), (5, 0, -1), (None, 5, 1), (5, None, -1),
    ...                  (-100, 100, None), (None, None, None), (1, 3, 2), (5, 1, -3)):
    ...         print(p(slice_fused_type_all(o, *args)))
    ... 
    [1, 2, 3, 4, 5]
    [5, 4, 3, 2]
    [1, 2, 3, 4, 5]
    [5, 4, 3, 2, 1]
    [1, 2, 3, 4, 5]
    [1, 2, 3, 4, 5]
    [2]
    [5]
    (1, 2, 3, 4, 5)
    (5, 4, 3, 2)
    (1, 2, 3, 4, 5)
    (5, 4, 3, 2, 1)
    (1, 2, 3, 4, 5)
    (1, 2, 3, 4, 5)
    (2,)
    (5,)
    12345
    5432
    12345
    54321
    12345
    12345
    2
    5
    12345
    5432
    12345
    54321
    12345
    12345
    2
    5
    """
    obj = seq[start:stop:step]
    return obj
