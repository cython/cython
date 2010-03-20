# 7.5 Errors <errno.h>

cdef extern from "errno.h" nogil:

    enum: EDOM
    enum: EILSEQ
    enum: ERANGE

    int errno

