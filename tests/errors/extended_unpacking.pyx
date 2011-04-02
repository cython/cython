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
 8: 4: can use starred expression only as assignment target
10: 4: can use starred expression only as assignment target
12: 4: can use starred expression only as assignment target
14: 4: can use starred expression only as assignment target
16: 5: can use starred expression only as assignment target
16: 9: can use starred expression only as assignment target
18:11: can use starred expression only as assignment target
18:24: can use starred expression only as assignment target

# syntax2()
24:11: more than 1 starred expression in assignment

# types()
30:15: Cannot coerce list to type 'int'
31:10: starred target must have Python object (list) type
"""
