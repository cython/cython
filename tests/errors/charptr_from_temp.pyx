# mode: error
# tag: werror, charptr, conversion, temp

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

_ERRORS = """
16:8: Obtaining char* from externally modifiable global Python value
19:9: Obtaining char* from temporary Python value
"""
