# mode: run
# tag: cpp, werror, no-cpp-locals
# cython: test_fail_if_c_code_has = __Pyx_FakeReference<int>

# Assigning a prvalue conditional expression directly into a C++ container
# element used to generate the ternary's temporary as __Pyx_FakeReference<T>
# rather than a plain T, producing a dangling reference read (GH-7927).

from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector


cdef class Holder:
    cdef unordered_map[int, vector[int]] logs

    def __init__(self, int n):
        cdef vector[int] blanks
        blanks.resize(n, 0)
        self.logs[0] = blanks

    def store(self, int i, bint cond):
        self.logs[0][i] = 1 if cond else 2

    def load(self, int i):
        cdef int result = self.logs[0][i]
        return result


def test_conditional_into_container_element():
    """
    >>> test_conditional_into_container_element()
    """
    cdef Holder h = Holder(4)
    h.store(0, True)
    h.store(1, False)
    h.store(2, True)
    h.store(3, False)
    assert h.load(0) == 1, h.load(0)
    assert h.load(1) == 2, h.load(1)
    assert h.load(2) == 1, h.load(2)
    assert h.load(3) == 2, h.load(3)


def test_conditional_into_vector_element(bint cond):
    """
    >>> test_conditional_into_vector_element(True)
    111
    >>> test_conditional_into_vector_element(False)
    222
    """
    cdef vector[int] v
    v.resize(1, 0)
    v[0] = 111 if cond else 222
    return v[0]
