# mode: error

cdef class C:
	cdef dict __dict__
	cdef object __weakref__

cdef class D:
	cdef public dict __dict__
	cdef public object __weakref__

cdef class E:
	cdef readonly dict __dict__
	cdef readonly object __weakref__

cdef void f():
	cdef C c = C()
	cdef dict x
	cdef object y
	x = c.__dict__
	c.__dict__ = x
	y = c.__weakref__
	c.__weakref__ = y

_ERRORS = u"""
8:18: Illegal use of special attribute __dict__
8:18: Illegal use of special attribute __dict__
8:18: Illegal use of special attribute __dict__
8:18: Special attribute __dict__ cannot be exposed to Python
9:20: Illegal use of special attribute __weakref__
9:20: Illegal use of special attribute __weakref__
9:20: Illegal use of special attribute __weakref__
9:20: Special attribute __weakref__ cannot be exposed to Python
12:20: Illegal use of special attribute __dict__
12:20: Special attribute __dict__ cannot be exposed to Python
13:22: Illegal use of special attribute __weakref__
13:22: Special attribute __weakref__ cannot be exposed to Python
19:6: Illegal use of special attribute __dict__
20:2: Illegal use of special attribute __dict__
21:6: Illegal use of special attribute __weakref__
22:2: Illegal use of special attribute __weakref__
"""
