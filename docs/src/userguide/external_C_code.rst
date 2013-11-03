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

.. _embedding Python: http://www.freenet.org.nz/python/embeddingpyrex/

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
   :keyword:`enum` if they contain normal :c:type:`int` values.  Note that
   Cython considers :keyword:`enum` to be equivalent to :c:type:`int`, so do
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

* If you want to include some external declarations, but don't want to specify
  a header file (because it's included by some other header that you've
  already included) you can put ``*`` in place of the header file name::

    cdef extern from *:
        ...

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
| .. sourcecode:: c       | ::                                          | Cython will refer to the as ``struct Foo`` in the generated C code.   |
|                         |                                             |                                                                       |
|   struct Foo {          |   cdef struct Foo:                          |                                                                       |
|     ...                 |     ...                                     |                                                                       |
|   };                    |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| .. sourcecode:: c       | ::                                          | Cython will refer to the type simply as ``Foo`` in                    |
|                         |                                             | the generated C code.                                                 |
|   typedef struct {      |   ctypedef struct Foo:                      |                                                                       |
|     ...                 |     ...                                     |                                                                       |
|   } Foo;                |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+
| .. sourcecode:: c       | ::                                          | If the C header uses both a tag and a typedef with *different*        |
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
| .. sourcecode:: c       | ::                                          | If the header uses the *same* name for the tag and typedef, you       |
|                         |                                             | won't be able to include a :keyword:`ctypedef` for it -- but then,    |
|   typedef struct Foo {  |   cdef struct Foo:                          | it's not necessary.                                                   |
|     ...                 |     ...                                     |                                                                       |
|   } Foo;                |                                             |                                                                       |
+-------------------------+---------------------------------------------+-----------------------------------------------------------------------+

Note that in all the cases below, you refer to the type in Cython code simply
as :c:type:`Foo`, not ``struct Foo``.

Accessing Python/C API routines
---------------------------------

One particular use of the ``cdef extern from`` statement is for gaining access to
routines in the Python/C API. For example,::

    cdef extern from "Python.h":

        object PyString_FromStringAndSize(char *s, Py_ssize_t len)

will allow you to create Python strings containing null bytes.

Special Types
--------------

Cython predefines the name ``Py_ssize_t`` for use with Python/C API routines. To
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

Resolving naming conflicts - C name specifications
----------------------------------------------------

Each Cython module has a single module-level namespace for both Python and C
names. This can be inconvenient if you want to wrap some external C functions
and provide the Python user with Python functions of the same names.

Cython provides a couple of different ways of solving this problem. The
best way, especially if you have many C functions to wrap, is probably to put
the extern C function declarations into a different namespace using the
facilities described in the section on sharing declarations between Cython
modules.

The other way is to use a C name specification to give different Cython and C
names to the C function. Suppose, for example, that you want to wrap an
external function called :func:`eject_tomato`. If you declare it as::

    cdef extern void c_eject_tomato "eject_tomato" (float speed)

then its name inside the Cython module will be ``c_eject_tomato``, whereas its name
in C will be ``eject_tomato``. You can then wrap it with::

    def eject_tomato(speed):
        c_eject_tomato(speed)

so that users of your module can refer to it as ``eject_tomato``.

Another use for this feature is referring to external names that happen to be
Cython keywords. For example, if you want to call an external function called
print, you can rename it to something else in your Cython module.

As well as functions, C names can be specified for variables, structs, unions,
enums, struct and union members, and enum values. For example,::

    cdef extern int one "ein", two "zwei"
    cdef extern float three "drei"

    cdef struct spam "SPAM":
      int i "eye"

    cdef enum surprise "inquisition":
      first "alpha"
      second "beta" = 3

Using Cython Declarations from C
==================================

Cython provides two methods for making C declarations from a Cython module
available for use by external C code---public declarations and C API
declarations.

.. note::

    You do not need to use either of these to make declarations from one
    Cython module available to another Cython module – you should use the
    :keyword:`cimport` statement for that. Sharing Declarations Between Cython Modules.

Public Declarations
---------------------

You can make C types, variables and functions defined in a Cython module
accessible to C code that is linked with the module, by declaring them with
the public keyword::

    cdef public struct Bunny: # public type declaration
        int vorpalness

    cdef public int spam # public variable declaration

    cdef public void grail(Bunny *): # public function declaration
        print "Ready the holy hand grenade"

