.. highlight:: python

.. _numpy-ufuncs:

*********************
Creating Numpy ufuncs
*********************

.. include::
    ../two-syntax-variants-used

Numpy supports a `special type of function called a ufunc
<https://numpy.org/doc/stable/reference/ufuncs.html>`_ .
These support array broadcasting (i.e. the ability to handle arguments with any
number of dimensions), alongside other useful features.

Cython can generate a ufunc from a Cython C function by tagging it with the ``@cython.ufunc``
decorator. The input and output argument types should be scalar variables ("generic ufuncs" are
not yet supported) and should either by Python objects or simple numeric types. The body
of such a function is inserted into an efficient, compiled loop.

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            import cython

            @cython.cfunc
            @cython.ufunc
            def add_one(x: cython.double) -> cython.double:
                # of course, this simple operation can already by done efficiently in Numpy!
                return x+1

    .. group-tab:: Cython

        .. code-block:: cython

            cimport cython


            @cython.ufunc
            cdef double add_one(double x):
                # of course, this simple operation can already by done efficiently in Numpy!
                return x+1

You can have as many arguments to your function as you like. If you want to have multiple
output arguments then you can use the :ref:`ctuple syntax<typing_types>`:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            import cython

            @cython.cfunc
            @cython.ufunc
            def add_one_add_two(x: cython.int) -> (cython.int, cython.int):
                return x+1, x+2

    .. group-tab:: Cython

        .. code-block:: cython

            cimport cython


            @cython.ufunc
            cdef (int, int) add_one_add_two(int x):
                return x+1, x+2

If you want to accept multiple different argument types then you can use :ref:`fusedtypes`:

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            import cython

            @cython.cfunc
            @cython.ufunc
            def generic_add_one(x: cython.numeric) -> cython.numeric:
                return x+1

    .. group-tab:: Cython

        .. code-block:: cython

            cimport cython


            @cython.ufunc
            cdef cython.numeric generic_add_one(cython.numeric x):
                return x+1

Finally, if you declare the ``cdef``/``@cfunc`` function as ``nogil`` then Cython will release the
:term:`GIL<Global Interpreter Lock or GIL>` once in the generated ufunc. This is a slight difference
from the general behaviour of ``nogil`` functions (they generally do not automatically
release the GIL, but instead can be run without the GIL).

This feature relies on Numpy. Therefore if you create a ufunc in
Cython, you must have the Numpy headers available when you build the generated C code, and
users of your module must have Numpy installed when they run it.
