__doc__ = u"""
  >>> go_py()
  Spam!
  Spam!
  Spam!
  Spam!
  >>> go_py_ret()
  2

  >>> go_c()
  Spam!
  Spam!
  Spam!
  Spam!
  >>> go_c_ret()
  2

  >>> go_list()
  Spam!
  Spam!
  Spam!
  Spam!
  >>> go_list_ret()
  2

  >>> go_tuple()
  Spam!
  Spam!
  Spam!
  Spam!
  >>> go_tuple_ret()
  2

  >>> go_dict()
  Spam!
  Spam!
  Spam!
  Spam!
  >>> go_dict_ret()
  2
"""

def go_py():
    for i in range(4):
        print u"Spam!"

def go_py_ret():
    for i in range(4):
        if i > 1:
            return i

def go_c():
    cdef int i
    for i in range(4):
        print u"Spam!"

def go_c_ret():
    cdef int i
    for i in range(4):
        if i > 1:
            return i

def go_list():
    cdef list l = range(4)
    for i in l:
        print u"Spam!"

def go_list_ret():
    cdef list l = range(4)
    for i in l:
        if i > 1:
            return i
 
def go_tuple():
    cdef tuple t = tuple(range(4))
    for i in t:
        print u"Spam!"

def go_tuple_ret():
    cdef tuple t = tuple(range(4))
    for i in t:
        if i > 1:
            return i

def go_dict():
    cdef dict d = dict(zip(range(4), range(4)))
    for i in d:
        print u"Spam!"

def go_dict_ret():
    cdef dict d = dict(zip(range(4), range(4)))
    for i in d:
        if i > 1 and i < 3:
            return i
