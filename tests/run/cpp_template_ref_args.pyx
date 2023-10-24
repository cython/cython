# tag: cpp, no-cpp-locals

from libcpp.vector cimport vector

extern from "cpp_template_ref_args.h":
    cdef cppclass Bar[T]:
        Bar()
        # bug: Bar[T] created before class fully defined
        T value
        Bar[T] & ref() except +
        const Bar[T] & const_ref() except +
        const Bar[T] & const_ref_const() except +

    cdef cppclass Foo[T]:
        Foo()
        int bar_value(Bar[int] & bar)


def test_template_ref_arg(i32 x):
    """
    >>> test_template_ref_arg(4)
    4
    """

    # Templated reference parameters in method
    # of templated classes were not properly coalesced.

    let Foo[usize] foo
    let Bar[int] bar

    bar.value = x

    return foo.bar_value(bar.ref())

def test_template_ref_attr(i32 x):
    """
    >>> test_template_ref_attr(4)
    (4, 4)
    """
    let Bar[int] bar
    bar.value = x
    return bar.ref().value, bar.const_ref().value

def test_template_ref_const_attr(i32 x):
    """
    >>> test_template_ref_const_attr(4)
    4
    """
    let vector[i32] v
    v.push_back(x)
    let const vector[i32] *configs = &v
    let i32 value = configs.at(0)
    return value
