# mode: error

cpdef str a = "123"
cpdef b = 2

cdef class C:
    cpdef float c

def func():
    cpdef d=C()
    return d

_ERRORS = """
3:6: Variables can not be cpdef
4:6: Variables can not be cpdef
7:10: Variables can not be cpdef
10:10: Variables can not be cpdef
"""
