.. highlight:: cython

.. _compilation:

***********
Compilation
***********

Cython code, unlike Python, must be compiled.  This happens in two stages:

  * A ``.pyx`` file is compiles by Cython to a ``.c`` file.

  * The ``.c`` file is compiled by a C comiler to a ``.so`` file (or a
    ``.pyd`` file on Windows)

The following sub-sections describe several ways to build your
extension modules.

=====================
From the Command Line
=====================

Run the Cython compiler command with your options and list of ``.pyx``
  files to generate.  For example::

    $ cython -a yourmod.pyx

This creates a ``yourmod.c`` file (and the -a switch produces a
generated html file).

Compiling your ``.c`` files will vary depending on your operating
system.  Python documentation for writing extension modules should
have some details for your system.  Here we give an example on a Linux
system::

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.5 -o yourmod.so yourmod.c

[``gcc`` will need to have paths to your included header files and
paths to libraries you need to link with]

A ``yourmod.so`` file is now in the same directory and your module,
``yourmod``, is available for you to import as you normally would.

=========
Distutils
=========

First, make sure that ``distutils`` package is installed in your
system.  The following assumes a Cython file to be compiled called
*hello.pyx*.  Now, create a ``setup.py`` script::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    ext_modules = [Extension("hello", ["hello.pyx"])]

    setup(
        name = ’Hello world app’,
        cmdclass = {’build_ext’: build_ext},
        ext_modules = ext_modules
    )

Run the command ``python setup.py build_ext --inplace`` in your
system's command shell and you are done.  Import your new extension
module into your python shell or script as normal.

=========
Pyximport
=========

For generating Cython code right in your pure python module just type::

    >>> import pyximport; pyximport.install()
    >>> import helloworld  
    Hello World

This allows you to automatically run Cython on every ``.pyx`` that
Python is trying to import.  You should use this for simple Cython
builds only where no extra C libraries and no special building setup
is needed.

In the case that Cython fails to compile a Python module, *pyximport*
will fall back to loading the source modules instead.

It is also possible to compile new ``.py`` modules that are being
imported (including the standard library and installed packages).  For
using this feature, just tell that to ``pyximport``::

    >>> pyximport.install(pyimport = True)

====
Sage
====

The Sage notebook allows transparently editing and compiling Cython
code simply by typing %cython at the top of a cell and evaluate
it. Variables and functions deﬁned in a Cython cell imported into the
running session.  Please check `Sage documentation
<http://www.sagemath.org/doc/>` for details.
