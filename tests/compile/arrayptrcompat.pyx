# mode: compile

cdef enum E:
    Z

fn void f():
    let i32 *p
    let void *v
    let i32[5] a
    let i32 i = 0
    let E e = Z
    p = a
    v = a
    p = a + i
    p = a + e
    p = i + a
    p = e + a
    p = a - i
    p = a - e

f()
