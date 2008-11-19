__doc__ = u"""
  >>> go_py()
  Spam!
  Spam!
  Spam!
  Spam!

  >>> go_c()
  Spam!
  Spam!
  Spam!
  Spam!

  >>> go_list()
  Spam!
  Spam!
  Spam!
  Spam!

  >>> go_tuple()
  Spam!
  Spam!
  Spam!
  Spam!
"""

def go_py():
    for i in range(4):
        print u"Spam!"

def go_c():
    cdef int i
    for i in range(4):
        print u"Spam!"

def go_list():
    cdef list l = range(4)
    for i in l:
        print u"Spam!"

def go_tuple():
    cdef tuple t = tuple(range(4))
    for i in t:
        print u"Spam!"

def go_dict():
    cdef dict d = dict(zip(range(4), range(4)))
    for i in d:
        print u"Spam!"
