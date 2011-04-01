# mode: compile

def f(a, b, c, x):
    cdef int i
    a = b + c

    try:
        i = 1
        raise x
        i = 2
    except a:
        i = 3

    try:
        i = 1
    except a:
        i = 2
    except b:
        i = 3

    try:
        i = 1
    except a, b:
        i = 2

    try:
        i = 1
    except a:
        i = 2
    except:
        i = 3

    try:
        i = 1
    except (a, b), c[42]:
        i = 2

    for a in b:
        try:
            c = x * 42
        except:
            i = 17

    try:
        i = 1
    except:
        raise

def g(a, b, c, x):
    cdef int i
    a = b + c

    try:
        i = 1
        raise x
        i = 2
    except a:
        i = 3

    try:
        i = 1
    except a:
        i = 2
    except b:
        i = 3

    try:
        i = 1
    except a as b:
        i = 2

    try:
        i = 1
    except a:
        i = 2
    except:
        i = 3

    try:
        i = 1
    except (a, b) as c:
        i = 2
    except (b, a) as c:
        i = 3
    except:
        i = 4
    else:
        i = 5
