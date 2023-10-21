from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

cdef class SomeMemory:
    cdef f64* data

    def __cinit__(self, usize number):
        # allocate some memory (uninitialised, may contain arbitrary data)
        self.data = <f64*> PyMem_Malloc(number * sizeof(f64))
        if not self.data:
            raise MemoryError()

    def resize(self, usize new_number):
        # Allocates new_number * sizeof(double) bytes,
        # preserving the current content and making a best-effort to
        # reuse the original data location.
        mem = <f64*> PyMem_Realloc(self.data, new_number * sizeof(f64))
        if not mem:
            raise MemoryError()
        # Only overwrite the pointer if the memory was really reallocated.
        # On error (mem is NULL), the originally memory has not been freed.
        self.data = mem

    def __dealloc__(self):
        PyMem_Free(self.data)  # no-op if self.data is NULL
