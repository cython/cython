cdef class Spam
cdef extern class external.Eggs
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_undefexttype.pyx:1:5: C class 'Spam' is declared but not defined
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_undefexttype.pyx:2:5: C class 'Eggs' is declared but not defined
"""
