# ticket: 241
# mode: error

cdef some_function(x, y):
    pass

cdef class A:
    cdef some_method(self, x, y=1):
        pass

# ok
some_function(1, 2)
some_function(1, y=2)

# nok
some_function(1, x=1)
some_function(1, x=2, y=2)
some_function(1, y=2, z=3)
some_function(1, z=3)
some_function(1, 2, z=3)
some_function(x=1, y=2, z=3)
some_function(x=1, y=2, x=1)
some_function(x=1, y=2, x=1, z=3)

cdef A a = A()
# ok
a.some_method(1)
a.some_method(1, 2)
a.some_method(1, y=2)
a.some_method(x=1, y=2)

# nok
a.some_method(1, x=1)
a.some_method(1, 2, x=1)
a.some_method(1, 2, y=2)
a.some_method(1, 2, x=1, y=2)
a.some_method(1, 2, y=2, x=1)
a.some_method(1, y=2, x=1)
a.some_method(1, 2, z=3)
a.some_method(1, y=2, z=3)
a.some_method(x=1, x=1)
a.some_method(x=1, x=1, y=2)
a.some_method(x=1, y=2, x=1)


_ERRORS = u"""
16:18: argument 'x' passed twice
17:18: argument 'x' passed twice
18:23: C function got unexpected keyword argument 'z'
19:18: C function got unexpected keyword argument 'z'
20:21: C function got unexpected keyword argument 'z'
21:25: C function got unexpected keyword argument 'z'
22:25: argument 'x' passed twice
23:25: argument 'x' passed twice
23:30: C function got unexpected keyword argument 'z'
33:18: argument 'x' passed twice
34:21: argument 'x' passed twice
35:21: argument 'y' passed twice
36:21: argument 'x' passed twice
36:26: argument 'y' passed twice
37:21: argument 'y' passed twice
37:26: argument 'x' passed twice
38:23: argument 'x' passed twice
39:21: C function got unexpected keyword argument 'z'
40:23: C function got unexpected keyword argument 'z'
41:20: argument 'x' passed twice
42:20: argument 'x' passed twice
43:25: argument 'x' passed twice
"""
