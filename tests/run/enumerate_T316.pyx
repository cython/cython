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

  >>> multi_c_enumerate()
  0 0 0 1
  1 1 1 2
  2 2 2 3
  3 3 3 4

  >>> py_enumerate_break(1,2,3,4)
  0 1
  :: 0 1

  >>> py_enumerate_return()
  :: 55 99
  >>> py_enumerate_return(1,2,3,4)
  0 1

  >>> py_enumerate_continue(1,2,3,4)
  0 1
  1 2
  2 3
  3 4
  :: 3 4

  >>> py_enumerate_dict({})
  :: 55 99
  >>> py_enumerate_dict(dict(a=1, b=2, c=3))
  0 a
  1 c
  2 b
  :: 2 b

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

def py_enumerate_dict(dict d):
    cdef int i = 55
    k = 99
    for i,k in enumerate(d):
        print i, k
    print u"::", i, k

def py_enumerate_break(*t):
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        break
    print u"::", i, k

def py_enumerate_return(*t):
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        return
    print u"::", i, k

def py_enumerate_continue(*t):
    i,k = 55,99
    for i,k in enumerate(t):
        print i, k
        continue
    print u"::", i, k

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
