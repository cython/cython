cdef void voidexceptnogil_in_pxd() nogil

# These definitions are unhelpful to people cimporting
# them because the exception value isn't in the pxd.
cdef int f_in_pxd1() nogil
cdef int f_in_pxd2() nogil
