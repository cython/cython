# mode: error
# tag: werror, charptr, conversion, temp

s = b"abc"

cdef char* cptr

cptr = s

cptr = s + b"cba"

_ERRORS = """
 8:8: Obtaining char* from externally modifiable global Python value
10:9: Obtaining char* from temporary Python value
"""
