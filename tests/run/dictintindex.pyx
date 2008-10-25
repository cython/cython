__doc__ = u"""
>>> test_index()
1
>>> test_del()
Traceback (most recent call last):
KeyError: 0
"""

def test_index():
    cdef int key = 0
    d = {0:1}
    return d[key]

def test_del():
    cdef int key = 0
    d = {0:1}
    del d[key]
    return d[key]
