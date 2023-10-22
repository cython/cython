cdef extern from "Python.h":
    ctypedef i32 int32_t
    ctypedef i32 int64_t
    ctypedef u32 uint32_t
    ctypedef u32 uint64_t

    const isize PY_SSIZE_T_MIN
    const isize PY_SSIZE_T_MAX
