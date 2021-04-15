# ticket: t208

def go_py_empty():
    """
    >>> go_py_empty()
    20
    """
    i = 20
    for i in range(4,0):
        print u"Spam!"
    return i

def go_c_empty():
    """
    >>> go_c_empty()
    20
    """
    cdef int i = 20
    for i in range(4,0):
        print u"Spam!"
    return i
