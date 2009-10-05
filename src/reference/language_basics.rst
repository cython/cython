.. highlight:: cython



.. _language_basics:

***************
Language Basics
***************

=================
Cython File Types
=================

There are three file types in cython:

* Definition files carry a ``.pxd`` suffix
* Implementation files carry a ``.pyx`` suffix
* Include files which carry a ``.pxi`` suffix


Definition File
===============

What can it contain?
--------------------

* Any kind of C type declaration.
* ``extern`` C function or variable decarations.
* Declarations for module implementations.
* The definition parts of **extension types**.
* All declarations of functions, etc., for an **external library**

What can't it contain?
----------------------

* Any non-extern C variable declaration.
* Implementations of C or Python functions.
* Python class definitions
* Python executable statements.
* Any declaration that is defined as **public** to make it accessible to other Cython modules.

 * This is not necessary, as it is automatic.
 * a **public** declaration is only needed to make it accessible to **external C code**.

What else?
----------

cimport
```````

* Use the **cimport** statement, as you would Python's import statement, to access these files
  from other definition or implementation files.
* **cimport** does not need to be called in ``.pyx`` file for for ``.pxd`` file that has the
  same name. This is automatic.
* For cimport to find the stated definition file, the path to the file must be appended to the
  ``-I`` option of the **cython compile command**.

compilation order
`````````````````

* When a ``.pyx`` file is to be compiled, cython first checks to see if a corresponding ``.pxd`` file
  exits and processes it first.



Implementation File
===================

What can it contain?
--------------------

* Basically anything Cythonic, but see below.

What can't it contain?
----------------------

* There are some restrictions when it comes to **extension types**, if the extension type is
  already defined else where... **more on this later**


Include File
============

What can it contain?
--------------------

* Any Cythonic code really, because the entire file is textually embedded at the location
  you prescribe.

How do I use it?
----------------

* Include the ``.pxi`` file with an ``include`` statement like: ``include "spamstuff.pxi``
* The ``include`` statement can appear anywhere in your cython file and at any indentation level
* The code in the ``.pxi`` file needs to be rooted at the "zero" indentation level.
* The included code can itself contain other ``include`` statements.


====================
Declaring Data Types
====================

.. note::
    .. todo::
        I think having paragraphs like this should be somewhere else which we can link to from here

As a dynamic language, Python encourages a programming style of considering classes and objects in terms of their methods and attributes, more than where they fit into the class hierarchy.

This can make Python a very relaxed and comfortable language for rapid development, but with a price - the ‘red tape’ of managing data types is dumped onto the interpreter. At run time, the interpreter does a lot of work searching namespaces, fetching attributes and parsing argument and keyword tuples. This run-time ‘late binding’ is a major cause of Python’s relative slowness compared to ‘early binding’ languages such as C++.

However with Cython it is possible to gain significant speed-ups through the use of ‘early binding’ programming techniques.

The cdef Statement
==================

The ``cdef`` statement is used to make C level declarations for:

:Variables:

::

    cdef int i, j, k
    cdef float f, g[42], *h

:Structs:

::

    cdef struct Grail:
        int age
        float volume

:Unions:

::

    cdef union Food:
        char *spam
        float *eggs


:Enums:

::

    cdef enum CheeseType:
        cheddar, edam,
        camembert

    cdef enum CheeseState:
        hard = 1
        soft = 2
        runny = 3

:Funtions:

::

    cdef int eggs(unsigned long l, float f):
        ...

:Extenstion Types:

::

    cdef class Spam:
        ...


.. note::
    Constants can be defined by using an anonymous enum::

        cdef enum:
            tons_of_spam = 3


Grouping cdef Declarations
==========================

A series of declarations can grouped into a ``cdef`` block::

        cdef:
            struct Spam:
                int tons

            int i
            float f
            Spam *p

            void f(Spam *s):
            print s.tons, "Tons of spam"

Parameters
==========

* Both C and Python **function** types can be declared to have parameters C data types.
* Use normal C declaration syntax::

    def spam(int i, char *s):
        ...

        cdef int eggs(unsigned long l, float f):
            ...

* As these parameters are passed into a Python declared function, they are magically **converted** to the specified C type value.

 * This holds true for only numeric and string types

* If no type is specified for a parameter or a return value, it is assumed to be a Python object

 * The following takes two Python objects as parameters and returns a Python object::

        cdef spamobjs(x, y):
            ...

  .. note::
      This is different then C language behavior, where  it is an int by default.



* Python object types have reference counting performed according to the standard Python C-API rules:

 * Borrowed references are taken as parameters
 * New references are returned

.. todo::
    link or label here the one ref count caveat for numpy.

* The name ``object`` can be used to explicitly declare something as a Python Object.

 * For sake of code clarity, it recomened to always use ``object`` explicitly in your code.

 * This is also useful for cases where the name being declared would otherwise be taken for a type::

     cdef foo(object int):
         ...

 * As a return type::

     cdef object foo(object int):
         ...

