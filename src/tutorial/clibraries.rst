Using C libraries
=================

Apart from writing fast code, one of the main use cases of Cython is
to call external C libraries from Python code.  As Cython code
compiles down to C code itself, it is actually trivial to call C
functions directly in the code.  You may have already seen this in the
simple tutorial on calling C functions.  The following gives a
complete example for using (and wrapping) an external C library in
Cython code, including appropriate error handling and considerations
about designing a suitable API for Python and Cython code.

Imagine you need an efficient way to store integer values in a FIFO
queue.  Since memory really matters, and the values are actually
coming from C code, you cannot afford to create and store Python
``int`` objects in a list or deque.  So you look out for a queue
implementation in C.

After some web search, you find the C-algorithms library [CAlg]_ and
decide to use its double ended queue implementation.  To make the
handling easier, however, you decide to wrap it in a Python extension
type that can encapsulate all memory management.

The C API of the queue implementation, which is defined in the header
file ``libcalg/queue.h``, essentially looks like this::

    /* file: queue.h */

    typedef struct _Queue Queue;
    typedef void *QueueValue;

    Queue *queue_new(void);
    void queue_free(Queue *queue);

    int queue_push_head(Queue *queue, QueueValue data);
    QueueValue queue_pop_head(Queue *queue);
    QueueValue queue_peek_head(Queue *queue);

    int queue_push_tail(Queue *queue, QueueValue data);
    QueueValue queue_pop_tail(Queue *queue);
    QueueValue queue_peek_tail(Queue *queue);

    int queue_is_empty(Queue *queue);

To get started, the first step is to redefine the C API in a ``.pxd``
file, say, ``cqueue.pxd``::

    # file: cqueue.pxd

    cdef extern from "libcalg/queue.h":
        ctypedef struct Queue:
            pass
        ctypedef void* QueueValue

        Queue* queue_new()
        void queue_free(Queue* queue)

        int queue_push_head(Queue* queue, QueueValue data)
        QueueValue  queue_pop_head(Queue* queue)
        QueueValue queue_peek_head(Queue* queue)

        int queue_push_tail(Queue* queue, QueueValue data)
        QueueValue queue_pop_tail(Queue* queue)
        QueueValue queue_peek_tail(Queue* queue)

        bint queue_is_empty(Queue* queue)

