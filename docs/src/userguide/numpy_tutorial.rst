.. highlight:: cython

.. _numpy_tutorial:

**************************
Cython for NumPy users
**************************

This tutorial is aimed at NumPy users who have no experience with Cython at
all. If you have some knowledge of Cython you may want to skip to the
''Efficient indexing'' section.

The main scenario considered is NumPy end-use rather than NumPy/SciPy
development. The reason is that Cython is not (yet) able to support functions
that are generic with respect to the number of dimensions in a
high-level fashion. This restriction is much more severe for SciPy development
than more specific, "end-user" functions. See the last section for more
information on this.

The style of this tutorial will not fit everybody, so you can also consider:

* Kurt Smith's `video tutorial of Cython at SciPy 2015
  <https://www.youtube.com/watch?v=gMvkiQ-gOW8&t=4730s&ab_channel=Enthought>`_.
  It's longuer but some readers like watching talks more than reading.
  The slides and notebooks of this talk are `on github
  <https://github.com/kwmsmith/scipy-2015-cython-tutorial>`_.
* Basic Cython documentation (see `Cython front page
  <https://cython.readthedocs.io/en/latest/index.html>`_).

Cython at a glance
==================

Cython is a compiler which compiles Python-like code files to C code. Still,
''Cython is not a Python to C translator''. That is, it doesn't take your full
program and "turns it into C" -- rather, the result makes full use of the
Python runtime environment. A way of looking at it may be that your code is
still Python in that it runs within the Python runtime environment, but rather
than compiling to interpreted Python bytecode one compiles to native machine
code (but with the addition of extra syntax for easy embedding of faster
C-like code).

This has two important consequences:

* Speed. How much depends very much on the program involved though. Typical Python numerical programs would tend to gain very little as most time is spent in lower-level C that is used in a high-level fashion. However for-loop-style programs can gain many orders of magnitude, when typing information is added (and is so made possible as a realistic alternative).
* Easy calling into C code. One of Cython's purposes is to allow easy wrapping
  of C libraries. When writing code in Cython you can call into C code as
  easily as into Python code.

Very few Python constructs are not yet supported, though making Cython compile all
Python code is a stated goal, you can see the differences with Python in
:ref:`limitations <cython-limitations>`.

Your Cython environment
=======================

Using Cython consists of these steps:

1. Write a :file:`.pyx` source file
2. Run the Cython compiler to generate a C file
3. Run a C compiler to generate a compiled library
4. Run the Python interpreter and ask it to import the module

However there are several options to automate these steps:

1. The `SAGE <http://sagemath.org>`_ mathematics software system provides
   excellent support for using Cython and NumPy from an interactive command
   line or through a notebook interface (like
   Maple/Mathematica). See `this documentation
   <http://doc.sagemath.org/html/en/developer/coding_in_cython.html>`_.
2. Cython can be used as an extension within a Jupyter notebook,
   making it easy to compile and use Cython code with just a ``%%cython``
   at the top of a cell. For more information see
   :ref:`Using the Jupyter Notebook <jupyter-notebook>`.
3. A version of pyximport is shipped with Cython,
   so that you can import pyx-files dynamically into Python and
   have them compiled automatically (See :ref:`pyximport`).
4. Cython supports distutils so that you can very easily create build scripts
   which automate the process, this is the preferred method for full programs.
   See :ref:`Compiling with distutils <compiling-distutils>`.
5. Manual compilation (see below)

.. Note::
    If using another interactive command line environment than SAGE, like
    IPython, Jupyter Notebook or Python itself, it is important that you restart the process
    when you recompile the module. It is not enough to issue an "import"
    statement again.

Installation
=============

If you already have a C compiler, just do::

   pip install Cython

otherwise, see :ref:`the installation page <install>`.


As of this writing SAGE comes with an older release of Cython than required
for this tutorial. So if using SAGE you should download the newest Cython and
then execute ::

    $ cd path/to/cython-distro
    $ path-to-sage/sage -python setup.py install

