.. highlight:: cython



.. _language_basics:

****************
Languange Basics
****************

.. contents::
    :depth: 2
    :local:

=================
Cython File Types
=================

There are three file types in cython:

* Definition files carry a `.pxd` suffix
* Implementation files carry a `.pyx` suffix
* Include files which carry a `.pxi` suffix

.. contents::
    :local:

Definition File
===============

What can it contain?
--------------------

* Any kind of C type declaration.
* `extern` C function or variable decarations.
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
* **cimport** does not need to be called in `.pyx` file for for `.pxd` file that has the
  same name. This is automatic.
* For cimport to find the stated definition file, the path to the file must be appended to the
  `-I` option of the **cython compile command**.

compilation order
`````````````````

* When a `.pyx` file is to be compiled, cython first checks to see if a corresponding `.pxd` file
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
  you prescribe. Think.. "C pre-processor".

How do I use it?
----------------

* Include the `.pxi` file with an `include` statement like: `include "spamstuff.pxi`
* The `include` statement can appear anywhere in your cython file and at any indentation level
* The code in the `.pxi` file needs to be rooted at the "zero" indentation level.
* The included code can itself contain other `include` statements.


===========
Data Typing
===========

.. contents::
    :local:

Grouping
========

Parameters
==========

Conversion
==========

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

.. contents::
    :local:

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



















