# mode: run
# tag: all_language_levels

cimport cython


class Iter(object):
    def __init__(self, it=()):
        self.it = iter(it)
    def __iter__(self):
        return self
    def __next__(self):
        return next(self.it)
    next = __next__


class Map(object):
    def __init__(self, mapping={}):
        self.mapping = mapping
    def __iter__(self):
        return iter(self.mapping)
    def keys(self):
        return self.mapping.keys()
    def __getitem__(self, key):
        return self.mapping[key]


#### tuples


@cython.test_fail_if_path_exists(
    "//TupleNode//TupleNode",
    "//MergedSequenceNode",
)
def unpack_tuple_literal():
    """
    >>> unpack_tuple_literal()
    (1, 2, 4, 5)
    """
    return (*(1, 2, *(4, 5)),)


def unpack_tuple_literal_mult():
    """
    >>> unpack_tuple_literal_mult()
    (1, 2, 4, 5, 4, 5, 1, 2, 4, 5, 4, 5, 1, 2, 4, 5, 4, 5)
    """
    return (*((1, 2, *((4, 5) * 2)) * 3),)


@cython.test_fail_if_path_exists(
    "//TupleNode//TupleNode",
    "//MergedSequenceNode",
)
def unpack_tuple_literal_empty():
    """
    >>> unpack_tuple_literal_empty()
    ()
    """
    return (*(*(), *()), *(), *(*(*(),),))


def unpack_tuple_simple(it):
    """
    >>> unpack_tuple_simple([])
    ()
    >>> unpack_tuple_simple(set())
    ()
    >>> unpack_tuple_simple(Iter())
    ()

    >>> unpack_tuple_simple([1])
    (1,)

    >>> unpack_tuple_simple([2, 1])
    (2, 1)
    >>> unpack_tuple_simple((2, 1))
    (2, 1)
    >>> sorted(unpack_tuple_simple(set([2, 1])))
    [1, 2]
    >>> unpack_tuple_simple(Iter([2, 1]))
    (2, 1)
    """
    return (*it,)


def unpack_tuple_from_iterable(it):
    """
    >>> unpack_tuple_from_iterable([1, 2, 3])
    (1, 2, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 3)
    >>> unpack_tuple_from_iterable((1, 2, 3))
    (1, 2, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 3)
    >>> sorted(unpack_tuple_from_iterable(set([1, 2, 3])))
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]

    >>> unpack_tuple_from_iterable([1, 2])
    (1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2)
    >>> sorted(unpack_tuple_from_iterable(set([1, 2])))
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]
    >>> unpack_tuple_from_iterable(Iter([1, 2]))
    (1, 2, 1, 2, 1, 2, 1)

    >>> unpack_tuple_from_iterable([3])
    (1, 2, 3, 1, 3, 3, 3, 2, 1, 3)
    >>> unpack_tuple_from_iterable(set([3]))
    (1, 2, 3, 1, 3, 3, 3, 2, 1, 3)
    >>> unpack_tuple_from_iterable(Iter([3]))
    (1, 2, 3, 1, 2, 1)

    >>> unpack_tuple_from_iterable([])
    (1, 2, 1, 2, 1)
    >>> unpack_tuple_from_iterable(set([]))
    (1, 2, 1, 2, 1)
    >>> unpack_tuple_from_iterable([])
    (1, 2, 1, 2, 1)
    >>> unpack_tuple_from_iterable(Iter([1, 2, 3]))
    (1, 2, 1, 2, 3, 1, 2, 1)
    """
    return (1, 2, *it, 1, *(*it, *it), *it, 2, 1, *it)


def unpack_tuple_keep_originals(a, b, c):
    """
    >>> a = b = [1, 2]
    >>> c = [3, 4]
    >>> unpack_tuple_keep_originals(a, b, c)
    (1, 2, 1, 2, 2, 3, 4)
    >>> a
    [1, 2]
    >>> b
    [1, 2]
    >>> c
    [3, 4]

    >>> a = b = (1, 2)
    >>> c = (3, 4)
    >>> unpack_tuple_keep_originals(a, b, c)
    (1, 2, 1, 2, 2, 3, 4)
    >>> a
    (1, 2)
    >>> b
    (1, 2)
    >>> c
    (3, 4)
    """
    return (*a, *b, 2, *c)


def unpack_tuple_in_string_formatting(a, *args):
    """
    >>> print(unpack_tuple_in_string_formatting(1, 2))
    1 2
    >>> print(unpack_tuple_in_string_formatting(1, 'x'))
    1 'x'
    >>> unpack_tuple_in_string_formatting(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...format...
    >>> unpack_tuple_in_string_formatting(1, 2, 3)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...format...
    """
    return "%s %r" % (a, *args)


#### lists


