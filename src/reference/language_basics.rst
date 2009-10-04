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

.. todo::
    The previous statement is still true ..??

* If no type is specified for a parameter or a return value, it is assumed to be a Python object

 * The following takes two Python objects as parameters and returns a Python object::

        cdef spamobjs(x, y):
            ...

 * .. note::
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


.. [#] The conversion is to/from str for Python 2.x, and bytes for Python 3.x.


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




Casting
=======

Python Objects
==============

==========================
Statements and Expressions
==========================


=========
Functions
=========

Callable from Python
=====================

Callable from C
================

Callable from both Python and C
================================

============================
Error and Exception Handling
============================


=======================
Conditional Compilation
=======================


Compile-Time Definitions
=========================


Conditional Statements
=======================



















