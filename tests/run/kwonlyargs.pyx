def c(a, b, c):
    z = 33

def d(a, b, *, c = 88):
    z = 44

def e(a, b, c = 88, **kwds):
    z = 55

def f(a, b, *, c, d = 42):
    z = 66

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    z = 77

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    z = 88
