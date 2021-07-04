# mode: run
# tag: cpp, werror, no-cpp-locals
# cython: experimental_cpp_class_def=True

from libcpp.vector cimport vector

cdef cppclass Wrapper[T]:
    T value
    __init__(T &value):
        this.value = value
    void set(T &value):
        this.value = value
    T get() const:
        return this.value


def test_const_get(int x):
    """
    >>> test_const_get(10)
    10
    """
    cdef const Wrapper[int] *wrapper = new Wrapper[int](x)
    try:
        return const_get(wrapper[0])
    finally:
        del wrapper

cdef int const_get(const Wrapper[int] wrapper):
    return wrapper.get()

def test_const_ref_get(int x):
    """
    >>> test_const_ref_get(100)
    100
    """
    cdef const Wrapper[int] *wrapper = new Wrapper[int](x)
    try:
        return const_ref_get(wrapper[0])
    finally:
        del wrapper

cdef int const_ref_get(const Wrapper[int] &wrapper):
    return wrapper.get()

def test_const_pointer_get(int x):
    """
    >>> test_const_pointer_get(1000)
    1000
    """
    cdef Wrapper[int] *wrapper = new Wrapper[int](x)
    cdef const Wrapper[int] *const_wrapper = wrapper
    try:
        return const_wrapper.get()
    finally:
        del wrapper


# TODO: parse vector[Wrapper[int]*]
ctypedef Wrapper[int] wrapInt

def test_vector_members(py_a, py_b):
    """
    >>> test_vector_members([1, 2, 3], [4,5, 6])
    ([1, 2, 3], 4)
    """
    cdef Wrapper[int] *value
    cdef const Wrapper[int] *const_value
    cdef vector[const Wrapper[int]*] a
    cdef vector[wrapInt*] b
    for x in py_a:
        a.push_back(new Wrapper[int](x))
    for x in py_b:
        b.push_back(new Wrapper[int](x))
    try:
        return vector_members(a, b)
    finally:
        for const_value in a:
            del const_value
        for value in b:
            del value

cdef vector_members(vector[const Wrapper[int]*] a, const vector[wrapInt*] b):
    # TODO: Cython-level error.
    # b[0].set(100)

    # TODO: const_iterator
    return [x.get() for x in a], b[0].get()
