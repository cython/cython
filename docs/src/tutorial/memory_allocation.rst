.. highlight:: cython

.. _memory_allocation:

*****************
Memory Allocation
*****************

Dynamic memory allocation is mostly a non-issue in Python.
Everything is an object, and the reference counting system and garbage collector
automatically return memory to the system when it is no longer being used.

Objects can be used in Cython as well, but sometimes this incurs a certain
amount of overhead.  In C, simple values and structs
(such as a local variable ``cdef double x``) are allocated on the stack and
passed by value, but for larger more complicated objects
(e.g. a dynamically-sized list of doubles) memory must be
manually requested and released.
C provides the functions ``malloc``, ``realloc``, and ``free`` for this purpose,
which can be imported in cython from ``clibc.stdlib``. Their signatures are::

    void* malloc(size_t size)
    void* realloc(void* ptr, size_t size)
    void free(void* ptr)

A very simple example of malloc usage is the following::

    import random
    from libc.stdlib cimport malloc, free

    def random_noise(int number=1):
        cdef int i
        # allocate number * sizeof(double) bytes of memory
        cdef double *my_array = <double *>malloc(number * sizeof(double))
        if not my_array:
            raise MemoryError()

        try:
            ran = random.normalvariate
            for i in range(number):
                my_array[i] = ran(0,1)

            return [ my_array[i] for i in range(number) ]
        finally:
            # return the previously allocated memory to the system
            free(my_array)

One important thing to remember is that blocks of memory obtained with malloc
*must* be manually released with free when one is done with them or it won't
be reclaimed until the python process exits. This is called a memory leak.
If a chuck of memory needs a larger lifetime then can be managed by a
``try..finally`` block, another helpful idiom is to tie its lifetime to a
Python object to leverage the Python runtime's memory management, e.g.::

  cdef class SomeMemory:
  
      cdef doube* data
      
      def __init__(self, number):
          # allocate some memory (filled with random data)
          self.data = <double*> malloc(number * sizeof(double))
          if self.data == NULL:
              raise MemoryError()
    
      def resize(self, new_number):
          # Allocates new_number * sizeof(double) bytes,
          # preserving the contents and making a best-effort to
          # re-use the original data location.
          self.data = <double*> realloc(self.data, new_number * sizeof(double))
          
      def __dealloc__(self, number):
          if self.data != NULL:
              free(self.data)

It should be noted that Cython has special support for (multi-dimensional)
arrays of simple types via NumPy and memory views which are more full featured
and easier to work with than pointers while still retaining the speed/static
typing benefits. 