This will install the newest Cython into SAGE.

Manual compilation
====================

As it is always important to know what is going on, I'll describe the manual
method here. First Cython is run::

    $ cython yourmod.pyx

This creates :file:`yourmod.c` which is the C source for a Python extension
module. A useful additional switch is ``-a`` which will generate a document
:file:`yourmod.html`) that shows which Cython code translates to which C code
line by line.

Then we compile the C file. This may vary according to your system, but the C
file should be built like Python was built. Python documentation for writing
extensions should have some details. On Linux this often means something
like::

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -o yourmod.so yourmod.c

This creates :file:`yourmod.so` in the same directory, which is importable by
Python by using a normal ``import yourmod`` statement.

The first Cython program
==========================

The code below does 2D discrete convolution of an image with a filter (and I'm
sure you can do better!, let it serve for demonstration purposes). It is both
valid Python and valid Cython code. I'll refer to it as both
:file:`convolve_py.py` for the Python version and :file:`convolve_cy.pyx` for the
Cython version -- Cython uses ".pyx" as its file suffix.

.. literalinclude:: ../../examples/userguide/convolve_py.py
    :linenos:

This should be compiled to produce :file:`convolve_cy.so` (for Linux systems). We
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
    In [4]: import convolve_cy
    In [4]: convolve_cy.naive_convolve(np.array([[1, 1, 1]], dtype=np.int),
    ...     np.array([[1],[2],[1]], dtype=np.int))
    Out [4]:
    array([[1, 1, 1],
        [2, 2, 2],
        [1, 1, 1]])
    In [11]: N = 100
    In [12]: f = np.arange(N*N, dtype=np.int).reshape((N,N))
    In [13]: g = np.arange(81, dtype=np.int).reshape((9, 9))
    In [19]: %timeit -n2 -r3 convolve_py.naive_convolve(f, g)
    422 ms ± 2.06 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    In [20]: %timeit -n2 -r3 convolve_cy.naive_convolve(f, g)
    342 ms ± 1.39 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

There's not such a huge difference yet; because the C code still does exactly
what the Python interpreter does (meaning, for instance, that a new object is
allocated for each number used). You can look at the Python interaction
and the generated C code by using `-a` when calling Cython from the command
line, `%%cython -a` when using a Jupyter Notebook, or by using
`cythonize('convolve_cy.pyx', annotate=True)` when using a `setup.py`.
Look at the generated html file and see what
is needed for even the simplest statements you get the point quickly. We need
to give Cython more information; we need to add types.

Adding types
=============

To add types we use custom Cython syntax, so we are now breaking Python source
compatibility. Here's :file:`convolve2.pyx`. *Read the comments!*

.. literalinclude:: ../../examples/userguide/convolve_typed.pyx
    :linenos:

At this point, have a look at the generated C code for :file:`convolve1.pyx` and
:file:`convolve2.pyx`. Click on the lines to expand them and see corresponding C.
(Note that this code annotation is currently experimental and especially
"trailing" cleanup code for a block may stick to the last expression in the
block and make it look worse than it is -- use some common sense).

* .. literalinclude: convolve1.html
* .. literalinclude: convolve2.html

Especially have a look at the for loops: In :file:`convolve1.c`, these are ~20 lines
of C code to set up while in :file:`convolve2.c` a normal C for loop is used.

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

More information on this syntax [:enhancements/buffer:can be found here].

Showing the changes needed to produce :file:`convolve3.pyx` only

.. literalinclude:: ../../examples/userguide/convolve_memview.pyx
    :linenos:

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
        def naive_convolve(np.ndarray[DTYPE_t, ndim=2] f, np.ndarray[DTYPE_t, ndim=2] g):
        ...

Now bounds checking is not performed (and, as a side-effect, if you ''do''
happen to access out of bounds you will in the best case crash your program
and in the worst case corrupt data). It is possible to switch bounds-checking
mode in many ways, see :ref:`compiler-directives` for more
information.

