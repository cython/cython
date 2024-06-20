# ticket: t518
# mode: compile

cdef extern from "cast_ctypedef_array_T518_helper.h":
    cdef struct __foo_struct:
       int i, j
    ctypedef __foo_struct foo_t[1]

    void foo_init(foo_t)
    void foo_clear(foo_t)

cdef foo_t value
foo_init(value)
foo_clear(value)

cdef void *pointer = <void*> value
foo_init(<foo_t>pointer)
foo_clear(<foo_t>pointer)
