.. highlight:: cython

.. _cython30:

*********************************
Migrating from Cython 0.29 to 3.0
*********************************

Cython 3.0 is a major revision of the compiler and the language
that comes with some backwards incompatible changes.
This document lists the important ones and explains how to deal with
them in existing code.


Python 3 syntax/semantics
=========================

Cython 3.0 now uses Python 3 syntax and semantics by default, which previously
required setting the ``language_level`` `directive <compiler-directives>` to
either ``3`` or ``3str``.
The new default setting is now ``language_level=3str``, which means Python 3
semantics, but unprefixed strings are ``str`` objects, i.e. unicode text strings
under Python 3 and byte strings under Python 2.7.

You can revert your code to the previous (Python 2.x) semantics by setting
``language_level=2``.

Further semantic changes due to the language level include:

* ``/``-division uses the true (float) division operator, unless ``cdivision`` is enabled.
* ``print`` is a function, not a statement.
* Python classes that are defined without bases (``class C: ...``) are "new-style"
  classes also in Py2.x (if you never heard about "old-style classes", you're probably
  happy without them).
* Annotations (type hints) are now stored as strings.
  (`PEP 563 <https://github.com/cython/cython/issues/2863>`_)
* ``StopIteration`` handling in generators has been changed according to
  `PEP 479 <https://www.python.org/dev/peps/pep-0479/>`_.


Python semantics
================

Some Python compatibility bugs were fixed, e.g.

* Subscripting (``x[1]``) now tries the mapping protocol before the sequence protocol.
  (https://github.com/cython/cython/issues/1807)
* Exponentiation of integer literals now follows Python semantics and not C semantics.
  (https://github.com/cython/cython/issues/2133)


Binding functions
=================

The :ref:`binding directive <compiler-directives>` is now enabled by default.
This makes Cython compiled Python (``def``) functions mostly compatible
with normal (non-compiled) Python functions, regarding signature introspection,
annotations, etc.

It also makes them bind as methods in Python classes on attribute assignments,
thus the name.
If this is not intended, i.e. if a function is really meant to be a function
and never a method, you can disable the binding (and all other Python function
features) by setting ``binding=False`` or selectively adding a decorator
``@cython.binding(False)``.
In pure Python mode, the decorator was not available in Cython 0.29.16 yet,
but compiled code does not suffer from this.

We recommend, however, to keep the new function features and instead deal
with the binding issue using the standard Python ``staticmethod()`` builtin.

::

    def func(self, b): ...

    class MyClass(object):
        binding_method = func

        no_method = staticmethod(func)


Namespace packages
==================

Cython now has support for loading pxd files also from namespace packages
according to `PEP-420 <https://www.python.org/dev/peps/pep-0420/>`_.
This might have an impact on the import path.


NumPy C-API
===========

Cython used to generate code that depended on the deprecated pre-NumPy-1.7 C-API.
This is no longer the case with Cython 3.0.

You can now define the macro ``NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION``
to get rid of the long-standing build warnings that the compiled C module
uses a deprecated API.  Either per file::

    # distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

or by setting it in your Extensions in ``setup.py``::

    Extension(...
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )

One side-effect of the different C-API usage is that your code may now
require a call to the `NumPy C-API initialisation function
<https://docs.scipy.org/doc/numpy-1.17.0/reference/c-api.array.html#importing-the-api>`_
where it previously got away without doing so.

In order to reduce the user impact here, Cython 3.0 will now call it
automatically when it sees ``numpy`` being cimported, but the function
not being used.
In the (hopefully rare) cases where this gets in the way, the internal
C-API initialisation can be disabled by faking the use of the function
without actually calling it, e.g.

::

    # Explicitly disable the automatic initialisation of NumPy's C-API.
    <void>import_array

Class-private name mangling
===========================

Cython has been updated to follow the `Python rules for class-private names
<https://docs.python.org/3/tutorial/classes.html#private-variables>`_
more closely. Essentially any name that starts with and doesn't end with 
``__`` within a class is mangled with the class name. Most user code
should be unaffected -- unlike in Python unmangled global names will
still be matched to ensure it is possible to access C names
beginning with ``__``::

     cdef extern void __foo()
     
     class C: # or "cdef class"
        def call_foo(self):
            return __foo() # still calls the global name
            
What will no-longer work is overriding methods starting with ``__`` in
a ``cdef class``::

    cdef class Base:
        cdef __bar(self):
            return 1

        def call_bar(self):
            return self.__bar()

    cdef class Derived(Base):
        cdef __bar(self):
            return 2

Here ``Base.__bar`` is mangled to ``_Base__bar`` and ``Derived.__bar``
to ``_Derived__bar``. Therefore ``call_bar`` will always call 
``_Base__bar``. This matches established Python behaviour and applies
for ``def``, ``cdef`` and ``cpdef`` methods and attributes.
