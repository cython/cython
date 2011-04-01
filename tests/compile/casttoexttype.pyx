# mode: compile

cdef extern class external.Spam:
    pass

cdef void foo(object x):
    pass

cdef void blarg(void *y, object z):
    foo(<Spam>y)
    foo(<Spam>z)

blarg(<void*>None, None)