.. todo::
    Do a see also here ..??

Optional Arguments
------------------

* Are supported for ``cdef`` and ``cpdef`` functions
* There differences though whether you declare them in a ``.pyx`` file or a ``.pxd`` file

 * When in a ``.pyx`` file, the signature is the same as it is in Python itself::

    cdef class A:
        cdef foo(self):
            print "A"
    cdef class B(A)
        cdef foo(self, x=None)
            print "B", x
    cdef class C(B):
        cpdef foo(self, x=True, int k=3)
            print "C", x, k


 * When in a ``.pxd`` file, the signature is different like this example: ``cdef foo(x=*)``::

    cdef class A:
        cdef foo(self)
    cdef class B(A)
        cdef foo(self, x=*)
    cdef class C(B):
        cpdef foo(self, x=*, int k=*)


  * The number of arguments may increase when subclassing, buty the arg types and order must be the same.

* There may be a slight performance penalty when the optional arg is overridden with one that does not have default values.

Keyword-only Arguments
=======================

* ``def`` functions can have keyword-only argurments listed after a ``"*"`` parameter and before a ``"**"`` parameter if any::

    def f(a, b, *args, c, d = 42, e, **kwds):
        ...

 * Shown above, the ``c``, ``d`` and ``e`` arguments can not be passed as positional arguments and must be passed as keyword arguments.
 * Furthermore, ``c`` and ``e`` are required keyword arguments since they do not have a default value.

* If the parameter name after the ``"*"`` is omitted, the function will not accept any extra positional argumrents::

    def g(a, b, *, c, d):
        ...

 * Shown above, the signature takes exactly two positional parameters and has two required keyword parameters



Automatic Type Conversion
=========================

* For basic numeric and string types, in most situations, when a Python object is used in the context of a C value and vice versa.

