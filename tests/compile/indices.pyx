# mode: compile

cdef i32* a
cdef object x

fn i32 f(i32 i):
    print i
    return i

x[f(1)] = 3
a[f(1)] = 3

x[f(2)] += 4
a[f(2)] += 4

print x[1]
print a[1]

x[<object>f(1)] = 15
