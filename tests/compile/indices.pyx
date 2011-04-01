# mode: compile

cdef int* a
cdef object x

cdef int f(int i):
    print i
    return i

x[f(1)] = 3
a[f(1)] = 3

x[f(2)] += 4
a[f(2)] += 4

print x[1]
print a[1]

x[<object>f(1)] = 15
