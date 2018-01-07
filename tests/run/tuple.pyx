
cimport cython


def f(obj1, obj2, obj3, obj4, obj5):
    """
    >>> f(1,2,3,4,5)
    ()
    """
    obj1 = ()
    return obj1


def g(obj1, obj2, obj3, obj4, obj5):
    """
    >>> g(1,2,3,4,5)
    (2,)
    """
    obj1 = ()
    obj1 = (obj2,)
    return obj1


def h(obj1, obj2, obj3, obj4, obj5):
    """
    >>> h(1,2,3,4,5)
    (2, 3)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    return obj1


def j(obj1, obj2, obj3, obj4, obj5):
    """
    >>> j(1,2,3,4,5)
    (2, 3, 4)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    return obj1


def k(obj1, obj2, obj3, obj4, obj5):
    """
    >>> k(1,2,3,4,5)
    (2, 3, 4)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    return obj1


def l(obj1, obj2, obj3, obj4, obj5):
    """
    >>> l(1,2,3,4,5)
    (17, 42, 88)
    """
    obj1 = ()
    obj1 = (obj2,)
    obj1 = obj2, obj3
    obj1 = (obj2, obj3, obj4)
    obj1 = (obj2, obj3, obj4,)
    obj1 = 17, 42, 88
    return obj1


def tuple_none():
    """
    >>> tuple_none()   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...itera...
    """
    return tuple(None)


def tuple_none_list():
    """
    >>> tuple_none_list()   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...iterable...
    """
    cdef list none = None
    return tuple(none)


@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    '//PythonCapiCallNode'
)
def tuple_of_tuple_literal():
    """
    >>> tuple_of_tuple_literal()
    (1, 2, 3)
    """
    return tuple(tuple(tuple((1,2,3))))


@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    '//PythonCapiCallNode'
)
def tuple_of_args_tuple(*args):
    """
    >>> tuple_of_args_tuple(1,2,3)
    (1, 2, 3)
    """
    return tuple(tuple(tuple(args)))


@cython.test_fail_if_path_exists('//SimpleCallNode//SimpleCallNode')
def tuple_of_object(ob):
    """
    >>> tuple(type(1))
    Traceback (most recent call last):
    TypeError: 'type' object is not iterable
    >>> sorted(tuple(set([1, 2, 3])))
    [1, 2, 3]
    """
    return tuple(ob)


@cython.test_fail_if_path_exists(
    '//SimpleCallNode',
    '//PythonCapiCallNode//PythonCapiCallNode'
)
def tuple_of_tuple_or_none(tuple x):
    """
    >>> tuple_of_tuple_or_none((1,2,3))
    (1, 2, 3)
    >>> tuple_of_tuple_or_none(None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...itera...
    """
    return tuple(tuple(tuple(x)))


@cython.test_fail_if_path_exists(
    "//ExprStatNode//TupleNode",
    "//ExprStatNode",
)
def unused_literals():
    """
    >>> unused_literals()
    """
    (1, 2, 3)
    (1, 2, 3 + 4)
    ("abc", 'def')
    #(int(), 2, 3)


@cython.test_assert_path_exists(
    "//ExprStatNode",
    "//ExprStatNode//TupleNode",
)
def unused_non_literal():
    """
    >>> unused_non_literal()
    """
    (set(), None)
    (range(10), None)
