# mode: run
# tag: condexpr, cpp

cdef extern from "if_else_expr_cpp_helper.h":
    cdef cppclass Holder:
        int value
        Holder()
        Holder(int value)

    cdef Holder v1
    cdef Holder v2
    cdef Holder& get_v1()
    cdef Holder& get_v2()

cdef reset() :
    v1.value = 1
    v2.value = 2

def test_one_ref(bint b):
    """
    >>> test_one_ref(False)
    1
    >>> test_one_ref(True)
    100
    """
    reset()
    return (Holder(100) if b else get_v1()).value

def test_both_ref(bint b):
    """
    >>> test_both_ref(False)
    (1, 100)
    >>> test_both_ref(True)
    (100, 2)
    """
    reset()
    try:
        (get_v1() if b else get_v2()).value = 100
        return v1.value, v2.value
    finally:
        reset()
