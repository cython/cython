.. highlight:: cython

.. _fusedtypes:

***********************
Fused Types (Templates)
***********************

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

.. literalinclude:: ../../examples/userguide/fusedtypes/char_or_float.pyx

This gives::

    >>> show_me()
    char -128
    float 128.0

``plus_one(a)`` "specializes" the fused type ``char_or_float`` as a ``char``,
whereas ``plus_one(b)`` specializes ``char_or_float`` as a ``float``.

Declaring Fused Types
=====================

Fused types may be declared as follows::

    cimport cython

    ctypedef fused my_fused_type:
        cython.int
        cython.double

This declares a new type called ``my_fused_type`` which can be *either* an
``int`` *or* a ``double``.  Alternatively, the declaration may be written as::

    my_fused_type = cython.fused_type(cython.int, cython.float)

Only names may be used for the constituent types, but they may be any
(non-fused) type, including a typedef.  i.e. one may write::

    ctypedef double my_double
    my_fused_type = cython.fused_type(cython.int, my_double)

Using Fused Types
=================

Fused types can be used to declare parameters of functions or methods::

    cdef cfunc(my_fused_type arg):
        return arg + 1

If the you use the same fused type more than once in an argument list, then each
specialization of the fused type must be the same::

    cdef cfunc(my_fused_type arg1, my_fused_type arg2):
        return cython.typeof(arg1) == cython.typeof(arg2)

In this case, the type of both parameters is either an int, or a double
(according to the previous examples). However, because these arguments use the
same fused type ``my_fused_type``, both ``arg1`` and ``arg2`` are
specialized to the same type.  Therefore this function returns True for every
possible valid invocation. You are allowed to mix fused types however::

    def func(A x, B y):
        ...

where ``A`` and ``B`` are different fused types.  This will result in
specialized code paths for all combinations of types contained in ``A``
and ``B``.

Fused types and arrays
----------------------

Note that specializations of only numeric types may not be very useful, as one
can usually rely on promotion of types.  This is not true for arrays, pointers
and typed views of memory however.  Indeed, one may write::

    def myfunc(A[:, :] x):
        ...

    # and

    cdef otherfunc(A *x):
        ...

Note that in Cython 0.20.x and earlier, the compiler generated the full cross
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

Indexing
--------

You can index functions with types to get certain specializations, i.e.::

    cfunc[cython.p_double](p1, p2)

    # From Cython space
    func[float, double](myfloat, mydouble)

    # From Python space
    func[cython.float, cython.double](myfloat, mydouble)

If a fused type is used as a base type, this will mean that the base type is the
fused type, so the base type is what needs to be specialized::

    cdef myfunc(A *x):
        ...

    # Specialize using int, not int *
    myfunc[int](myint)

Calling
-------

A fused function can also be called with arguments, where the dispatch is
figured out automatically::

    cfunc(p1, p2)
    func(myfloat, mydouble)

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
(specified as a fused type). In example::

    ctypedef fused bunch_of_types:
        ...

    ctypedef fused string_t:
        cython.p_char
        bytes
        unicode

    cdef cython.integral myfunc(cython.integral i, bunch_of_types s):
        cdef int *int_pointer
        cdef long *long_pointer

        # Only one of these branches will be compiled for each specialization!
        if cython.integral is int:
            int_pointer = &i
        else:
            long_pointer = &i

        if bunch_of_types in string_t:
            print("s is a string!")

__signatures__
==============

Finally, function objects from ``def`` or ``cpdef`` functions have an attribute
__signatures__, which maps the signature strings to the actual specialized
functions. This may be useful for inspection.  Listed signature strings may also
be used as indices to the fused function, but the index format may change between
Cython versions::

    specialized_function = fused_function["MyExtensionClass|int|float"]

It would usually be preferred to index like this, however::

    specialized_function = fused_function[MyExtensionClass, int, float]

Although the latter will select the biggest types for ``int`` and ``float`` from
Python space, as they are not type identifiers but builtin types there. Passing
``cython.int`` and ``cython.float`` would resolve that, however.

For memoryview indexing from python space we can do the following::

    ctypedef fused my_fused_type:
        int[:, ::1]
        float[:, ::1]

    def func(my_fused_type array):
        ...

    my_fused_type[cython.int[:, ::1]](myarray)

The same goes for when using e.g. ``cython.numeric[:, :]``.
