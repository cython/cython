import cython
from cython.cimports.libc.stdlib import free

@cython.cclass
class OwnedPointer:
    ptr: cython.p_void

    def __dealloc__(self):
        if self.ptr is not cython.NULL:
            free(self.ptr)

    @staticmethod
    @cython.cfunc
    def create(ptr: cython.p_void):
        p = OwnedPointer()
        p.ptr = ptr
        return p
