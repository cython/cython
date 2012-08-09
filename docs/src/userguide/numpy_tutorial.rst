.. highlight:: cython

.. _numpy_tutorial:

**************************
Cython for NumPy users
**************************

This tutorial is aimed at NumPy users who have no experience with Cython at
all. If you have some knowledge of Cython you may want to skip to the
''Efficient indexing'' section which explains the new improvements made in
summer 2008.

The main scenario considered is NumPy end-use rather than NumPy/SciPy
development. The reason is that Cython is not (yet) able to support functions
that are generic with respect to datatype and the number of dimensions in a
high-level fashion. This restriction is much more severe for SciPy development
than more specific, "end-user" functions. See the last section for more
information on this.

The style of this tutorial will not fit everybody, so you can also consider:

* Robert Bradshaw's `slides on cython for SciPy2008 
  <http://wiki.sagemath.org/scipy08?action=AttachFile&do=get&target=scipy-cython.tgz>`_ 
  (a higher-level and quicker introduction)
* Basic Cython documentation (see `Cython front page <http://cython.org>`_).
* ``[:enhancements/buffer:Spec for the efficient indexing]``

.. Note:: 
    The fast array access documented below is a completely new feature, and
    there may be bugs waiting to be discovered. It might be a good idea to do
    a manual sanity check on the C code Cython generates before using this for
    serious purposes, at least until some months have passed.

Cython at a glance
====================

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

Some Python constructs are not yet supported, though making Cython compile all
Python code is a stated goal (among the more important omissions are inner
functions and generator functions).

Your Cython environment
========================

Using Cython consists of these steps:

1. Write a :file:`.pyx` source file
2. Run the Cython compiler to generate a C file
3. Run a C compiler to generate a compiled library
4. Run the Python interpreter and ask it to import the module

However there are several options to automate these steps:

1. The `SAGE <http://sagemath.org>`_ mathematics software system provides
   excellent support for using Cython and NumPy from an interactive command
   line (like IPython) or through a notebook interface (like
   Maple/Mathematica). See `this documentation
   <http://www.sagemath.org/doc/prog/node40.html>`_.  
2. A version of `pyximport <http://www.prescod.net/pyximport/>`_ is shipped
   with Cython, so that you can import pyx-files dynamically into Python and
   have them compiled automatically (See :ref:`pyximport`).
3. Cython supports distutils so that you can very easily create build scripts
   which automate the process, this is the preferred method for full programs.
4. Manual compilation (see below)

.. Note:: 
    If using another interactive command line environment than SAGE, like
    IPython or Python itself, it is important that you restart the process
    when you recompile the module. It is not enough to issue an "import"
    statement again.

Installation
=============

