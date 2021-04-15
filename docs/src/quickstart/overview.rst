Cython - an overview
====================

[Cython]_ is a programming language that makes writing C extensions
for the Python language as easy as Python itself.  It aims to become
a superset of the [Python]_ language which gives it high-level,
object-oriented, functional, and dynamic programming.  Its main feature
on top of these is support for optional static type declarations as
part of the language.  The source code gets translated into optimized
C/C++ code and compiled as Python extension modules.  This allows for
both very fast program execution and tight integration with external C
libraries, while keeping up the high programmer productivity for
which the Python language is well known.

The primary Python execution environment is commonly referred to as
CPython, as it is written in C.  Other major implementations use Java
(Jython [Jython]_), C# (IronPython [IronPython]_) and Python itself
(PyPy [PyPy]_).  Written in C, CPython has been conducive to wrapping
many external libraries that interface through the C language.  It
has, however, remained non trivial to write the necessary glue code in
C, especially for programmers who are more fluent in a high-level
language like Python than in a close-to-the-metal language like C.

Originally based on the well-known Pyrex [Pyrex]_, the Cython project
has approached this problem by means of a source code compiler that
translates Python code to equivalent C code.  This code is executed
within the CPython runtime environment, but at the speed of compiled C
and with the ability to call directly into C libraries.
At the same time, it keeps the original interface of the Python
source code, which makes it directly usable from Python code.  These
two-fold characteristics enable Cython's two major use cases:
extending the CPython interpreter with fast binary modules, and
interfacing Python code with external C libraries.

While Cython can compile (most) regular Python code, the generated C
code usually gains major (and sometime impressive) speed improvements
from optional static type declarations for both Python and C types.
These allow Cython to assign C semantics to parts of the code, and to
translate them into very efficient C code.  Type declarations can
therefore be used for two purposes: for moving code sections from
dynamic Python semantics into static-and-fast C semantics, but also
for directly manipulating types defined in external libraries.  Cython
thus merges the two worlds into a very broadly applicable programming
language.

.. [Cython] G. Ewing, R. W. Bradshaw, S. Behnel, D. S. Seljebotn et al.,
   The Cython compiler, https://cython.org/.
.. [IronPython] Jim Hugunin et al., https://archive.codeplex.com/?p=IronPython.
.. [Jython] J. Huginin, B. Warsaw, F. Bock, et al.,
   Jython: Python for the Java platform, https://www.jython.org.
.. [PyPy] The PyPy Group, PyPy: a Python implementation written in Python,
   https://pypy.org/.
.. [Pyrex] G. Ewing, Pyrex: C-Extensions for Python,
   https://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/
.. [Python] G. van Rossum et al., The Python programming language,
   https://www.python.org/.
