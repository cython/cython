# mode: error

ctypedef int (*spamfunc)(int, char *) except 42
ctypedef int (*grailfunc)(int, char *) noexcept

cdef grailfunc grail
cdef spamfunc spam

grail = spam # type mismatch
spam = grail # type mismatch


_ERRORS = u"""
9:8: Cannot assign type 'spamfunc' to 'grailfunc'. Exception values are incompatible. Suggest adding 'noexcept' to type 'int (int, char *) except 42'.
10:7: Cannot assign type 'grailfunc' to 'spamfunc'. Exception values are incompatible.
"""
