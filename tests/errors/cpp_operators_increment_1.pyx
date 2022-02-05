# mode: error
# tag: cpp

cimport cython

cdef extern from *:
    cdef cppclass NoIncrement:
        pass

    cdef cppclass OnlyPreNonMember:
        pass

    OnlyPreNonMember operator++(OnlyPreNonMember)

# Don't add to this testcase! it's to test the case that there is *one*
# non-member operator found for NoIncrement and that it should be discarded


cdef void misuse_classes():
    # https://github.com/cython/cython/issues/4539
    # NoIncrement would mistakenly find the non-member operator++ for a different type
    cdef NoIncrement no
    cython.operator.preincrement(no)

_ERRORS = """
23:19: '++' operator not defined for NoIncrement (Cannot assign type 'NoIncrement' to 'OnlyPreNonMember')
23:19: Invalid operand type for '++' (NoIncrement)
"""