Negative indices are dealt with by ensuring Cython that the indices will be
positive, by casting the variables to unsigned integer types (if you do have
negative values, then this casting will create a very large positive value
instead and you will attempt to access out-of-bounds values). Casting is done
with a special ``<>``-syntax. The code below is changed to use either
unsigned ints or casting as appropriate::

        ...
        cdef int s, t                                                                            # changed
        cdef unsigned int x, y, v, w                                                             # changed
        cdef int s_from, s_to, t_from, t_to
        cdef DTYPE_t value
        for x in range(xmax):
            for y in range(ymax):
                s_from = max(smid - x, -smid)
                s_to = min((xmax - x) - smid, smid + 1)
                t_from = max(tmid - y, -tmid)
                t_to = min((ymax - y) - tmid, tmid + 1)
                value = 0
                for s in range(s_from, s_to):
                    for t in range(t_from, t_to):
                        v = <unsigned int>(x - smid + s)                                         # changed
                        w = <unsigned int>(y - tmid + t)                                         # changed
                        value += g[<unsigned int>(smid - s), <unsigned int>(tmid - t)] * f[v, w] # changed
                h[x, y] = value
        ...

(In the next Cython release we will likely add a compiler directive or
argument to the ``np.ndarray[]``-type specifier to disable negative indexing
so that casting so much isn't necessary; feedback on this is welcome.)

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
    objects (like ``f``, ``g`` and ``h`` in our sample code) to ``None``.
    Setting such objects to ``None`` is entirely legal, but all you can do with them
    is check whether they are None. All other use (attribute lookup or indexing)
    can potentially segfault or corrupt data (rather than raising exceptions as
    they would in Python).

    The actual rules are a bit more complicated but the main message is clear: Do
    not use typed objects without knowing that they are not set to ``None``.

Declaring the NumPy arrays as contiguous
========================================

Insert stuff here.

Making the function cleaner
===========================

Some comments here.

.. literalinclude:: ../../examples/userguide/convolve_infer_types.pyx
    :linenos:

More generic code
==================

It would be possible to do

.. literalinclude:: ../../examples/userguide/convolve_fused_types.pyx
    :linenos:

i.e. use :obj:`object` rather than :obj:`np.ndarray`. Under Python 3.0 this
can allow your algorithm to work with any libraries supporting the buffer
interface; and support for e.g. the Python Imaging Library may easily be added
if someone is interested also under Python 2.x.

There is some speed penalty to this though (as one makes more assumptions
compile-time if the type is set to :obj:`np.ndarray`, specifically it is
assumed that the data is stored in pure strided mode and not in indirect
mode).

Where to go from here?
======================

* Since there is no Python interaction in the loops, it is possible with Cython
  to release the GIL and use multiple cores easily. To learn how to do that,
  you can see :ref:`using parallelism in Cython <parallel>`.
* If you want to learn how to make use of `BLAS <http://www.netlib.org/blas/>`_
  or `LAPACK <http://www.netlib.org/lapack/>`_ with Cython, you can watch
  `the presentation of Ian Henriksen at SciPy 2015
  <https://www.youtube.com/watch?v=R4yB-8tB0J0&t=693s&ab_channel=Enthought>`_.

The future
==========

These are some points to consider for further development. All points listed
here has gone through a lot of thinking and planning already; still they may
or may not happen depending on available developer time and resources for
Cython.

1. Support for efficient access to complex floating point types in arrays. The
   main obstacle here is getting support for efficient complex datatypes in
   Cython.
2. Calling NumPy/SciPy functions currently has a Python call overhead; it
   would be possible to take a short-cut from Cython directly to C. (This does
   however require some isolated and incremental changes to those libraries;
   mail the Cython mailing list for details).
3. Efficient code that is generic with respect to the number of dimensions.
   This can probably be done today by calling the NumPy C multi-dimensional
   iterator API directly; however it would be nice to have for-loops over
   :func:`enumerate` and :func:`ndenumerate` on NumPy arrays create efficient
   code.

