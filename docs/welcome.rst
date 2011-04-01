.. highlight:: cython

.. _overview:

********
Welcome!
********

===============
What is Cython?
===============

Cython is a programming language based on Python
with extra syntax to provide static type declarations.

================
What Does It Do?
================

It takes advantage of the benefits of Python while allowing one to achieve the speed of C.

============================
How Exactly Does It Do That?
============================

The source code gets translated into optimized C/C++
code and compiled as Python extension modules.

This allows for both very fast program execution and tight
integration with external C libraries, while keeping
up the high *programmer productivity* for which the
Python language is well known.

=============
Tell Me More!
=============

The Python language is well known.

The primary Python execution environment is commonly referred to as CPython, as it is written in
C. Other major implementations use:

:Java: Jython [#Jython]_
:C#: IronPython [#IronPython]_)
:Python itself: PyPy [#PyPy]_

Written in C, CPython has been
conducive to wrapping many external libraries that interface through the C language. It has, however, remained non trivial to write the necessary glue code in
C, especially for programmers who are more fluent in a
high-level language like Python than in a do-it-yourself
language like C.

Originally based on the well-known Pyrex [#Pyrex]_, the
Cython project has approached this problem by means
of a source code compiler that translates Python code
to equivalent C code. This code is executed within the
CPython runtime environment, but at the speed of
compiled C and with the ability to call directly into C
libraries.

At the same time, it keeps the original interface of the Python source code, which makes it directly
usable from Python code. These two-fold characteristics enable Cython’s two major use cases:

#. Extending the CPython interpreter with fast binary modules, and
#. Interfacing Python code with external C libraries.

While Cython can compile (most) regular Python
code, the generated C code usually gains major (and
sometime impressive) speed improvements from optional static type declarations for both Python and
C types. These allow Cython to assign C semantics to
parts of the code, and to translate them into very efficient C code.

Type declarations can therefore be used
for two purposes:

#. For moving code sections from dynamic Python semantics into static-and-fast C semantics, but also for..
#. Directly manipulating types defined in external libraries. Cython thus merges the two worlds into a very broadly applicable programming language.

==================
Where Do I Get It?
==================

Well.. at `cython.org <http://cython.org>`_.. of course!

======================
How Do I Report a Bug?
======================

=================================
I Want To Make A Feature Request!
=================================

============================================
Is There a Mail List? How Do I Contact You?
============================================



.. rubric:: Footnotes

.. [#Jython] **Jython:** \J. Huginin, B. Warsaw, F. Bock, et al., Jython: Python for the Java platform, http://www.jython.org/

.. [#IronPython] **IronPython:** Jim Hugunin et al., http://www.codeplex.com/IronPython.


.. [#PyPy] **PyPy:** The PyPy Group, PyPy: a Python implementation written in Python, http://codespeak.net/pypy.

.. [#Pyrex] **Pyrex:** G. Ewing, Pyrex: C-Extensions for Python, http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/













