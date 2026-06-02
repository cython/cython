.. _cython_and_gil:

Cython and the GIL
==================

Python has a global lock (:term:`the GIL <Global Interpreter Lock or GIL>`)
to ensure that data related to the Python interpreter is not corrupted.
It is *sometimes* useful to release this lock in Cython when you are not
accessing Python data.

There are two occasions when you may want to release the GIL:

#. Using :ref:`Cython's parallelism mechanism <parallel>`. The contents of 
   a ``prange`` loop for example are required to be ``nogil``.

#. If you want other (external) Python threads to be able to run at the same time.

    #. if you have a large computationally/IO-intensive block that doesn't need the
       GIL then it may be "polite" to release it, just to benefit users of your code
       who want to do multi-threading. However, this is mostly useful rather than necessary.

    #. (very, very occasionally) in long-running Cython code that never calls into the
       Python interpreter, it can sometimes be useful to briefly release the GIL with a 
       short ``with nogil: pass`` block. This is because Cython doesn't release it 
       spontaneously (unlike the Python interpreter), so if you're waiting on another
       Python thread to complete a task, this can avoid deadlocks. This sub-point
       probably doesn't apply to you unless you're compiling GUI code with Cython.

If neither of these two points apply then you probably do not need to release the GIL.
The sort of Cython code that can run without the GIL (no calls to Python, purely C-level
numeric operations) is often the sort of code that runs efficiently. This sometimes
gives people the impression that the inverse is true and the trick is releasing the GIL,
rather than the actual code they’re running. Don’t be misled by this --
your (single-threaded) code will run the same speed with or without the GIL.

Marking functions as able to run without the GIL
------------------------------------------------

You can mark a whole function (either a Cython function or an :ref:`external function <nogil>`) as
``nogil`` by appending this to the function signature or by using the ``@cython.nogil`` decorator:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.nogil
            @cython.cfunc
            @cython.noexcept
            def some_func() -> None:
            ...

    .. group-tab:: Cython

        .. code-block:: cython

            cdef void some_func() noexcept nogil:
                ....

Be aware that this does not release the GIL when calling the function. It merely indicates that
a function is suitable for use when the GIL is released. It is also fine to call these functions
while holding the GIL.

In this case we've marked the function as ``noexcept`` to indicate that it cannot raise a Python
exception. Be aware that a function with an ``except *`` exception specification (typically functions
returning ``void``) will be expensive to call because Cython will need to temporarily reacquire
the GIL after every call to check the exception state. Most other exception specifications are
cheap to handle in a ``nogil`` block since the GIL is only acquired if an exception is
actually thrown.

Releasing (and reacquiring) the GIL
-----------------------------------

To actually release the GIL you can use context managers

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            with cython.nogil:
                ...              # some code that runs without the GIL
                with cython.gil:
                    ...          # some code that runs with the GIL
                ...              # some more code without the GIL

    .. group-tab:: Cython

        .. code-block:: cython

            with nogil:
                ...      # some code that runs without the GIL
                with gil:
                    ...  # some code that runs with the GIL
                ...      # some more code without the GIL

The ``with gil`` block is a useful trick to allow a small
chunk of Python code or Python object processing inside a non-GIL block. Try not to use it
too much since there is a cost to waiting for and acquiring the GIL, and because these
blocks cannot run in parallel since all executions require the same lock.

A function may be marked as ``with gil`` or decorated with ``@cython.with_gil``  to ensure that the
GIL is acquired immediately when calling it.

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.with_gil
            @cython.cfunc
            def some_func() -> cython.int
                ...

            with cython.nogil:
                ...          # some code that runs without the GIL
                some_func()  # some_func() will internally acquire the GIL
                ...          # some code that runs without the GIL
            some_func()      # GIL is already held hence the function does not need to acquire the GIL

    .. group-tab:: Cython

        .. code-block:: cython

            cdef int some_func() with gil:
                ...

            with nogil:
                ...          # some code that runs without the GIL
                some_func()  # some_func() will internally acquire the GIL
                ...          # some code that runs without the GIL
            some_func()      # GIL is already held hence the function does not need to acquire the GIL

Conditionally acquiring the GIL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's possible to release the GIL based on a compile-time condition.
This is most often used when working with :ref:`fusedtypes`

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            with cython.nogil(some_type is not object):
                ...  # some code that runs without the GIL, unless we're processing objects

    .. group-tab:: Cython

        .. code-block:: cython

            with nogil(some_type is not object):
                ...  # some code that runs without the GIL, unless we're processing objects

Exceptions and the GIL
----------------------

A small number of "Python operations" may be performed in a ``nogil``
block without needing to explicitly use ``with gil``. The main example
is throwing exceptions. Here Cython knows that an exception will always
require the GIL and so re-acquires it implicitly. Similarly, if
a ``nogil`` function throws an exception, Cython is able to propagate
it correctly without you needing to write explicit code to handle it.
In most cases this is efficient since Cython is able to use the
function's exception specification to check for an error, and then
acquire the GIL only if needed, but ``except *`` functions are
less efficient since Cython must always re-acquire the GIL.

.. _gil_as_lock:

Don't use the GIL as a lock
---------------------------

It may be tempting to try to use the GIL for your own locking
purposes and to say "the entire contents of a ``with gil`` block will
run atomically since we hold the GIL". Don't do this!

The GIL is only for the benefit of the interpreter, not for you.
There are two issues here: 

#. that future improvements in the Python interpreter may destroy 
   your "locking".
#. Second, that the GIL can be released if any Python code is
   executed. The easiest way to run arbitrary Python code is to
   destroy a Python object that has a ``__del__`` function, but
   there are numerous other creative ways to do so, and it is
   almost impossible to know that you aren't going to trigger one
   of these.

If you want a reliable lock then use the tools in the standard library's
``threading`` module.
