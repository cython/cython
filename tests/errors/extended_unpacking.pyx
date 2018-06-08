# mode: error

# invalid syntax (not handled by the parser)

def syntax1():
    a = b = c = d = e = f = g = h = i = 1 # prevent undefined names

    *a

    *1

    *"abc"

    *a*b

    [*a, *b]

    (a, b, *c, d, e, f, *g, h, i)
    [a, b, *c, d, e, f, *g, h, i]
    {a, b, *c, d, e, f, *g, h, i}


def syntax2():
    list_of_sequences = [[1,2], [3,4]]

    for *a,*b in list_of_sequences:
        pass


def types(l):
    cdef int a,b
    a, *b = (1,2,3,4)
    a, *b = l


_ERRORS = u"""
# syntax1()
 8: 4: starred expression is not allowed here
10: 4: starred expression is not allowed here
12: 4: starred expression is not allowed here
14: 4: starred expression is not allowed here

# syntax2()
26:11: more than 1 starred expression in assignment

# types()
32:15: Cannot coerce list to type 'int'
33:8: starred target must have Python object (list) type
"""
