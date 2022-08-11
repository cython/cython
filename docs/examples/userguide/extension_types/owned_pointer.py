import cython
from cython.cimports.libc.stdlib import free

@cython.cclass
class OwnedPointer:
    ptr: cython.pointer(cython.void)

    def __dealloc__(self):
        if self.ptr is not cython.NULL:
            free(self.ptr)

    @staticmethod
    @cython.cfunc
    def create(ptr: cython.pointer(cython.void)):
        p = OwnedPointer()
        p.ptr = ptr
        return p
