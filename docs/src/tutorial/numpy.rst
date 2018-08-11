.. _working-numpy:

=======================
Working with NumPy
=======================

.. NOTE:: Cython 0.16 introduced typed memoryviews as a successor to the NumPy
          integration described here.  They are easier to use than the buffer syntax
          below, have less overhead, and can be passed around without requiring the GIL.
          They should be preferred to the syntax presented in this page.
          See :ref:`Cython for NumPy users <numpy_tutorial>`.

You can use NumPy from Cython exactly the same as in regular Python, but by
doing so you are losing potentially high speedups because Cython has support
for fast access to NumPy arrays. Let's see how this works with a simple
example.

The code below does 2D discrete convolution of an image with a filter (and I'm
sure you can do better!, let it serve for demonstration purposes). It is both
valid Python and valid Cython code. I'll refer to it as both
:file:`convolve_py.py` for the Python version and :file:`convolve1.pyx` for
the Cython version -- Cython uses ".pyx" as its file suffix.

.. literalinclude:: ../../examples/tutorial/numpy/convolve_py.py

This should be compiled to produce :file:`yourmod.so` (for Linux systems, on Windows
systems, it will be :file:`yourmod.pyd`). We
run a Python session to test both the Python version (imported from
``.py``-file) and the compiled Cython module.

.. sourcecode:: ipython

    In [1]: import numpy as np
    In [2]: import convolve_py
    In [3]: convolve_py.naive_convolve(np.array([[1, 1, 1]], dtype=np.int),
    ...     np.array([[1],[2],[1]], dtype=np.int))
    Out [3]:
    array([[1, 1, 1],
        [2, 2, 2],
        [1, 1, 1]])
    In [4]: import convolve1
    In [4]: convolve1.naive_convolve(np.array([[1, 1, 1]], dtype=np.int),
    ...     np.array([[1],[2],[1]], dtype=np.int))
    Out [4]:
    array([[1, 1, 1],
        [2, 2, 2],
        [1, 1, 1]])
    In [11]: N = 100
    In [12]: f = np.arange(N*N, dtype=np.int).reshape((N,N))
    In [13]: g = np.arange(81, dtype=np.int).reshape((9, 9))
    In [19]: %timeit -n2 -r3 convolve_py.naive_convolve(f, g)
    2 loops, best of 3: 1.86 s per loop
    In [20]: %timeit -n2 -r3 convolve1.naive_convolve(f, g)
    2 loops, best of 3: 1.41 s per loop

There's not such a huge difference yet; because the C code still does exactly
what the Python interpreter does (meaning, for instance, that a new object is
allocated for each number used). Look at the generated html file and see what
is needed for even the simplest statements you get the point quickly. We need
to give Cython more information; we need to add types.

Adding types
=============

To add types we use custom Cython syntax, so we are now breaking Python source
compatibility. Consider this code (*read the comments!*) :

.. literalinclude:: ../../examples/tutorial/numpy/convolve2.pyx

After building this and continuing my (very informal) benchmarks, I get:

.. sourcecode:: ipython

    In [21]: import convolve2
    In [22]: %timeit -n2 -r3 convolve2.naive_convolve(f, g)
    2 loops, best of 3: 828 ms per loop

Efficient indexing
====================

There's still a bottleneck killing performance, and that is the array lookups
and assignments. The ``[]``-operator still uses full Python operations --
what we would like to do instead is to access the data buffer directly at C
speed.

What we need to do then is to type the contents of the :obj:`ndarray` objects.
We do this with a special "buffer" syntax which must be told the datatype
(first argument) and number of dimensions ("ndim" keyword-only argument, if
not provided then one-dimensional is assumed).

These are the needed changes::

    ...
    def naive_convolve(np.ndarray[DTYPE_t, ndim=2] f, np.ndarray[DTYPE_t, ndim=2] g):
    ...
    cdef np.ndarray[DTYPE_t, ndim=2] h = ...

Usage:

.. sourcecode:: ipython

    In [18]: import convolve3
    In [19]: %timeit -n3 -r100 convolve3.naive_convolve(f, g)
    3 loops, best of 100: 11.6 ms per loop

Note the importance of this change.

*Gotcha*: This efficient indexing only affects certain index operations,
namely those with exactly ``ndim`` number of typed integer indices. So if
``v`` for instance isn't typed, then the lookup ``f[v, w]`` isn't
optimized. On the other hand this means that you can continue using Python
objects for sophisticated dynamic slicing etc. just as when the array is not
typed.

Tuning indexing further
========================

The array lookups are still slowed down by two factors:

1. Bounds checking is performed.
2. Negative indices are checked for and handled correctly.  The code above is
   explicitly coded so that it doesn't use negative indices, and it
   (hopefully) always access within bounds. We can add a decorator to disable
   bounds checking::

        ...
        cimport cython
        @cython.boundscheck(False) # turn off bounds-checking for entire function
        @cython.wraparound(False)  # turn off negative index wrapping for entire function
        def naive_convolve(np.ndarray[DTYPE_t, ndim=2] f, np.ndarray[DTYPE_t, ndim=2] g):
        ...

Now bounds checking is not performed (and, as a side-effect, if you ''do''
happen to access out of bounds you will in the best case crash your program
and in the worst case corrupt data). It is possible to switch bounds-checking
mode in many ways, see :ref:`compiler-directives` for more
information.

Also, we've disabled the check to wrap negative indices (e.g. g[-1] giving
the last value).  As with disabling bounds checking, bad things will happen
if we try to actually use negative indices with this disabled.

The function call overhead now starts to play a role, so we compare the latter
two examples with larger N:

.. sourcecode:: ipython

    In [11]: %timeit -n3 -r100 convolve4.naive_convolve(f, g)
    3 loops, best of 100: 5.97 ms per loop
    In [12]: N = 1000
    In [13]: f = np.arange(N*N, dtype=np.int).reshape((N,N))
    In [14]: g = np.arange(81, dtype=np.int).reshape((9, 9))
    In [17]: %timeit -n1 -r10 convolve3.naive_convolve(f, g)
    1 loops, best of 10: 1.16 s per loop
    In [18]: %timeit -n1 -r10 convolve4.naive_convolve(f, g)
    1 loops, best of 10: 597 ms per loop

(Also this is a mixed benchmark as the result array is allocated within the
function call.)

.. Warning::

    Speed comes with some cost. Especially it can be dangerous to set typed
    objects (like ``f``, ``g`` and ``h`` in our sample code) to
    ``None``.  Setting such objects to ``None`` is entirely
    legal, but all you can do with them is check whether they are None. All
    other use (attribute lookup or indexing) can potentially segfault or
    corrupt data (rather than raising exceptions as they would in Python).

    The actual rules are a bit more complicated but the main message is clear:
    Do not use typed objects without knowing that they are not set to None.

More generic code
==================

It would be possible to do::

    def naive_convolve(object[DTYPE_t, ndim=2] f, ...):

i.e. use :obj:`object` rather than :obj:`np.ndarray`. Under Python 3.0 this
can allow your algorithm to work with any libraries supporting the buffer
interface; and support for e.g. the Python Imaging Library may easily be added
if someone is interested also under Python 2.x.

There is some speed penalty to this though (as one makes more assumptions
compile-time if the type is set to :obj:`np.ndarray`, specifically it is
assumed that the data is stored in pure strided mode and not in indirect
mode).
