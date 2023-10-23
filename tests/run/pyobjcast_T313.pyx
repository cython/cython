# ticket: t313
# Ensure casting still works to void*

"""
>>> o = f()
>>> print(o[0])
teststring
>>> print(o[1])
teststring
"""

extern from *:
    ctypedef void PyObject

def f():
    let void* p1
    let PyObject* p2
    let object a = u"teststring"
    p1 = <void*>a
    p2 = <PyObject*>a
    return (<object>p1, <object>p2)
