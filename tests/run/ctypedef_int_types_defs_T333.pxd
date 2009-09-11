cdef extern from "ctypedef_int_types_chdr_T333.h":
    ctypedef int SChar     ## "signed char"
    ctypedef int UChar     ## "unsigned char"
    ctypedef int SShort    ## "signed short"
    ctypedef int UShort    ## "unsigned short"
    ctypedef int SInt      ## "signed int"
    ctypedef int UInt      ## "unsigned int"
    ctypedef int SLong     ## "signed long"
    ctypedef int ULong     ## "unsigned long"
    ctypedef int SLongLong ## "signed PY_LONG_LONG"
    ctypedef int ULongLong ## "unsigned PY_LONG_LONG"

cdef extern from *:
    ctypedef int ExtSInt "signed short"
    ctypedef int ExtUInt "unsigned short"
