"""
Tests accessing attributes of extension type variables
set to None

>>> obj = MyClass(2, 3)
>>> func(obj)
2
>>> func(None)
Traceback (most recent call last):
   ...
AttributeError: 'NoneType' object has no attribute 'a'

>>> checking(obj)
2
2
>>> checking(None)
var is None

>>> check_and_assign(obj)
Traceback (most recent call last):
   ...
AttributeError: 'NoneType' object has no attribute 'a'

"""

cdef class MyClass:
    cdef int a, b
    def __init__(self, a, b):
        self.a = a
        self.b = b

def func(MyClass var):
    print var.a

def some():
    return MyClass(4, 5)

def checking(MyClass var):
    state = (var is None)
    if not state:
        print var.a
    if var is not None:
        print var.a
    else:
        print "var is None"

def check_and_assign(MyClass var):
    if var is not None:
        print var.a
        var = None
        print var.a

