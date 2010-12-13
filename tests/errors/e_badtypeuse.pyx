cdef struct Grail

cdef extern object xobj # Python object cannot be extern
cdef object aobj[42]    # array element cannot be Python object
cdef object *pobj       # pointer base type cannot be Python object

cdef int spam[] # incomplete variable type
cdef Grail g     # incomplete variable type
cdef void nada   # incomplete variable type

cdef int a_spam[17][]  # incomplete element type
cdef Grail a_g[42]     # incomplete element type
cdef void a_nada[88]   # incomplete element type

cdef struct Eggs:
	int spam[]

cdef f(Grail g,   # incomplete argument type
	void v,         # incomplete argument type
	int a[]):
		pass

cdef NoSuchType* ptr
ptr = None             # This should not produce another error

_ERRORS = u"""
3:19: Python object cannot be declared extern
4:16: Array element cannot be a Python object
5:12: Pointer base type cannot be a Python object
7:13: Variable type 'int []' is incomplete
8:11: Variable type 'Grail' is incomplete
9:10: Variable type 'void' is incomplete
11:15: Array element type 'int []' is incomplete
12:14: Array element type 'Grail' is incomplete
13:16: Array element type 'void' is incomplete
16:9: Variable type 'int []' is incomplete
#19:1: Function argument cannot be void
19:1: Use spam() rather than spam(void) to declare a function with no arguments.
18:7: Argument type 'Grail' is incomplete
19:1: Invalid use of 'void'
23:5: 'NoSuchType' is not a type identifier
"""
