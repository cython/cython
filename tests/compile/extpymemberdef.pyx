# mode: compile

cdef class Spam:
    pub i8 c
    pub i32 i
    pub i64 l
    pub u8 uc
    pub u32 ui
    pub u64 ul
    pub f32 f
    pub f64 d
    pub char *s
    cdef readonly char[42] a
    pub object o
    cdef readonly i32 r
    cdef readonly Spam e
