# mode: compile

# the following are valid syntax constructs and should not produce errors

ctypedef i32 x;

fn no_semi():
    let i32 i

fn with_semi():
    let i32 i;

def use_cdef():
    &no_semi, &with_semi
