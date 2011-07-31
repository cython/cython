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
cdef int[::view.generic_contiguous, ::1] a2

cdef int[::view.contiguous, ::view.generic_contiguous] a3
cdef int[::view.generic_contiguous, ::view.generic_contiguous] a4

cdef int[::view.contiguous, ::view.contiguous] a5
cdef int[:, ::view.contiguous, ::view.indirect_contiguous] a6

cdef int[::view.generic_contiguous, ::view.contiguous] a7
cdef int[::view.contiguous, ::view.generic_contiguous] a8

# These are VALID
cdef int[::view.indirect_contiguous, ::view.contiguous] a9

_ERRORS = u'''
11:25: Cannot specify an array that is both C and Fortran contiguous.
12:31: Cannot specify an array that is both C and Fortran contiguous.
13:19: Only the value 1 (one) or valid axis specification allowed in the step slot.
14:20: Only the value 1 (one) or valid axis specification allowed in the step slot.
15:20: Only the value 1 (one) or valid axis specification allowed in the step slot.
16:17: there must be nothing or the value 0 (zero) in the start slot.
17:18: there must be nothing or the value 0 (zero) in the start slot.
18:22: Axis specification only allowed in the 'stop' slot.
19:23: The value 1 (one) may appear in the first or last axis specification only.
20:22: Invalid axis specification.
21:25: Invalid axis specification.
22:22: no expressions allowed in axis spec, only names and literals.
25:51: Memoryview 'object[::contiguous, :]' not conformable to memoryview 'object[:, ::contiguous]'.
28:36: Different base types for memoryviews (int, Python object)
31:15: Invalid axis specification for a C/Fortran contiguous array.
32:15: Invalid axis specification for a C/Fortran contiguous array.
34:9: Generic contiguous cannot be combined with direct contiguous
35:9: Generic contiguous cannot be combined with direct contiguous
37:9: Only one direct contiguous axis may be specified.
38:9: Indirect contiguous dimensions must precede direct contiguous
40:9: Generic contiguous cannot be combined with direct contiguous
41:9: Generic contiguous cannot be combined with direct contiguous
'''
