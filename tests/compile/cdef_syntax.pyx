# mode: compile

# the following are valid syntax constructs and should not produce errors

ctypedef i32 x;

cdef no_semi():
    cdef i32 i

cdef with_semi():
    cdef i32 i;

def use_cdef():
    &no_semi, &with_semi
