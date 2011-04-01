# mode: compile

def f(a, b, c):
    cdef int i
    for a in b:
        i = 1
        continue
        i = 2
        break
        i = 3

    for i in b:
        i = 1

    for a in "spam":
        i = 1

    for a[b] in c:
        i = 1

    for a,b in c:
        i = 1

    for a in b,c:
        i = 1



