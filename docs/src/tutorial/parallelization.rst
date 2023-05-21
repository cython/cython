.. _parallel-tutorial:

=================================
Writing parallel code with Cython
=================================

.. include::
    ../two-syntax-variants-used

One method of speeding up your Cython code is parallelization:
you write code that can be run on multiple cores of your CPU simultaneously.
For code that lends itself to parallelization this can produce quite
dramatic speed-ups, equal to the number of cores your CPU has (for example
a 4× speed-up on a 4-core CPU).

This tutorial assumes that you are already familiar with Cython's 
:ref:`"typed memoryviews"<memoryviews>` (since code using memoryviews is often
the sort of code that's easy to parallelize with Cython), and also that you're
somewhat familiar with the pitfalls of writing parallel code in general
(it aims to be a Cython tutorial rather than a complete introduction
to parallel programming).

Before starting, a few notes:

- Not all code can be parallelized - for some code the algorithm simply
  relies on being executed in order and you should not attempt to
  parallelize it.  A cumulative sum is a good example.
  
- Not all code is worth parallelizing.  There's a reasonable amount of
  overhead in starting a parallel section and so you need to make sure
  that you're operating on enough data to make this overhead worthwhile.
  Additionally, make sure that you are doing actual work on the data!
  Multiple threads simply reading the same data tends not to parallelize
  too well.  If in doubt, time it.

- Cython requires the contents of parallel blocks to be ``nogil``.  If
  your algorithm requires access to Python objects then it may not be
  suitable for parallelization.
  
- Cython's inbuilt parallelization uses the OpenMP constructs
  ``omp parallel for`` and ``omp parallel``.  These are ideal
  for parallelizing relatively small, self-contained blocks of code
  (especially loops).  However, If you want to use other models of 
  parallelization such as spawning and waiting for tasks, or 
  off-loading some "side work" to a continuously running secondary 
  thread, then you might be better using other methods (such as 
  Python's ``threading`` module).
  
- Actually implementing your parallel Cython code should probably be 
  one of the last steps in your optimization.  You should start with
  some working serial code first.  However, it's worth planning for
  early since it may affect your choice of algorithm.

This tutorial does not aim to explore all the options available to
customize parallelization.  See the
:ref:`main parallelism documentation<parallel>` for details.
You should also be aware that a lot of the choices Cython makes
about how your code is parallelized are fairly fixed and if you want
specific OpenMP behaviour that Cython doesn't provide by default you
may be better writing it in C yourself.

Compilation
===========

OpenMP requires support from your C/C++ compiler. This support is
usually enabled through a special command-line argument:
on GCC this is ``-fopenmp`` while on MSVC it is
``/openmp``. If your compiler doesn't support OpenMP (or if you
forget to pass the argument) then the code will usually still
compile but will not run in parallel.

The following ``setup.py`` file can be used to compile the
examples in this tutorial:

.. literalinclude:: ../../examples/tutorial/parallelization/setup.py

Element-wise parallel operations
================================

The easiest and most common parallel operation in Cython is to
iterate across an array element-wise, performing the same
operation on each array element.  In the simple example
below we calculate the ``sin`` of every element in an array:

.. tabs::

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/parallelization/parallel_sin.pyx

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/parallelization/parallel_sin.py

We parallelize the outermost loop.  This is usually a good idea
since there is some overhead to entering and leaving a parallel block.
However, you should also consider the likely size of your arrays.
If ``input`` usually had a size of ``(2, 10000000)`` then parallelizing
over the dimension of length ``2`` would likely be a worse choice.

The body of the loop itself is ``nogil`` - i.e. you cannot perform
"Python" operations.  This is a fairly strong limitation and if you
find that you need to use the GIL then it is likely that Cython's
parallelization features are not suitable for you.  It is possible
to throw exceptions from within the loop, however -- Cython simply
regains the GIL and raises an exception, then terminates the loop
on all threads.

It's necessary to explicitly type the loop variable ``i``  as a
C integer.  For a non-parallel loop Cython can infer this, but it
does not currently infer the loop variable for parallel loops, 
so not typing ``i`` will lead to compile errors since it will be
a Python object and so unusable without the GIL.

The C code generated is shown below, for the benefit of experienced
users of OpenMP. It is simplified a little for readability here:

.. code-block:: C

    #pragma omp parallel
    {
        #pragma omp for firstprivate(i) lastprivate(i) lastprivate(j)
        for (__pyx_t_8 = 0; __pyx_t_8 < __pyx_t_9; __pyx_t_8++){
            i = __pyx_t_8;
            /* body goes here */
        }
    }
    
Private variables
-----------------

One useful point to note from the generated C code above - variables
used in the loops like ``i`` and ``j`` are marked as ``firstprivate``
and ``lastprivate``.  Within the loop each thread has its own copy of
the data, the data is initialized
according to its value before the loop, and after the loop the "global"
copy is set equal to the last iteration (i.e. as if the loop were run
in serial).

The basic rules that Cython applies are:

- C scalar variables within a ``prange`` block are made 
  ``firstprivate`` and ``lastprivate``,

- C scalar variables assigned within a  
  :ref:`parallel block<parallel-block>`
  are ``private`` (which means they can't be used to pass data in
  and out of the block),

- array variables (e.g. memoryviews) are not made private.  Instead
  Cython assumes that you have structured your loop so that each iteration
  is acting on different data,

- Python objects are also not made private, although access to them
  is controlled via Python's GIL.

Cython does not currently provide much opportunity of override these
choices.
  
Reductions
==========

The second most common parallel operation in Cython is the "reduction"
operation.  A common example is to accumulate a sum over the whole
array, such as in the calculation of a vector norm below:

.. tabs::

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/parallelization/norm.pyx

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/parallelization/norm.py

Cython is able to infer reductions for ``+=``, ``*=``, ``-=``,
``&=``, ``|=``, and ``^=``.  These only apply to C scalar variables
so you cannot easily reduce a 2D memoryview to a 1D memoryview for
example.

The C code generated is approximately:

.. code-block:: C

    #pragma omp parallel reduction(+:total)
    {
        #pragma omp for firstprivate(i) lastprivate(i)
        for (__pyx_t_2 = 0; __pyx_t_2 < __pyx_t_3; __pyx_t_2++){
            i = __pyx_t_2;
            total = total + /* some indexing code */;
            
        }
    }

.. _parallel-block:
    
``parallel`` blocks
===================

Much less frequently used than ``prange`` is Cython's ``parallel``
operator.  ``parallel`` generates a block of code that is run simultaneously
on multiple threads at once.  Unlike ``prange``, however, work is
not automatically divided between threads.

Here we present three common uses for the ``parallel`` block:

Stringing together prange blocks
--------------------------------

There is some overhead in entering and leaving a parallelized section.
Therefore, if you have multiple parallel sections with small
serial sections in between it can be more efficient to
write one large parallel block.  Any small serial
sections are duplicated, but the overhead is reduced.

In the example below we do an in-place normalization of a vector.
The first parallel loop calculates the norm, the second parallel
loop applies the norm to the vector, and we avoid jumping in and out of serial
code in between.

.. tabs::

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/parallelization/normalize.pyx
        
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/parallelization/normalize.py

The C code is approximately:

.. code-block:: C

    #pragma omp parallel private(norm) reduction(+:total)
    {
        /* some calculations of array size... */
        #pragma omp for firstprivate(i) lastprivate(i)
        for (__pyx_t_2 = 0; __pyx_t_2 < __pyx_t_3; __pyx_t_2++){
            /* ... */
        }
        norm = sqrt(total);
        #pragma omp for firstprivate(i) lastprivate(i)
        for (__pyx_t_2 = 0; __pyx_t_2 < __pyx_t_3; __pyx_t_2++){
            /* ... */
        }
    }

Allocating "scratch space" for each thread
------------------------------------------

Suppose that each thread requires a small amount of scratch space
to work in.  They cannot share scratch space because that would
lead to data races.  In this case the allocation and deallocation
is done in a parallel section (so occurs on a per-thread basis)
surrounding a loop which then uses the scratch space.

Our example here uses C++ to find the median of each column in
a 2D array (just a parallel version of ``numpy.median(x, axis=0)``).
We must reorder each column to find the median of it, but don't want
to modify the input array.  Therefore, we allocate a C++ vector per
thread to use as scratch space, and work in that.  For efficiency
the vector is allocated outside the ``prange`` loop.

.. tabs::

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/parallelization/median.pyx
        
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/parallelization/median.py

.. note::

    Pure and classic syntax examples are not quite identical
    since pure Python syntax does not support C++ "new", so we allocate the
    scratch space slightly differently

In the generated code the ``scratch`` variable is marked as
``private`` in the outer parallel block.  A rough outline is:

.. code-block:: C++

    #pragma omp parallel private(scratch)
    {
        scratch = new std::vector<double> ((x.shape[0]))
        #pragma omp for firstprivate(i) lastprivate(i) lastprivate(j) lastprivate(median_it)
        for (__pyx_t_9 = 0; __pyx_t_9 < __pyx_t_10; __pyx_t_9++){
            i = __pyx_t_9;
            /* implementation goes here */
        }
        /* some exception handling detail omitted */
        delete scratch;
    }

Performing different tasks on each thread
-----------------------------------------

Finally, if you manually specify the number of threads and
then identify each thread using ``omp.get_thread_num()``
you can manually split work between threads.  This is
a fairly rare use-case in Cython, and probably suggests
that the ``threading`` module is more suitable for what
you're trying to do.  However it is an option.

.. tabs::

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/parallelization/manual_work.pyx
           :lines: 2-
        
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/parallelization/manual_work.py
           :lines: 2-

The utility of this kind of block is limited by the fact that
variables assigned to in the block are ``private`` to each thread,
so cannot be accessed in the serial section afterwards.

The generated C code for the example above is fairly simple:

.. code-block:: C

    #pragma omp parallel private(thread_num) 
    {
        thread_num = omp_get_thread_num();
        switch (thread_num) {
            /* ... */
        }
    }
