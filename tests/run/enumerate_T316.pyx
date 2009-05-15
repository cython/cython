__doc__ = u"""
  >>> go_c_enumerate()
  0 1
  1 2
  2 3
  3 4

  >>> go_py_enumerate()
  0 1
  1 2
  2 3
  3 4

  >>> empty_c_enumerate()
  (55, 99)

  >>> go_c_enumerate_step()
  0 1
  1 3
  2 5

  >>> single_target_enumerate()
  0 1
  1 2
  2 3
  3 4

  >>> multi_enumerate()
  0 0 0 1
  1 1 1 2
  2 2 2 3
  3 3 3 4

"""

def go_py_enumerate():
    for i,k in enumerate(range(1,5)):
        print i, k

def go_c_enumerate():
    cdef int i,k
    for i,k in enumerate(range(1,5)):
        print i, k

def go_c_enumerate_step():
    cdef int i,k
    for i,k in enumerate(range(1,7,2)):
        print i, k

def empty_c_enumerate():
    cdef int i = 55, k = 99
    for i,k in enumerate(range(0)):
        print i, k
    return i, k

def single_target_enumerate():
    for t in enumerate(range(1,5)):
        print t[0], t[1]

def multi_enumerate():
    for a,(b,(c,d)) in enumerate(enumerate(enumerate(range(1,5)))):
        print a,b,c,d

def multi_c_enumerate():
    cdef int a,b,c,d
    for a,(b,(c,d)) in enumerate(enumerate(enumerate(range(1,5)))):
        print a,b,c,d
