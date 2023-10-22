# mode: compile

cdef i32 f() except -1:
    let list l
    let object x = (), y = (1,), z
    z = list
    l = list(x)
    l = list(*y)
    z = l.insert
    l.insert(17, 42)
    l.append(88)
    l.sort()
    l.reverse()
    z = l.as_tuple()
    return z is not None

def test():
    f()
