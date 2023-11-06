
cimport cython

dict_size = 4
d = dict(zip(range(10,dict_size+10), range(dict_size)))


def dict_iteritems(dict d):
    """
    >>> it = dict_iteritems(d)
    >>> type(it) is list
    False
    >>> sorted(it)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    return d.iteritems()


def dict_iterkeys(dict d):
    """
    >>> it = dict_iterkeys(d)
    >>> type(it) is list
    False
    >>> sorted(it)
    [10, 11, 12, 13]
    """
    return d.iterkeys()


def dict_itervalues(dict d):
    """
    >>> it = dict_itervalues(d)
    >>> type(it) is list
    False
    >>> sorted(it)
    [0, 1, 2, 3]
    """
    return d.itervalues()


@cython.test_fail_if_path_exists(
    "//WhileStatNode")
def items(dict d):
    """
    >>> items(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    l = []
    for k,v in d.items():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iteritems(dict d):
    """
    >>> iteritems(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> iteritems({})
    []
    """
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_iteritems(d):
    """
    >>> optimistic_iteritems(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems({})
    []
    >>> class mydict(object):
    ...     def __init__(self, t): self.t = t
    ...     def iteritems(self): return self.t(d.items())
    >>> optimistic_iteritems(mydict(list))
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems(mydict(tuple))
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems(mydict(iter))
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    """
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iteritems_dict():
    """
    >>> iteritems_dict()
    [(11, 1), (12, 2), (13, 3)]
    """
    l = []
    for k,v in {11 : 1, 12 : 2, 13 : 3}.iteritems():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iteritems_int(dict d):
    """
    >>> iteritems_int(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> iteritems_int({})
    []
    >>> iteritems_int({'a': 1})
    Traceback (most recent call last):
    TypeError: an integer is required
    >>> iteritems_int({1: 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    >>> iteritems_int({'a': 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    cdef int k,v
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_iteritems_int(d):
    """
    >>> optimistic_iteritems_int(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems_int({})
    []
    >>> class mydict(object):
    ...     def __init__(self, t): self.t = t
    ...     def iteritems(self): return self.t(d.items())
    >>> optimistic_iteritems_int(mydict(list))
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems_int(mydict(tuple))
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> optimistic_iteritems_int(mydict(iter))
    [(10, 0), (11, 1), (12, 2), (13, 3)]

    >>> optimistic_iteritems_int({'a': 1})
    Traceback (most recent call last):
    TypeError: an integer is required
    >>> optimistic_iteritems_int({1: 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    >>> optimistic_iteritems_int({'a': 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    cdef int k,v
    l = []
    for k,v in d.iteritems():
        l.append((k,v))
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iteritems_tuple(dict d):
    """
    >>> iteritems_tuple(d)
    [(10, 0), (11, 1), (12, 2), (13, 3)]
    >>> iteritems_tuple({})
    []
    """
    l = []
    for t in d.iteritems():
        l.append(t)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iteritems_listcomp(dict d):
    cdef list l = [(k,v) for k,v in d.iteritems()]
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterkeys(dict d):
    """
    >>> iterkeys(d)
    [10, 11, 12, 13]
    >>> iterkeys({})
    []
    """
    l = []
    for k in d.iterkeys():
        l.append(k)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_iterkeys(d):
    """
    >>> optimistic_iterkeys(d)
    [10, 11, 12, 13]
    >>> optimistic_iterkeys({})
    []
    >>> class mydict(object):
    ...     def __init__(self, t): self.t = t
    ...     def iterkeys(self): return self.t(d)
    >>> optimistic_iterkeys(mydict(lambda x:x))
    [10, 11, 12, 13]
    >>> optimistic_iterkeys(mydict(lambda x:x.keys()))
    [10, 11, 12, 13]
    >>> optimistic_iterkeys(mydict(list))
    [10, 11, 12, 13]
    >>> optimistic_iterkeys(mydict(tuple))
    [10, 11, 12, 13]
    >>> optimistic_iterkeys(mydict(iter))
    [10, 11, 12, 13]
    """
    l = []
    for k in d.iterkeys():
        l.append(k)
    l.sort()
    return l

@cython.test_fail_if_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_iterkeys_argerror(d):
    """
    >>> try: optimistic_iterkeys_argerror(d)
    ... except (TypeError, AttributeError): pass
    """
    for k in d.iterkeys(1):
        print k

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterkeys_int(dict d):
    """
    >>> iterkeys_int(d)
    [10, 11, 12, 13]
    >>> iterkeys_int({})
    []
    >>> iterkeys_int({'a': 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    cdef int k
    l = []
    for k in d.iterkeys():
        l.append(k)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterdict(dict d):
    """
    >>> iterdict(d)
    [10, 11, 12, 13]
    >>> iterdict({})
    []
    """
    l = []
    for k in d:
        l.append(k)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterdict_int(dict d):
    """
    >>> iterdict_int(d)
    [10, 11, 12, 13]
    >>> iterdict_int({})
    []
    >>> iterdict_int({'a': 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    cdef int k
    l = []
    for k in d:
        l.append(k)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterdict_reassign(dict d):
    """
    >>> iterdict_reassign(d)
    [10, 11, 12, 13]
    >>> iterdict_reassign({})
    []
    """
    cdef dict d_new = {}
    l = []
    for k in d:
        d = d_new
        l.append(k)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterdict_listcomp(dict d):
    """
    >>> iterdict_listcomp(d)
    [10, 11, 12, 13]
    >>> iterdict_listcomp({})
    []
    """
    cdef list l = [k for k in d]
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def itervalues(dict d):
    """
    >>> itervalues(d)
    [0, 1, 2, 3]
    >>> itervalues({})
    []
    """
    l = []
    for v in d.itervalues():
        l.append(v)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_itervalues(d):
    """
    >>> optimistic_itervalues(d)
    [0, 1, 2, 3]
    >>> optimistic_itervalues({})
    []
    >>> class mydict(object):
    ...     def __init__(self, t): self.t = t
    ...     def itervalues(self): return self.t(d.values())
    >>> optimistic_itervalues(mydict(lambda x:x))
    [0, 1, 2, 3]
    >>> optimistic_itervalues(mydict(list))
    [0, 1, 2, 3]
    >>> optimistic_itervalues(mydict(tuple))
    [0, 1, 2, 3]
    >>> optimistic_itervalues(mydict(iter))
    [0, 1, 2, 3]
    """
    l = []
    for v in d.itervalues():
        l.append(v)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def itervalues_int(dict d):
    """
    >>> itervalues_int(d)
    [0, 1, 2, 3]
    >>> itervalues_int({})
    []
    >>> itervalues_int({'a': 'b'})
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    cdef int v
    l = []
    for v in d.itervalues():
        l.append(v)
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def itervalues_listcomp(dict d):
    """
    >>> itervalues_listcomp(d)
    [0, 1, 2, 3]
    >>> itervalues_listcomp({})
    []
    """
    cdef list l = [v for v in d.itervalues()]
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def itervalues_kwargs(**d):
    """
    >>> itervalues_kwargs(a=1, b=2, c=3, d=4)
    [1, 2, 3, 4]
    >>> itervalues_kwargs()
    []
    """
    cdef list l = [v for v in d.itervalues()]
    l.sort()
    return l

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def iterdict_change_size(dict d):
    """
    >>> count, i = 0, -1
    >>> d = {1:2, 10:20}
    >>> for i in d:
    ...     d[i+1] = 5
    ...     count += 1
    ...     if count > 5:
    ...         break # safety
    Traceback (most recent call last):
    RuntimeError: dictionary changed size during iteration

    >>> iterdict_change_size({1:2, 10:20})
    Traceback (most recent call last):
    RuntimeError: dictionary changed size during iteration
    >>> print( iterdict_change_size({}) )
    DONE
    """
    cdef int count = 0
    i = -1
    for i in d:
        d[i+1] = 5
        count += 1
        if count > 5:
            break # safety
    return "DONE"

@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def optimistic_iterdict_change_size(d):
    """
    >>> count, i = 0, -1
    >>> d = {1:2, 10:20}
    >>> for i in d:
    ...     d[i+1] = 5
    ...     count += 1
    ...     if count > 5:
    ...         break # safety
    Traceback (most recent call last):
    RuntimeError: dictionary changed size during iteration

    >>> optimistic_iterdict_change_size({1:2, 10:20})
    Traceback (most recent call last):
    RuntimeError: dictionary changed size during iteration
    >>> print( optimistic_iterdict_change_size({}) )
    DONE
    >>> class mydict(object):
    ...     _d = {1:2, 10:20}
    ...     def iterkeys(self): return self._d
    ...     def __setitem__(self, key, value): self._d[key] = value
    >>> optimistic_iterdict_change_size(mydict())
    Traceback (most recent call last):
    RuntimeError: dictionary changed size during iteration
    """
    cdef int count = 0
    i = -1
    for i in d.iterkeys():
        d[i+1] = 5
        count += 1
        if count > 5:
            break # safety
    return "DONE"


@cython.test_assert_path_exists(
    "//WhileStatNode",
    "//WhileStatNode//DictIterationNextNode")
def values_of_expression(**kwargs):
    """
    >>> sorted(values_of_expression(a=3, b=4))
    [3, 4]
    """
    # this can be optimised even in Py2
    return [ arg for arg in dict(kwargs.items()).values() ]


def items_of_expression(*args, **kwargs):
    """
    >>> sorted(items_of_expression(a=3, b=4))
    [('a', 3), ('b', 4)]

    >>> sorted(items_of_expression([('a', 3)], b=4))
    [('a', 3), ('b', 4)]
    """
    return [item for item in dict(*args, **kwargs).items()]


def iteritems_of_expression(*args, **kwargs):
    """
    >>> sorted(iteritems_of_expression(a=3, b=4))
    [('a', 3), ('b', 4)]

    >>> sorted(iteritems_of_expression([('a', 3)], b=4))
    [('a', 3), ('b', 4)]
    """
    return [item for item in dict(*args, **kwargs).iteritems()]


def for_in_items_of_expression(*args, **kwargs):
    """
    >>> sorted(for_in_items_of_expression(a=3, b=4))
    [('a', 3), ('b', 4)]

    >>> sorted(for_in_items_of_expression([('a', 3)], b=4))
    [('a', 3), ('b', 4)]
    """
    result = []
    for k, v in dict(*args, **kwargs).items():
        result.append((k, v))
    return result


def for_in_iteritems_of_expression(*args, **kwargs):
    """
    >>> sorted(for_in_iteritems_of_expression(a=3, b=4))
    [('a', 3), ('b', 4)]

    >>> sorted(for_in_iteritems_of_expression([('a', 3)], b=4))
    [('a', 3), ('b', 4)]
    """
    result = []
    for k, v in dict(*args, **kwargs).iteritems():
        result.append((k, v))
    return result


cdef class NotADict:
    """
    >>> NotADict().listvalues()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: descriptor 'values' for 'mappingproxy' objects doesn't apply to a 'iterdict.NotADict' object
    """
    cdef long v
    def __cinit__(self):
        self.v = 1
    itervalues = type(object.__dict__).values

    def listvalues(self):
        return [v for v in self.itervalues()]
