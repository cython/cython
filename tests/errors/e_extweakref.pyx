cdef class C:
	cdef object __weakref__

cdef class D:
	cdef public object __weakref__

cdef class E:
	cdef readonly object __weakref__

cdef void f():
	cdef C c
	cdef object x
	x = c.__weakref__
	c.__weakref__ = x
_ERRORS = u"""
5:20: Illegal use of special attribute __weakref__
5:20: Illegal use of special attribute __weakref__
5:20: Illegal use of special attribute __weakref__
5:20: Special attribute __weakref__ cannot be exposed to Python
8:22: Illegal use of special attribute __weakref__
8:22: Special attribute __weakref__ cannot be exposed to Python
13:6: Illegal use of special attribute __weakref__
14:2: Illegal use of special attribute __weakref__
"""
