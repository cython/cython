.. highlight:: cython

.. _compilation:

****************************
Source Files and Compilation
****************************

Cython source file names consist of the name of the module followed by a
``.pyx`` extension, for example a module called primes would have a source
file named :file:`primes.pyx`.

Cython code, unlike Python, must be compiled.  This happens in two stages:

  * A ``.pyx`` file is compiled by Cython to a ``.c`` file.

  * The ``.c`` file is compiled by a C compiler to a ``.so`` file (or a
    ``.pyd`` file on Windows)

Once you have written your ``.pyx`` file, there are a couple of ways of turning it
into an extension module.

The following sub-sections describe several ways to build your
extension modules, and how to pass directives to the Cython compiler.

Compiling from the command line
===============================

One way is to compile it manually with the Cython
compiler, e.g.:

.. sourcecode:: text

    $ cython primes.pyx

This will produce a file called :file:`primes.c`, which then needs to be
compiled with the C compiler using whatever options are appropriate on your
platform for generating an extension module. For these options look at the
official Python documentation.

The other, and probably better, way is to use the :mod:`distutils` extension
provided with Cython. The benefit of this method is that it will give the
platform specific compilation options, acting like a stripped down autotools.


Basic setup.py
===============
The distutils extension provided with Cython allows you to pass ``.pyx`` files
directly to the ``Extension`` constructor in your setup file.

If you have a single Cython file that you want to turn into a compiled
extension, say with filename :file:`example.pyx` the associated :file:`setup.py`
would be::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        ext_modules = cythonize("example.pyx")
    )

To understand the :file:`setup.py` more fully look at the official
:mod:`distutils` documentation. To compile the extension for use in the
current directory use:

.. sourcecode:: text

    $ python setup.py build_ext --inplace


Multiple Cython Files in a Package
===================================

To automatically compile multiple Cython files without listing all of them
explicitly, you can use glob patterns::

    setup(
        ext_modules = cythonize("package/*.pyx")
    )

You can also use glob patterns in :class:`Extension` objects if you pass
them through :func:`cythonize`::

    extensions = [Extension("*", ["*.pyx"])]

    setup(
        ext_modules = cythonize(extensions)
    )


Pyximport
===========

Cython is a compiler.  Therefore it is natural that people tend to go
through an edit/compile/test cycle with Cython modules.  :mod:`pyximport`
simplifies this process by executing the "compile" step at need during
import.  For instance, if you write a Cython module called :file:`foo.pyx`,
with Pyximport you can import it in a regular Python module like this::


    import pyximport; pyximport.install()
    import foo

Doing so will result in the compilation of :file:`foo.pyx` (with appropriate
exceptions if it has an error in it).

If you would always like to import Cython files without building them specially,
you can also add the first line above to your :file:`sitecustomize.py`.
That will install the hook every time you run Python.  Then you can use
Cython modules just with simple import statements, even like this:

.. sourcecode:: text

    $ python -c "import foo"

Note that it is not recommended to let :mod:`pyximport` build code
on end user side as it hooks into their import system.  The best way
to cater for end users is to provide pre-built binary packages in the
`wheel <https://wheel.readthedocs.io/>`_ packaging format.

To have more information of :mod:`pyximport`, please refer to :ref:`pyximport`.