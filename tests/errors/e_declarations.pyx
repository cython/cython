# mode: error

cdef extern void fa[5]()
cdef extern i32 af()[5]
cdef extern i32 ff()()

fn void f():
    let void *p
    let i32 (*h)()
    h = <i32 ()()>f  # this is an error
    h = <i32 (*)()>f  # this is OK


_ERRORS = u"""
3:20: Template arguments must be a list of names
3:20: Template parameter not a type
5:18: Function cannot return a function
10:13: Function cannot return a function
10:8: Cannot cast to a function type
"""
