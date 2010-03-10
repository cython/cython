
# wrong size RHS (as handled by the parser)

def length1():
    a, b = [1,2,3]

def length2():
    a, b = [1]

def length3():
    a, b = []

def length4():
    a, *b = []

def length5():
    a, *b, c = []
    a, *b, c = [1]

def length_recursive():
    *(a, b), c  = (1,2)


_ERRORS = u"""
 5:4: too many values to unpack (expected 2, got 3)
 8:4: need more than 1 value to unpack
11:4: need more than 0 values to unpack
14:4: need more than 0 values to unpack
17:4: need more than 0 values to unpack
18:4: need more than 1 value to unpack
21:6: need more than 1 value to unpack
"""
