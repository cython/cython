# mode: compile

cdef class Spam:
    cdef public i8 c
    cdef public i32 i
    cdef public i64 l
    cdef public u8 uc
    cdef public u32 ui
    cdef public u64 ul
    cdef public f32 f
    cdef public f64 d
    cdef public char *s
    cdef readonly char[42] a
    cdef public object o
    cdef readonly i32 r
    cdef readonly Spam e
