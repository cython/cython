.. glossary::

   Extension type
      "Extension type" can refer to either a Cython class defined with ``cdef class`` or more generally to any Python type that is ultimately defined as a C struct (including most of the built-in types).
      
   Dynamic allocation
   Heap allocation
      A C variable allocated with ``malloc`` (in C) or ``new`` (in C++) is `allocated dynamically/heap allocated <https://en.wikipedia.org/wiki/C_dynamic_memory_allocation>`__. Its lifetime is until the user deletes it explicitly (with ``free`` in C or ``del`` in C++). This can be in a different function.

   pointer
      A **pointer** is a variable that stores the address of another variable (i.e. direct address of the memory location). They allow for dynamic memory allocation and deallocation. They can be used to build dynamic data structures. `Read more <https://en.wikipedia.org/wiki/Pointer_(computer_programming)#C_pointers>`__.
      
   Python object
      When using Python, the contents of every variable are a Python object (including Cython extension types). Key features of Python objects is that they are passed by reference and their lifetime of Python objects is managed automatically so that they are destroyed when no more references exist to them. In Cython they are distinct from C types, which are passed by value and whose lifetime is managed depending on if they are allocated on the stack or heap. To explicitly declare a Python object in Cython use ``cdef object``. Internally in C they are handled as ``PyObject*``.
      
   Stack allocation
      A C variable declared within a function as ``cdef SomeType a`` said to be allocated on the stack. It exists for the duration of the function only.
      
   Typed memoryview
      A useful Cython type for getting quick access to blocks of memory. A memoryview alone does not actually own any memory. However, it can be initialized with a Python object that has the `buffer protocol`_ (typically "array" types, for example a Numpy array). It keeps a reference to that Python object alive and provides quick access to the memory without needing to go through the Python ``__getitem__``/``__setitem__`` methods.

.. _buffer protocol: https://docs.python.org/3/c-api/buffer.html