Unless you are used to some other automatic method:
`download Cython <http://cython.org/#download>`_ (0.9.8.1.1 or later), unpack it,
and run the usual ```python setup.py install``. This will install a
``cython`` executable on your system. It is also possible to use Cython from
the source directory without installing (simply launch :file:`cython.py` in the
root directory).

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

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.5 -o yourmod.so yourmod.c

``gcc`` should have access to the NumPy C header files so if they are not
installed at :file:`/usr/include/numpy` or similar you may need to pass another
option for those.

This creates :file:`yourmod.so` in the same directory, which is importable by
Python by using a normal ``import yourmod`` statement.

The first Cython program
==========================

The code below does 2D discrete convolution of an image with a filter (and I'm
sure you can do better!, let it serve for demonstration purposes). It is both
valid Python and valid Cython code. I'll refer to it as both
:file:`convolve_py.py` for the Python version and :file:`convolve1.pyx` for the
Cython version -- Cython uses ".pyx" as its file suffix.

.. code-block:: python

    from __future__ import division
    import numpy as np
    def naive_convolve(f, g):
        # f is an image and is indexed by (v, w)
        # g is a filter kernel and is indexed by (s, t),
        #   it needs odd dimensions
        # h is the output image and is indexed by (x, y),
        #   it is not cropped
        if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
            raise ValueError("Only odd dimensions on filter supported")
        # smid and tmid are number of pixels between the center pixel
        # and the edge, ie for a 5x5 filter they will be 2.
        #
        # The output size is calculated by adding smid, tmid to each
        # side of the dimensions of the input image.
        vmax = f.shape[0]
        wmax = f.shape[1]
        smax = g.shape[0]
        tmax = g.shape[1]
        smid = smax // 2
        tmid = tmax // 2
        xmax = vmax + 2*smid
        ymax = wmax + 2*tmid
        # Allocate result image.
        h = np.zeros([xmax, ymax], dtype=f.dtype)
        # Do convolution
        for x in range(xmax):
            for y in range(ymax):
                # Calculate pixel value for h at (x,y). Sum one component
                # for each pixel (s, t) of the filter g.
                s_from = max(smid - x, -smid)
                s_to = min((xmax - x) - smid, smid + 1)
                t_from = max(tmid - y, -tmid)
                t_to = min((ymax - y) - tmid, tmid + 1)
                value = 0
                for s in range(s_from, s_to):
                    for t in range(t_from, t_to):
                        v = x - smid + s
                        w = y - tmid + t
                        value += g[smid - s, tmid - t] * f[v, w]
                h[x, y] = value
        return h

This should be compiled to produce :file:`yourmod.so` (for Linux systems). We
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
compatibility. Here's :file:`convolve2.pyx`. *Read the comments!*  ::

    from __future__ import division
    import numpy as np
    # "cimport" is used to import special compile-time information
    # about the numpy module (this is stored in a file numpy.pxd which is
    # currently part of the Cython distribution).
    cimport numpy as np
    # We now need to fix a datatype for our arrays. I've used the variable
    # DTYPE for this, which is assigned to the usual NumPy runtime
    # type info object.
    DTYPE = np.int
    # "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
    # every type in the numpy module there's a corresponding compile-time
    # type with a _t-suffix.
    ctypedef np.int_t DTYPE_t
    # The builtin min and max functions works with Python objects, and are
    # so very slow. So we create our own.
    #  - "cdef" declares a function which has much less overhead than a normal
    #    def function (but it is not Python-callable)
    #  - "inline" is passed on to the C compiler which may inline the functions
    #  - The C type "int" is chosen as return type and argument types
    #  - Cython allows some newer Python constructs like "a if x else b", but
    #    the resulting C file compiles with Python 2.3 through to Python 3.0 beta.
    cdef inline int int_max(int a, int b): return a if a >= b else b
    cdef inline int int_min(int a, int b): return a if a <= b else b
    # "def" can type its arguments but not have a return type. The type of the
    # arguments for a "def" function is checked at run-time when entering the
    # function.
    #
    # The arrays f, g and h is typed as "np.ndarray" instances. The only effect
    # this has is to a) insert checks that the function arguments really are
    # NumPy arrays, and b) make some attribute access like f.shape[0] much
    # more efficient. (In this example this doesn't matter though.)
    def naive_convolve(np.ndarray f, np.ndarray g):
        if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
            raise ValueError("Only odd dimensions on filter supported")
        assert f.dtype == DTYPE and g.dtype == DTYPE
        # The "cdef" keyword is also used within functions to type variables. It
        # can only be used at the top indendation level (there are non-trivial
        # problems with allowing them in other places, though we'd love to see
        # good and thought out proposals for it).
        #
        # For the indices, the "int" type is used. This corresponds to a C int,
        # other C types (like "unsigned int") could have been used instead.
        # Purists could use "Py_ssize_t" which is the proper Python type for
        # array indices.
        cdef int vmax = f.shape[0]
        cdef int wmax = f.shape[1]
        cdef int smax = g.shape[0]
        cdef int tmax = g.shape[1]
        cdef int smid = smax // 2
        cdef int tmid = tmax // 2
        cdef int xmax = vmax + 2*smid
        cdef int ymax = wmax + 2*tmid
        cdef np.ndarray h = np.zeros([xmax, ymax], dtype=DTYPE)
        cdef int x, y, s, t, v, w
        # It is very important to type ALL your variables. You do not get any
        # warnings if not, only much slower code (they are implicitly typed as
        # Python objects).
        cdef int s_from, s_to, t_from, t_to
        # For the value variable, we want to use the same data type as is
        # stored in the array, so we use "DTYPE_t" as defined above.
        # NB! An important side-effect of this is that if "value" overflows its
        # datatype size, it will simply wrap around like in C, rather than raise
        # an error like in Python.
        cdef DTYPE_t value
        for x in range(xmax):
            for y in range(ymax):
                s_from = int_max(smid - x, -smid)
                s_to = int_min((xmax - x) - smid, smid + 1)
                t_from = int_max(tmid - y, -tmid)
                t_to = int_min((ymax - y) - tmid, tmid + 1)
                value = 0
                for s in range(s_from, s_to):
                    for t in range(t_from, t_to):
                        v = x - smid + s
                        w = y - tmid + t
                        value += g[smid - s, tmid - t] * f[v, w]
                h[x, y] = value
        return h

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

Showing the changes needed to produce :file:`convolve3.pyx` only::

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
        @cython.boundscheck(False) # turn of bounds-checking for entire function
        def naive_convolve(np.ndarray[DTYPE_t, ndim=2] f, np.ndarray[DTYPE_t, ndim=2] g):
        ...
        
Now bounds checking is not performed (and, as a side-effect, if you ''do''
happen to access out of bounds you will in the best case crash your program
and in the worst case corrupt data). It is possible to switch bounds-checking
mode in many ways, see [:docs/compilerdirectives:compiler directives] for more
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
assumed that the data is stored in pure strided more and not in indirect
mode).

[:enhancements/buffer:More information]

The future
============

These are some points to consider for further development. All points listed
here has gone through a lot of thinking and planning already; still they may
or may not happen depending on available developer time and resources for
Cython.

1. Support for efficient access to structs/records stored in arrays; currently
   only primitive types are allowed.  
2. Support for efficient access to complex floating point types in arrays. The
   main obstacle here is getting support for efficient complex datatypes in
   Cython.
3. Calling NumPy/SciPy functions currently has a Python call overhead; it
   would be possible to take a short-cut from Cython directly to C. (This does
   however require some isolated and incremental changes to those libraries;
   mail the Cython mailing list for details).  
4. Efficient code that is generic with respect to the number of dimensions.
   This can probably be done today by calling the NumPy C multi-dimensional
   iterator API directly; however it would be nice to have for-loops over
   :func:`enumerate` and :func:`ndenumerate` on NumPy arrays create efficient
   code.
5. A high-level construct for writing type-generic code, so that one can write
   functions that work simultaneously with many datatypes. Note however that a
   macro preprocessor language can help with doing this for now.

