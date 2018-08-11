Calling C functions
====================

This tutorial describes shortly what you need to know in order to call
C library functions from Cython code.  For a longer and more
comprehensive tutorial about using external C libraries, wrapping them
and handling errors, see :doc:`clibraries`.

For simplicity, let's start with a function from the standard C
library.  This does not add any dependencies to your code, and it has
the additional advantage that Cython already defines many such
functions for you. So you can just cimport and use them.

For example, let's say you need a low-level way to parse a number from
a ``char*`` value.  You could use the ``atoi()`` function, as defined
by the ``stdlib.h`` header file.  This can be done as follows:

.. literalinclude:: ../../examples/tutorial/external/atoi.pyx

You can find a complete list of these standard cimport files in
Cython's source package
`Cython/Includes/ <https://github.com/cython/cython/tree/master/Cython/Includes>`_.
They are stored in ``.pxd`` files, the standard way to provide reusable
Cython declarations that can be shared across modules
(see :ref:`sharing-declarations`).

Cython also has a complete set of declarations for CPython's C-API.
For example, to test at C compilation time which CPython version
your code is being compiled with, you can do this:

.. literalinclude:: ../../examples/tutorial/external/py_version_hex.pyx

Cython also provides declarations for the C math library:

.. literalinclude:: ../../examples/tutorial/external/libc_sin.pyx


Dynamic linking
---------------

The libc math library is special in that it is not linked by default
on some Unix-like systems, such as Linux. In addition to cimporting the
declarations, you must configure your build system to link against the
shared library ``m``.  For distutils, it is enough to add it to the
``libraries`` parameter of the ``Extension()`` setup:

.. literalinclude:: ../../examples/tutorial/external/setup.py

External declarations
---------------------

If you want to access C code for which Cython does not provide a ready
to use declaration, you must declare them yourself.  For example, the
above ``sin()`` function is defined as follows::

  cdef extern from "math.h":
      double sin(double x)

This declares the ``sin()`` function in a way that makes it available
to Cython code and instructs Cython to generate C code that includes
the ``math.h`` header file.  The C compiler will see the original
declaration in ``math.h`` at compile time, but Cython does not parse
"math.h" and requires a separate definition.

Just like the ``sin()`` function from the math library, it is possible
to declare and call into any C library as long as the module that
Cython generates is properly linked against the shared or static
library.

Note that you can easily export an external C function from your Cython
module by declaring it as ``cpdef``.  This generates a Python wrapper
for it and adds it to the module dict.  Here is a Cython module that
provides direct access to the C ``sin()`` function for Python code:

.. literalinclude:: ../../examples/tutorial/external/cpdef_sin.pyx

You get the same result when this declaration appears in the ``.pxd``
file that belongs to the Cython module (i.e. that has the same name,
see :ref:`sharing-declarations`).
This allows the C declaration to be reused in other Cython modules,
while still providing an automatically generated Python wrapper in
this specific module.


Naming parameters
-----------------

Both C and Cython support signature declarations without parameter
names like this::

  cdef extern from "string.h":
      char* strstr(const char*, const char*)

However, this prevents Cython code from calling it with keyword
arguments.  It is therefore preferable
to write the declaration like this instead:

.. literalinclude:: ../../examples/tutorial/external/keyword_args.pyx

You can now make it clear which of the two arguments does what in
your call, thus avoiding any ambiguities and often making your code
more readable:

.. literalinclude:: ../../examples/tutorial/external/keyword_args_call.pyx

Note that changing existing parameter names later is a backwards
incompatible API modification, just as for Python code.  Thus, if
you provide your own declarations for external C or C++ functions,
it is usually worth the additional bit of effort to choose the
names of their arguments well.
