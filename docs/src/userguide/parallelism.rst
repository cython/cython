.. highlight:: cython

.. py:module:: cython.parallel

.. _parallel:

**********************************
Using Parallelism
**********************************

Cython supports native parallelism through the :py:mod:`cython.parallel`
module. To use this kind of parallelism, the GIL must be released
(see :ref:`Releasing the GIL <nogil>`).
It currently supports OpenMP, but later on more backends might be supported.

.. NOTE:: Functionality in this module may only be used from the main thread
          or parallel regions due to OpenMP restrictions.

__ nogil_

.. function:: prange([start,] stop[, step][, nogil=False][, schedule=None[, chunksize=None]][, num_threads=None])

    This function can be used for parallel loops. OpenMP automatically
    starts a thread pool and distributes the work according to the schedule
    used. ``step`` must not be 0. This function can only be used with the
    GIL released. If ``nogil`` is true, the loop will be wrapped in a nogil
    section.

    Thread-locality and reductions are automatically inferred for variables.

    If you assign to a variable in a prange block, it becomes lastprivate, meaning that the
    variable will contain the value from the last iteration. If you use an
    inplace operator on a variable, it becomes a reduction, meaning that the
    values from the thread-local copies of the variable will be reduced with
    the operator and assigned to the original variable after the loop. The
    index variable is always lastprivate.
    Variables assigned to in a parallel with block will be private and unusable
    after the block, as there is no concept of a sequentially last value.

    The ``schedule`` is passed to OpenMP and can be one of the following:

    +-----------------+------------------------------------------------------+
    | Schedule        | Description                                          |
    +=================+======================================================+
    |static           | The iteration space is divided into chunks that are  |
    |                 | approximately equal in size, and at most one chunk   |
    |                 | is distributed to each thread, if ``chunksize`` is   |
    |                 | not given. If ``chunksize`` is specified, iterations |
    |                 | are distributed cyclically in a static manner with a |
    |                 | blocksize of ``chunksize``.                          |
    +-----------------+------------------------------------------------------+
    |dynamic          | The iterations are distributed to threads in the team|
    |                 | as the threads request them, with a default chunk    |
    |                 | size of 1.                                           |
    +-----------------+------------------------------------------------------+
    |guided           | The iterations are distributed to threads in the team|
    |                 | as the threads request them. The size of each chunk  |
    |                 | is proportional to the number of unassigned          |
    |                 | iterations divided by the number of threads in the   |
    |                 | team, decreasing to 1 (or ``chunksize`` if given).   |
    +-----------------+------------------------------------------------------+
    |runtime          | The schedule and chunk size are taken from the       |
    |                 | runtime-scheduling-variable, which can be set through|
    |                 | the ``omp_set_schedule`` function call, or the       |
    |                 | ``OMP_SCHEDULE`` environment variable.               |
    +-----------------+------------------------------------------------------+

..    |auto             | The decision regarding scheduling is delegated to the|
..    |                 | compiler and/or runtime system. The programmer gives |
..    |                 | the implementation the freedom to choose any possible|
..    |                 | mapping of iterations to threads in the team.        |
..    +-----------------+------------------------------------------------------+

    The default schedule is implementation defined. For more information consult
    the OpenMP specification [#]_.

    The ``num_threads`` argument indicates how many threads the team should consist of. If not given,
    OpenMP will decide how many threads to use. Typically this is the number of cores available on
    the machine. However, this may be controlled through the ``omp_set_num_threads()`` function, or
    through the ``OMP_NUM_THREADS`` environment variable.

    The ``chunksize`` argument indicates the chunksize to be used for dividing the iterations among threads.
    This is only valid for ``static``, ``dynamic`` and ``guided`` scheduling, and is optional. Different chunksizes
    may give substatially different performance results, depending on the schedule, the load balance it provides,
    the scheduling overhead and the amount of false sharing (if any).

    Example with a reduction::

        from cython.parallel import prange

        cdef int i
        cdef int sum = 0

        for i in prange(n, nogil=True):
            sum += i

        print sum

    Example with a typed memoryview (e.g. a NumPy array)::

        from cython.parallel import prange

        def func(double[:] x, double alpha):
            cdef Py_ssize_t i

            for i in prange(x.shape[0]):
                x[i] = alpha * x[i]

.. function:: parallel(num_threads=None)

    This directive can be used as part of a ``with`` statement to execute code
    sequences in parallel. This is currently useful to setup thread-local
    buffers used by a prange. A contained prange will be a worksharing loop
    that is not parallel, so any variable assigned to in the parallel section
    is also private to the prange. Variables that are private in the parallel
    block are unavailable after the parallel block.

    Example with thread-local buffers::

       from cython.parallel import parallel, prange
       from libc.stdlib cimport abort, malloc, free

       cdef Py_ssize_t idx, i, n = 100
       cdef int * local_buf
       cdef size_t size = 10

       with nogil, parallel():
           local_buf = <int *> malloc(sizeof(int) * size)
           if local_buf == NULL:
               abort()

           # populate our local buffer in a sequential loop
           for idx in range(size):
               local_buf[i] = i * 2

           # share the work using the thread-local buffer(s)
           for i in prange(n, schedule='guided'):
               func(local_buf)

           free(local_buf)

    Later on sections might be supported in parallel blocks, to distribute
    code sections of work among threads.

.. function:: threadid()

    Returns the id of the thread. For n threads, the ids will range from 0 to
    n.

Compiling
=========
To actually use the OpenMP support, you need to tell the C or C++ compiler to
enable OpenMP. For gcc this can be done as follows in a setup.py::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    ext_module = Extension(
        "hello",
        ["hello.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )

    setup(
        name = 'Hello world app',
        cmdclass = {'build_ext': build_ext},
        ext_modules = [ext_module],
    )

Breaking
========
The parallel with and prange blocks support break, continue and return in
nogil mode. Additionally, it is valid to use a ``with gil`` block inside these
blocks, and have exceptions propagate from them.
However, because the blocks use OpenMP, they can not just be left, so the
exiting procedure is best-effort. For prange() this means that the loop
body is skipped after the first break, return or exception for any subsequent
iteration in any thread. It is undefined which value shall be returned if
multiple different values may be returned, as the iterations are in no
particular order::

    from cython.parallel import prange

    cdef int func(Py_ssize_t n):
        cdef Py_ssize_t i

        for i in prange(n, nogil=True):
            if i == 8:
                with gil:
                    raise Exception()
            elif i == 4:
                break
            elif i == 2:
                return i

In the example above it is undefined whether an exception shall be raised,
whether it will simply break or whether it will return 2.

Using OpenMP Functions
======================
OpenMP functions can be used by cimporting ``openmp``::

    from cython.parallel cimport parallel
    cimport openmp

    cdef int num_threads

    openmp.omp_set_dynamic(1)
    with nogil, parallel():
        num_threads = openmp.omp_get_num_threads()
        ...

.. rubric:: References

.. [#] http://www.openmp.org/mp-documents/spec30.pdf
