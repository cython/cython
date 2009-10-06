.. highlight:: cython

.. _compilation:

***********
Compilation
***********

* Cython code, unlike Python, must be compiled.
* This happens in two stages:

 * A ``.pyx`` file is compiles by Cython to a ``.c`` file.
 * The ``.c`` file is compiled by a C comiler to a ``.so`` file (or a ``.pyd`` file on Windows)

* The following sub-sections describe several ways to build your extension modules.

.. note:: The ``-a`` option

    * Using the Cython compiler with the ``-a`` option will produce a really nice HTML file of the Cython generated ``.c`` code.
    * Double clicking on the highlighted sections will expand the code to reveal what Cython has actually generated for you.
    * This is very useful for understanding, optimizing or debugging your module.

=====================
From the Command Line
=====================

* Run the Cython compiler command with your options and list of ``.pyx`` files to generate::

    $ cython -a yourmod.pyx

* This creates a ``yourmod.c`` file. (and the -a switch produces a generated html file)
* Compiling your ``.c`` files will vary depending on your operating system.

 * Python documentation for writing extension modules should have some details for your system.

* Here we give an example on a Linux system::

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.5 -o yourmod.so yourmod.c

 * ``gcc`` will need to have paths to your included header files and paths to libraries you need to link with.
 * A ``yourmod.so`` file is now in the same directory.
 * Your module, ``yourmod`` is available for you to import as you normally would.


=========
Distutils
=========

* Ensure Distutils is installed in your system.
* The following assumes a Cython file to be compiled called *hello.pyx*.
* Create a ``setup.py`` script::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    ext_modules = [Extension("hello", ["hello.pyx"])]

    setup(
        name = ’Hello world app’,
        cmdclass = {’build_ext’: build_ext},
        ext_modules = ext_modules
    )

* Run the command ``python setup.py build_ext --inplace`` in your system's command shell.
* Your done.. import your new extension module into your python shell or script as normal.

=====
SCons
=====

to be completed...

=========
Pyximport
=========

* For generating Cython code right in your pure python modulce::

    >>> import pyximport; pyximport.install()
    >>> import helloworld
    Hello World

* Use for simple Cython builds only.

 * No extra C libraries.
 * No special build setup needed.

* Also has experimental compilation support for normal Python modules.

 * Allows you to automatically run Cython on every ``.pyx`` and ``.py`` module that Python imports.

  * This includes the standard library and installed packages.
  * In the case that Cython fails to compile a Python module, *pyximport* will fall back to loading the source modules instead.

* The ``.py`` import mechanism is installed like this::

    >>> pyximport.install(pyimport = True)


.. note:: Authors

    Paul Prescod, Stefan Behnal

====
Sage
====

The Sage notebook allows transparently editing and
compiling Cython code simply by typing %cython at
the top of a cell and evaluate it. Variables and func-
tions deﬁned in a Cython cell imported into the run-
ning session.

.. todo:: Provide a link to Sage docs
























