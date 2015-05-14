
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


@cython.test_fail_if_path_exists(
    "//SetNode//SetNode",
    "//MergedSetNode//SetNode",
    "//MergedSetNode//MergedSetNode",
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


@cython.test_fail_if_path_exists(
    "//DictNode//DictNode",
    "//MergedDictNode//DictNode",
    "//MergedDictNode//MergedDictNode",
)
def unpack_dict_literal():
    """
    >>> d = unpack_dict_literal()
    >>> d == dict(a=1, b=2, c=4, d=5) or d
    True
    """
    return {**{'a': 1, 'b': 2, **{'c': 4, 'd': 5}}}


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
