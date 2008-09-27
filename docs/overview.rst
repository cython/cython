.. highlight:: cython

.. _overview:

********
Overview
********

About Cython
==============

Cython is a language that makes writing C extensions for the Python language
as easy as Python itself. Cython is based on the well-known `Pyrex
<http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/>`_ language by Greg Ewing,
but supports more cutting edge functionality and optimizations [#]_. 
The Cython language is very close to the Python language, but Cython
additionally supports calling C functions and declaring C types on variables
and class attributes. This allows the compiler to generate very efficient C
code from Cython code.

This makes Cython the ideal language for wrapping external C libraries,
and for fast C modules that speed up the execution of Python code.  

Future Plans
============
Cython is not finished. Substantial tasks remaining. See
:ref:`cython-limitations` for a current list. 

.. rubric:: Footnotes

.. [#] For differences with Pyrex see :ref:`pyrex-differences`.

