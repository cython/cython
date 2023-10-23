cdef extern from "externsue.h":
    enum Eggs:
        Runny, Firm, Hard

    struct Spam:
        i32 i

    union Soviet:
        i8 c

cdef extern Eggs e
cdef extern Spam s
cdef extern Soviet u

fn void tomato():
    global e
    e = Runny
    e = Firm
    e = Hard
