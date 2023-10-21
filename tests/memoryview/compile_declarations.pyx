# mode: compile

cimport cython
# from cython.view cimport contig as foo, full as bar #, follow
from cython cimport view
from cython.view cimport (generic, strided, indirect,
                          contiguous, indirect_contiguous)

cdef char[:] one_dim
cdef char[:, :, :] three_dim
cdef u32[::1, :] view1
cdef u32[:, ::1] view2
cdef i128[::1, :, :, :] fort_contig
cdef u64[:, :, :, ::1] c_contig
cdef u16[::1] c_and_fort
cdef u64[:, :, :, ::0x0001] c_contig0

cdef i32[::generic, ::generic] a1
cdef i32[::strided, ::generic] a2
cdef i32[::indirect, ::generic] a3
cdef i32[::generic, ::strided] a4
cdef i32[::strided, ::strided] a5
cdef i32[::indirect, ::strided] a6
cdef i32[::generic, ::indirect] a7
cdef i32[::strided, ::indirect] a8
cdef i32[::indirect, ::indirect] a9

cdef i32[::generic, ::contiguous] a13
cdef i32[::strided, ::contiguous] a14
cdef i32[::indirect, ::contiguous] a15
cdef i32[::generic, ::indirect_contiguous] a16
cdef i32[::strided, ::indirect_contiguous] a17
cdef i32[::indirect, ::indirect_contiguous] a18

cdef i32[::generic, ::] a19
cdef i32[::strided, :] a20
cdef i32[::indirect, :] a21
cdef i32[::contiguous, :] a23
cdef i32[::indirect_contiguous, :] a24

cdef i32[::indirect_contiguous, ::1] a25
cdef i32[::indirect_contiguous, ::1, :] a26
cdef i32[::indirect_contiguous, :, ::1] a27
cdef i32[::indirect_contiguous, ::1, :] a28
cdef i32[::indirect_contiguous, ::view.contiguous, :] a29
cdef i32[::indirect_contiguous, :, ::view.contiguous] a30

cdef i32[::indirect, ::1] a31
cdef i32[::indirect, ::1, :] a32 = object()
cdef i32[::indirect, :, ::1] a33 = object()
cdef i32[::indirect, ::1, :] a34
cdef i32[::indirect, ::view.contiguous, :] a35
cdef i32[::indirect, :, ::view.contiguous] a36

cdef i32[::1, :] my_f_contig = a32[0]
cdef i32[:, ::1] my_c_contig = a33[0]

my_f_contig = a32[0, :, :]
my_c_contig = a33[0, :, :]

my_f_contig = a32[0, ...]
my_c_contig = a33[0, ...]

# Test casting to cython.view.array
cdef f64[:, :] m1 = <f64[:10, :10]> NULL
cdef f64[:, :] m2 = <f64[:10, :10:1]> NULL
cdef f64[:, :] m3 = <f64[:10:1, :10]> NULL

cdef f64[:, :, :] m4 = <f64[:10, :10, :10]> NULL
cdef f64[:, :, :] m5 = <f64[:10, :10, :10:1]> NULL
cdef f64[:, :, :] m6 = <f64[:10:1, :10, :10]> NULL
