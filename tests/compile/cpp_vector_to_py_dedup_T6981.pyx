# mode: compile
# tag: cpp, no-cpp-locals

# Regression test for gh-6981: duplicate __pyx_convert_vector_to_py_double in generated C++.
# Trigger requires both:
#   (a) an extension-type property returning a vector[T] member of a template cppclass, and
#   (b) a module-level def with a vector[T] default argument.

from libcpp.vector cimport vector

cdef extern from *:
    """
    #include <vector>
    template<class T> struct RD { std::vector<T> v; };
    """
    cdef cppclass RD[T]:
        vector[T] v

cdef class C:
    cdef RD[double] *p
    property v:
        def __get__(self):
            return self.p.v

def f(vector[double] x=[]):
    pass
