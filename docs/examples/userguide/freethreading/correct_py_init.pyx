# distutils: language=c++

from libcpp.atomic cimport atomic
from libcpp.mutex cimport py_safe_call_object_once, py_safe_once_flag

import time

def expensive_function():
    time.sleep(5)
    return {"hello": "world"}

cdef class A:
    cdef object _py_obj
    cdef py_safe_once_flag flag
    cdef atomic[int] cache_flag

    def __init__(self):
        self._py_obj = None
        self.cache_flag.store(0)

    @property
    def obj(self):
        if not self.cache_flag.load():
            def closure():
                self._py_obj = expensive_function()
                self.cache_flag.store(True)
            py_safe_call_object_once(self.flag, closure)
        return self._py_obj
