# tag: cpp

cdef extern from "cpp_nested_classes_support.h":
    cdef cppclass A:
        cppclass B:
            int square(int)
            cppclass C:
                int cube(int)
        B* createB()

def test():
    """
    >>> test()
    """
    cdef A a
    cdef A.B b
    assert b.square(3) == 9
    cdef A.B.C c
    assert c.cube(3) == 27
    
    cdef A.B *b_ptr = a.createB()
    assert b_ptr.square(4) == 16
    del b_ptr