Note how these declarations are almost identical to the header file
declarations, so you can often just copy them over.  One noteworthy
difference is the first line.  ``Queue`` is in this case used as an
*opaque handle*; only the library that is called knows what is really
inside.  Since no Cython code needs to know the contents of the
struct, we do not need to declare its contents, so we simply provide
an empty definition (as we do not want to declare the ``_Queue`` type
which is referenced in the C header) [#]_.

.. [#] There's a subtle difference between ``cdef struct Queue: pass``
       and ``ctypedef struct Queue: pass``.  The former declares a
       type which is referenced in C code as ``struct Queue``, while
       the latter is referenced in C as ``Queue``.  This is a C
       language quirk that Cython is not able to hide.  Most modern C
       libraries use the ``ctypedef`` kind of struct.

Another exception is the last line.  The integer return value of the
``queue_is_empty`` method is actually a C boolean value, i.e. it is
either zero or non-zero, indicating if the queue is empty or not.
This is best expressed by Cython's ``bint`` type, which is a normal
``int`` type when used in C but maps to Python's boolean values
``True`` and ``False`` when converted to a Python object.

Next, we need to design the Queue class that should wrap the C queue.
It will live in a file called ``queue.pyx``. [#]_

.. [#] Note that the name of the ``.pyx`` file must be different from
       the ``cqueue.pxd`` file with declarations from the C library,
       as both do not describe the same code.  A ``.pxd`` file next to
       a ``.pyx`` file with the same name defines exported
       declarations for code in the ``.pyx`` file.

Here is a first start for the Queue class::

    # file: queue.pyx

    cimport cqueue

    cdef class Queue:
        cdef cqueue.Queue _c_queue
        def __cinit__(self):
            self._c_queue = cqueue.queue_new()

Note that it says ``__cinit__`` rather than ``__init__``.  While
``__init__`` is available as well, it is not guaranteed to be run (for
instance, one could create a subclass and forget to call the
ancestor's constructor).  Because not initializing C pointers often
leads to crashing the Python interpreter without leaving as much as a
stack trace, Cython provides ``__cinit__`` which is *always* called on
construction.  However, as ``__cinit__`` is called during object
construction, ``self`` is not fully constructed yet, and one must
avoid doing anything with ``self`` but assigning to ``cdef`` fields.

Note also that the above method takes no parameters, although subtypes
may want to accept some.  Although it is guaranteed to get called, the
no-arguments ``__cinit__()`` method is a special case here as it does
not prevent subclasses from adding parameters as they see fit.  If
parameters are added they must match those of any declared
``__init__`` method.

Before we continue implementing the other methods, it is important to
understand that the above implementation is not safe.  In case
anything goes wrong in the call to ``queue_new()``, this code will
simply swallow the error, so we will likely run into a crash later on.
According to the documentation of the ``queue_new()`` function, the
only reason why the above can fail is due to insufficient memory.  In
that case, it will return ``NULL``, whereas it would normally return a
pointer to the new queue.

The normal Python way to get out of this is to raise an exception, but
in this specific case, allocating a new exception instance may
actually fail because we are running out of memory.  Luckily, CPython
provides a function ``PyErr_NoMemory()`` that safely raises the right
exception for us.  We can thus change the init function as follows::

    cimport cpython.exc    # standard cimport from CPython's C-API
    cimport cqueue

    cdef class Queue:
        cdef cqueue.Queue _c_queue
        def __cinit__(self):
            self._c_queue = cqueue.queue_new()
            if self._c_queue is NULL:
	        cpython.exc.PyErr_NoMemory()

The ``cpython`` package contains pre-defined ``.pxd`` files that ship
with Cython.  If you need any CPython C-API functions, you can cimport
them from this package.  See Cython's ``Cython/Includes/`` source
package for a complete list of ``.pxd`` files, including parts of the
standard C library.

The next thing to do is to clean up when the Queue instance is no
longer used (i.e. all references to it have been deleted).  To this
end, CPython provides a callback that Cython makes available as a
special method ``__dealloc__()``.  In our case, all we have to do is
to free the C Queue, but only if we succeeded in initialising it in
the init method::

        def __dealloc__(self):
            if self._c_queue is not NULL:
                cqueue.queue_free(self._c_queue)

At this point, we have a working Cython module that we can test.  To
compile it, we need to configure a ``setup.py`` script for distutils.
Reusing the basic script from the main tutorial::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("queue", ["queue.pyx"])]
    ) 

We can extend this script to include the necessary setup for building
against the external C library.  Assuming it's installed in the normal
places (e.g. under ``/usr/lib`` and ``/usr/include`` on a Unix-like
system), we could simply change the extension setup from

::

    ext_modules = [Extension("queue", ["queue.pyx"])]

to

::

    ext_modules = [
        Extension("queue", ["queue.pyx"],
                  libraries=["calg"])
        ]

If it is not installed in a 'normal' location, users can provide the
required parameters externally by passing appropriate C compiler
flags, such as::

    CFLAGS="-I/usr/local/otherdir/calg/include"  \
    LDFLAGS="-L/usr/local/otherdir/calg/lib"     \
        python setup.py build_ext -i

Once we have compiled the module for the first time, we can now import
it and instantiate a new Queue::

    PYTHONPATH=. python -c 'import queue.Queue as Q ; Q()'

However, this is all our Queue class can do so far, so let's make it
more usable.

Before implementing the public interface of this class, it is good
practice to look at what interfaces Python offers, e.g. in its
``list`` or ``collections.deque`` classes.  Since we only need a FIFO
queue, it's enough to provide the methods ``append()``, ``peek()`` and
``pop()``, and additionally an ``extend()`` method to add multiple
values at once.  Also, since we already know that all values will be
coming from C, it's better to provide only ``cdef`` methods for now,
and to give them a straight C interface.

In C, it is common for data structures to store data as a ``void*`` to
whatever data item type.  Since we only want to store ``int`` values,
which usually fit into the size of a pointer type, we can avoid
additional memory allocations through a trick: we cast our ``int`` values
to ``void*`` and vice versa, and store the value directly as the
pointer value.

Here is a simple implementation for the ``append()`` method::

        cdef append(self, int value):
            cqueue.queue_push_tail(self._c_queue, <void*>value)

Again, the same error handling considerations as for the
``__cinit__()`` method apply, so that we end up with this
implementation instead::

        cdef append(self, int value):
            if not cqueue.queue_push_tail(self._c_queue,
                                          <void*>value):
                cpython.exc.PyErr_NoMemory()

Adding an ``extend()`` method should now be straight forward::

    cdef extend(self, int* values, Py_ssize_t count):
        """Append all ints to the queue.
        """
        cdef Py_ssize_t i
        for i in range(count):
            if not cqueue.queue_push_tail(
                    self._c_queue, <void*>values[i]):
                cpython.exc.PyErr_NoMemory()

This becomes handy when reading values from a NumPy array, for
example.

So far, we can only add data to the queue.  The next step is to write
the two methods to get the first element: ``peek()`` and ``pop()``,
which provide read-only and destructive read access respectively::

    cdef int peek(self):
        return <int>cqueue.queue_peek_head(self._c_queue)

    cdef int pop(self):
        return <int>cqueue.queue_pop_head(self._c_queue)

Simple enough.  Now, what happens when the queue is empty?  According
to the documentation, the functions return a ``NULL`` pointer, which
is typically not a valid value.  Since we are simply casting to and
from ints, we cannot distinguish anymore if the return value was
``NULL`` because the queue was empty or because the value stored in
the queue was ``0``.  However, in Cython code, we would expect the
first case to raise an exception, whereas the second case should
simply return ``0``.  To deal with this, we need to special case this
value, and check if the queue really is empty or not::

    cdef int peek(self) except? 0:
        cdef int value = \
          <int>cqueue.queue_peek_head(self._c_queue)
        if value == 0:
            # this may mean that the queue is empty, or
            # that it happens to contain a 0 value
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
        return value

The ``except? 0`` declaration is worth explaining.  If the function
was a Python function returning a Python object value, CPython would
simply return ``NULL`` instead of a Python object to indicate a raised
exception, which would immediately be propagated by the surrounding
code.  The problem is that any ``int`` value is a valid queue item
value, so there is no way to explicitly indicate an error to the
calling code.

The only way CPython (and Cython) can deal with this situation is to
call ``PyErr_Occurred()`` when returning from a function to check if
an exception was raised, and if so, propagate the exception.  This
obviously has a performance penalty.  Cython therefore allows you to
indicate which value is explicitly returned in the case of an
exception, so that the surrounding code only needs to check for an
exception when receiving this exact value.  All other values will be
accepted almost without a penalty.

Now that the ``peek()`` method is implemented, the ``pop()`` method
also needs adaptation.  Since it removes a value from the queue,
however, it is not enough to test if the queue is empty *after* the
removal.  Instead, we must test it on entry::

    cdef int pop(self) except? 0:
        if cqueue.queue_is_empty(self._c_queue):
            raise IndexError("Queue is empty")
        return <int>cqueue.queue_pop_head(self._c_queue)

Lastly, we can provide the Queue with an emptiness indicator in the
normal Python way by defining the ``__bool__()`` special method (note
that Python 2 calls this method ``__nonzero__``, whereas Cython code
can use both)::

    def __bool__(self):
        return not cqueue.queue_is_empty(self._c_queue)

Note that this method returns either ``True`` or ``False`` as we
declared the return type of the ``queue_is_empty`` function as
``bint``.

Now that the implementation is complete, you may want to write some
tests for it to make sure it works correctly.  Especially doctests are
very nice for this purpose, as they provide some documentation at the
same time.  To enable doctests, however, you need a Python API that
you can call.  C methods are not visible from Python code, and thus
not callable from doctests.

A quick way to provide a Python API for the class is to change the
methods from ``cdef`` to ``cpdef``.  This will let Cython generate two
entry points, one that is callable from normal Python code using the
Python call semantics and Python objects as arguments, and one that is
callable from C code with fast C semantics and without requiring
intermediate argument conversion from or to Python types.

The following listing shows the complete implementation that uses
``cpdef`` methods where possible::

    cimport cqueue
    cimport cpython.exc

    cdef class Queue:
        cdef cqueue.Queue* _c_queue
        def __cinit__(self):
            self._c_queue = cqueue.queue_new()
            if self._c_queue is NULL:
                cpython.exc.PyErr_NoMemory()

        def __dealloc__(self):
            if self._c_queue is not NULL:
                cqueue.queue_free(self._c_queue)

        cpdef append(self, int value):
            if not cqueue.queue_push_tail(self._c_queue,
                                          <void*>value):
                cpython.exc.PyErr_NoMemory()

        cdef extend(self, int* values, Py_ssize_t count):
            cdef Py_ssize_t i
            for i in xrange(count):
                if not cqueue.queue_push_tail(
                        self._c_queue, <void*>values[i]):
                    cpython.exc.PyErr_NoMemory()

        cpdef int peek(self) except? 0:
            cdef int value = \
                <int>cqueue.queue_peek_head(self._c_queue)
            if value == 0:
                # this may mean that the queue is empty,
                # or that it happens to contain a 0 value
                if cqueue.queue_is_empty(self._c_queue):
                    raise IndexError("Queue is empty")
            return value

        cdef int pop(self) except? 0:
            if cqueue.queue_is_empty(self._c_queue):
                raise IndexError("Queue is empty")
            return <int>cqueue.queue_pop_head(self._c_queue)

        def __bool__(self):
            return not cqueue.queue_is_empty(self._c_queue)

The ``cpdef`` feature is obviously not available for the ``extend()``
method, as the method signature is incompatible with Python argument
types.  However, if wanted, we can rename the C-ish ``extend()``
method to e.g. ``c_extend()``, and write a new ``extend()`` method
instead that accepts an arbitrary Python iterable::

        cdef c_extend(self, int* values, Py_ssize_t count):
            cdef Py_ssize_t i
            for i in range(count):
                if not cqueue.queue_push_tail(
                        self._c_queue, <void*>values[i]):
                    cpython.exc.PyErr_NoMemory()

        cpdef extend(self, values):
            for value in values:
                self.append(value)

As a quick test with numbers from 0 to 9999 on the author's machine
indicates, using this Queue from Cython code with C ``int`` values is
about five times as fast as using it from Cython code with Python
values, almost eight times faster than using it from Python code in a
Python loop, and still more than twice as fast as using Python's
highly optimised ``collections.deque`` type from Cython code with
Python integers.

.. [CAlg] Simon Howard, C Algorithms library, http://c-algorithms.sourceforge.net/
