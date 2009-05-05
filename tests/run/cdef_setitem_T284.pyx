__doc__ = u'''
>>> no_cdef()
>>> with_cdef()
>>> test_list(range(11), -2, None)
[0, 1, 2, 3, 4, 5, 6, 7, 8, None, 10]
>>> test_list(range(11), "invalid index", None)
Traceback (most recent call last):
...
TypeError: list indices must be integers, not str
'''
def no_cdef():
    lst = range(11)
    ob = 10L
    lst[ob] = -10
    dd = {}
    dd[ob] = -10

def with_cdef():
    cdef list lst = range(11)
    ob = 10L
    lst[ob] = -10
    cdef dict dd = {}
    dd[ob] = -10

def test_list(list L, object i, object a):
    L[i] = a
    return L
