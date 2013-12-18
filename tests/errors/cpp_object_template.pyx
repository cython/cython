# mode: error

from libcpp.vector cimport vector

cdef class A:
    pass

def main():
    cdef vector[object] vo
    vo.push_back(object())
    cdef vector[A] va
    va.push_back(A())

_ERRORS = u"""
9:16: Python object type 'Python object' cannot be used as a template argument
11:16: Python object type 'A' cannot be used as a template argument
"""
