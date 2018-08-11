.. highlight:: cython

.. _sharing-declarations:

********************************************
Sharing Declarations Between Cython Modules
********************************************

This section describes how to make C declarations, functions and extension
types in one Cython module available for use in another Cython module.
These facilities are closely modeled on the Python import mechanism,
and can be thought of as a compile-time version of it.


Definition and Implementation files
====================================

A Cython module can be split into two parts: a definition file with a ``.pxd``
suffix, containing C declarations that are to be available to other Cython
modules, and an implementation file with a ``.pyx`` suffix, containing
everything else. When a module wants to use something declared in another
module's definition file, it imports it using the :keyword:`cimport`
statement.

A ``.pxd`` file that consists solely of extern declarations does not need
to correspond to an actual ``.pyx`` file or Python module. This can make it a
convenient place to put common declarations, for example declarations of
functions from  an :ref:`external library <external-C-code>` that one
wants to use in several modules.


What a Definition File contains
================================

A definition file can contain:

* Any kind of C type declaration.
* extern C function or variable declarations.
* Declarations of C functions defined in the module.
* The definition part of an extension type (see below).

It cannot contain the implementations of any C or Python functions, or any
Python class definitions, or any executable statements. It is needed when one
wants to  access :keyword:`cdef` attributes and methods, or to inherit from
:keyword:`cdef` classes defined in this module.

.. note::

    You don't need to (and shouldn't) declare anything in a declaration file
    public in order to make it available to other Cython modules; its mere
    presence in a definition file does that. You only need a public
    declaration if you want to make something available to external C code.


What an Implementation File contains
======================================

An implementation file can contain any kind of Cython statement, although there
are some restrictions on the implementation part of an extension type if the
corresponding definition file also defines that type (see below).
If one doesn't need to :keyword:`cimport` anything from this module, then this
is the only file one needs.


.. _cimport:

The cimport statement
=======================

The :keyword:`cimport` statement is used in a definition or
implementation file to gain access to names declared in another definition
file. Its syntax exactly parallels that of the normal Python import
statement::

    cimport module [, module...]

    from module cimport name [as name] [, name [as name] ...]

Here is an example. :file:`dishes.pxd` is a definition file which exports a
C data type. :file:`restaurant.pyx` is an implementation file which imports and
uses it.

:file:`dishes.pxd`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/dishes.pxd

:file:`restaurant.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/restaurant.pyx

It is important to understand that the :keyword:`cimport` statement can only
be used to import C data types, C functions and variables, and extension
types. It cannot be used to import any Python objects, and (with one
exception) it doesn't imply any Python import at run time. If you want to
refer to any Python names from a module that you have cimported, you will have
to include a regular import statement for it as well.

The exception is that when you use :keyword:`cimport` to import an extension type, its
type object is imported at run time and made available by the name under which
you imported it. Using :keyword:`cimport` to import extension types is covered in more
detail below.

If a ``.pxd`` file changes, any modules that :keyword:`cimport` from it may need to be
recompiled.  The ``Cython.Build.cythonize`` utility can take care of this for you.


Search paths for definition files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you :keyword:`cimport` a module called ``modulename``, the Cython
compiler searches for a file called :file:`modulename.pxd`.
It searches for this file along the path for include files
(as specified by ``-I`` command line options or the ``include_path``
option to ``cythonize()``), as well as ``sys.path``.

Using ``package_data`` to install ``.pxd`` files in your ``setup.py`` script
allows other packages to cimport items from your module as a dependency.

Also, whenever you compile a file :file:`modulename.pyx`, the corresponding
definition file :file:`modulename.pxd` is first searched for along the
include path (but not ``sys.path``), and if found, it is processed before
processing the ``.pyx`` file.


Using cimport to resolve naming conflicts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :keyword:`cimport` mechanism provides a clean and simple way to solve the
problem of wrapping external C functions with Python functions of the same
name. All you need to do is put the extern C declarations into a ``.pxd`` file
for an imaginary module, and :keyword:`cimport` that module. You can then
refer to the C functions by qualifying them with the name of the module.
Here's an example:

:file:`c_lunch.pxd`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/c_lunch.pxd

:file:`lunch.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/lunch.pyx

You don't need any :file:`c_lunch.pyx` file, because the only things defined
in :file:`c_lunch.pxd` are extern C entities. There won't be any actual
``c_lunch`` module at run time, but that doesn't matter; the
:file:`c_lunch.pxd` file has done its job of providing an additional namespace
at compile time.


Sharing C Functions
===================

C functions defined at the top level of a module can be made available via
:keyword:`cimport` by putting headers for them in the ``.pxd`` file, for
example:

:file:`volume.pxd`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/volume.pxd

:file:`volume.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/volume.pyx

:file:`spammery.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/spammery.pyx

.. note::

    When a module exports a C function in this way, an object appears in the
    module dictionary under the function's name. However, you can't make use of
    this object from Python, nor can you use it from Cython using a normal import
    statement; you have to use :keyword:`cimport`.

.. _sharing_extension_types:

Sharing Extension Types
=======================

An extension type can be made available via :keyword:`cimport` by splitting
its definition into two parts, one in a definition file and the other in the
corresponding implementation file.

The definition part of the extension type can only declare C attributes and C
methods, not Python methods, and it must declare all of that type's C
attributes and C methods.

The implementation part must implement all of the C methods declared in the
definition part, and may not add any further C attributes. It may also define
Python methods.

Here is an example of a module which defines and exports an extension type,
and another module which uses it:

:file:`shrubbing.pxd`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/shrubbing.pxd

:file:`shrubbing.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/shrubbing.pyx

:file:`landscaping.pyx`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/landscaping.pyx

One would then need to compile both of these modules, e.g. using

:file:`setup.py`:

.. literalinclude:: ../../examples/userguide/sharing_declarations/setup.py

Some things to note about this example:

* There is a :keyword:`cdef` class Shrubbery declaration in both
  :file:`Shrubbing.pxd` and :file:`Shrubbing.pyx`. When the Shrubbing module
  is compiled, these two declarations are combined into one.
* In Landscaping.pyx, the :keyword:`cimport` Shrubbing declaration allows us
  to refer to the Shrubbery type as :class:`Shrubbing.Shrubbery`. But it
  doesn't bind the name Shrubbing in Landscaping's module namespace at run
  time, so to access :func:`Shrubbing.standard_shrubbery` we also need to
  ``import Shrubbing``.
* One caveat if you use setuptools instead of distutils, the default
  action when running ``python setup.py install`` is to create a zipped
  ``egg`` file which will not work with ``cimport`` for ``pxd`` files
  when you try to use them from a dependent package.
  To prevent this, include ``zip_safe=False`` in the arguments to ``setup()``.
