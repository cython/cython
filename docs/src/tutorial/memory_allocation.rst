.. _memory_allocation:

*****************
Memory Allocation
*****************

.. include::
    ../two-syntax-variants-used

Dynamic memory allocation is mostly a non-issue in Python.  Everything is an
object, and the reference counting system and garbage collector automatically
return memory to the system when it is no longer being used.

When it comes to more low-level data buffers, Cython has special support for
(multi-dimensional) arrays of simple types via NumPy, memory views or Python's
stdlib array type.  They are full featured, garbage collected and much easier
to work with than bare pointers in C, while still retaining the speed and static
typing benefits.
See :ref:`array-array` and :ref:`memoryviews`.

In some situations, however, these objects can still incur an unacceptable
amount of overhead, which can then makes a case for doing manual memory
management in C.

Simple C values and structs (such as a local variable ``cdef double x`` / ``x: cython.double``) are
usually :term:`allocated on the stack<Stack allocation>` and passed by value, but for larger and more
complicated objects (e.g. a dynamically-sized list of doubles), the memory must
be :term:`manually requested and released<Dynamic allocation or Heap allocation>`.  C provides the functions :c:func:`malloc`,
:c:func:`realloc`, and :c:func:`free` for this purpose, which can be imported
in cython from ``clibc.stdlib``. Their signatures are:

.. code-block:: c

    void* malloc(size_t size)
    void* realloc(void* ptr, size_t size)
    void free(void* ptr)

A very simple example of malloc usage is the following:


.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/memory_allocation/malloc.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/memory_allocation/malloc.pyx

Note that the C-API functions for allocating memory on the Python heap
are generally preferred over the low-level C functions above as the
memory they provide is actually accounted for in Python's internal
memory management system.  They also have special optimisations for
smaller memory blocks, which speeds up their allocation by avoiding
costly operating system calls.

The C-API functions can be found in the ``cpython.mem`` standard
declarations file:

.. tabs::
    .. group-tab:: Pure Python

        .. code-block:: python

            from cython.cimports.cpython.mem import PyMem_Malloc, PyMem_Realloc, PyMem_Free

    .. group-tab:: Cython

        .. code-block:: cython

            from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

Their interface and usage is identical to that of the corresponding
low-level C functions.

One important thing to remember is that blocks of memory obtained with
:c:func:`malloc` or :c:func:`PyMem_Malloc` *must* be manually released
with a corresponding call to :c:func:`free` or :c:func:`PyMem_Free`
when they are no longer used (and *must* always use the matching
type of free function).  Otherwise, they won't be reclaimed until the
python process exits.  This is called a memory leak.

If a chunk of memory needs a larger lifetime than can be managed by a
``try..finally`` block, another helpful idiom is to tie its lifetime
to a Python object to leverage the Python runtime's memory management,
e.g.:

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/memory_allocation/some_memory.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/memory_allocation/some_memory.pyx
