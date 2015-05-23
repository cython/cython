# tag: cpp


cdef extern from "cpp_template_ref_args.h":

    cdef cppclass Bar[T]:
        Bar()
        # bug: Bar[T] created before class fully defined
        T value
        Bar[T] & ref() except +
        const Bar[T] & const_ref() except +

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

def test_template_ref_attr(int x):
    """
    >>> test_template_ref_attr(4)
    (4, 4)
    """
    cdef Bar[int] bar
    bar.value = x
    return bar.ref().value, bar.const_ref().value
