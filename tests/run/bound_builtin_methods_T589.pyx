# ticket: 589

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
    "//SimpleCallNode",
    "//SimpleCallNode//NameNode")
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
