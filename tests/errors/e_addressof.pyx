# mode: error

cdef class Ext:
    cdef int a
    cdef object o

def f(int a):
    cdef Ext e = Ext()
    x = &a  # ok

    cdef object o = &a  # pointer != object

    po1 = &o        # pointer to Python variable
    po2 = &o.xyz    # pointer to Python expression
    po3 = &e.o      # pointer to Python object
    po4 = &e.a      # ok (C attribute)

    po5 = &(o + 1)  # pointer to non-lvalue Python expression
    po6 = &(a + 1)  # pointer to non-lvalue C expression


_ERRORS="""
11:20: Cannot convert 'int *' to Python object
13:10: Cannot take address of Python variable 'o'
14:10: Cannot take address of Python object attribute 'xyz'
15:10: Cannot take address of Python object attribute 'o'
18:10: Taking address of non-lvalue (type Python object)
19:10: Taking address of non-lvalue (type long)
"""
