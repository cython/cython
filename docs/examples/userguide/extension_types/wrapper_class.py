import cython
from cython.cimports.libc.stdlib import malloc, free

# Example C struct
my_c_struct = cython.struct(
    a = cython.int,
    b = cython.int,
)

@cython.cclass
class WrapperClass:
    """A wrapper class for a C/C++ data structure"""
    _ptr: cython.pointer[my_c_struct]
    ptr_owner: cython.bint

    def __cinit__(self):
        self.ptr_owner = False

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not cython.NULL and self.ptr_owner is True:
            free(self._ptr)
            self._ptr = cython.NULL

    def __init__(self):
        # Prevent accidental instantiation from normal Python code
        # since we cannot pass a struct pointer into a Python constructor.
        raise TypeError("This class cannot be instantiated directly.")

    # Extension class properties
    @property
    def a(self):
        return self._ptr.a if self._ptr is not cython.NULL else None

    @property
    def b(self):
        return self._ptr.b if self._ptr is not cython.NULL else None

    @staticmethod
    @cython.cfunc
    def from_ptr(_ptr: cython.pointer[my_c_struct], owner: cython.bint=False) -> WrapperClass:
        """Factory function to create WrapperClass objects from
        given my_c_struct pointer.

        Setting ``owner`` flag to ``True`` causes
        the extension type to ``free`` the structure pointed to by ``_ptr``
        when the wrapper object is deallocated."""
        # Fast call to __new__() that bypasses the __init__() constructor.
        wrapper: WrapperClass  = WrapperClass.__new__(WrapperClass)
        wrapper._ptr = _ptr
        wrapper.ptr_owner = owner
        return wrapper

    @staticmethod
    @cython.cfunc
    def new_struct() -> WrapperClass:
        """Factory function to create WrapperClass objects with
        newly allocated my_c_struct"""
        _ptr: cython.pointer[my_c_struct] = cython.cast(
                cython.pointer[my_c_struct], malloc(cython.sizeof(my_c_struct)))
        if _ptr is cython.NULL:
            raise MemoryError
        _ptr.a = 0
        _ptr.b = 0
        return WrapperClass.from_ptr(_ptr, owner=True)
