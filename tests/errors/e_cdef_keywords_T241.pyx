# ticket: t241
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
22:17: argument 'x' passed twice
23:17: argument 'x' passed twice
24:22: C function got unexpected keyword argument 'z'
25:17: C function got unexpected keyword argument 'z'
26:20: C function got unexpected keyword argument 'z'
27:24: C function got unexpected keyword argument 'z'
28:24: argument 'x' passed twice
29:24: argument 'x' passed twice
29:29: C function got unexpected keyword argument 'z'

39:17: argument 'x' passed twice
40:20: argument 'x' passed twice
41:20: argument 'y' passed twice
42:20: argument 'x' passed twice
42:25: argument 'y' passed twice
43:20: argument 'y' passed twice
43:25: argument 'x' passed twice
44:22: argument 'x' passed twice
45:20: C function got unexpected keyword argument 'z'
46:22: C function got unexpected keyword argument 'z'
47:19: argument 'x' passed twice
48:19: argument 'x' passed twice
49:24: argument 'x' passed twice

58:14: argument 's1' passed twice
59:24: argument 's1' passed twice
60:27: argument 's1' passed twice
61:27: argument 's2' passed twice

67:14: C function got unexpected keyword argument 'char'
68:24: C function got unexpected keyword argument 'char'
"""
