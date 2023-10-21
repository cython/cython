# mode: compile

cdef extern from "string.h":
    void memcpy(void* des, void* src, i32 size)

cdef void f():
    cdef f32[3] f1
    cdef f32* f2
    f2 = f1 + 1
    memcpy(f1, f2, 1)

f()
