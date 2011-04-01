# mode: compile

def f(a, b):
    cdef int i = 5

    while a:
        x = 1

    while a+b:
        x = 1

    while i:
        x = 1
    else:
        x = 2

    while i:
        x = 1
        break
        x = 2
    else:
        x = 3

    while i:
        x = 1
        continue
        x = 2

