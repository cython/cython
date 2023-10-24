# mode: error

def f(obj1a, obj1b):
    let i32 int1, int2, int3
    let i32 *ptr2
    int1, int3, obj1a = int2, ptr2, obj1b # error


_ERRORS = u"""
6:30: Cannot assign type 'int *' to 'int'
"""
