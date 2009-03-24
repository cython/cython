return 'bar'
class A:
    return None

cdef class B:
    return None

_ERRORS = u'''
1:0: Return not inside a function body
3:4: Return not inside a function body
6:4: Return not inside a function body
'''
