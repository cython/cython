cdef extern from "setjmp.h" nogil:
    ctypedef struct jmp_buf:
        pass
    int setjmp(jmp_buf STATE)
    void longjmp(jmp_buf STATE, int VALUE)
