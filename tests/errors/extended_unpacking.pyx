
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
 7: 4: can use starred expression only as assignment target
 9: 4: can use starred expression only as assignment target
11: 4: can use starred expression only as assignment target
13: 4: can use starred expression only as assignment target
15: 5: can use starred expression only as assignment target
15: 9: can use starred expression only as assignment target
17:11: can use starred expression only as assignment target
17:24: can use starred expression only as assignment target

# syntax2()
23:11: more than 1 starred expression in assignment

# types()
29:15: Cannot coerce list to type 'int'
30:10: starred target must have Python object (list) type
"""
