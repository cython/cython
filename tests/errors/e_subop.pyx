# mode: error

def f():
    let i32 int2
    let char *ptr1, *ptr2, *ptr3
    ptr1 = int2 - ptr3  # error
    ptr1 = ptr2 - ptr3  # error

_ERRORS = u"""
6:16: Invalid operand types for '-' (int; char *)
7:16: Cannot assign type 'ptrdiff_t' to 'char *'
"""
