cdef enum E:
    a

cdef enum G:
    b

cdef void f():
    cdef E e
    cdef G g
    cdef int i, j
    cdef float f, h
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
