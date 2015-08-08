# distutils: extra_compile_args=-std=c++0x
# mode: run
# tag: cpp, werror

from libcpp.memory cimport unique_ptr, shared_ptr

cdef extern from "cpp_smart_ptr_helper.h":
    cdef cppclass CountAllocDealloc:
        CountAllocDealloc(int*, int*)

def test_unique_ptr():
    """
    >>> test_unique_ptr()
    """
    cdef int alloc_count = 0, dealloc_count = 0
    cdef unique_ptr[CountAllocDealloc] x_ptr
    x_ptr.reset(new CountAllocDealloc(&alloc_count, &dealloc_count))
    assert alloc_count == 1
    x_ptr.reset()
    assert alloc_count == 1
    assert dealloc_count == 1
