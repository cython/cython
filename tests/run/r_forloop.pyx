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
  >>> go_c_int(1,5)
  Spam!
  Spam!
  >>> go_c_enumerate()
  True
  True
  True
  True
  >>> go_c_all()
  Spam!
  Spam!
  Spam!
  >>> go_c_all_exprs(1)
  Spam!
  >>> go_c_all_exprs(3)
  Spam!
  Spam!
  >>> go_c_const_exprs()
  Spam!
  Spam!
  >>> go_c_calc(2)
  Spam!
  Spam!
  >>> go_c_ret()
  2
  >>> go_c_calc_ret(2)
  6

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

  >>> global_result
  6
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

def go_c_enumerate():
    cdef int i,k
    for i,k in enumerate(range(4)):
        print i == k

def go_c_int(int a, int b):
    cdef int i
    for i in range(a,b,2):
        print u"Spam!"

def go_c_all():
    cdef int i
    for i in range(8,2,-2):
        print u"Spam!"

def go_c_all_exprs(x):
    cdef int i
    for i in range(4*x,2*x,-3):
        print u"Spam!"

def go_c_const_exprs():
    cdef int i
    for i in range(4*2+1,2*2,-2-1):
        print u"Spam!"

def f(x):
    return 2*x

def go_c_calc(x):
    cdef int i
    for i in range(2*f(x),f(x), -2):
        print u"Spam!"

def go_c_calc_ret(x):
    cdef int i
    for i in range(2*f(x),f(x), -2):
        if i < 2*f(x):
            return i

def go_c_ret():
    cdef int i
    for i in range(4):
        if i > 1:
            return i

def go_list():
    cdef list l = list(range(4))
    for i in l:
        print u"Spam!"

def go_list_ret():
    cdef list l = list(range(4))
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

# test global scope also
global_result = None
cdef int i
for i in range(4*2+1,2*2,-2-1):
    if i < 7:
        global_result = i
        break
