__doc__ = u"""
>>> set_attr(5)
>>> get_attr()
None
"""

cdef class MyExt:
    cdef object attr

def set_attr(value):
    MyExt().attr = value

def get_attr():
    return MyExt().attr
