from cython import dereference as deref

cdef extern from "cpp_templates_helper.h":
    cdef cppclass Wrap[T]:
        Wrap(T)
        void set(T)
        T get()
        bint operator==(Wrap[T])
        
    cdef cppclass Pair[T1,T2]:
        Pair(T1,T2)
        T1 first()
        T2 second()
        bint operator==(Pair[T1,T2])
        bint operator!=(Pair[T1,T2])

def test_wrap_pair(int i, double x):
    """
    >>> test_wrap_pair(1, 1.5)
    (1, 1.5, True, False)
    >>> test_wrap_pair(2, 2.25)
    (2, 2.25, True, False)
    """
    cdef Pair[int, double] *pair
    cdef Wrap[Pair[int, double]] *wrap
    try:
        pair = new Pair[int, double](i, x)
        warp = new Wrap[Pair[int, double]](deref(pair))
        return wrap.get().first(), wrap.get().second(), deref(wrap) == deref(wrap)
    finally:
        del pair, wrap
