# mode: error

ctypedef int (*spamfunc)(int, char *) except 42
ctypedef int (*grailfunc)(int, char *) noexcept

cdef grailfunc grail
cdef spamfunc spam

grail = spam # type mismatch
spam = grail # type mismatch


_ERRORS = u"""
9:8: Cannot assign type 'spamfunc' (alias of 'int (*)(int, char *) except 42') to 'grailfunc' (alias of 'int (*)(int, char *) noexcept'). Exception values are incompatible. Suggest adding 'noexcept' to the type of 'spam'.
10:7: Cannot assign type 'grailfunc' (alias of 'int (*)(int, char *) noexcept') to 'spamfunc' (alias of 'int (*)(int, char *) except 42'). Exception values are incompatible.
"""
