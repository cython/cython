NAME
====

**cython_freeze** - create a C file for embedding Cython modules


SYNOPSIS
========
::

    cython_freeze [-o outfile] [-p] module [...]


DESCRIPTION
===========

**cython_freeze** generates a C source file to embed a Python interpreter
with one or more Cython modules built in.  This allows one to create a single
executable from Cython code, without having to have separate shared objects
for each Cython module.  A major advantage of this approach is that it allows
debugging with gprof(1), which does not work with shared objects.

Unless ``-p`` is given, the first module's ``__name__`` is set to
``"__main__"`` and is imported on startup; if ``-p`` is given, a normal Python
interpreter is built, with the given modules built into the binary.

Note that this method differs from ``cython --embed``.  The ``--embed`` options
modifies the resulting C source file to include a ``main()`` function, so it
can only be used on a single Cython module.  The advantage ``--embed`` is
simplicity.  This module, on the other hand, can be used with multiple
modules, but it requires another C source file to be created.


OPTIONS
=======
::

    -o FILE, --outfile=FILE   write output to FILE instead of standard output
    -p, --pymain              do not automatically run the first module as __main__


EXAMPLE
=======

In the ``Demos/freeze`` directory, there exist two Cython modules:

* ``lcmath.pyx``: A module that interfaces with the -lm library.

* ``combinatorics.pyx``: A module that implements n-choose-r using lcmath.

Both modules have the Python idiom ``if __name__ == "__main__"``, which only
execute if that module is the "main" module.  If run as main, lcmath prints the
factorial of the argument, while combinatorics prints n-choose-r.

The provided Makefile creates an executable, *nCr*, using combinatorics as the
"main" module.  It basically performs the following (ignoring the compiler
flags)::

    $ cython_freeze combinatorics lcmath > nCr.c
    $ cython combinatorics.pyx
    $ cython lcmath.pyx
    $ gcc -c nCr.c
    $ gcc -c combinatorics.c
    $ gcc -c lcmath.c
    $ gcc nCr.o combinatorics.o lcmath.o -o nCr

Because the combinatorics module was listed first, its ``__name__`` is set
to ``"__main__"``, while lcmath's is set to ``"lcmath"``.  The executable now
contains a Python interpreter and both Cython modules. ::

    $ ./nCr
    USAGE: ./nCr n r
    Prints n-choose-r.
    $ ./nCr 15812351235 12
    5.10028093999e+113

You may wish to build a normal Python interpreter, rather than having one
module as "main".  This may happen if you want to use your module from an
interactive shell or from another script, yet you still want it statically
linked so you can profile it with gprof.  To do this, add the ``--pymain``
flag to ``cython_freeze``.  In the Makefile, the *python* executable is built
like this. ::

    $ cython_freeze --pymain combinatorics lcmath -o python.c
    $ gcc -c python.c
    $ gcc python.o combinatorics.o lcmath.o -o python

Now ``python`` is a normal Python interpreter, but the lcmath and combinatorics
modules will be built into the executable. ::

    $ ./python
    Python 2.6.2 (release26-maint, Apr 19 2009, 01:58:18)
    [GCC 4.3.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import lcmath
    >>> lcmath.factorial(155)
    4.7891429014634364e+273


PREREQUISITES
=============

Cython 0.11.2 (or newer, assuming the API does not change)


SEE ALSO
========

* `Python <https://www.python.org/>`_
* `Cython <http://www.cython.org>`_
* `freeze.py <https://wiki.python.org/moin/Freeze>`_
