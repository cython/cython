# mode: error

cimport cython
from cython cimport view






cdef signed short[::1, ::1] both
cdef signed short[::1, :, :, ::1] both2
cdef signed char[::2] err0
cdef signed char[::-100] err1
cdef signed char[::-1] err2
cdef long long[01::1, 0x01:, '0'   :, False:] fort_contig0
cdef signed char[1::] bad_start
cdef unsigned long[:,:1] bad_stop
cdef unsigned long[:,::1,:] neither_c_or_f
cdef signed char[::1-1+1] expr_spec
cdef signed char[::blargh] bad_name
cdef double[::alist[0]['view'].full] expr_attribute

cdef object[::1, :] unconformable1 = object()
cdef object[:, ::1] unconformable2 = unconformable1

cdef int[::1, :] dtype_unconformable = object()
unconformable1 = dtype_unconformable

# These are INVALID
cdef int[::view.contiguous, ::1] a1
#cdef int[::view.generic_contiguous, ::1] a2

#cdef int[::view.contiguous, ::view.generic_contiguous] a3
#cdef int[::view.generic_contiguous, ::view.generic_contiguous] a4

cdef int[::view.contiguous, ::view.contiguous] a5
cdef int[:, ::view.contiguous, ::view.indirect_contiguous] a6

#cdef int[::view.generic_contiguous, ::view.contiguous] a7
#cdef int[::view.contiguous, ::view.generic_contiguous] a8

# These are VALID
cdef int[::view.indirect_contiguous, ::view.contiguous] a9

_ERRORS = u'''
11:25: Cannot specify an array that is both C and Fortran contiguous.
12:31: Cannot specify an array that is both C and Fortran contiguous.
13:19: Step must be omitted, 1, or a valid specifier.
14:20: Step must be omitted, 1, or a valid specifier.
15:20: Step must be omitted, 1, or a valid specifier.
16:17: Start must not be given.
17:18: Start must not be given.
18:22: Axis specification only allowed in the 'step' slot.
19:19: Fortran contiguous specifier must follow an indirect dimension
20:22: Invalid axis specification.
21:25: Invalid axis specification.
22:22: no expressions allowed in axis spec, only names and literals.
25:51: Memoryview 'object[::contiguous, :]' not conformable to memoryview 'object[:, ::contiguous]'.
28:36: Different base types for memoryviews (int, Python object)
31:9: Dimension may not be contiguous
37:9: Only one direct contiguous axis may be specified.
38:9:Only dimensions 3 and 2 may be contiguous and direct
'''
