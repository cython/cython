# distutils: extra_compile_args=-std=c++0x
# mode: run
# tag: cpp, werror

from libcpp.memory cimport unique_ptr, shared_ptr, default_delete 
from libcpp cimport nullptr

cdef extern from "cpp_smart_ptr_helper.h":
    cdef cppclass CountAllocDealloc:
        CountAllocDealloc(int*, int*)

    cdef cppclass FreePtr[T]:
        pass

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

    ##Repeat the above test with an explicit default_delete type
    alloc_count = 0
    dealloc_count = 0
    cdef unique_ptr[CountAllocDealloc,default_delete[CountAllocDealloc]] x_ptr2
    x_ptr2.reset(new CountAllocDealloc(&alloc_count, &dealloc_count))
    assert alloc_count == 1
    x_ptr2.reset()
    assert alloc_count == 1
    assert dealloc_count == 1
    
    alloc_count = 0
    dealloc_count = 0
    cdef unique_ptr[CountAllocDealloc,FreePtr[CountAllocDealloc]] x_ptr3
    x_ptr3.reset(new CountAllocDealloc(&alloc_count, &dealloc_count))
    assert x_ptr3.get() != nullptr;
    x_ptr3.reset()
    assert x_ptr3.get() == nullptr;
