# tag: cpp

cdef extern from "cpp_nested_classes_support.h":
    cdef cppclass A:
        cppclass B:
            int square(int)
            cppclass C:
                int cube(int)
        B* createB()
        ctypedef int my_int
        @staticmethod
        my_int negate(my_int)

def test_nested_classes():
    """
    >>> test_nested_classes()
    """
    cdef A a
    cdef A.B b
    assert b.square(3) == 9
    cdef A.B.C c
    assert c.cube(3) == 27

    cdef A.B *b_ptr = a.createB()
    assert b_ptr.square(4) == 16
    del b_ptr

def test_nested_typedef(py_x):
    cdef A.my_int x = py_x
    assert A.negate(x) == -py_x
