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
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_extweakref.pyx:5:20: Special attribute __weakref__ cannot be exposed to Python
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_extweakref.pyx:8:22: Special attribute __weakref__ cannot be exposed to Python
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_extweakref.pyx:13:6: Illegal use of special attribute __weakref__
/Local/Projects/D/Pyrex/Source/Tests/Errors2/e_extweakref.pyx:14:2: Illegal use of special attribute __weakref__
"""