* The following table summarises the conversion possibilities:

    +----------------------------+--------------------+------------------+
    | C types                    | From Python types  | To Python types  |
    +============================+====================+==================+
    | [unsigned] char            | int, long          | int              |
    +----------------------------+                    |                  |
    | [unsigned] short           |                    |                  |
    +----------------------------+                    |                  |
    | int, long                  |                    |                  |
    +----------------------------+--------------------+------------------+
    | unsigned int               | int, long          | long             |
    +----------------------------+                    |                  |
    | unsigned long              |                    |                  |
    +----------------------------+                    |                  |
    | [unsigned] long long       |                    |                  |
    +----------------------------+--------------------+------------------+
    | float, double, long double | int, long, float   | float            |
    +----------------------------+--------------------+------------------+
    | char *                     | str/bytes          | str/bytes [#]_   |
    +----------------------------+--------------------+------------------+
    | struct                     |                    | dict             |
    +----------------------------+--------------------+------------------+

.. note::
    **Python String in a C Context**

    * A Python string, passed to C context expecting a ``char*``, is only valid as long as the Python string exists.
    * A reference to the Python string must be kept around for as long as the C string is needed.
    * If this can't be guarenteed, then make a copy of the C string.
    * Cython may produce an error message: ``Obtaining char* from a temporary Python value`` and will not resume compiling in situations like this::

        cdef char *s
        s = pystring1 + pystring2

    * The reason is that concatenating to strings in Python produces a temporary variable.

     * The variable is decrefed, and the Python string deallocated as soon as the statement has finished,

     * Therefore the lvalue **``s``** is left dangling.

    * The solution is to assign the result of the concatenation to a Python variable, and then obtain the ``char*`` from that::

        cdef char *s
        p = pystring1 + pystring2
        s = p

    .. note::
        **It is up to you to be aware of this, and not to depend on Cython's error message, as it is not guarenteed to be generated for every situation.**


Type Casting
=============

* The syntax used in type casting are ``"<"`` and ``">"``

 .. note::
    The syntax is different from C convention

 ::

        cdef char *p, float *q
        p = <char*>q

* If one of the types is a python object for ``<type>x``, Cython will try and do a coersion.

 .. note:: Cython will not stop a casting where there is no conversion, but it will emit a warning.

* If the address is what is wanted, cast to a ``void*`` first.


Type Checking
-------------

* A cast like ``<MyExtensionType>x`` will cast x to type ``MyExtensionType`` without type checking at all.

* To have a cast type checked, use the syntax like: ``<MyExtenstionType?>x``.

 * In this case, Cython will throw an error if ``"x"`` is not a (subclass) of ``MyExtenstionClass``

* Automatic type checking for extension types can be obtained by whenever ``isinstance()`` is used as the second parameter


Python Objects
==============

==========================
Statements and Expressions
==========================

* For the most part, control structures and expressions follow Python syntax.
* When applied to Python objects, the semantics are the same unless otherwise noted.
* Most Python operators can be applied to C values with the obvious semantics.
* An expression with mixed Python and C values will have **conversions** performed automatically.
* Python operations are automatically checked for errors, with the appropriate action taken.

Differences Between Cython and C
================================

* Most notable are C constructs which have no direct equivalent in Python.

 * An integer literal is treated as a C constant

  * It will be truncated to whatever size your C compiler thinks appropriate.
  * Cast to a Python object like this::

      <object>10000000000000000000

  * The ``"L"``, ``"LL"`` and the ``"U"`` suffixes have the same meaning as in C

* There is no ``->`` operator in Cython.. instead of ``p->x``, use ``p.x``.
* There is no ``*`` operator in Cython.. instead of ``*p``, use ``p[0]``.
* ``&`` is permissible and has the same semantics as in C.
* ``NULL`` is the null C pointer.

 * Do NOT use 0.
 * ``NULL`` is a reserved word in Cython

* Syntax for **Type casts** are ``<type>value``.

Scope Rules
===========

* All determination of scoping (local, module, built-in) in Cython is determined statically.
* As with Python, a variable assignment which is not declared explicitly is implicitly declared to be a Python variable residing in the scope where it was assigned.

.. note::
    * Module-level scope behaves the same way as a Python local scope if you refer to the variable before assigning to it.

     * Tricks, like the following will NOT work in Cython::

            try:
                x = True
            except NameError:
                True = 1

     * The above example will not work because ``True`` will always be looked up in the module-level scope. Do the following instead::

            import __builtin__
            try:
                True = __builtin__.True
            except AttributeError:
                True = 1


=====================
Functions and Methods
=====================

Callable from Python
=====================

Callable from C
================

Callable from both Python and C
================================

Overriding
==========

``cpdef`` functions can override ``cdef`` functions::

    cdef class A:
        cdef foo(self):
            print "A"
    cdef class B(A)
        cdef foo(self, x=None)
            print "B", x
    cdef class C(B):
        cpdef foo(self, x=True, int k=3)
            print "C", x, k


Function Pointers
=================

* Functions declared in a ``struct`` are automatically converted to function pointers.
* see **using exceptions with function pointers**


============================
Error and Exception Handling
============================

* A plain ``cdef`` declared function, that does not return a Python object...

 * Has no way of reporting a Python exception to it's caller.
 * Will only print a warning message and the exception is ignored.

* Inorder to propagate exceptions like this to it's caller, you need to declare an exception value for it.
* There are three forms of declaring an exception for a C compiled program.

 * First::

    cdef int spam() except -1:
        ...

  * In the example above, if an error occurs inside spam, it will immediately return with the value of ``-1``, causing an exception to be propagated to it's caller.
  * Functions declared with an exception value, should explicitly prevent a return of that value.

 * Second::

    cdef int spam() except? -1:
        ...

  * Used when a ``-1`` may possibly be returned and is not to be considered an error.
  * The ``"?"`` tells Cython that ``-1`` only indicates a *possible* error.
  * Now, each time ``-1`` is returned, Cython generates a call to ``PyErr_Occurrd`` to verify it is an actual error.

 * Third::

     cdef int spam() except +

  * A call to ``PyErr_Occurred`` happens *every* time the function gets called.

    .. note:: Returning ``void``

        A need to propagate errors when returning ``void`` must use this version.

* Exception values can only be declared for functions returning an..

 * integer
 * enum
 * float
 * pointer type
 * Must be a constant expression

.. note::

    .. note:: Function pointers

        * Require the same exception value specification as it's user has declared.
        * Use cases here are when used as parameters and when assigned to a variable
        * Example::

            int (*grail)(int, char *) except -1

    .. note:: Python Objects

        * Declared exception values are **not** need.
        * Remember that Cython assumes that a function function without a declared return value, returns a Python object.
        * Exceptions on such functions are implicitly propagated by returning ``NULL``

    .. note:: C++

        For exceptions from C++ compiled programs, see **Wrapping C++ Classes**

Checking return values for non-Cython functions..
=================================================

* Do not try to raise exceptions by returning the specified value.. Example::

    cdef extern FILE *fopen(char *filename, char *mode) except NULL # WRONG!

 * The except clause does not work that way.
 * It's only purpose is to propagate Python exceptions that have already been raised, either by...

  * A Cython function
  * A C function that calls Python/C API routines.

* To propagate an exception for these circumstances you need to raise it yourself::

     cdef FILE *p
     p = fopen("spam.txt", "r")
     if p == NULL:
         raise SpamError("Couldn't open the spam file")



=======================
Conditional Compilation
=======================


Compile-Time Definitions
=========================


Conditional Statements
=======================





.. [#] The conversion is to/from str for Python 2.x, and bytes for Python 3.x.













