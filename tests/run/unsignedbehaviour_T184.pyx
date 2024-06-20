# ticket: t184

"""
>>> c_call()
(-10, 10)
>>> py_call()
(-10, 10)
>>> loop()
19
>>> rangelist()
[-3, -2, -1, 0, 1, 2]
"""

cdef c_g(int a, int b):
    return (a, b)

def py_g(a, b):
    return (a, b)

def c_call():
    cdef unsigned int i = 10
    return c_g(-i, i)

def py_call():
    cdef unsigned int i = 10
    return py_g(-i, i)

def loop():
    cdef unsigned int i = 10
    times = 0
    for x in range(-i,i):
        times += 1
    return times

def rangelist():
    cdef unsigned int i = 3
    return list(range(-i, i))
