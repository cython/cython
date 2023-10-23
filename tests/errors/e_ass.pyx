# mode: error

fn void foo(obj):
    let i32 i1
    let char *p1
    let i32 *p2
    i1 = p1 # error
    p2 = obj # error

    obj = p2 # error


_ERRORS = u"""
7:9: Cannot assign type 'char *' to 'int'
8:9: Cannot convert Python object to 'int *'
10:10: Cannot convert 'int *' to Python object
"""
