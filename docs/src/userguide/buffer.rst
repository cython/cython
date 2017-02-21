.. _buffer:

Implementing the buffer protocol
================================

Cython objects can expose memory buffers to Python code
by implementing the "buffer protocol".
This chapter shows how to implement the protocol
and make use of the memory managed by an extension type from NumPy.


A matrix class
--------------

The following Cython/C++ code implements a matrix of floats,
where the number of columns is fixed at construction time
but rows can be added dynamically.

::

    # matrix.pyx
    from libcpp.vector cimport vector

    cdef class Matrix:
        cdef unsigned ncols
        cdef vector[float] v

        def __cinit__(self, unsigned ncols):
            self.ncols = ncols

        def add_row(self):
            """Adds a row, initially zero-filled."""
            self.v.extend(self.ncols)

There are no methods to do anything productive with the matrices' contents.
We could implement custom ``__getitem__``, ``__setitem__``, etc. for this,
but instead we'll use the buffer protocol to expose the matrix's data to Python
so we can use NumPy to do useful work.

Implementing the buffer protocol requires adding two methods,
``__getbuffer__`` and ``__releasebuffer__``,
which Cython handles specially.

::

    from cpython cimport Py_buffer
    from libcpp.vector cimport vector

    cdef class Matrix:
        cdef Py_ssize_t ncols
        cdef Py_ssize_t shape[2]
        cdef Py_ssize_t strides[2]
        cdef vector[float] v

        def __cinit__(self, Py_ssize_t ncols):
            self.ncols = ncols

        def add_row(self):
            """Adds a row, initially zero-filled."""
            self.v.extend(self.ncols)

        def __getbuffer__(self, Py_buffer *buffer, int flags):
            cdef Py_ssize_t itemsize = sizeof(self.v[0])

            self.shape[0] = self.v.size() / self.ncols
            self.shape[1] = self.ncols

            # Stride 1 is the distance, in bytes, between two items in a row;
            # this is the distance between two adjacent items in the vector.
            # Stride 0 is the distance between the first elements of adjacent rows.
            self.strides[1] = <Py_ssize_t>(  <char *>&(self.v[1])
                                           - <char *>&(self.v[0]))
            self.strides[0] = self.ncols * self.strides[1]

            buffer.buf = <char *>&(self.v[0])
            buffer.format = 'f'                     # float
            buffer.internal = NULL                  # see References
            buffer.itemsize = itemsize
            buffer.len = self.v.size() * itemsize   # product(shape) * itemsize
            buffer.ndim = 2
            buffer.obj = self
            buffer.readonly = 0
            buffer.shape = self.shape
            buffer.strides = self.strides
            buffer.suboffsets = NULL                # for pointer arrays only

        def __releasebuffer__(self, Py_buffer *buffer):
            pass

The method ``Matrix.__getbuffer__`` fills a descriptor structure,
called a ``Py_buffer``, that is defined by the Python C-API.
It contains a pointer to the actual buffer in memory,
as well as metadata about the shape of the array and the strides
(step sizes to get from one element or row to the next).
Its ``shape`` and ``strides`` members are pointers
that must point to arrays of type and size ``Py_ssize_t[ndim]``.
These arrays have to stay alive as long as any buffer views the data,
so we store them on the ``Matrix`` object as members.

The code is not yet complete, but we can already compile it
and test the basic functionality.

::

    >>> from matrix import Matrix
    >>> import numpy as np
    >>> m = Matrix(10)
    >>> np.asarray(m)
    array([], shape=(0, 10), dtype=float32)
    >>> m.add_row()
    >>> a = np.asarray(m)
    >>> a[:] = 1
    >>> m.add_row()
    >>> a = np.asarray(m)
    >>> a
    array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]], dtype=float32)

Now we can view the ``Matrix`` as a NumPy ``ndarray``,
and modify its contents using standard NumPy operations.


Memory safety and reference counting
------------------------------------

The ``Matrix`` class as implemented so far is unsafe.
The ``add_row`` operation can move the underlying buffer,
which invalidates any NumPy (or other) view on the data.
If you try to access values after an ``add_row`` call,
you'll get outdated values or a segfault.

This is where ``__releasebuffer__`` comes in.
We can add a reference count to each matrix,
and lock it for mutation whenever a view exists.

::

    cdef class Matrix:
        # ...
        cdef int view_count

        def __cinit__(self, Py_ssize_t ncols):
            self.ncols = ncols
            self.view_count = 0

        def add_row(self):
            if self.view_count > 0:
                raise ValueError("can't add row while being viewed")
            self.v.resize(self.v.size() + self.ncols)

        def __getbuffer__(self, Py_buffer *buffer, int flags):
            # ... as before

            self.view_count += 1

        def __releasebuffer__(self, Py_buffer *buffer):
            self.view_count -= 1


Flags
-----
We skipped some input validation in the code.
The ``flags`` argument to ``__getbuffer__`` comes from ``np.asarray``
(and other clients) and is an OR of boolean flags
that describe the kind of array that is requested.
Strictly speaking, if the flags contain ``PyBUF_ND``, ``PyBUF_SIMPLE``,
or ``PyBUF_F_CONTIGUOUS``, ``__getbuffer__`` must raise a ``BufferError``.
These macros can be ``cimport``'d from ``cpython.buffer``.

(The matrix-in-vector structure actually conforms to ``PyBUF_ND``,
but that would prohibit ``__getbuffer__`` from filling in the strides.
A single-row matrix is F-contiguous, but a larger matrix is not.)


References
----------

The buffer interface used here is set out in
:PEP:`3118`, Revising the buffer protocol.

A tutorial for using this API from C is on Jake Vanderplas's blog,
`An Introduction to the Python Buffer Protocol
<https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/>`_.

Reference documentation is available for
`Python 3 <https://docs.python.org/3/c-api/buffer.html>`_
and `Python 2 <https://docs.python.org/2.7/c-api/buffer.html>`_.
The Py2 documentation also describes an older buffer protocol
that is no longer in use;
since Python 2.6, the :PEP:`3118` protocol has been implemented,
and the older protocol is only relevant for legacy code.
