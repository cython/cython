# ticket: t518
# mode: compile

extern from "cast_ctypedef_array_T518_helper.h":
    struct __foo_struct:
       i32 i, j
    ctypedef __foo_struct foo_t[1]

    fn void foo_init(foo_t)
    fn void foo_clear(foo_t)

cdef foo_t value
foo_init(value)
foo_clear(value)

cdef void *pointer = <void*> value
foo_init(<foo_t>pointer)
foo_clear(<foo_t>pointer)
