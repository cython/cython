# ticket: t589

cimport cython

_set = set # CPython may not define it (in Py2.3), but Cython does :)


def test_set_clear_bound():
    """
    >>> type(test_set_clear_bound()) is _set
    True
    >>> list(test_set_clear_bound())
    []
    """
    cdef set s1 = set([1])
    clear = s1.clear
    clear()
    return s1

text = u'ab jd  sdflk as sa  sadas asdas fsdf '
pipe_sep = u'|'


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
)
def test_unicode_join_bound(unicode sep, l):
    """
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( pipe_sep.join(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    >>> print( test_unicode_join_bound(pipe_sep, l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    join = sep.join
    return join(l)


def test_unicode_join_bound_no_assignment(unicode sep):
    """
    >>> test_unicode_join_bound_no_assignment(text)
    """
    sep.join


def test_dict_items_bound_no_assignment(dict d):
    """
    >>> test_dict_items_bound_no_assignment({1:2})
    """
    d.items


def list_pop(list l):
    """
    >>> list_pop([1,2,3])
    (2, [1, 3])
    """
    pop = l.pop
    r = pop(1)
    return r, l


def list_pop_literal():
    """
    >>> list_pop_literal()
    (2, [1, 3])
    """
    l = [1,2,3]
    pop = l.pop
    r = pop(1)
    return r, l


def list_pop_reassign():
    """
    >>> list_pop_reassign()
    2
    """
    l = [1,2,3]
    pop = l.pop
    l = None
    r = pop(1)
    return r


def list_insert(list l):
    """
    >>> list_insert([1,2,3])
    (None, [1, 4, 2, 3])
    """
    insert = l.insert
    r = insert(1, 4)
    return r, l


def list_insert_literal():
    """
    >>> list_insert_literal()
    (None, [1, 4, 2, 3])
    """
    l = [1,2,3]
    insert = l.insert
    r = insert(1, 4)
    return r, l


def list_insert_reassign():
    """
    >>> list_insert_reassign()
    (None, [1, 4, 2, 3])
    """
    l = [1,2,3]
    insert = l.insert
    m, l = l, None
    r = insert(1, 4)
    return r, m
