.. _pxd_files:

pxd files
=========

In addition to the ``.pyx`` source files, Cython uses ``.pxd`` files
which work like C header files -- they contain Cython declarations
(and sometimes code sections) which are only meant for inclusion by
Cython modules.  A ``pxd`` file is imported into a ``pyx`` module by
using the ``cimport`` keyword.

``pxd`` files have many use-cases:

 1. They can be used for sharing external C declarations.
 2. They can contain functions which are well suited for inlining by
    the C compiler. Such functions should be marked ``inline``, example:
    ::

       cdef inline int int_min(int a, int b):
           return b if b < a else a

 3. When accompanying an equally named ``pyx`` file, they
    provide a Cython interface to the Cython module so that other
    Cython modules can communicate with it using a more efficient
    protocol than the Python one.

In our integration example, we might break it up into ``pxd`` files like this:

 1. Add a ``cmath.pxd`` function which defines the C functions available from
    the C ``math.h`` header file, like ``sin``. Then one would simply do
    ``from cmath cimport sin`` in ``integrate.pyx``.
 2. Add a ``integrate.pxd`` so that other modules written in Cython
    can define fast custom functions to integrate.
    ::

       cdef class Function:
           cpdef evaluate(self, double x)
       cpdef integrate(Function f, double a,
                       double b, int N)

    Note that if you have a cdef class with attributes, the attributes must
    be declared in the class declaration ``pxd`` file (if you use one), not
    the ``pyx`` file. The compiler will tell you about this.
