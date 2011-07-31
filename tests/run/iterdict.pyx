
cimport cython

dict_size = 4
d = dict(zip(range(10,dict_size+10), range(dict_size)))

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
def iteritems_dict(dict d):
    """
    >>> iteritems_dict(d)
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
def iterkeys_int(dict d):
    """
    >>> iterkeys_int(d)
    [10, 11, 12, 13]
    >>> iterkeys_int({})
    []
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
def itervalues_int(dict d):
    """
    >>> itervalues_int(d)
    [0, 1, 2, 3]
    >>> itervalues_int({})
    []
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
