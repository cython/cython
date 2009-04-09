
# invalid syntax (not handled by the parser)

def syntax1():
    a = b = c = d = e = f = g = h = i = 1 # prevent undefined names
    list_of_sequences = [[1,2], [3,4]]

    *a

    *1

    *"abc"

    *a*b

    [*a, *b]

    (a, b, *c, d, e, f, *g, h, i)

    for *a,*b in list_of_sequences:
        pass


_ERRORS = u"""
 8: 4: can use starred expression only as assignment target
10: 4: can use starred expression only as assignment target
12: 4: can use starred expression only as assignment target
14: 4: can use starred expression only as assignment target
16: 5: can use starred expression only as assignment target
16: 9: can use starred expression only as assignment target
18:11: can use starred expression only as assignment target
18:24: can use starred expression only as assignment target
20:11: more than 1 starred expression in assignment
"""
