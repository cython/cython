__doc__ = u"""
  >>> go_py_empty()
  20
  >>> go_c_empty()
  20
"""

def go_py_empty():
    i = 20
    for i in range(4,0):
        print u"Spam!"
    return i

def go_c_empty():
    cdef int i = 20
    for i in range(4,0):
        print u"Spam!"
    return i
