# mode: compile

ctypedef enum someenum_t:
    ENUMVALUE_1
    ENUMVALUE_2

cdef somefunction(someenum_t val):
    if val == ENUMVALUE_1:
        pass

somefunction(ENUMVALUE_1)
somefunction(ENUMVALUE_2)
