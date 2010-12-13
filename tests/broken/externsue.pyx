cdef extern from "externsue.h":

    enum Eggs:
        runny, firm, hard

    struct Spam:
        int i

    union Soviet:
        char c

cdef extern Eggs e
cdef extern Spam s
cdef extern Soviet u

cdef void tomato():
    global e
    e = runny
    e = firm
    e = hard

