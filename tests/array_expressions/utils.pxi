cimport cython
from cython cimport view

from cpython.object cimport Py_EQ
cimport numpy as np

import sys
import numpy as np


__test__ = {}

def testcase(f):
    assert f.__doc__, f
    __test__[f.__name__] = f.__doc__
    return f

def testcase_like(similar_func, docstring_specializer=None):
    def decorator(wrapper_func):
        assert similar_func.__doc__
        doc = similar_func.__doc__.replace(similar_func.__name__,
                                           wrapper_func.__name__)
        if docstring_specializer:
            doc = docstring_specializer(doc)

        wrapper_func.__doc__ = doc
        return testcase(wrapper_func)
    return decorator

def testcase_like_sub(similar_func, sub_dict):
    def docstring_specializer(s):
        # not the most efficient implementation :)
        for k, v in sub_dict.items():
            s = s.replace(k, v)
        return s
    return testcase_like(similar_func, docstring_specializer)

cdef class UniqueObject(object):
    cdef public object value
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return UniqueObject(self.value + other.value)

    def __richcmp__(self, other, int opid):
        if opid == Py_EQ:
            return self.value == other.value
        return NotImplemented

    def __str__(self):
        return str(self.value)

    def __dealloc__(self):
        pass
        # sys.stdout.write("dealloc %s " % self.value)

class UniqueObjectInplace(UniqueObject):
    def __add__(self, other):
        self.value += other.value
        return self

def object_range(n, shape=None, cls=UniqueObject):
    result = np.array([cls(i) for i in range(n)], dtype=np.object)
    if shape:
        result = result.reshape(shape)
    return result

def operands(dtype):
    return np.arange(10, dtype=dtype), np.arange(100, dtype=dtype).reshape(10, 10)

cdef fused fused_dtype_t:
    long
    long double
    double complex
    object
