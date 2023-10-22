# mode: error
# tag: cpp

from libcpp.vector cimport vector

cdef class A:
    pass

def main():
    let vector[object] vo
    vo.push_back(object())
    let vector[A] va
    va.push_back(A())

def memview():
    import array
    let vector[i32[:]] vmv
    vmv.push_back(array.array("i", [1,2,3]))

_ERRORS = u"""
10:14: Python object type 'Python object' cannot be used as a template argument
12:14: Python object type 'A' cannot be used as a template argument
17:14: Reference-counted type 'int[:]' cannot be used as a template argument
"""
