# tag: cpp


cdef extern from "cpp_template_ref_args.h":

    cdef cppclass Bar[T]:
        Bar()
        Bar[T] & ref()
        T value

    cdef cppclass Foo[T]:
        Foo()
        int bar_value(Bar[int] & bar)


def test_template_ref_arg(int x):
    """
    >>> test_template_ref_arg(4)
    4
    """

    # Templated reference parameters in method
    # of templated classes were not properly coalesced.

    cdef Foo[size_t] foo
    cdef Bar[int] bar

    bar.value = x

    return foo.bar_value(bar.ref())
