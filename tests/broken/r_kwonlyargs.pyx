def pd(d):
    l = []
    i = d.items()
    i.sort()
    for kv in i:
        l.append("%r: %r" % kv)
    return "{%s}" % ", ".join(l)

def c(a, b, c):
    print "a =", a, "b =", b, "c =", c

def d(a, b, *, c = 88):
    print "a =", a, "b =", b, "c =", c

def e(a, b, c = 88, **kwds):
    print "a =", a, "b =", b, "c =", c, "kwds =", pd(kwds)

def f(a, b, *, c, d = 42):
    print "a =", a, "b =", b, "c =", c, "d =", d

def g(a, b, *, c, d = 42, e = 17, f, **kwds):
    print "a =", a, "b =", b, "c =", c, "d =", d, "e =", e, "f =", f, "kwds =", pd(kwds)

def h(a, b, *args, c, d = 42, e = 17, f, **kwds):
    print "a =", a, "b =", b, "args =", args, "c =", c, "d =", d, "e =", e, "f =", f, "kwds =", pd(kwds)
