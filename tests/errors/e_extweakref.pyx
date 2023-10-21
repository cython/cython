# mode: error

cdef class C:
	cdef object __weakref__

cdef class D:
	cdef pub object __weakref__

cdef class E:
	cdef readonly object __weakref__

cdef void f():
	cdef C c = C()
	cdef object x
	x = c.__weakref__
	c.__weakref__ = x
_ERRORS = u"""
7:17: Illegal use of special attribute __weakref__
7:17: Illegal use of special attribute __weakref__
7:17: Illegal use of special attribute __weakref__
7:17: Special attribute __weakref__ cannot be exposed to Python
10:22: Illegal use of special attribute __weakref__
10:22: Special attribute __weakref__ cannot be exposed to Python
15:6: Illegal use of special attribute __weakref__
16:2: Illegal use of special attribute __weakref__
"""
