# mode: compile

extern from *:
    ctypedef i32 intptr_t

fn i32 _is_aligned(void *ptr):
    return ((<intptr_t>ptr) & ((sizeof(i32))-1)) == 0

_is_aligned(NULL)
