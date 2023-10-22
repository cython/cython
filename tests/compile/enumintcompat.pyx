# mode: compile

cdef enum E:
    a

cdef enum G:
    b

cdef void f():
    let E e=a
    let G g=b
    let i32 i, j=0
    let f32 f, h=0
    i = j | e
    i = e | j
    i = j ^ e
    i = j & e
    i = j << e
    i = j >> e
    i = j + e
    i = j - e
    i = j * e
    i = j / e
    i = j % e
    # f = j ** e # Cython prohibits this
    i = e + g
    f = h
    i = ~a
    i = -a

f()
