.. highlight:: cython

.. _fusedtypes:

***********************
Fused Types (Templates)
***********************

.. include::
    ../two-syntax-variants-used

Fused types allow you to have one type definition that can refer to multiple
types.  This allows you to write a single static-typed cython algorithm that can
operate on values of multiple types. Thus fused types allow `generic
programming`_ and are akin to templates in C++ or generics in languages like
Java / C#.

.. _generic programming: https://en.wikipedia.org/wiki/Generic_programming

.. Note:: Fused types are not currently supported as attributes of extension
          types.  Only variables and function/method arguments can be declared
          with fused types.


Quickstart
==========

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/char_or_float.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/char_or_float.pyx

This gives:

.. code-block:: pycon

    >>> show_me()
    char -128
    float 128.0

``plus_one(a)`` "specializes" the fused type ``char_or_float`` as a ``char``,
whereas ``plus_one(b)`` specializes ``char_or_float`` as a ``float``.

Declaring Fused Types
=====================

Fused types may be declared as follows:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            my_fused_type = cython.fused_type(cython.int, cython.float)

    .. group-tab:: Cython

        .. code-block:: cython

            ctypedef fused my_fused_type:
                int
                double

This declares a new type called ``my_fused_type`` which can be *either* an
``int`` *or* a ``double``.

Only names may be used for the constituent types, but they may be any
(non-fused) type, including a typedef. I.e. one may write:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            my_double = cython.typedef(cython.double)
            my_fused_type = cython.fused_type(cython.int, my_double)

    .. group-tab:: Cython

        .. code-block:: cython

            ctypedef double my_double
            ctypedef fused fused_type:
                int
                my_double

Using Fused Types
=================

Fused types can be used to declare parameters of functions or methods:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.cfunc
            def cfunc(arg: my_fused_type):
                return arg + 1

    .. group-tab:: Cython

        .. code-block:: cython

            cdef cfunc(my_fused_type arg):
                return arg + 1

If the same fused type appears more than once in the function arguments,
then they will all have the same specialised type:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.cfunc
            def cfunc(arg1: my_fused_type, arg2: my_fused_type):
                # arg1 and arg2 always have the same type here
                return arg1 + arg2

    .. group-tab:: Cython

        .. code-block:: cython

            cdef cfunc(my_fused_type arg1, my_fused_type arg2):
                # arg1 and arg2 always have the same type here
                return arg1 + arg2

Here, the type of both parameters is either an int, or a double
(according to the previous examples), because they use the same fused type
name ``my_fused_type``.  Mixing different fused types (or differently named
fused types) in the arguments will specialise them independently:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            def func(x: A, y: B):
                ...

    .. group-tab:: Cython

        .. code-block:: cython


            def func(A x, B y):
                ...

This will result in specialized code paths for all combinations of types
contained in ``A`` and ``B``, e.g.:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            my_fused_type = cython.fused_type(cython.int, cython.double)



            my_fused_type2 = cython.fused_type(cython.int, cython.double)


            @cython.cfunc
            def func(a: my_fused_type, b: my_fused_type2):
                # a and b may have the same or different types here
                print("SAME!" if my_fused_type is my_fused_type2 else "NOT SAME!")
                return a + b

    .. group-tab:: Cython

        .. code-block:: cython

            ctypedef fused my_fused_type:
                int
                double

            ctypedef fused my_fused_type2:
                int
                double

            cdef func(my_fused_type a, my_fused_type2 b):
                # a and b may have the same or different types here
                print("SAME!" if my_fused_type is my_fused_type2 else "NOT SAME!")
                return a + b




.. Note::  A simple typedef to rename the fused type does not currently work here.
    See Github issue :issue:`4302`.


Fused types and arrays
----------------------

Note that specializations of only numeric types may not be very useful, as one
can usually rely on promotion of types.  This is not true for arrays, pointers
and typed views of memory however.  Indeed, one may write:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.cfunc
            def myfunc(x: A[:, :]):
                ...

            # and

            @cython.cfunc
            cdef otherfunc(x: cython.pointer[A]):
                ...


    .. group-tab:: Cython

        .. code-block:: cython

            cdef myfunc(A[:, :] x):
                ...

            # and

            cdef otherfunc(A *x):
                ...

Following code snippet shows an example with pointer to the fused type:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/pointer.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/pointer.pyx

.. Note::

    In Cython 0.20.x and earlier, the compiler generated the full cross
    product of all type combinations when a fused type was used by more than one
    memory view in a type signature, e.g.

    ::

        def myfunc(A[:] a, A[:] b):
            # a and b had independent item types in Cython 0.20.x and earlier.
            ...

    This was unexpected for most users, unlikely to be desired, and also inconsistent
    with other structured type declarations like C arrays of fused types, which were
    considered the same type.  It was thus changed in Cython 0.21 to use the same
    type for all memory views of a fused type.  In order to get the original
    behaviour, it suffices to declare the same fused type under different names, and
    then use these in the declarations::

        ctypedef fused A:
            int
            long

        ctypedef fused B:
            int
            long

        def myfunc(A[:] a, B[:] b):
            # a and b are independent types here and may have different item types
            ...

    To get only identical types also in older Cython versions (pre-0.21), a ``ctypedef``
    can be used::

        ctypedef A[:] A_1d

        def myfunc(A_1d a, A_1d b):
            # a and b have identical item types here, also in older Cython versions
            ...


Selecting Specializations
=========================

You can select a specialization (an instance of the function with specific or
specialized (i.e., non-fused) argument types) in two ways: either by indexing or
by calling.


.. _fusedtypes_indexing:

Indexing
--------

