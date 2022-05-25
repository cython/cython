# mode: error
# tag: werror, charptr, conversion, temp, py_unicode_strings

cdef bytes c_s = b"abc"
s = b"abc"

cdef char* cptr

# constant => ok
cptr = b"xyz"

# global cdef variable => ok
cptr = c_s

# pyglobal => warning
cptr = s

# temp => error
cptr = s + b"cba"

# indexing => error (but not clear enough to make it a compiler error)
cptr = s[0]
cdef char* x = <char*>s[0]

# slicing => error
cptr = s[:2]


cdef unicode  c_u = u"abc"
u = u"abc"

cdef Py_UNICODE* cuptr

# constant => ok
cuptr = u"xyz"

# global cdef variable => ok
cuptr = c_u

# pyglobal => warning
cuptr = u

# temp => error
cuptr = u + u"cba"


# coercion in conditional expression => ok
boolval = list(u)
cptr = c_s if boolval else c_s

# temp in conditional expression => error
cptr = s + b'x' if boolval else s + b'y'


_ERRORS = """
16:7: Obtaining 'char *' from externally modifiable global Python value
19:9: Storing unsafe C derivative of temporary Python reference
#22:8: Storing unsafe C derivative of temporary Python reference
#23:5: Storing unsafe C derivative of temporary Python reference
#23:15: Casting temporary Python object to non-numeric non-Python type
26:8: Storing unsafe C derivative of temporary Python reference
41:8: Obtaining 'Py_UNICODE *' from externally modifiable global Python value
44:10: Storing unsafe C derivative of temporary Python reference
52:7: Storing unsafe C derivative of temporary Python reference
52:7: Unsafe C derivative of temporary Python reference used in conditional expression
"""
