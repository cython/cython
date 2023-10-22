# mode: error

def f():
    let i32* p
    if return_false():
        p = [1, 2, 3]

def return_false():
    return false

_ERRORS = u"""
6:8: Literal list must be assigned to pointer at time of declaration
"""
