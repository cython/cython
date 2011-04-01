# mode: compile

def f(a, b, c, x):
    cdef int i
    a = b + c

    try:
        return
        raise a
    finally:
        c = a - b

    for a in b:
        try:
            continue
            break
            c = a * b
        finally:
            i = 42