You can index functions with types to get certain specializations, i.e.:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/indexing.py
            :caption: indexing.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/indexing.pyx
            :caption: indexing.pyx

Indexed functions can be called directly from Python:

.. code-block:: pycon

    >>> import cython
    >>> import indexing
    cfunc called: double 5.0 double 1.0
    cpfunc called: float 1.0 double 2.0
    func called: float 1.0 double 2.0
    >>> indexing.cpfunc[cython.float, cython.float](1, 2)
    cpfunc called: float 1.0 float 2.0
    >>> indexing.func[cython.float, cython.float](1, 2)
    func called: float 1.0 float 2.0

If a fused type is used as a component of a more complex type
(for example a pointer to a fused type, or a memoryview of a fused type),
then you should index the function with the individual component and
not the full argument type:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            @cython.cfunc
            def myfunc(x: cython.pointer[A]):
                ...

            # Specialize using int, not int *
            myfunc[cython.int](myint)

    .. group-tab:: Cython

        .. code-block:: cython

            cdef myfunc(A *x):
                ...

            # Specialize using int, not int *
            myfunc[int](myint)

For memoryview indexing from python space we can do the following:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/memoryview_indexing.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/memoryview_indexing.pyx

The same goes for when using e.g. ``cython.numeric[:, :]``.

Calling
-------

A fused function can also be called with arguments, where the dispatch is
figured out automatically:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            def main():
                p1: cython.double = 1.0
                p2: cython.float = 2.0
                cfunc(p1, p1)          # prints "cfunc called: double 1.0 double 1.0"
                cpfunc(p1, p2)         # prints "cpfunc called: double 1.0 float 2.0"

    .. group-tab:: Cython

        .. code-block:: cython

            def main():
                cdef double p1 = 1.0
                cdef float p2 = 2.0
                cfunc(p1, p1)          # prints "cfunc called: double 1.0 double 1.0"
                cpfunc(p1, p2)         # prints "cpfunc called: double 1.0 float 2.0"

For a ``cdef`` or ``cpdef`` function called from Cython this means that the
specialization is figured out at compile time. For ``def`` functions the
arguments are typechecked at runtime, and a best-effort approach is performed to
figure out which specialization is needed. This means that this may result in a
runtime ``TypeError`` if no specialization was found. A ``cpdef`` function is
treated the same way as a ``def`` function if the type of the function is
unknown (e.g. if it is external and there is no cimport for it).

The automatic dispatching rules are typically as follows, in order of
preference:

* try to find an exact match
* choose the biggest corresponding numerical type (biggest float, biggest
  complex, biggest int)

Built-in Fused Types
====================

There are some built-in fused types available for convenience, these are::

    cython.integral # short, int, long
    cython.floating # float, double
    cython.numeric  # short, int, long, float, double, float complex, double complex

Casting Fused Functions
=======================

.. note:: Pointers to functions are currently not supported by pure Python mode. (GitHub issue :issue:`4279`)

Fused ``cdef`` and ``cpdef`` functions may be cast or assigned to C function pointers as follows::

    cdef myfunc(cython.floating, cython.integral):
        ...

    # assign directly
    cdef object (*funcp)(float, int)
    funcp = myfunc
    funcp(f, i)

    # alternatively, cast it
    (<object (*)(float, int)> myfunc)(f, i)

    # This is also valid
    funcp = myfunc[float, int]
    funcp(f, i)

Type Checking Specializations
=============================

Decisions can be made based on the specializations of the fused parameters.
False conditions are pruned to avoid invalid code. One may check with ``is``,
``is not`` and ``==`` and ``!=`` to see if a fused type is equal to a certain
other non-fused type (to check the specialization), or use ``in`` and ``not in``
to figure out whether a specialization is part of another set of types
(specified as a fused type). In example:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/type_checking.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/type_checking.pyx

.. _fused_gil_conditional:

Conditional GIL Acquiring / Releasing
=====================================

Acquiring and releasing the GIL can be controlled by a condition
which is known at compile time (see :ref:`gil_conditional`).

This is most useful when combined with fused types.
A fused type function may have to handle both cython native types
(e.g. cython.int or cython.double) and python types (e.g. object or bytes).
Conditional Acquiring / Releasing the GIL provides a method for running
the same piece of code either with the GIL released (for cython native types)
and with the GIL held (for python types):

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/conditional_gil.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/conditional_gil.pyx

__signatures__
==============

Finally, function objects from ``def`` or ``cpdef`` functions have an attribute
``__signatures__``, which maps the signature strings to the actual specialized
functions. This may be useful for inspection:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/fusedtypes/indexing.py
            :lines: 1-9,14-16
            :caption: indexing.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/fusedtypes/indexing.pyx
            :lines: 1-9,14-16
            :caption: indexing.pyx

.. code-block:: pycon

   >>> from indexing import cpfunc
   >>> cpfunc.__signatures__,
   ({'double|double': <cyfunction __pyx_fuse_0_0cpfunc at 0x107292f20>, 'double|float': <cyfunction __pyx_fuse_0_1cpfunc at 0x1072a6040>, 'float|double': <cyfunction __pyx_fuse_1_0cpfunc at 0x1072a6120>, 'float|float': <cyfunction __pyx_fuse_1_1cpfunc at 0x1072a6200>},)

Listed signature strings may also
be used as indices to the fused function, but the index format may change between
Cython versions

.. code-block:: pycon

    >>> specialized_function = cpfunc["double|float"]
    >>> specialized_function(5.0, 1.0)
    cpfunc called: double 5.0 float 1.0

However, the better way how to index is by providing list of types as mentioned in :ref:`fusedtypes_indexing` section.
