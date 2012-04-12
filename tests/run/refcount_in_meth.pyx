#!/usr/bin/env python

__doc__=u"""
>>> t = RefCountInMeth()
>>> t.chk_meth()
True
>>> t.chk_nogil()
True
>>> t.chk_meth_if()
True
>>> t.chk_nogil_if()
True
"""

from cpython.ref cimport PyObject

def get_refcount(obj):
    return (<PyObject*>obj).ob_refcnt

cdef class RefCountInMeth(object):
    cdef double value

    def __cinit__(self):
        self.value = 1.5

    cdef double c_get_value(self) nogil:
        return self.value

    cdef double c_get_value_if(self) nogil:
        cdef double v
        if 9>4:
            v = 2.3
        return self.value

    cdef int c_meth(self):
        cdef int v

        v = get_refcount(self)
        return v

    cdef int c_meth_if(self):
        cdef int v
        if 5>6:
            v = 7
        v = get_refcount(self)
        return v

    def chk_meth(self):
        cdef int a,b

        a = get_refcount(self)
        b = self.c_meth()
        return a==b

    def chk_meth_if(self):
        cdef int a,b

        a = get_refcount(self)
        b = self.c_meth_if()
        return a==b

    def chk_nogil(self):
        cdef double v
        v = self.c_get_value()
        return v==self.value

    def chk_nogil_if(self):
        cdef double v
        v = self.c_get_value_if()
        return v==self.value

