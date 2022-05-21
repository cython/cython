.. highlight:: python

.. _numpy-ufuncs:

**************************
Creating Numpy ufuncs
**************************

Numpy supports a `special type of function called a ufunc
<https://numpy.org/doc/stable/reference/ufuncs.html>`_ . 
These support array broadcasting (i.e. the ability to handle arguments with any
number of dimensions), alongside other useful features.

Cython can generate a ufunc from a Cython C function by tagging it with the ``@cython.ufunc``
decorator. The input and output argument types should be scalar variables ("generic ufuncs" are
not yet supported) and should either by Python objects or simple numeric types. The body
of such a function is inserted into an efficient, compiled loop.

.. code-block:: cython

    cimport cython

    @cython.ufunc
    cdef double add_one(double x):
        # of course, this simple operation can already by done efficiently in Numpy!
        return x+1  

You can have as many arguments to your function as you like. If you want to have multiple
output arguments then you can use the :ref:`ctuple syntax<typing_types>`:

.. code-block:: cython

    cimport cython

    @cython.ufunc
    cdef (int, int) add_one_add_two(int x):
        return x+1, x+2

If you want to accept multiple different argument types then you can use :ref:`fusedtypes`:

.. code-block:: cython

    cimport cython

    @cython.ufunc
    cdef cython.numeric generic_add_one(cython.numeric x):
        return x+1

This feature relies on Numpy. Therefore if you create a ufunc in
Cython, you must have the Numpy headers available when you build the generated C code, and 
users of your module must have Numpy installed when they run it.
