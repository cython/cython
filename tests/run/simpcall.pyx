def f(x, y):
    x = y

cdef void g(int i, float f, char *p):
    f = i

cdef h(int i, obj):
    i = obj

def z(a, b, c):
    f()
    f(a)
    f(a, b)
    f(a, b,)
    g(1, 2.0, "spam")
    g(a, b, c)
    h(42, "eggs")
    