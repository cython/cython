from cython cimport view

# VALID
cdef int[::view.indirect, ::1, :] a
cdef int[::view.indirect, :, ::1] b
cdef int[::view.indirect_contiguous, ::1, :] c
