# mode: compile
# tag: fused

# This previously lead to a crash due to an empty module body.

ctypedef fused cinteger:
    i32
    i64
    isize
