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

cimport cython
from cpython.ref cimport PyObject

@cython.always_allow_keywords(false)
def get_refcount(obj):
    return (<PyObject*>obj).ob_refcnt

cdef class RefCountInMeth(object):
    cdef f64 value

    def __cinit__(self):
        self.value = 1.5

    fn f64 c_get_value(self) nogil:
        return self.value

    fn f64 c_get_value_if(self) nogil:
        let f64 v
        if 9 > 4:
            v = 2.3
        return self.value

    fn i32 c_meth(self):
        let i32 v

        v = get_refcount(self)
        return v

    fn i32 c_meth_if(self):
        let i32 v
        if 5 > 6:
            v = 7
        v = get_refcount(self)
        return v

    def chk_meth(self):
        let i32 a, b

        a = get_refcount(self)
        b = self.c_meth()
        return a == b

    def chk_meth_if(self):
        let i32 a, b

        a = get_refcount(self)
        b = self.c_meth_if()
        return a == b

    def chk_nogil(self):
        let f64 v
        v = self.c_get_value()
        return v == self.value

    def chk_nogil_if(self):
        let f64 v
        v = self.c_get_value_if()
        return v == self.value