If there are any public declarations in a Cython module, a header file called
:file:`modulename.h` file is generated containing equivalent C declarations for
inclusion in other C code.

Users who are embedding Python in C with Cython need to make sure to call Py_Initialize()
and Py_Finalize(). For example, in the following snippet that includes :file:`modulename.h`::

    #include <Python.h>
    #include "modulename.h"

    void grail() {
        Py_Initialize();
        initmodulename();
        Bunny b;
        grail(b);
        Py_Finalize();
    }

Any C code wanting to make use of these declarations will need to be linked,
either statically or dynamically, with the extension module.

If the Cython module resides within a package, then the name of the ``.h``
file consists of the full dotted name of the module, e.g. a module called
:mod:`foo.spam` would have a header file called :file:`foo.spam.h`.

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

Any public C type or extension type declarations in the Cython module are also
made available when you include :file:`modulename_api.h`.::

    # delorean.pyx
    cdef public struct Vehicle:
        int speed
        float power

    cdef api void activate(Vehicle *v):
        if v.speed >= 88 and v.power >= 1.21:
            print "Time travel achieved"

.. sourcecode:: c
            
    # marty.c
    #include "delorean_api.h"

    Vehicle car;

    int main(int argc, char *argv[]) {
        import_delorean();
        car.speed = atoi(argv[1]);
        car.power = atof(argv[2]); 
        activate(&car);
    }

.. note::

    Any types defined in the Cython module that are used as argument or
    return types of the exported functions will need to be declared public,
    otherwise they won't be included in the generated header file, and you will
    get errors when you try to compile a C file that uses the header.

Using the :keyword:`api` method does not require the C code using the
declarations to be linked with the extension module in any way, as the Python
import machinery is used to make the connection dynamically. However, only
functions can be accessed this way, not variables.

You can use both :keyword:`public` and :keyword:`api` on the same function to
make it available by both methods, e.g.::

    cdef public api void belt_and_braces():
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
        void order_spam(int tons)
        char *get_lunch(float tomato_size)

This can be a useful thing to do in a ``.pxd`` file (see
:ref:`sharing-declarations`) to make the module's public interface
available by all three methods.

Acquiring and Releasing the GIL
---------------------------------

Cython provides facilities for acquiring and releasing the
`Global Interpreter Lock (GIL) <http://docs.python.org/dev/glossary.html#term-global-interpreter-lock>`_.
This may be useful when calling into (external C) code that may block, or when wanting to use Python from a
C callback.

.. _nogil:

Releasing the GIL
^^^^^^^^^^^^^^^^^

You can release the GIL around a section of code using the
``with nogil`` statement::

    with nogil:
        <code to be executed with the GIL released>

Code in the body of the statement must not manipulate Python objects in any
way, and must not call anything that manipulates Python objects without first
re-acquiring the GIL. Cython currently does not check this.

.. _gil:

Acquiring the GIL
^^^^^^^^^^^^^^^^^

A C function that is to be used as a callback from C code that is executed
without the GIL needs to acquire the GIL before it can manipulate Python
objects. This can be done by specifying with :keyword:`gil` in the function
header::

    cdef void my_callback(void *data) with gil:
        ...

If the callback may be called from another non-Python thread,
care must be taken to initialize the GIL first, through a call to
`PyEval_InitThreads() <http://docs.python.org/dev/c-api/init.html#PyEval_InitThreads>`_.
If you're already using  :ref:`cython.parallel <parallel>` in your module, this will already have been taken care of.

The GIL may also be acquired through the ``with gil`` statement::

    with gil:
        <execute this block with the GIL acquired>

Declaring a function as callable without the GIL
--------------------------------------------------

You can specify :keyword:`nogil` in a C function header or function type to
declare that it is safe to call without the GIL.::

    cdef void my_gil_free_func(int spam) nogil:
        ...

If you are implementing such a function in Cython, it cannot have any Python
arguments, Python local variables, or Python return type, and cannot
manipulate Python objects in any way or call any function that does so without
acquiring the GIL first. Some of these restrictions are currently checked by
Cython, but not all. It is possible that more stringent checking will be
performed in the future.

.. NOTE:: This declaration declares that it is safe to call the function without the GIL,
          it does not in itself release the GIL.

Declaring a function with :keyword:`gil` also implicitly makes its signature
:keyword:`nogil`.

