# mode: run
# tag: cpp, werror

from cython.operator cimport dereference as deref

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
    (1, 1.5, True)
    >>> test_wrap_pair(2, 2.25)
    (2, 2.25, True)
    """
    try:
        wrap = new Wrap[Pair[int, double]](Pair[int, double](i, x))
        return wrap.get().first(), wrap.get().second(), deref(wrap) == deref(wrap)
    finally:
        del wrap

def test_wrap_pair_pair(int i, int j, double x):
    """
    >>> test_wrap_pair_pair(1, 3, 1.5)
    (1, 3, 1.5, True)
    >>> test_wrap_pair_pair(2, 5, 2.25)
    (2, 5, 2.25, True)
    """
    try:
        wrap = new Wrap[Pair[int, Pair[int, double]]](
                        Pair[int, Pair[int, double]](i,Pair[int, double](j, x)))
        return (wrap.get().first(),
                wrap.get().second().first(),
                wrap.get().second().second(),
                deref(wrap) == deref(wrap))
    finally:
        del wrap
