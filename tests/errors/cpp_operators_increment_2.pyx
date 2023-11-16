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

    # FIXME this is rejected as redeclared rather than an overload added
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
    cython.operator.postincrement(o_pre)  # TODO - should generate error
    cython.operator.postincrement(o_pre_nm)  # TODO should generate error
    cython.operator.preincrement(no)
    cython.operator.preincrement(o_post)  # TODO - this generates an error for the wrong reasons currently
    cython.operator.preincrement(o_post_nm)  # TODO - this generates an error for the wrong reasons currently

_ERRORS = """
36:19: Invalid operand type for '++' (NoIncrement)
39:19: Invalid operand type for '++' (NoIncrement)
40:19: Invalid operand type for '++' (OnlyPost)
41:19: Invalid operand type for '++' (OnlyPostNonMember)
"""
