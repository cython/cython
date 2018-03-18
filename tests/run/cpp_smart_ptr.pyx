# mode: run
# tag: cpp, werror, cpp11
# distutils: extra_compile_args=-std=c++0x

from libcpp.memory cimport unique_ptr, shared_ptr, default_delete
from libcpp cimport nullptr

cdef extern from "cpp_smart_ptr_helper.h":
    cdef cppclass CountAllocDealloc:
        CountAllocDealloc(int*, int*)

    cdef cppclass FreePtr[T]:
        pass


ctypedef const CountAllocDealloc const_CountAllocDealloc


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


def test_const_shared_ptr():
    """
    >>> test_const_shared_ptr()
    """
    cdef int alloc_count = 0, dealloc_count = 0
    cdef shared_ptr[const CountAllocDealloc] ptr = shared_ptr[const_CountAllocDealloc](
        new CountAllocDealloc(&alloc_count, &dealloc_count))
    assert alloc_count == 1
    assert dealloc_count == 0

    cdef shared_ptr[const CountAllocDealloc] ptr2 = ptr
    assert alloc_count == 1
    assert dealloc_count == 0

    ptr.reset()
    assert alloc_count == 1
    assert dealloc_count == 0

    ptr2.reset()
    assert alloc_count == 1
    assert dealloc_count == 1


cdef cppclass A:
    pass

cdef cppclass B(A):
    pass

cdef cppclass C(B):
    pass

cdef shared_ptr[A] holding_subclass = shared_ptr[A](new C())
