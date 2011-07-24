# mode: compile

cimport cython
# from cython.view cimport contig as foo, full as bar #, follow
from cython cimport view
from cython.view cimport (generic, strided, indirect,
                          generic_contiguous, contiguous, indirect_contiguous)

cdef char[:] one_dim
cdef char[:,:,:] three_dim
cdef unsigned int[::1, :] view1
cdef unsigned int[:, ::1] view2
cdef long long[::1, :, :, :] fort_contig
cdef unsigned long[:, :, :, ::1] c_contig
cdef unsigned short int[::1] c_and_fort
cdef long long[0x0::0x1, 00:, -0   :,0 :] fort_contig0
cdef unsigned long[0:, 0:, 0:, 0::0x0001] c_contig0

cdef int[::generic, ::generic] a1
cdef int[::strided, ::generic] a2
cdef int[::indirect, ::generic] a3
cdef int[::generic, ::strided] a4
cdef int[::strided, ::strided] a5
cdef int[::indirect, ::strided] a6
cdef int[::generic, ::indirect] a7
cdef int[::strided, ::indirect] a8
cdef int[::indirect, ::indirect] a9

cdef int[::generic, ::generic_contiguous] a10
cdef int[::strided, ::generic_contiguous] a11
cdef int[::indirect, ::generic_contiguous] a12
cdef int[::generic, ::contiguous] a13
cdef int[::strided, ::contiguous] a14
cdef int[::indirect, ::contiguous] a15
cdef int[::generic, ::indirect_contiguous] a16
cdef int[::strided, ::indirect_contiguous] a17
cdef int[::indirect, ::indirect_contiguous] a18

cdef int[::generic, ::] a19
cdef int[::strided, :] a20
cdef int[::indirect, :] a21
cdef int[::generic_contiguous, :] a22
cdef int[::contiguous, :] a23
cdef int[::indirect_contiguous, :] a24

