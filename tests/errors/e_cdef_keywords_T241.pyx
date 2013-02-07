# ticket: 241
# mode: error

cdef some_function(x, y):
    pass

cdef class A:
    cdef some_method(self, x, y=1):
        pass

from libc.string cimport strcmp

cdef extern from "string.h":
    char *strstr(char*, char*)


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

# ok
strcmp("abc", "cde")
strcmp("abc", s2="cde")
strcmp(s1="abc", s2="cde")
strcmp(s2="cde", s1="abc")

# nok
strcmp("abc", s1="cde")
strcmp("abc", s2="cde", s1="cde")
strcmp(s1="abc", s2="cde", s1="cde")
strcmp(s2="cde", s1="abc", s2="cde")

# ok
strstr("abc", "abcdef")

# nok
strstr("abc", char="abcdef")
strstr("abc", "abcdef", char="xyz")


_ERRORS = u"""
22:18: argument 'x' passed twice
23:18: argument 'x' passed twice
24:23: C function got unexpected keyword argument 'z'
25:18: C function got unexpected keyword argument 'z'
26:21: C function got unexpected keyword argument 'z'
27:25: C function got unexpected keyword argument 'z'
28:25: argument 'x' passed twice
29:25: argument 'x' passed twice
29:30: C function got unexpected keyword argument 'z'

39:18: argument 'x' passed twice
40:21: argument 'x' passed twice
41:21: argument 'y' passed twice
42:21: argument 'x' passed twice
42:26: argument 'y' passed twice
43:21: argument 'y' passed twice
43:26: argument 'x' passed twice
44:23: argument 'x' passed twice
45:21: C function got unexpected keyword argument 'z'
46:23: C function got unexpected keyword argument 'z'
47:20: argument 'x' passed twice
48:20: argument 'x' passed twice
49:25: argument 'x' passed twice

58:16: argument 's1' passed twice
59:26: argument 's1' passed twice
60:29: argument 's1' passed twice
61:29: argument 's2' passed twice

67:18: C function got unexpected keyword argument 'char'
68:28: C function got unexpected keyword argument 'char'
"""
