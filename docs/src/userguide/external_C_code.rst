.. highlight:: cython

.. _external-C-code:

**********************************
Interfacing with External C Code
**********************************

One of the main uses of Cython is wrapping existing libraries of C code. This
is achieved by using external declarations to declare the C functions and
variables from the library that you want to use.

You can also use public declarations to make C functions and variables defined
in a Cython module available to external C code. The need for this is expected
to be less frequent, but you might want to do it, for example, if you are
`embedding Python`_ in another application as a scripting language. Just as a
Cython module can be used as a bridge to allow Python code to call C code, it
can also be used to allow C code to call Python code.

.. _embedding Python: https://web.archive.org/web/20120225082358/http://www.freenet.org.nz:80/python/embeddingpyrex/

External declarations
=======================

By default, C functions and variables declared at the module level are local
to the module (i.e. they have the C static storage class). They can also be
declared extern to specify that they are defined elsewhere, for example,::

    cdef extern int spam_counter

    cdef extern void order_spam(int tons)

Referencing C header files
---------------------------

When you use an extern definition on its own as in the examples above, Cython
includes a declaration for it in the generated C file. This can cause problems
if the declaration doesn't exactly match the declaration that will be seen by
other C code. If you're wrapping an existing C library, for example, it's
important that the generated C code is compiled with exactly the same
declarations as the rest of the library.

To achieve this, you can tell Cython that the declarations are to be found in a
C header file, like this::

    cdef extern from "spam.h":

        int spam_counter

        void order_spam(int tons)

The ``cdef extern`` from clause does three things:

1. It directs Cython to place a ``#include`` statement for the named header file in
   the generated C code.
2. It prevents Cython from generating any C code
   for the declarations found in the associated block.
3. It treats all declarations within the block as though they started with
   ``cdef extern``.

It's important to understand that Cython does not itself read the C header
file, so you still need to provide Cython versions of any declarations from it
that you use. However, the Cython declarations don't always have to exactly
match the C ones, and in some cases they shouldn't or can't. In particular:

#. Leave out any platform-specific extensions to C declarations such as
   ``__declspec()``.

#. If the header file declares a big struct and you only want to use a few
   members, you only need to declare the members you're interested in. Leaving
   the rest out doesn't do any harm, because the C compiler will use the full
   definition from the header file.

   In some cases, you might not need any of the struct's members, in which
   case you can just put pass in the body of the struct declaration, e.g.::

        cdef extern from "foo.h":
            struct spam:
                pass

   .. note::

       you can only do this inside a ``cdef extern from`` block; struct
       declarations anywhere else must be non-empty.

#. If the header file uses ``typedef`` names such as :c:type:`word` to refer
   to platform-dependent flavours of numeric types, you will need a
   corresponding :keyword:`ctypedef` statement, but you don't need to match
   the type exactly, just use something of the right general kind (int, float,
   etc). For example,::

       ctypedef int word

   will work okay whatever the actual size of a :c:type:`word` is (provided the header
   file defines it correctly). Conversion to and from Python types, if any, will also
   be used for this new type.

#. If the header file uses macros to define constants, translate them into a
   normal external variable declaration.  You can also declare them as an
   :keyword:`enum` if they contain normal :c:expr:`int` values.  Note that
   Cython considers :keyword:`enum` to be equivalent to :c:expr:`int`, so do
   not do this for non-int values.

#. If the header file defines a function using a macro, declare it as though
   it were an ordinary function, with appropriate argument and result types.

#. For archaic reasons C uses the keyword ``void`` to declare a function
   taking no parameters. In Cython as in Python, simply declare such functions
   as :meth:`foo()`.

A few more tricks and tips:

* If you want to include a C header because it's needed by another header, but
  don't want to use any declarations from it, put pass in the extern-from
  block::

      cdef extern from "spam.h":
          pass

* If you want to include a system header, put angle brackets inside the quotes::

      cdef extern from "<sysheader.h>":
          ...

* If you want to include some external declarations, but don't want to specify
  a header file (because it's included by some other header that you've
  already included) you can put ``*`` in place of the header file name::

    cdef extern from *:
        ...

