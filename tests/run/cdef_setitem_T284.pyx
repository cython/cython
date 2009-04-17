__doc__ = u'''
>>> no_cdef()
>>> with_cdef()
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
