.. _pxd_files:

*********
pxd files
*********

.. include::
    ../two-syntax-variants-used

In addition to the ``.pyx`` and ``.py`` source files, Cython uses ``.pxd`` files
which work like C header files -- they contain Cython declarations
(and sometimes code sections) which are only meant for inclusion by
Cython modules.  A ``.pxd`` file is imported into a ``.pyx`` module by
using the ``cimport`` keyword.

``.pxd`` files have many use-cases:

1.  They can be used for sharing external C declarations.
2.  They can contain functions which are well suited for inlining by
    the C compiler. Such functions should be marked ``inline``, example:

    .. literalinclude:: ../../examples/tutorial/pxd_files/inline.pxd
        :caption: inline.pxd

3.  When accompanying an equally named ``.pyx`` / ``.py`` file, they
    provide a Cython interface to the Cython module so that other
    Cython modules can communicate with it using a more efficient
    protocol than the Python one.

In our integration example, we might break it up into ``.pxd`` files like this:

1.  Add a ``cmath.pxd``:

    .. literalinclude:: ../../examples/tutorial/pxd_files/cmath.pxd
        :caption: cmath.pxd

    Then one would simply do

    .. tabs::

        .. group-tab:: Pure Python

            .. literalinclude:: ../../examples/tutorial/pxd_files/integrate.py
                :caption: integrate.py

            .. include::
                ../cimport-warning

        .. group-tab:: Cython

            .. literalinclude:: ../../examples/tutorial/pxd_files/integrate.pyx
                :caption: integrate.pyx

2.  Add a ``integrate.pxd`` so that other modules written in Cython
    can define fast custom functions to integrate:

    .. code-block:: cython
        :caption: integrate.pxd

        cdef class Function:
           cpdef evaluate(self, double x)

        cpdef integrate(Function f, double a, double b, int N)

    Note that if you have a cdef class with attributes, the attributes must
    be declared in the class declaration ``.pxd`` file (if you use one), not
    the ``.pyx`` / ``.py`` file. The compiler will tell you about this.


__init__.pxd
============

Cython also supports ``__init__.pxd`` files for declarations in package's
namespaces, similar to ``__init__.py`` files in Python.

Continuing the integration example, we could package the module as follows:

1.  Place the module files in a directory tree as one usually would for
    Python:

    .. tabs::

        .. group-tab:: Pure Python

            .. code-block:: text

                CyIntegration/
                ├── __init__.py
                ├── __init__.pxd
                ├── integrate.py
                └── integrate.pxd

        .. group-tab:: Cython

            .. code-block:: text

                CyIntegration/
                ├── __init__.pyx
                ├── __init__.pxd
                ├── integrate.pyx
                └── integrate.pxd

2.  In ``__init__.pxd``, use ``cimport`` for any declarations that one
    would want to be available from the package's main namespace:

    .. tabs::

        .. group-tab:: Pure Python

            .. code-block:: python

                from cython.cimports.CyIntegration import integrate

        .. group-tab:: Cython

            .. code-block:: cython

                from CyIntegration cimport integrate

    Other modules would then be able to use ``cimport`` on the package in
    order to recursively gain faster, Cython access to the entire package
    and the data declared in its modules:

    .. tabs::

        .. group-tab:: Pure Python

            .. code-block:: python

                from cython.cimports import CyIntegration

                @cython.ccall
                def do_integration(f: CyIntegration.integrate.Function):
                    return CyIntegration.integrate.integrate(f, 0., 2., 1)

            .. include::
                ../cimport-warning

        .. group-tab:: Cython

            .. code-block:: cython

                cimport CyIntegration


                cpdef do_integration(CyIntegration.integrate.Function f):
                    return CyIntegration.integrate.integrate(f, 0., 2., 1)