* If a ``cdef extern from "inc.h"`` block is not empty and contains only
  function or variable declarations (and no type declarations of any kind),
  Cython will put the ``#include "inc.h"`` statement after all
  declarations generated by Cython. This means that the included file
  has access to the variables, functions, structures, ... which are
  declared by Cython.

Implementing functions in C
---------------------------

When you want to call C code from a Cython module, usually that code
will be in some external library that you link your extension against.
However, you can also directly compile C (or C++) code as part of your
Cython module. In the ``.pyx`` file, you can put something like::

    cdef extern from "spam.c":
        void order_spam(int tons)

Cython will assume that the function ``order_spam()`` is defined in the
file ``spam.c``. If you also want to cimport this function from another
module, it must be declared (not extern!) in the ``.pxd`` file::

    cdef void order_spam(int tons)

For this to work, the signature of ``order_spam()`` in ``spam.c`` must
match the signature that Cython uses, in particular the function must
be static:

.. code-block:: c

    static void order_spam(int tons)
    {
        printf("Ordered %i tons of spam!\n", tons);
    }


.. _struct-union-enum-styles:

Styles of struct, union and enum declaration
----------------------------------------------

There are two main ways that structs, unions and enums can be declared in C
header files: using a tag name, or using a typedef. There are also some
variations based on various combinations of these.

It's important to make the Cython declarations match the style used in the
header file, so that Cython can emit the right sort of references to the type
in the code it generates. To make this possible, Cython provides two different
syntaxes for declaring a struct, union or enum type. The style introduced
above corresponds to the use of a tag name. To get the other style, you prefix
the declaration with :keyword:`ctypedef`, as illustrated below.

The following table shows the various possible styles that can be found in a
header file, and the corresponding Cython declaration that you should put in
the ``cdef extern`` from block. Struct declarations are used as an example; the
same applies equally to union and enum declarations.

