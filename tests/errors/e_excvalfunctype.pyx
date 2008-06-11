ctypedef int (*spamfunc)(int, char *) except 42
ctypedef int (*grailfunc)(int, char *)

cdef grailfunc grail
cdef spamfunc spam

grail = spam # type mismatch
spam = grail # type mismatch
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_excvalfunctype.pyx:7:28: Cannot assign type 'e_excvalfunctype.spamfunc' to 'e_excvalfunctype.grailfunc'
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_excvalfunctype.pyx:8:28: Cannot assign type 'e_excvalfunctype.grailfunc' to 'e_excvalfunctype.spamfunc'
"""
