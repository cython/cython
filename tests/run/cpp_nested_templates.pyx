# mode: run
# tag: cpp, werror

from cython.operator cimport dereference as deref

extern from "cpp_templates_helper.h":
    cdef cppclass Wrap[T]:
        Wrap(T)
        void set(T)
        T get()
        bint operator==(Wrap[T])

    cdef cppclass Pair[T1, T2]:
        Pair(T1,T2)
        T1 first()
        T2 second()
        bint operator==(Pair[T1, T2])
        bint operator!=(Pair[T1, T2])

def test_wrap_pair(i32 i, f64 x):
    """
    >>> test_wrap_pair(1, 1.5)
    (1, 1.5, True)
    >>> test_wrap_pair(2, 2.25)
    (2, 2.25, True)
    """
    try:
        wrap = new Wrap[Pair[i32, f64]](Pair[i32, f64](i, x))
        return wrap.get().first(), wrap.get().second(), deref(wrap) == deref(wrap)
    finally:
        del wrap

def test_wrap_pair_pair(i32 i, i32 j, f64 x):
    """
    >>> test_wrap_pair_pair(1, 3, 1.5)
    (1, 3, 1.5, True)
    >>> test_wrap_pair_pair(2, 5, 2.25)
    (2, 5, 2.25, True)
    """
    try:
        wrap = new Wrap[Pair[i32, Pair[i32, f64]]](
                        Pair[i32, Pair[i32, f64]](i, Pair[i32, f64](j, x)))
        return (wrap.get().first(),
                wrap.get().second().first(),
                wrap.get().second().second(),
                deref(wrap) == deref(wrap))
    finally:
        del wrap