+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| C code                  | Possibilities for corresponding Cython Code | Comments                                                              |
+=========================+=============================================+=======================================================================+
| .. code-block:: c       | ::                                          | Cython will refer to the type as ``struct Foo`` in                    |
|                         |                                             | the generated C code.                                                 |
|   struct Foo {          |   cdef struct Foo:                          |                                                                       |
|     ...                 |     ...                                     |                                                                       |
|   };                    |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| .. code-block:: c       | ::                                          | Cython will refer to the type simply as ``Foo`` in                    |
|                         |                                             | the generated C code.                                                 |
|   typedef struct {      |   ctypedef struct Foo:                      |                                                                       |
|     ...                 |     ...                                     |                                                                       |
|   } Foo;                |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| .. code-block:: c       | ::                                          | If the C header uses both a tag and a typedef with *different*        |
|                         |                                             | names, you can use either form of declaration in Cython               |
|   typedef struct foo {  |   cdef struct foo:                          | (although if you need to forward reference the type,                  |
|     ...                 |     ...                                     | you'll have to use the first form).                                   |
|   } Foo;                |   ctypedef foo Foo #optional                |                                                                       |
|                         |                                             |                                                                       |
|                         | or::                                        |                                                                       |
|                         |                                             |                                                                       |
|                         |   ctypedef struct Foo:                      |                                                                       |
|                         |     ...                                     |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| .. code-block:: c       | ::                                          | If the header uses the *same* name for the tag and typedef, you       |
|                         |                                             | won't be able to include a :keyword:`ctypedef` for it -- but then,    |
|   typedef struct Foo {  |   cdef struct Foo:                          | it's not necessary.                                                   |
|     ...                 |     ...                                     |                                                                       |
|   } Foo;                |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+

See also use of :ref:`external_extension_types`.
Note that in all the cases below, you refer to the type in Cython code simply
as :c:type:`Foo`, not ``struct Foo``.

Pointers
--------
When interacting with a C-api there may be functions that require pointers as arguments.
Pointers are variables that contain a memory address to another variable.

For example::

    cdef extern from "<my_lib.h>":
        cdef void increase_by_one(int *my_var)

This function takes a pointer to an integer as argument.  Knowing the address of the
integer allows the function to modify the value in place, so that the caller can see
the changes afterwards.  In order to get the address from an existing variable,
use the ``&`` operator::

    cdef int some_int = 42
    cdef int *some_int_pointer = &some_int
    increase_by_one(some_int_pointer)
    # Or without creating the extra variable
    increase_by_one(&some_int)
    print(some_int)  # prints 44 (== 42+1+1)

If you want to manipulate the variable the pointer points to, you can access it by
referencing its first element like you would in python ``my_pointer[0]``. For example::

    cdef void increase_by_one(int *my_var):
        my_var[0] += 1

For a deeper introduction to pointers, you can read `this tutorial at tutorialspoint
<https://www.tutorialspoint.com/cprogramming/c_pointers.htm>`_. For differences between
Cython and C syntax for manipulating pointers, see :ref:`statements_and_expressions`.

Accessing Python/C API routines
---------------------------------

One particular use of the ``cdef extern from`` statement is for gaining access to
routines in the Python/C API. For example,::

    cdef extern from "Python.h":

        object PyString_FromStringAndSize(char *s, Py_ssize_t len)

will allow you to create Python strings containing null bytes.

Note that Cython comes with ready-to-use declarations of (almost) all C-API functions
in the cimportable ``cpython.*`` modules.  See the list in
https://github.com/cython/cython/tree/master/Cython/Includes/cpython

You should always use submodules (e.g. ``cpython.object``, ``cpython.list``) to
access these functions. Historically Cython has made some of the C-API functions
available under directly under the ``cpython`` module. However, this is
deprecated, will be removed eventually, and any new additions will not be added
there.

Special Types
--------------

Cython predefines the name :c:type:`Py_ssize_t` for use with Python/C API routines. To
make your extensions compatible with 64-bit systems, you should always use
this type where it is specified in the documentation of Python/C API routines.

Windows Calling Conventions
----------------------------

The ``__stdcall`` and ``__cdecl`` calling convention specifiers can be used in
Cython, with the same syntax as used by C compilers on Windows, for example,::

    cdef extern int __stdcall FrobnicateWindow(long handle)

    cdef void (__stdcall *callback)(void *)

If ``__stdcall`` is used, the function is only considered compatible with
other ``__stdcall`` functions of the same signature.


.. _resolve-conflicts:

Resolving naming conflicts - C name specifications
--------------------------------------------------

Each Cython module has a single module-level namespace for both Python and C
names.  This can be inconvenient if you want to wrap some external C functions
and provide the Python user with Python functions of the same names.

Cython provides a couple of different ways of solving this problem.  The best
way, especially if you have many C functions to wrap, is to put the extern
C function declarations into a ``.pxd`` file and thus a different namespace,
using the facilities described in :ref:`sharing declarations between Cython
modules <sharing-declarations>`.  Writing them into a ``.pxd`` file allows
their reuse across modules, avoids naming collisions in the normal Python way
and even makes it easy to rename them on cimport.  For example, if your
``decl.pxd`` file declared a C function ``eject_tomato``::

    cdef extern from "myheader.h":
        void eject_tomato(float speed)

then you can cimport and wrap it in a ``.pyx`` file as follows::

    from decl cimport eject_tomato as c_eject_tomato

    def eject_tomato(speed):
        c_eject_tomato(speed)

or simply cimport the ``.pxd`` file and use it as prefix::

    cimport decl

    def eject_tomato(speed):
        decl.eject_tomato(speed)

Note that this has no runtime lookup overhead, as it would in Python.
Cython resolves the names in the ``.pxd`` file at compile time.

For special cases where namespacing or renaming on import is not enough,
e.g. when a name in C conflicts with a Python keyword, you can use a C name
specification to give different Cython and C names to the C function at
declaration time.  Suppose, for example, that you want to wrap an external
C function called :func:`yield`.  If you declare it as::

    cdef extern from "myheader.h":
        void c_yield "yield" (float speed)

then its Cython visible name will be ``c_yield``, whereas its name in C
will be ``yield``.  You can then wrap it with::

    def call_yield(speed):
        c_yield(speed)

As for functions, C names can be specified for variables, structs, unions,
enums, struct and union members, and enum values.  For example::

    cdef extern int one "eins", two "zwei"
    cdef extern float three "drei"

    cdef struct spam "SPAM":
        int i "eye"

    cdef enum surprise "inquisition":
        first "alpha"
        second "beta" = 3

Note that Cython will not do any validation or name mangling on the string
you provide.  It will inject the bare text into the C code unmodified, so you
are entirely on your own with this feature.  If you want to declare a name
``xyz`` and have Cython inject the text "make the C compiler fail here" into
the C file for it, you can do this using a C name declaration.  Consider this
an advanced feature, only for the rare cases where everything else fails.


.. _verbatim_c:

Including verbatim C code
-------------------------

For advanced use cases, Cython allows you to directly write C code
as "docstring" of a ``cdef extern from`` block:

.. literalinclude:: ../../examples/userguide/external_C_code/verbatim_c_code.pyx

The above is essentially equivalent to having the C code in a file
``header.h`` and writing ::

    cdef extern from "header.h":
        long c_square(long x)
        void c_assign(long& x, long y)

This feature is commonly used for platform specific adaptations at
compile time, for example:

.. literalinclude:: ../../examples/userguide/external_C_code/platform_adaptation.pyx

It is also possible to combine a header file and verbatim C code::

    cdef extern from "badheader.h":
        """
        /* This macro breaks stuff */
        #undef int
        """
        # Stuff from badheader.h

In this case, the C code ``#undef int`` is put right after
``#include "badheader.h"`` in the C code generated by Cython.

Verbatim C code can also be used for version specific adaptations, e.g. when
a struct field was added to a library but is not available in older versions:

.. literalinclude:: ../../examples/userguide/external_C_code/struct_field_adaptation.pyx

Note that the string is parsed like any other docstring in Python.
If you require character escapes to be passed into the C code file,
use a raw docstring, i.e. ``r""" ... """``.


Using Cython Declarations from C
================================

Cython provides two methods for making C declarations from a Cython module
available for use by external C code---public declarations and C API
declarations.

.. note::

    You do not need to use either of these to make declarations from one
    Cython module available to another Cython module – you should use the
    :keyword:`cimport` statement for that. Sharing Declarations Between Cython Modules.

.. _inittab_guide:

Public Declarations
---------------------

You can make C types, variables and functions defined in a Cython module
accessible to C code that is linked together with the Cython-generated C file,
by declaring them with the public keyword::

    cdef public struct Bunny:  # a public type declaration
        int vorpalness

    cdef public int spam  # a public variable declaration

    cdef public void grail(Bunny *)  # a public function declaration

If there are any public declarations in a Cython module, a header file called
:file:`modulename.h` file is generated containing equivalent C declarations for
inclusion in other C code.

A typical use case for this is building an extension module from multiple
C sources, one of them being Cython generated (i.e. with something like
``Extension("grail", sources=["grail.pyx", "grail_helper.c"])`` in ``setup.py``.
In this case, the file ``grail_helper.c`` just needs to add
``#include "grail.h"`` in order to access the public Cython variables.

A more advanced use case is embedding Python in C using Cython.
In this case, make sure to call :c:func:`Py_Initialize()` and :c:func:`Py_Finalize()`.
For example, in the following snippet that includes :file:`grail.h`:

.. code-block:: c

    #include <Python.h>
    #include "grail.h"

    int main() {
        Py_Initialize();
        initgrail();  /* Python 2.x only ! */
        Bunny b;
        grail(b);
        Py_Finalize();
    }

This C code can then be built together with the Cython-generated C code
in a single program (or library). Be aware that this program will not include
any external dependencies that your module uses. Therefore typically this will
not generate a truly portable application for most cases.

In Python 3.x, calling the module init function directly should be avoided.  Instead,
use the `inittab mechanism <https://docs.python.org/3/c-api/import.html#c._inittab>`_
to link Cython modules into a single shared library or program.

.. code-block:: c

    err = PyImport_AppendInittab("grail", PyInit_grail);
    Py_Initialize();
    grail_module = PyImport_ImportModule("grail");

If the Cython module resides within a package, then the name of the ``.h``
file consists of the full dotted name of the module, e.g. a module called
:mod:`foo.spam` would have a header file called :file:`foo.spam.h`.

.. NOTE::

    On some operating systems like Linux, it is also possible to first
    build the Cython extension in the usual way and then link against
    the resulting ``.so`` file like a dynamic library.
    Beware that this is not portable, so it should be avoided.

.. _CYTHON_EXTERN_C:

C++ public declarations
^^^^^^^^^^^^^^^^^^^^^^^

When a file is compiled as C++, its public functions are declared as C++ API (using ``extern "C++"``) by default.
This disallows to call the functions from C code.  If the functions are really meant as a plain C API,
the ``extern`` declaration needs to be manually specified by the user.
This can be done by setting the ``CYTHON_EXTERN_C`` C macro to ``extern "C"`` during the compilation of the generated C++ file::

    from setuptools import Extension, setup
    from Cython.Build import cythonize

    extensions = [
        Extension(
            "module", ["module.pyx"],
            define_macros=[("CYTHON_EXTERN_C", 'extern "C"')],
            language="c++",
        )
    ]

    setup(
        name="My hello app",
        ext_modules=cythonize(extensions),
    )

.. _api:

C API Declarations
-------------------

The other way of making declarations available to C code is to declare them
with the :keyword:`api` keyword. You can use this keyword with C functions and
extension types. A header file called :file:`modulename_api.h` is produced
containing declarations of the functions and extension types, and a function
called :func:`import_modulename`.

C code wanting to use these functions or extension types needs to include the
header and call the :func:`import_modulename` function. The other functions
can then be called and the extension types used as usual.

If the C code wanting to use these functions is part of more than one shared
library or executable, then :func:`import_modulename` function needs to be
called in each of the shared libraries which use these functions. If you
crash with a segmentation fault (SIGSEGV on linux) when calling into one of
these api calls, this is likely an indication that the shared library which
contains the api call which is generating the segmentation fault does not call
the :func:`import_modulename` function before the api call which crashes.

Any public C type or extension type declarations in the Cython module are also
made available when you include :file:`modulename_api.h`.:

.. literalinclude:: ../../examples/userguide/external_C_code/delorean.pyx

.. literalinclude:: ../../examples/userguide/external_C_code/marty.c
    :language: C

.. note::

    Any types defined in the Cython module that are used as argument or
    return types of the exported functions will need to be declared public,
    otherwise they won't be included in the generated header file, and you will
    get errors when you try to compile a C file that uses the header.

Using the :keyword:`api` method does not require the C code using the
declarations to be linked with the extension module in any way, as the Python
import machinery is used to make the connection dynamically. However, only
functions can be accessed this way, not variables. Note also that for the
module import mechanism to be set up correctly, the user must call
:c:func:`Py_Initialize()` and :c:func:`Py_Finalize()`; if you experience a segmentation fault in
the call to :func:`import_modulename`, it is likely that this wasn't done.

You can use both :keyword:`public` and :keyword:`api` on the same function to
make it available by both methods, e.g.::

    cdef public api void belt_and_braces() except *:
        ...

However, note that you should include either :file:`modulename.h` or
:file:`modulename_api.h` in a given C file, not both, otherwise you may get
conflicting dual definitions.

If the Cython module resides within a package, then:

* The name of the header file contains of the full dotted name of the module.
* The name of the importing function contains the full name with dots replaced
  by double underscores.

E.g. a module called :mod:`foo.spam` would have an API header file called
:file:`foo.spam_api.h` and an importing function called
:func:`import_foo__spam`.

Multiple public and API declarations
--------------------------------------

You can declare a whole group of items as :keyword:`public` and/or
:keyword:`api` all at once by enclosing them in a :keyword:`cdef` block, for
example,::

    cdef public api:
        void order_spam(int tons) except *
        char *get_lunch(float tomato_size) except NULL

This can be a useful thing to do in a ``.pxd`` file (see
:ref:`sharing-declarations`) to make the module's public interface
available by all three methods.

Acquiring and Releasing the GIL
---------------------------------

Cython provides facilities for acquiring and releasing the
Global Interpreter Lock (GIL) (see :term:`our glossary<Global Interpreter Lock or GIL>` or `external documentation <https://docs.python.org/dev/glossary.html#term-global-interpreter-lock>`_).
This may be useful when calling from multi-threaded code into
(external C) code that may block, or when wanting to use Python
from a (native) C thread callback.  Releasing the GIL should
obviously only be done for thread-safe code or for code that
uses other means of protection against race conditions and
concurrency issues.

Note that acquiring the GIL is a blocking thread-synchronising
operation, and therefore potentially costly.  It might not be
worth releasing the GIL for minor calculations.  Usually, I/O
operations and substantial computations in parallel code will
benefit from it.

.. _nogil:

Releasing the GIL
^^^^^^^^^^^^^^^^^

You can release the GIL around a section of code using the
``with nogil`` statement::

    with nogil:
        <code to be executed with the GIL released>

Code in the body of the with-statement must not manipulate Python objects
in any way, and must not call anything that manipulates Python objects without
first re-acquiring the GIL.  Cython validates these operations at compile time,
but cannot look into external C functions, for example.  They must be correctly
declared as requiring or not requiring the GIL (see below) in order to make
Cython's checks effective.

Since Cython 3.0, some simple Python statements can be used inside of ``nogil``
sections: ``raise``, ``assert`` and ``print`` (the Py2 statement, not the function).
Since they tend to be lone Python statements, Cython will automatically acquire
and release the GIL around them for convenience.

.. _gil:

Acquiring the GIL
^^^^^^^^^^^^^^^^^

A C function that is to be used as a callback from C code that is executed
without the GIL needs to acquire the GIL before it can manipulate Python
objects. This can be done by specifying ``with gil`` in the function
header::

    cdef void my_callback(void *data) with gil:
        ...

If the callback may be called from another non-Python thread,
care must be taken to initialize the GIL first, through a call to
`PyEval_InitThreads() <https://docs.python.org/dev/c-api/init.html#c.PyEval_InitThreads>`_.
If you're already using  :ref:`cython.parallel <parallel>` in your module, this will already have been taken care of.

The GIL may also be acquired through the ``with gil`` statement::

    with gil:
        <execute this block with the GIL acquired>

.. _gil_conditional:

Conditional Acquiring / Releasing the GIL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Sometimes it is helpful to use a condition to decide whether to run a
certain piece of code with or without the GIL. This code would run anyway,
the difference is whether the GIL will be held or released.
The condition must be constant (at compile time).

This could be useful for profiling, debugging, performance testing, and
for fused types (see :ref:`fused_gil_conditional`).::

    DEF FREE_GIL = True

    with nogil(FREE_GIL):
        <code to be executed with the GIL released>

        with gil(False):
           <GIL is still released>

Declaring a function as callable without the GIL
--------------------------------------------------

You can specify :keyword:`nogil` in a C function header or function type to
declare that it is safe to call without the GIL.::

    cdef void my_gil_free_func(int spam) nogil:
        ...

When you implement such a function in Cython, it cannot have any Python
arguments or Python object return type.  Furthermore, any operation
that involves Python objects (including calling Python functions) must
explicitly acquire the GIL first, e.g. by using a ``with gil`` block
or by calling a function that has been defined ``with gil``.  These
restrictions are checked by Cython and you will get a compile error
if it finds any Python interaction inside of a ``nogil`` code section.

.. NOTE:: The ``nogil`` function annotation declares that it is safe
          to call the function without the GIL.  It is perfectly allowed
          to execute it while holding the GIL.  The function does not in
          itself release the GIL if it is held by the caller.

Declaring a function ``with gil`` (i.e. as acquiring the GIL on entry) also
implicitly makes its signature :keyword:`nogil`.
