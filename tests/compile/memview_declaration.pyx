cimport cython
from cython.view cimport contig as foo, full as bar, follow
from cython cimport view

cdef char[:] one_dim
cdef char[:,:,:] three_dim
cdef unsigned int[::1, :] view1
cdef unsigned int[:, ::1] view2
cdef long long[::1, :, :, :] fort_contig
cdef unsigned long[:, :, :, ::1] c_contig
cdef unsigned short int[::1] c_and_fort
cdef long long[0x0::0x1, 00:, -0   :,0 :] fort_contig0
cdef unsigned long[0:, 0:, 0:, 0::0x0001] c_contig0

cdef float[::foo & bar, ::cython.view.direct & cython.view.follow] view4
cdef int[::view.full & foo] view3
cdef int[::view.ptr & follow] view1000
