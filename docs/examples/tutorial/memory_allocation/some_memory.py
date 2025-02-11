from cython.cimports.cpython.mem import PyMem_Malloc, PyMem_Realloc, PyMem_Free

@cython.cclass
class SomeMemory:
    data: cython.p_double

    def __cinit__(self, number: cython.size_t):
        # allocate some memory (uninitialised, may contain arbitrary data)
        self.data = cython.cast(cython.p_double, PyMem_Malloc(
            number * cython.sizeof(cython.double)))
        if not self.data:
            raise MemoryError()

    def resize(self, new_number: cython.size_t):
        # Allocates new_number * sizeof(double) bytes,
        # preserving the current content and making a best-effort to
        # reuse the original data location.
        mem = cython.cast(cython.p_double, PyMem_Realloc(
            self.data, new_number * cython.sizeof(cython.double)))
        if not mem:
            raise MemoryError()
        # Only overwrite the pointer if the memory was really reallocated.
        # On error (mem is NULL), the originally memory has not been freed.
        self.data = mem

    def __dealloc__(self):
        PyMem_Free(self.data)  # no-op if self.data is NULL
