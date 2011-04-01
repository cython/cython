# mode: compile

cdef extern from "string.h":
    void memcpy(void* des, void* src, int size)

cdef void f():
    cdef float f1[3]
    cdef float* f2
    f2 = f1 + 1
    memcpy(f1, f2, 1)

f()
