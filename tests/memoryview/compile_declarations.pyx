# mode: compile

cimport cython
# from cython.view cimport contig as foo, full as bar #, follow
from cython cimport view
from cython.view cimport (generic, strided, indirect,
                          contiguous, indirect_contiguous)

cdef char[:] one_dim
cdef char[:,:,:] three_dim
cdef unsigned int[::1, :] view1
cdef unsigned int[:, ::1] view2
cdef long long[::1, :, :, :] fort_contig
cdef unsigned long[:, :, :, ::1] c_contig
cdef unsigned short int[::1] c_and_fort
cdef unsigned long[:, :, :, ::0x0001] c_contig0

cdef int[::generic, ::generic] a1
cdef int[::strided, ::generic] a2
cdef int[::indirect, ::generic] a3
cdef int[::generic, ::strided] a4
cdef int[::strided, ::strided] a5
cdef int[::indirect, ::strided] a6
cdef int[::generic, ::indirect] a7
cdef int[::strided, ::indirect] a8
cdef int[::indirect, ::indirect] a9

cdef int[::generic, ::contiguous] a13
cdef int[::strided, ::contiguous] a14
cdef int[::indirect, ::contiguous] a15
cdef int[::generic, ::indirect_contiguous] a16
cdef int[::strided, ::indirect_contiguous] a17
cdef int[::indirect, ::indirect_contiguous] a18

cdef int[::generic, ::] a19
cdef int[::strided, :] a20
cdef int[::indirect, :] a21
cdef int[::contiguous, :] a23
cdef int[::indirect_contiguous, :] a24

cdef int[::indirect_contiguous, ::1] a25
cdef int[::indirect_contiguous, ::1, :] a26
cdef int[::indirect_contiguous, :, ::1] a27
cdef int[::indirect_contiguous, ::1, :] a28
cdef int[::indirect_contiguous, ::view.contiguous, :] a29
cdef int[::indirect_contiguous, :, ::view.contiguous] a30

cdef int[::indirect, ::1] a31
cdef int[::indirect, ::1, :] a32 = object()
cdef int[::indirect, :, ::1] a33 = object()
cdef int[::indirect, ::1, :] a34
cdef int[::indirect, ::view.contiguous, :] a35
cdef int[::indirect, :, ::view.contiguous] a36

cdef int[::1, :] my_f_contig = a32[0]
cdef int[:, ::1] my_c_contig = a33[0]

my_f_contig = a32[0, :, :]
my_c_contig = a33[0, :, :]

my_f_contig = a32[0, ...]
my_c_contig = a33[0, ...]

# Test casting to cython.view.array
cdef double[:, :] m1 = <double[:10, :10]> NULL
cdef double[:, :] m2 = <double[:10, :10:1]> NULL
cdef double[:, :] m3 = <double[:10:1, :10]> NULL

cdef double[:, :, :] m4 = <double[:10, :10, :10]> NULL
cdef double[:, :, :] m5 = <double[:10, :10, :10:1]> NULL
cdef double[:, :, :] m6 = <double[:10:1, :10, :10]> NULL
