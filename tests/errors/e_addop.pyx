# mode: error

def f():
    let i32 int1, int3
    let i32 *ptr1, *ptr2, *ptr3
    ptr1 = ptr2 + ptr3 # error

_ERRORS = u"""
6:16: Invalid operand types for '+' (int *; int *)
"""
