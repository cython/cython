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


.. function:: prange([start,] stop[, step][, nogil=False][, schedule=None[, chunksize=None]][, num_threads=None])

    This function can be used for parallel loops. OpenMP automatically
    starts a thread pool and distributes the work according to the schedule
    used.

    Thread-locality and reductions are automatically inferred for variables.

    If you assign to a variable in a prange block, it becomes lastprivate, meaning that the
    variable will contain the value from the last iteration. If you use an
    inplace operator on a variable, it becomes a reduction, meaning that the
    values from the thread-local copies of the variable will be reduced with
    the operator and assigned to the original variable after the loop. The
    index variable is always lastprivate.
    Variables assigned to in a parallel with block will be private and unusable
    after the block, as there is no concept of a sequentially last value.


    :param start:
        The index indicating the start of the loop (same as the start argument in range).

    :param stop:
        The index indicating when to stop the loop (same as the stop argument in range).

    :param step:
        An integer giving the step of the sequence (same as the step argument in range).
        It must not be 0.

    :param nogil:
        This function can only be used with the GIL released.
        If ``nogil`` is true, the loop will be wrapped in a nogil section.

    :param schedule:
        The ``schedule`` is passed to OpenMP and can be one of the following:

        static:
            If a chunksize is provided, iterations are distributed to all
            threads ahead of time in blocks of the given chunksize.  If no
            chunksize is given, the iteration space is divided into chunks that
            are approximately equal in size, and at most one chunk is assigned
            to each thread in advance.

            This is most appropriate when the scheduling overhead matters and
            the problem can be cut down into equally sized chunks that are
            known to have approximately the same runtime.

        dynamic:
            The iterations are distributed to threads as they request them,
            with a default chunk size of 1.

            This is suitable when the runtime of each chunk differs and is not
            known in advance and therefore a larger number of smaller chunks
            is used in order to keep all threads busy.

        guided:
            As with dynamic scheduling, the iterations are distributed to
            threads as they request them, but with decreasing chunk size.  The
            size of each chunk is proportional to the number of unassigned
            iterations divided by the number of participating threads,
            decreasing to 1 (or the chunksize if provided).

            This has an advantage over pure dynamic scheduling when it turns
            out that the last chunks take more time than expected or are
            otherwise being badly scheduled, so that most threads start running
            idle while the last chunks are being worked on by only a smaller
            number of threads.

        runtime:
            The schedule and chunk size are taken from the runtime scheduling
            variable, which can be set through the ``openmp.omp_set_schedule()``
            function call, or the OMP_SCHEDULE environment variable.  Note that
            this essentially disables any static compile time optimisations of
            the scheduling code itself and may therefore show a slightly worse
            performance than when the same scheduling policy is statically
            configured at compile time.
            The default schedule is implementation defined. For more information consult
            the OpenMP specification [#]_.

            ..  auto             The decision regarding scheduling is delegated to the
            ..                   compiler and/or runtime system. The programmer gives
            ..                   the implementation the freedom to choose any possible
            ..                   mapping of iterations to threads in the team.



    :param num_threads:
        The ``num_threads`` argument indicates how many threads the team should consist of. If not given,
        OpenMP will decide how many threads to use. Typically this is the number of cores available on
        the machine. However, this may be controlled through the ``omp_set_num_threads()`` function, or
        through the ``OMP_NUM_THREADS`` environment variable.

    :param chunksize: 
        The ``chunksize`` argument indicates the chunksize to be used for dividing the iterations among threads.
        This is only valid for ``static``, ``dynamic`` and ``guided`` scheduling, and is optional. Different chunksizes
        may give substantially different performance results, depending on the schedule, the load balance it provides,
        the scheduling overhead and the amount of false sharing (if any).

Example with a reduction:

.. literalinclude:: ../../examples/userguide/parallelism/simple_sum.pyx

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
           if local_buf is NULL:
               abort()

           # populate our local buffer in a sequential loop
           for i in xrange(size):
               local_buf[i] = i * 2

           # share the work using the thread-local buffer(s)
           for i in prange(n, schedule='guided'):
               func(local_buf)

           free(local_buf)

    Later on sections might be supported in parallel blocks, to distribute
    code sections of work among threads.

.. function:: threadid()

    Returns the id of the thread. For n threads, the ids will range from 0 to
    n-1.


Compiling
=========

To actually use the OpenMP support, you need to tell the C or C++ compiler to
enable OpenMP.  For gcc this can be done as follows in a setup.py:

.. literalinclude:: ../../examples/userguide/parallelism/setup.py

For Microsoft Visual C++ compiler, use ``'/openmp'`` instead of ``'-fopenmp'``.


Breaking out of loops
=====================

The parallel with and prange blocks support the statements break, continue and
return in nogil mode. Additionally, it is valid to use a ``with gil`` block
inside these blocks, and have exceptions propagate from them.
However, because the blocks use OpenMP, they can not just be left, so the
exiting procedure is best-effort. For prange() this means that the loop
body is skipped after the first break, return or exception for any subsequent
iteration in any thread. It is undefined which value shall be returned if
multiple different values may be returned, as the iterations are in no
particular order:

.. literalinclude:: ../../examples/userguide/parallelism/breaking_loop.pyx

In the example above it is undefined whether an exception shall be raised,
whether it will simply break or whether it will return 2.

Using OpenMP Functions
======================
OpenMP functions can be used by cimporting ``openmp``:

.. literalinclude:: ../../examples/userguide/parallelism/cimport_openmp.pyx

.. rubric:: References

.. [#] https://www.openmp.org/mp-documents/spec30.pdf
