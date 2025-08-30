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

ctypedef int *intp
cdef intp[:, :] myarray

cdef int[:] a10 = <int[:10]> object()
cdef int[:] a11 = <int[:5.4]> <int *> 1

cdef struct Valid:
    int array[1][2][3][4][5][6][7][8]
cdef struct Invalid:
    int array[1][2][3][4][5][6][7][8][9]

cdef Valid[:] validslice
cdef Invalid[:] invalidslice

cdef int[:, :, :, :] four_D
four_D[None, None, None, None]
four_D[None, None, None, None, None]

cdef int[:, :, :, :, :, :, :, :] eight_D = object()

cdef double[:] m
print <long> &m

# These are VALID
cdef int[::view.indirect_contiguous, ::view.contiguous] a9
four_D[None, None, None]

_ERRORS = u'''
11:25: Cannot specify an array that is both C and Fortran contiguous.
12:31: Cannot specify an array that is both C and Fortran contiguous.
13:19: Step must be omitted, 1, or a valid specifier.
14:20: Step must be omitted, 1, or a valid specifier.
15:20: Step must be omitted, 1, or a valid specifier.
16:15: Start must not be given.
17:17: Start must not be given.
18:22: Axis specification only allowed in the 'step' slot.
19:18: Fortran contiguous specifier must follow an indirect dimension
20:22: Invalid axis specification.
21:19: Invalid axis specification.
22:22: no expressions allowed in axis spec, only names and literals.
25:37: Memoryview 'object[::1, :]' not conformable to memoryview 'object[:, ::1]'.
28:17: Different base types for memoryviews (int, Python object)
31:8: Dimension may not be contiguous
37:8: Only one direct contiguous axis may be specified.
38:8:Only dimensions 3 and 2 may be contiguous and direct
44:9: Invalid base type for memoryview slice: intp
46:35: Can only create cython.array from pointer or array
47:24: Cannot assign type 'double' to 'Py_ssize_t'
55:12: Invalid base type for memoryview slice: Invalid
58:6: More dimensions than the maximum number of buffer dimensions were used.
59:6: More dimensions than the maximum number of buffer dimensions were used.
61:8: More dimensions than the maximum number of buffer dimensions were used.
64:13: Cannot take address of memoryview slice
'''
