# mode: compile

cdef extern from "string.h":
    void memcpy(void* des, void* src, int size)

cdef void f():
    cdef float[3] f1
    cdef float* f2
    f2 = f1 + 1
    memcpy(f1, f2, 1)

f()
