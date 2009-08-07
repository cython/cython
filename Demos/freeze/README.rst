NAME
====

cython_freeze.py - create a C file for embedding Cython modules


SYNOPSIS
========

cython_freeze.py module [...]


DESCRIPTION
===========

**cython_freeze.py** generates a C source file to embed a Python interpreter
with one or more Cython modules built in.  This allows one to create a single
executable from Cython code, without having to have separate shared objects
for each Cython module.

A major advantage of this approach is that it allows debuging with gprof(1),
which does not work with shared objects.

Note that this method differs from ``cython --embed``.  The ``--embed`` options
modifies the resulting C source file to include a ``main()`` function, so it
can only be used on a single Cython module.  The advantage ``--embed`` is
simplicity.  This module, on the other hand, can be used with multiple
modules, but it requires another C source file to be created.


EXAMPLE
=======

In the example directory, there exist two Cython modules:

cmath.pyx
    A module that interfaces with the -lm library.

combinatorics.pyx
    A module that implements n-choose-r using cmath.

Both modules have the Python idiom ``if __name__ == "__main__"``, which only
execute if that module is the "main" module.  If run as main, cmath prints the
factorial of the argument, while combinatorics prints n-choose-r.

The provided Makefile creates an executable, *nCr*, using combinatorics as the
"main" module.  It basically performs the following (ignoring the compiler
flags)::

    $ cython_freeze.py combintorics cmath > nCr.c
    $ cython combinatorics.pyx
    $ cython cmath.pyx
    $ gcc nCr.c -o nCr.o
    $ gcc combinatorics.c -o combinatorics.o
    $ gcc cmath.c -o cmath.o
    $ gcc nCr.o combinatorics.o cmath.o -o nCr

Because the combinatorics module was listed first, its ``__name__`` is set
to ``"__main__"``, while cmath's is set to ``"cmath"``.  The executable now
contains a Python interpreter and both Cython modules. ::

    $ ./nCr
    USAGE: ./nCr n r
    Prints n-choose-r.
    $ ./nCr 15812351235 12
    5.10028093999e+113




PREREQUISITES
=============

Cython 0.11.2 (or newer, assuming the API does not change)


SEE ALSO
========

* `Python <http://www.python.org>`_
* `Cython <http://www.cython.org>`_
* `freeze.py <http://wiki.python.org/moin/Freeze>`_