@cython.test_fail_if_path_exists(
    "//ListNode//ListNode",
    "//MergedSequenceNode",
)
def unpack_list_literal():
    """
    >>> unpack_list_literal()
    [1, 2, 4, 5]
    """
    return [*[1, 2, *[4, 5]]]


def unpack_list_literal_mult():
    """
    >>> unpack_list_literal_mult()
    [1, 2, 4, 5, 4, 5, 1, 2, 4, 5, 4, 5, 1, 2, 4, 5, 4, 5]
    """
    return [*([1, 2, *([4, 5] * 2)] * 3)]


@cython.test_fail_if_path_exists(
    "//ListNode//ListNode",
    "//MergedSequenceNode",
)
def unpack_list_literal_empty():
    """
    >>> unpack_list_literal_empty()
    []
    """
    return [*[*[], *[]], *[], *[*[*[]]]]


def unpack_list_simple(it):
    """
    >>> unpack_list_simple([])
    []
    >>> unpack_list_simple(set())
    []
    >>> unpack_list_simple(Iter())
    []

    >>> unpack_list_simple([1])
    [1]

    >>> unpack_list_simple([2, 1])
    [2, 1]
    >>> unpack_list_simple((2, 1))
    [2, 1]
    >>> sorted(unpack_list_simple(set([2, 1])))
    [1, 2]
    >>> unpack_list_simple(Iter([2, 1]))
    [2, 1]
    """
    return [*it]


def unpack_list_from_iterable(it):
    """
    >>> unpack_list_from_iterable([1, 2, 3])
    [1, 2, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 3]
    >>> unpack_list_from_iterable((1, 2, 3))
    [1, 2, 1, 2, 3, 1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 3]
    >>> sorted(unpack_list_from_iterable(set([1, 2, 3])))
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]

    >>> unpack_list_from_iterable([1, 2])
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2]
    >>> sorted(unpack_list_from_iterable(set([1, 2])))
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]
    >>> unpack_list_from_iterable(Iter([1, 2]))
    [1, 2, 1, 2, 1, 2, 1]

    >>> unpack_list_from_iterable([3])
    [1, 2, 3, 1, 3, 3, 3, 2, 1, 3]
    >>> unpack_list_from_iterable(set([3]))
    [1, 2, 3, 1, 3, 3, 3, 2, 1, 3]
    >>> unpack_list_from_iterable(Iter([3]))
    [1, 2, 3, 1, 2, 1]

    >>> unpack_list_from_iterable([])
    [1, 2, 1, 2, 1]
    >>> unpack_list_from_iterable(set([]))
    [1, 2, 1, 2, 1]
    >>> unpack_list_from_iterable([])
    [1, 2, 1, 2, 1]
    >>> unpack_list_from_iterable(Iter([1, 2, 3]))
    [1, 2, 1, 2, 3, 1, 2, 1]
    """
    return [1, 2, *it, 1, *[*it, *it], *it, 2, 1, *it]


def unpack_list_keep_originals(a, b, c):
    """
    >>> a = b = [1, 2]
    >>> c = [3, 4]
    >>> unpack_list_keep_originals(a, b, c)
    [1, 2, 1, 2, 2, 3, 4]
    >>> a
    [1, 2]
    >>> b
    [1, 2]
    >>> c
    [3, 4]
    """
    return [*a, *b, 2, *c]


###### sets


@cython.test_fail_if_path_exists(
    "//SetNode//SetNode",
    "//MergedSequenceNode",
)
def unpack_set_literal():
    """
    >>> s = unpack_set_literal()
    >>> s == set([1, 2, 4, 5]) or s
    True
    """
    return {*{1, 2, *{4, 5}}}


def unpack_set_simple(it):
    """
    >>> s = unpack_set_simple([])
    >>> s == set([]) or s
    True

    >>> s = unpack_set_simple(set())
    >>> s == set([]) or s
    True

    >>> s = unpack_set_simple(Iter())
    >>> s == set([]) or s
    True

    >>> s = unpack_set_simple([1])
    >>> s == set([1]) or s
    True

    >>> s = unpack_set_simple([2, 1])
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_simple((2, 1))
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_simple(set([2, 1]))
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_simple(Iter([2, 1]))
    >>> s == set([1, 2]) or s
    True
    """
    return {*it}


def unpack_set_from_iterable(it):
    """
    >>> s = unpack_set_from_iterable([1, 2, 3])
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable([1, 2])
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable(set([1, 2]))
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable(Iter([1, 2]))
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable([3])
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable(set([3]))
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable(Iter([3]))
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable([])
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable(set([]))
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable([])
    >>> s == set([1, 2]) or s
    True

    >>> s = unpack_set_from_iterable((1, 2, 3))
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable(set([1, 2, 3]))
    >>> s == set([1, 2, 3]) or s
    True

    >>> s = unpack_set_from_iterable(Iter([1, 2, 3]))
    >>> s == set([1, 2, 3]) or s
    True
    """
    return {1, 2, *it, 1, *{*it, *it}, *it, 2, 1, *it, *it}


