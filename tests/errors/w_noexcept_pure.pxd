cdef object test_return_object_noexcept_in_pxd(x) noexcept
cdef object test_return_object_in_pxd(x)

cdef extern from *:
    cdef object extern_return_object() # Ok

    cdef object extern_noexcept() noexcept # Ok
