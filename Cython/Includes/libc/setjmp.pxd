extern from "<setjmp.h>" nogil:
    ctypedef struct jmp_buf:
        pass
    int setjmp(jmp_buf state)
    void longjmp(jmp_buf state, i32 value)

    ctypedef struct sigjmp_buf:
        pass
    int sigsetjmp(sigjmp_buf state, i32 savesigs)
    void siglongjmp(sigjmp_buf state, i32 value)
