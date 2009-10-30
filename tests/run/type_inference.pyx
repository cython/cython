# cython: infer_types = True


from cython cimport typeof

def simple():
    """
    >>> simple()
    """
    i = 3
    assert typeof(i) == "long", typeof(i)
    x = 1.41
    assert typeof(x) == "double", typeof(x)
    xptr = &x
    assert typeof(xptr) == "double *", typeof(xptr)
    xptrptr = &xptr
    assert typeof(xptrptr) == "double **", typeof(xptrptr)
    b = b"abc"
    assert typeof(b) == "char *", typeof(b)
    s = "abc"
    assert typeof(s) == "str object", typeof(s)
    u = u"xyz"
    assert typeof(u) == "unicode object", typeof(u)
    L = [1,2,3]
    assert typeof(L) == "list object", typeof(L)
    t = (4,5,6)
    assert typeof(t) == "tuple object", typeof(t)

def multiple_assignments():
    """
    >>> multiple_assignments()
    """
    a = 3
    a = 4
    a = 5
    assert typeof(a) == "long"
    b = a
    b = 3.1
    b = 3.14159
    assert typeof(b) == "double"
    c = a
    c = b
    c = [1,2,3]
    assert typeof(c) == "Python object"

def arithmatic():
    """
    >>> arithmatic()
    """
    a = 1 + 2
    assert typeof(a) == "long"
    b = 1 + 1.5
    assert typeof(b) == "double"
    c = 1 + <object>2
    assert typeof(c) == "Python object"
    d = "abc %s" % "x"
    assert typeof(d) == "Python object"
    
def cascade():
    """
    >>> cascade()
    """
    a = 1.0
    b = a + 2
    c = b + 3
    d = c + 4
    assert typeof(d) == "double"
    e = a + b + c + d
    assert typeof(e) == "double"

def cascaded_assignment():
    a = b = c = d = 1.0
    assert typeof(a) == "double"
    assert typeof(b) == "double"
    assert typeof(c) == "double"
    assert typeof(d) == "double"
    e = a + b + c + d
    assert typeof(e) == "double"

def increment():
    """
    >>> increment()
    """
    a = 5
    a += 1
    assert typeof(a) == "long"

def loop():
    """
    >>> loop()
    """
    for a in range(10):
        pass
    assert typeof(a) == "long"

    b = 1.0
    for b in range(5):
        pass
    assert typeof(b) == "double"

    for c from 0 <= c < 10 by .5:
        pass
    assert typeof(c) == "double"

    for d in range(0, 10L, 2):
        pass
    assert typeof(a) == "long"
