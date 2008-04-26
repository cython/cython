cdef extern from *:
    ctypedef class __builtin__.list [ object PyListObject ]:
        pass

cdef class Sub2(list):
    cdef char character

cdef class Sub1(Sub2):
    cdef char character
