# mode: run
# tag: list, tuple, slice, slicing

cimport cython


@cython.test_fail_if_path_exists("//CondExprNode")
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

@cython.test_fail_if_path_exists("//CondExprNode")
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


@cython.test_fail_if_path_exists("//CondExprNode")
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


@cython.test_fail_if_path_exists("//CondExprNode")
def slice_list_copy(list l):
    """
    >>> slice_list_copy([])
    []
    >>> slice_list_copy([1,2,3])
    [1, 2, 3]
    """
    return l[:]


@cython.test_fail_if_path_exists("//CondExprNode")
def slice_tuple_copy(tuple l):
    """
    >>> slice_tuple_copy(())
    ()
    >>> slice_tuple_copy((1,2,3))
    (1, 2, 3)
    """
    return l[:]


@cython.test_fail_if_path_exists("//CondExprNode")
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


@cython.test_fail_if_path_exists("//CondExprNode")
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


@cython.test_fail_if_path_exists("//CondExprNode")
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


@cython.test_fail_if_path_exists("//CondExprNode")
def slice_list_assign_list(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_list(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = [1,2,3,4]
    return l


@cython.test_fail_if_path_exists("//CondExprNode")
def slice_list_assign_tuple(list l):
    """
    >>> l = [1,2,3,4]
    >>> l2 = l[:]
    >>> slice_list_assign_tuple(l2)
    [1, 1, 2, 3, 4, 4]
    """
    l[1:3] = (1,2,3,4)
    return l


@cython.test_fail_if_path_exists("//CondExprNode")
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


# Readers will find the common boilerplate in the tests below:
#     >>> l = [1,2,3,4,5]
#     >>> t = tuple(l)
#     >>> b = ''.join(map(str, l)).encode('ASCII')
#     >>> u = b.decode('ASCII')
#     >>> o = (l, t, b, u)
#     >>> n = ('list', 'tuple', 'bytes', 'unicode')
#     >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
#     >>> r = lambda i, *a: '%s[%s] -> %s' % (n[i], ':'.join(map(repr, a)), FUNCTION_NAME(o[i], *a))
# Originally, this was planned to be a basic iteration over
#   the various object types contained within the sliceable fused
#   type, but Python2 -> Python3 semantics changed the class names
#   and string representations used for raw bytes and unicode.
# As a result, we dynamically adjust the printed string output
#   for each test in order to ensure consistent results when running
#   both Python2 and Python3.

ctypedef fused sliceable:
    list
    tuple
    bytes
    unicode


@cython.test_assert_path_exists("//SliceIndexNode//CondExprNode")
def slice_fused_type_start(sliceable seq, start):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s: '%s[%r:] -> %s' % (n[i], s, p(slice_fused_type_start(o[i], s)))
    >>> for i in range(len(o)):
    ...     for s in (0, len(l) - 1, len(l), -1, -len(l), None):
    ...         print(r(i, s))
    ... 
    list[0:] -> [1, 2, 3, 4, 5]
    list[4:] -> [5]
    list[5:] -> []
    list[-1:] -> [5]
    list[-5:] -> [1, 2, 3, 4, 5]
    list[None:] -> [1, 2, 3, 4, 5]
    tuple[0:] -> (1, 2, 3, 4, 5)
    tuple[4:] -> (5,)
    tuple[5:] -> ()
    tuple[-1:] -> (5,)
    tuple[-5:] -> (1, 2, 3, 4, 5)
    tuple[None:] -> (1, 2, 3, 4, 5)
    bytes[0:] -> 12345
    bytes[4:] -> 5
    bytes[5:] -> 
    bytes[-1:] -> 5
    bytes[-5:] -> 12345
    bytes[None:] -> 12345
    unicode[0:] -> 12345
    unicode[4:] -> 5
    unicode[5:] -> 
    unicode[-1:] -> 5
    unicode[-5:] -> 12345
    unicode[None:] -> 12345
    """
    obj = seq[start:]
    return obj


@cython.test_assert_path_exists("//SliceIndexNode//CondExprNode")
def slice_fused_type_stop(sliceable seq, stop):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s: '%s[:%r] -> %s' % (n[i], s, p(slice_fused_type_stop(o[i], s)))
    >>> for i in range(len(o)):
    ...     for s in (0, len(l) - 1, len(l), -1, -len(l), None):
    ...         print(r(i, s))
    ... 
    list[:0] -> []
    list[:4] -> [1, 2, 3, 4]
    list[:5] -> [1, 2, 3, 4, 5]
    list[:-1] -> [1, 2, 3, 4]
    list[:-5] -> []
    list[:None] -> [1, 2, 3, 4, 5]
    tuple[:0] -> ()
    tuple[:4] -> (1, 2, 3, 4)
    tuple[:5] -> (1, 2, 3, 4, 5)
    tuple[:-1] -> (1, 2, 3, 4)
    tuple[:-5] -> ()
    tuple[:None] -> (1, 2, 3, 4, 5)
    bytes[:0] -> 
    bytes[:4] -> 1234
    bytes[:5] -> 12345
    bytes[:-1] -> 1234
    bytes[:-5] -> 
    bytes[:None] -> 12345
    unicode[:0] -> 
    unicode[:4] -> 1234
    unicode[:5] -> 12345
    unicode[:-1] -> 1234
    unicode[:-5] -> 
    unicode[:None] -> 12345
    """
    obj = seq[:stop]
    return obj


@cython.test_assert_path_exists("//SliceIndexNode//CondExprNode")
def slice_fused_type_start_and_stop(sliceable seq, start, stop):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, t, s: '%s[%r:%r] -> %s' % (n[i], t, s, p(slice_fused_type_start_and_stop(o[i], t, s)))
    >>> for i in range(len(o)): 
    ...     for start, stop in ((0, len(l)), (0, None), (None, len(l)),
    ...                         (-len(l), 0), (1, 0), (0, 1)):
    ...         print(r(i, start, stop))
    ... 
    list[0:5] -> [1, 2, 3, 4, 5]
    list[0:None] -> [1, 2, 3, 4, 5]
    list[None:5] -> [1, 2, 3, 4, 5]
    list[-5:0] -> []
    list[1:0] -> []
    list[0:1] -> [1]
    tuple[0:5] -> (1, 2, 3, 4, 5)
    tuple[0:None] -> (1, 2, 3, 4, 5)
    tuple[None:5] -> (1, 2, 3, 4, 5)
    tuple[-5:0] -> ()
    tuple[1:0] -> ()
    tuple[0:1] -> (1,)
    bytes[0:5] -> 12345
    bytes[0:None] -> 12345
    bytes[None:5] -> 12345
    bytes[-5:0] -> 
    bytes[1:0] -> 
    bytes[0:1] -> 1
    unicode[0:5] -> 12345
    unicode[0:None] -> 12345
    unicode[None:5] -> 12345
    unicode[-5:0] -> 
    unicode[1:0] -> 
    unicode[0:1] -> 1
    """
    obj = seq[start:stop]
    return obj


def slice_fused_type_step(sliceable seq, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s: '%s[::%r] -> %s' % (n[i], s, p(slice_fused_type_step(o[i], s)))
    >>> for i in range(len(o)):
    ...     for s in (1, -1, 2, -3, 5, -5, None):
    ...         print(r(i, s))
    ... 
    list[::1] -> [1, 2, 3, 4, 5]
    list[::-1] -> [5, 4, 3, 2, 1]
    list[::2] -> [1, 3, 5]
    list[::-3] -> [5, 2]
    list[::5] -> [1]
    list[::-5] -> [5]
    list[::None] -> [1, 2, 3, 4, 5]
    tuple[::1] -> (1, 2, 3, 4, 5)
    tuple[::-1] -> (5, 4, 3, 2, 1)
    tuple[::2] -> (1, 3, 5)
    tuple[::-3] -> (5, 2)
    tuple[::5] -> (1,)
    tuple[::-5] -> (5,)
    tuple[::None] -> (1, 2, 3, 4, 5)
    bytes[::1] -> 12345
    bytes[::-1] -> 54321
    bytes[::2] -> 135
    bytes[::-3] -> 52
    bytes[::5] -> 1
    bytes[::-5] -> 5
    bytes[::None] -> 12345
    unicode[::1] -> 12345
    unicode[::-1] -> 54321
    unicode[::2] -> 135
    unicode[::-3] -> 52
    unicode[::5] -> 1
    unicode[::-5] -> 5
    unicode[::None] -> 12345
    >>> for v in o:
    ...     try: slice_fused_type_step(v, 0)
    ...     except ValueError: pass
    ...     try: slice_fused_type_step(v, v)
    ...     except TypeError: pass
    """
    obj = seq[::step]
    return obj


def slice_fused_type_start_and_step(sliceable seq, start, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s, t: '%s[%r::%r] -> %s' % (n[i], s, t, p(slice_fused_type_start_and_step(o[i], s, t)))
    >>> for i in range(len(o)):
    ...     for start, step in ((0, 1), (0, -1), (1, 1), (1, -1),
    ...                         (None, 1), (None, -1), (None, None),
    ...                         (1, 2), (len(l), -2), (len(l), len(l))):
    ...         print(r(i, start, step))
    ... 
    list[0::1] -> [1, 2, 3, 4, 5]
    list[0::-1] -> [1]
    list[1::1] -> [2, 3, 4, 5]
    list[1::-1] -> [2, 1]
    list[None::1] -> [1, 2, 3, 4, 5]
    list[None::-1] -> [5, 4, 3, 2, 1]
    list[None::None] -> [1, 2, 3, 4, 5]
    list[1::2] -> [2, 4]
    list[5::-2] -> [5, 3, 1]
    list[5::5] -> []
    tuple[0::1] -> (1, 2, 3, 4, 5)
    tuple[0::-1] -> (1,)
    tuple[1::1] -> (2, 3, 4, 5)
    tuple[1::-1] -> (2, 1)
    tuple[None::1] -> (1, 2, 3, 4, 5)
    tuple[None::-1] -> (5, 4, 3, 2, 1)
    tuple[None::None] -> (1, 2, 3, 4, 5)
    tuple[1::2] -> (2, 4)
    tuple[5::-2] -> (5, 3, 1)
    tuple[5::5] -> ()
    bytes[0::1] -> 12345
    bytes[0::-1] -> 1
    bytes[1::1] -> 2345
    bytes[1::-1] -> 21
    bytes[None::1] -> 12345
    bytes[None::-1] -> 54321
    bytes[None::None] -> 12345
    bytes[1::2] -> 24
    bytes[5::-2] -> 531
    bytes[5::5] -> 
    unicode[0::1] -> 12345
    unicode[0::-1] -> 1
    unicode[1::1] -> 2345
    unicode[1::-1] -> 21
    unicode[None::1] -> 12345
    unicode[None::-1] -> 54321
    unicode[None::None] -> 12345
    unicode[1::2] -> 24
    unicode[5::-2] -> 531
    unicode[5::5] -> 
    >>> for o in (l, t, b):
    ...     try: slice_fused_type_start_and_step(o, 0, 0)
    ...     except ValueError: pass
    """
    obj = seq[start::step]
    return obj


def slice_fused_type_stop_and_step(sliceable seq, stop, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s, t: '%s[:%r:%r] -> %s' % (n[i], s, t, p(slice_fused_type_stop_and_step(o[i], s, t)))
    >>> for i in range(len(o)):
    ...     for stop, step in ((len(l), 1), (len(l), None), (None, 1),
    ...                        (len(l), -1), (len(l) - 1, 2), (len(l), -2),
    ...                        (len(l), len(l))):
    ...         print(r(i, stop, step))
    ... 
    list[:5:1] -> [1, 2, 3, 4, 5]
    list[:5:None] -> [1, 2, 3, 4, 5]
    list[:None:1] -> [1, 2, 3, 4, 5]
    list[:5:-1] -> []
    list[:4:2] -> [1, 3]
    list[:5:-2] -> []
    list[:5:5] -> [1]
    tuple[:5:1] -> (1, 2, 3, 4, 5)
    tuple[:5:None] -> (1, 2, 3, 4, 5)
    tuple[:None:1] -> (1, 2, 3, 4, 5)
    tuple[:5:-1] -> ()
    tuple[:4:2] -> (1, 3)
    tuple[:5:-2] -> ()
    tuple[:5:5] -> (1,)
    bytes[:5:1] -> 12345
    bytes[:5:None] -> 12345
    bytes[:None:1] -> 12345
    bytes[:5:-1] -> 
    bytes[:4:2] -> 13
    bytes[:5:-2] -> 
    bytes[:5:5] -> 1
    unicode[:5:1] -> 12345
    unicode[:5:None] -> 12345
    unicode[:None:1] -> 12345
    unicode[:5:-1] -> 
    unicode[:4:2] -> 13
    unicode[:5:-2] -> 
    unicode[:5:5] -> 1
    >>> for v in o:
    ...     try: slice_fused_type_stop_and_step(v, len(l), 0)
    ...     except ValueError: pass
    ...     try: slice_fused_type_stop_and_step(v, len(l), v)
    ...     except TypeError: pass
    """
    obj = seq[:stop:step]
    return obj


def slice_fused_type_all(sliceable seq, start, stop, step):
    """
    >>> l = [1,2,3,4,5]
    >>> t = tuple(l)
    >>> b = ''.join(map(str, l)).encode('ASCII')
    >>> u = b.decode('ASCII')
    >>> o = (l, t, b, u)
    >>> n = ('list', 'tuple', 'bytes', 'unicode')
    >>> p = lambda o: o.decode() if isinstance(o, type(b)) else str(o)
    >>> r = lambda i, s, t, e: '%s[%r:%r:%r] -> %s' % (n[i], s, t, e, p(slice_fused_type_all(o[i], s, t, e)))
    >>> for i in range(len(o)):
    ...     for args in ((0, len(l), 1), (len(l), 0, -1), (None, len(l), 1),
    ...                  (len(l), None, -1), (-len(l), len(l), None), (None, None, None),
    ...                  (1, 3, 2), (len(l), 1, -3), (len(l), 0, 1)):
    ...         print(r(i, *args))
    ... 
    list[0:5:1] -> [1, 2, 3, 4, 5]
    list[5:0:-1] -> [5, 4, 3, 2]
    list[None:5:1] -> [1, 2, 3, 4, 5]
    list[5:None:-1] -> [5, 4, 3, 2, 1]
    list[-5:5:None] -> [1, 2, 3, 4, 5]
    list[None:None:None] -> [1, 2, 3, 4, 5]
    list[1:3:2] -> [2]
    list[5:1:-3] -> [5]
    list[5:0:1] -> []
    tuple[0:5:1] -> (1, 2, 3, 4, 5)
    tuple[5:0:-1] -> (5, 4, 3, 2)
    tuple[None:5:1] -> (1, 2, 3, 4, 5)
    tuple[5:None:-1] -> (5, 4, 3, 2, 1)
    tuple[-5:5:None] -> (1, 2, 3, 4, 5)
    tuple[None:None:None] -> (1, 2, 3, 4, 5)
    tuple[1:3:2] -> (2,)
    tuple[5:1:-3] -> (5,)
    tuple[5:0:1] -> ()
    bytes[0:5:1] -> 12345
    bytes[5:0:-1] -> 5432
    bytes[None:5:1] -> 12345
    bytes[5:None:-1] -> 54321
    bytes[-5:5:None] -> 12345
    bytes[None:None:None] -> 12345
    bytes[1:3:2] -> 2
    bytes[5:1:-3] -> 5
    bytes[5:0:1] -> 
    unicode[0:5:1] -> 12345
    unicode[5:0:-1] -> 5432
    unicode[None:5:1] -> 12345
    unicode[5:None:-1] -> 54321
    unicode[-5:5:None] -> 12345
    unicode[None:None:None] -> 12345
    unicode[1:3:2] -> 2
    unicode[5:1:-3] -> 5
    unicode[5:0:1] -> 
    >>> for v in o:
    ...     try: slice_fused_type_stop_and_step(v, len(l), 0)
    ...     except ValueError: pass
    ...     try: slice_fused_type_stop_and_step(v, len(l), v)
    ...     except TypeError: pass
    """
    obj = seq[start:stop:step]
    return obj
