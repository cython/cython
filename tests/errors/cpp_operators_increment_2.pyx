# mode: error
# tag: cpp

cimport cython

cdef extern from *:
    cdef cppclass NoIncrement:
        pass

    cdef cppclass OnlyPre:
        OnlyPre operator++()

    cdef cppclass OnlyPreNonMember:
        pass

    OnlyPreNonMember operator++(OnlyPreNonMember)

    cdef cppclass OnlyPost:
        OnlyPost operator++(int)

    cdef cppclass OnlyPostNonMember:
        pass

    # FIXME this is redeclared rather than an overload added
    OnlyPostNonMember operator++(OnlyPostNonMember, int)


cdef void misuse_classes():
    # https://github.com/cython/cython/issues/4539
    # NoIncrement would mistakenly find the non-member operator++ for a different type
    cdef NoIncrement no
    cdef OnlyPre o_pre
    cdef OnlyPreNonMember o_pre_nm
    cdef OnlyPost o_post
    cdef OnlyPostNonMember o_post_nm
    cython.operator.postincrement(no)
    cython.operator.postincrement(o_pre)  # TODO - error message is wrong
    cython.operator.postincrement(o_pre_nm)
    cython.operator.preincrement(no)
    cython.operator.preincrement(o_post)
    cython.operator.preincrement(o_post_nm)

# TODO - not all the error messages are quite right (but they should all fail)
_ERRORS = """
36:19: '++' operator not defined for NoIncrement (Call with wrong number of arguments (expected 1, got 2))
36:19: Invalid operand type for '++' (NoIncrement)
37:19: '++' operator not defined for OnlyPre (Call with wrong number of arguments (expected 0, got 2))
37:19: Invalid operand type for '++' (OnlyPre)
38:19: '++' operator not defined for OnlyPreNonMember (Call with wrong number of arguments (expected 1, got 2))
38:19: Invalid operand type for '++' (OnlyPreNonMember)
39:19: '++' operator not defined for NoIncrement (Cannot assign type 'NoIncrement' to 'OnlyPreNonMember')
39:19: Invalid operand type for '++' (NoIncrement)
40:19: '++' operator not defined for OnlyPost (Cannot assign type 'OnlyPost' to 'OnlyPreNonMember')
40:19: Invalid operand type for '++' (OnlyPost)
41:19: '++' operator not defined for OnlyPostNonMember (Cannot assign type 'OnlyPostNonMember' to 'OnlyPreNonMember')
41:19: Invalid operand type for '++' (OnlyPostNonMember)
"""
