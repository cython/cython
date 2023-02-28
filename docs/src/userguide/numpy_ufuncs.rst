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

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc.pyx

You can have as many arguments to your function as you like. If you want to have multiple
output arguments then you can use the :ref:`ctuple syntax<typing_types>`:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc_ctuple.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc_ctuple.pyx

If you want to accept multiple different argument types then you can use :ref:`fusedtypes`:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc_fused.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/numpy_ufuncs/ufunc_fused.pyx

Finally, if you declare the ``cdef`` function as ``nogil`` then Cython will release the
:term:`GIL<Global Interpreter Lock or GIL>` once in the generated ufunc. This is a slight difference
from the general behaviour of ``nogil`` functions (they generally do not automatically
release the GIL, but instead can be run without the GIL).

This feature relies on Numpy. Therefore if you create a ufunc in
Cython, you must have the Numpy headers available when you build the generated C code, and
users of your module must have Numpy installed when they run it.
