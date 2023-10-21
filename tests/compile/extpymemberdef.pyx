# mode: compile

cdef class Spam:
    cdef pub i8 c
    cdef pub i32 i
    cdef pub i64 l
    cdef pub u8 uc
    cdef pub u32 ui
    cdef pub u64 ul
    cdef pub f32 f
    cdef pub f64 d
    cdef pub char *s
    cdef readonly char[42] a
    cdef pub object o
    cdef readonly i32 r
    cdef readonly Spam e
