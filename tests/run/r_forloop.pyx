__doc__ = u"""
  >>> go_py()
  Spam!
  Spam!
  Spam!
  Spam!
  Spam!

  >>> go_c()
  Spam!
  Spam!
  Spam!
  Spam!
  Spam!
"""

def go_py():
    for i in range(5):
        print u"Spam!"

def go_c():
    cdef int i
    for i in range(5):
        print u"Spam!"
