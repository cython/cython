# distutils: language=c++

import time

def expensive_function():
    time.sleep(5)
    return {"hello": "world"}

cdef class A:
cdef class A:
    cdef object _py_obj
    def __init__(self):
        self._py_obj = None

    @property
    def obj(self):
        if not self._py_obj:
            self._py_obj = expensive_function()
        return self._py_obj

