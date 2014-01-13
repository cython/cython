# mode: compile

def f(obj, int i, double f, char *s1, char s2[]):
    pass

cdef g(obj, int i, double f, char *s1, char s2[]):
    pass

cdef do_g(object (*func)(object, int, double, char*, char*)):
    return func(1, 2, 3.14159, "a", "b")

do_g(&g)
