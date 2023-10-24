# mode: error

def f():
    let i32 int1, int2
    let char *ptr
    int1 = int2 | ptr # error

_ERRORS = u"""
6:16: Invalid operand types for '|' (int; char *)
"""
