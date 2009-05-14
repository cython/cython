# Ensure casting still works to void*

"""
>>> f()
('teststring', 'teststring')
"""

cdef extern from *:
    ctypedef void PyObject

def f():
    cdef void* p1
    cdef PyObject* p2
    a = "teststring"
    p1 = <void*>a
    p2 = <PyObject*>a
    return (<object>p1, <object>p2)
    
