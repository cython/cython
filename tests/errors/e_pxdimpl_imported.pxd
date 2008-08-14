
cdef class A:
    cdef int test(self)

    # Should give error:
    def somefunc(self):
        pass

    # While this should *not* be an error...:
    def __getbuffer__(self, Py_buffer* info, int flags):
        pass
    # This neither:
    def __releasebuffer__(self, Py_buffer* info):
        pass

    # Terminate with an error to be sure the compiler is
    # not terminating prior to previous errors
    def terminate(self):
        pass

cdef extern from "foo.h":
    cdef class pxdimpl.B [object MyB]:
        def otherfunc(self):
            pass

