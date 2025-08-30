# mode: compile
# tag: fused

# This previously lead to a crash due to an empty module body.

ctypedef fused cinteger:
    int
    long
    Py_ssize_t
