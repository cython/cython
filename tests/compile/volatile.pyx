# mode: compile

cdef volatile i32 x = 1

cdef const volatile char* greeting1 = "hello world"
cdef volatile const char* greeting2 = "goodbye"


extern from "stdlib.h":
    volatile void* malloc(usize)

fn volatile i64* test(volatile usize s):
    let volatile i64* arr = <i64*><volatile i64*>malloc(s)
    return arr

test(64)