def unpack_set_keep_originals(a, b, c):
    """
    >>> a = b = set([1, 2])
    >>> c = set([3, 4])
    >>> s = unpack_set_keep_originals(a, b, c)
    >>> s == set([1, 2, 3, 4]) or s
    True
    >>> a == set([1, 2]) or a
    True
    >>> b == set([1, 2]) or b
    True
    >>> c == set([3, 4]) or c
    True
    """
    return {*a, *b, 2, *c}


#### dicts


@cython.test_fail_if_path_exists(
    "//DictNode//DictNode",
    "//MergedDictNode",
)
def unpack_dict_literal():
    """
    >>> d = unpack_dict_literal()
    >>> d == dict(a=1, b=2, c=4, d=5) or d
    True
    """
    return {**{'a': 1, 'b': 2, **{'c': 4, 'd': 5}}}


@cython.test_fail_if_path_exists(
    "//DictNode//DictNode",
    "//MergedDictNode",
)
def unpack_dict_literal_empty():
    """
    >>> unpack_dict_literal_empty()
    {}
    """
    return {**{**{}, **{}}, **{}, **{**{**{}}}}


def unpack_dict_simple(it):
    """
    >>> d = unpack_dict_simple({})
    >>> d == {} or d
    True

    >>> d = unpack_dict_simple([])
    >>> d == {} or d
    True

    >>> d = unpack_dict_simple(set())
    >>> d == {} or d
    True

    >>> d = unpack_dict_simple(Iter())
    >>> d == {} or d
    True

    >>> d = unpack_dict_simple(Map())
    >>> d == {} or d
    True

    >>> d = unpack_dict_simple(dict(a=1))
    >>> d == dict(a=1) or d
    True

    >>> d = unpack_dict_simple(dict(a=1, b=2))
    >>> d == dict(a=1, b=2) or d
    True

    >>> d = unpack_dict_simple(Map(dict(a=1, b=2)))
    >>> d == dict(a=1, b=2) or d
    True
    """
    return {**it}


def unpack_dict_from_iterable(it):
    """
    >>> d = unpack_dict_from_iterable(dict(a=1, b=2, c=3))
    >>> d == dict(a=1, b=2, c=3) or d
    True

    >>> d = unpack_dict_from_iterable(dict(a=1, b=2))
    >>> d == dict(a=1, b=2) or d
    True

    >>> d = unpack_dict_from_iterable(Map(dict(a=1, b=2)))
    >>> d == dict(a=1, b=2) or d
    True

    >>> d = unpack_dict_from_iterable(dict(a=3))
    >>> d == dict(a=3, b=5) or d
    True

    >>> d = unpack_dict_from_iterable(Map(dict(a=3)))
    >>> d == dict(a=3, b=5) or d
    True

    >>> d = unpack_dict_from_iterable({})
    >>> d == dict(a=4, b=5) or d
    True

    >>> d = unpack_dict_from_iterable(Map())
    >>> d == dict(a=4, b=5) or d
    True

    >>> d = unpack_dict_from_iterable(Iter())
    Traceback (most recent call last):
    TypeError: 'Iter' object is not a mapping

    >>> d = unpack_dict_from_iterable([])
    Traceback (most recent call last):
    TypeError: 'list' object is not a mapping

    >>> d = unpack_dict_from_iterable(dict(b=2, c=3))
    >>> d == dict(a=4, b=2, c=3) or d
    True

    >>> d = unpack_dict_from_iterable(Map(dict(b=2, c=3)))
    >>> d == dict(a=4, b=2, c=3) or d
    True

    >>> d = unpack_dict_from_iterable(dict(a=2, c=3))
    >>> d == dict(a=2, b=5, c=3) or d
    True

    >>> d = unpack_dict_from_iterable(Map(dict(a=2, c=3)))
    >>> d == dict(a=2, b=5, c=3) or d
    True
    """
    return {'a': 2, 'b': 3, **it, 'a': 1, **{**it, **it}, **it, 'a': 4, 'b': 5, **it, **it}


def unpack_dict_keep_originals(a, b, c):
    """
    >>> a = b = {1: 2}
    >>> c = {2: 3, 4: 5}
    >>> d = unpack_dict_keep_originals(a, b, c)
    >>> d == {1: 2, 2: 3, 4: 5} or d
    True
    >>> a
    {1: 2}
    >>> b
    {1: 2}
    >>> c == {2: 3, 4: 5} or c
    True
    """
    return {**a, **b, 2: 4, **c}
