.. highlight:: cython

.. _cython-limitations:

*************
Limitations
*************

This page used to list bugs in Cython that made the semantics of
compiled code differ from that in Python.  Most of the missing
features have been fixed in Cython 0.15.  A future version of
Cython is planned to provide full Python language compatibility.
For now, the issue tracker can provide an overview of deviations
that we are aware of and would like to see fixed.

https://github.com/cython/cython/labels/Python%20Semantics

Below is a list of differences that we will probably not be addressing.
Most of these things that fall more into the implementation details rather
than semantics, and we may decide not to fix (or require a --pedantic flag to get).


Nested tuple argument unpacking
===============================

::

    def f((a,b), c):
        pass

This was removed in Python 3.


Inspect support
===============

While it is quite possible to emulate the interface of functions in
Cython's own function type, and recent Cython releases have seen several
improvements here, the "inspect" module does not consider a Cython
implemented function a "function", because it tests the object type
explicitly instead of comparing an abstract interface or an abstract
base class. This has a negative impact on code that uses inspect to
inspect function objects, but would require a change to Python itself.


Stack frames
============

Currently we generate fake tracebacks as part of exception propagation,
but don't fill in locals and can't fill in co_code.
To be fully compatible, we would have to generate these stack frame objects at
function call time (with a potential performance penalty).  We may have an
option to enable this for debugging.


Identity vs. equality for inferred literals
===========================================

::

    a = 1.0          # a inferred to be C type 'double'
    b = c = None     # b and c inferred to be type 'object'
    if some_runtime_expression:
        b = a        # creates a new Python float object
        c = a        # creates a new Python float object
    print(b is c)     # most likely not the same object
