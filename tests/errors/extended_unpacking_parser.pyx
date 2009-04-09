
# invalid syntax (as handled by the parser)

def syntax():
    *a, *b = 1,2,3,4,5

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
 5:4: more than 1 starred expression in assignment
10:4: too many values to unpack (expected 2, got 3)
13:4: need more than 1 value to unpack
16:4: need more than 0 values to unpack
19:4: need more than 0 values to unpack
22:4: need more than 0 values to unpack
23:4: need more than 1 value to unpack
26:6: need more than 1 value to unpack
"""
