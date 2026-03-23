from libcpp.mutex cimport py_safe_call_once, py_safe_once_flag

import time

cdef void init_py_obj(void *void_instance):
    cdef A instance = <A>void_instance
    instance._py_obj = expensive_function()

def expensive_function():
    time.sleep(5)
    return {"hello": "world"}

cdef class A:
    cdef py_safe_once_flag flag

    def __init__(self):
        self._py_obj = None

    @property
    def obj(self):
        cdef void *void_self = <void *>self
        py_safe_call_once(self.flag, init_py_obj, void_self)
        return self._py_obj

