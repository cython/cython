# mode: error

cimport cython
from cython.view cimport contig as foo, full as bar, follow
from cython cimport view
biz = cython.view.contig
foz = cython.view.full
adict = {'view': cython.view}
alist = [adict]

cdef signed short[::1, ::1] both
cdef signed short[::1, :, :, ::1] both2
cdef signed char[::2] err0
cdef signed char[::-100] err1
cdef signed char[::-1] err2
cdef long long[01::1, 0x01:, '0'   :, False:] fort_contig0
cdef signed char[1::] bad_start
cdef unsigned long[:,:1] bad_stop
cdef unsigned long[:,::1,:] neither_c_or_f
cdef signed char[::1, ::view.follow & view.direct] bad_f_contig
cdef signed char[::1, ::view.follow] bad_f_contig2
cdef signed char[::view.contig | view.direct] not_ampersand
cdef signed char[::view.ptr & view.direct] no_access_spec
cdef signed char[::1-1+1] expr_spec
cdef signed char[::blargh] bad_name
cdef double[::alist[0]['view'].full] expr_attribute
cdef double[::view.ptr & view.follow] no_single_follow

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
20:36: Invalid axis specification for a C/Fortran contiguous array.
21:28: Invalid axis specification for a C/Fortran contiguous array.
22:31: Invalid operator, only an ampersand '&' is allowed.
23:28: Invalid axis specification.
24:22: Invalid axis specification.
25:25: Invalid axis specification.
26:22: no expressions allowed in axis spec, only names (e.g. cython.view.contig).
27:12: Invalid use of the follow specifier.
'''
