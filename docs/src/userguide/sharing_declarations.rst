.. highlight:: cython

.. _sharing-declarations:

********************************************
Sharing Declarations Between Cython Modules
********************************************

.. include::
    ../two-syntax-variants-used

This section describes how to make C declarations, functions and extension
types in one Cython module available for use in another Cython module.
These facilities are closely modeled on the Python import mechanism,
and can be thought of as a compile-time version of it.


Definition and Implementation files
====================================

A Cython module can be split into two parts: a definition file with a ``.pxd``
suffix, containing C declarations that are to be available to other Cython
modules, and an implementation file with a ``.pyx``/``.py`` suffix, containing
everything else. When a module wants to use something declared in another
module's definition file, it imports it using the :keyword:`cimport`
statement or using special :py:mod:`cython.cimports` package.

A ``.pxd`` file that consists solely of extern declarations does not need
to correspond to an actual ``.pyx``/``.py`` file or Python module. This can make it a
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
wants to  access :keyword:`cdef`/``@cfunc`` attributes and methods, or to inherit from
:keyword:`cdef`/``@cclass`` classes defined in this module.

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
statement. When pure python syntax is used, the same effect can be done by
importing from special :py:mod:`cython.cimports` package. In later text the term
to ``cimport`` refers to using both :keyword:`cimport` statement or
:py:mod:`cython.cimports` package.

.. tabs::

    .. group-tab:: Pure Python

        .. code-block:: python

            from cython.cimports.module import name [as name][, name [as name] ...]

    .. group-tab:: Cython

        .. code-block:: cython

            cimport module [, module...]

            from module cimport name [as name] [, name [as name] ...]

Here is an example. :file:`dishes.pxd` is a definition file which exports a
C data type. :file:`restaurant.pyx`/:file:`restaurant.py` is an implementation file
which imports and uses it.

.. literalinclude:: ../../examples/userguide/sharing_declarations/dishes.pxd
    :caption: dishes.pxd

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/sharing_declarations/restaurant.py
            :caption: dishes.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/sharing_declarations/restaurant.pyx
            :caption: dishes.pyx

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

Also, whenever you compile a file :file:`modulename.pyx`/:file:`modulename.py`,
the corresponding definition file :file:`modulename.pxd` is first searched for along the
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

.. literalinclude:: ../../examples/userguide/sharing_declarations/c_lunch.pxd
    :caption: c_lunch.pxd

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/sharing_declarations/lunch.py
            :caption: lunch.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/sharing_declarations/lunch.pyx
            :caption: lunch.pyx

You don't need any :file:`c_lunch.pyx`/:file:`c_lunch.py` file, because the only
things defined in :file:`c_lunch.pxd` are extern C entities. There won't be any actual
``c_lunch`` module at run time, but that doesn't matter; the
:file:`c_lunch.pxd` file has done its job of providing an additional namespace
at compile time.


Sharing C Functions
===================

C functions defined at the top level of a module can be made available via
:keyword:`cimport` by putting headers for them in the ``.pxd`` file, for
example:

.. literalinclude:: ../../examples/userguide/sharing_declarations/volume.pxd
    :caption: volume.pxd

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/sharing_declarations/volume.py
            :caption: volume.py

        .. literalinclude:: ../../examples/userguide/sharing_declarations/spammery.py
            :caption: spammery.py

        .. note::

            Type definitions of function ``cube()`` in :file:`volume.py` are not provided
            since they are used from .pxd definition file. See :ref:`augmenting_pxd` and
            GitHub issue :issue:`4388`.

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/sharing_declarations/volume.pyx
            :caption: volume.pyx

        .. literalinclude:: ../../examples/userguide/sharing_declarations/spammery.pyx
            :caption: spammery.pyx

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

.. literalinclude:: ../../examples/userguide/sharing_declarations/shrubbing.pxd
    :caption: shrubbing.pxd

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/sharing_declarations/shrubbing.py
            :caption: shrubbing.py

        .. literalinclude:: ../../examples/userguide/sharing_declarations/landscaping.py
            :caption: landscaping.py

        One would then need to compile both of these modules, e.g. using

        .. literalinclude:: ../../examples/userguide/sharing_declarations/setup_py.py
            :caption: setup.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/sharing_declarations/shrubbing.pyx
            :caption: shrubbing.pyx

        .. literalinclude:: ../../examples/userguide/sharing_declarations/landscaping.pyx
            :caption: landscaping.pyx

        One would then need to compile both of these modules, e.g. using

        .. literalinclude:: ../../examples/userguide/sharing_declarations/setup_pyx.py
            :caption: setup.py

Some things to note about this example:

* There is a :keyword:`cdef`/``@cclass`` class Shrubbery declaration in both
  :file:`shrubbing.pxd` and :file:`shrubbing.pyx`. When the shrubbing module
  is compiled, these two declarations are combined into one.
* In :file:`landscaping.pyx`/:file:`landscaping.py`, the :keyword:`cimport` shrubbing
  declaration allows us to refer to the Shrubbery type as :class:`shrubbing.Shrubbery`.
  But it doesn't bind the name shrubbing in landscaping's module namespace at run
  time, so to access :func:`shrubbing.standard_shrubbery` we also need to
  ``import shrubbing``.


.. _versioning:

Versioning
==========
  
``.pxd`` files can be labelled with a minimum Cython version as part of
their file name, similar to the version tagging of ``.so`` files in PEP 3149.
For example a file called :file:`shrubbing.cython-30.pxd` will only be
found by ``cimport shrubbing`` on Cython 3.0 and higher. Cython will use the
file tagged with the highest compatible version number.
 
Note that versioned files that are distributed across different directories
will not be found. Only the first directory in the Python module search
path in which a matching ``.pxd`` file is found will be considered.
 
The purpose of this feature is to allow third-party packages to release
Cython interfaces to their packages that take advantage of the latest Cython
features while not breaking compatibility for users with older versions of Cython.
Users intending to use ``.pxd`` files solely within their own project
need not produce these tagged files.
