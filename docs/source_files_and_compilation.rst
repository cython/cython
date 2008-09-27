.. _compilation_label:

****************************
Source Files and Compilation
****************************

Cython source file names consist of the name of the module followed by a
``.pyx`` extension, for example a module called primes would have a source
file named :file:`primes.pyx`.

Once you have written your ``.pyx`` file, there are a couple of ways of turning it
into an extension module. One way is to compile it manually with the Cython
compiler, e.g.::

    $ cython primes.pyx

This will produce a file called :file:`primes.c`, which then needs to be
compiled with the C compiler using whatever options are appropriate on your
platform for generating an extension module. For these options look at the
official Python documentation.

The other, and probably better, way is to use the :mod:`distutils` extension
provided with Cython. The benifit of this method is that it will give the
platform specific compilation options, acting like a stripped down autotools.

Basic setup.py
===============
The distutils extension provided with Cython allows you to pass ``.pyx`` files
directly to the ``Extension`` constructor in your setup file.

If you have a single Cython file that you want to turn into a compiled
extension, say with filename :file:`example.pyx` the associated :file:`setup.py`
would be::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("example", ["example.pyx"])]
    ) 

To understand the :file:`setup.py` more fully look at the official
``distutils`` documentation. To compile the extension for use in the
current directory use::

    $ python setup.py build_ext --inplace

Cython Files Depending on C Files
===================================

TODO

Multiple Cython Files in a Package
===================================

TODO

Distributing Pyrex modules
===========================
It is strongly recommended that you distribute the generated ``.c`` files as well
as your Cython sources, so that users can install your module without needing
to have Cython available.

It is also recommended that Cython compilation not be enabled by default in the
version you distribute. Even if the user has Cython installed, he probably
doesn't want to use it just to install your module. Also, the version he has
may not be the same one you used, and may not compile your sources correctly.

This simply means that the :file:`setup.py` file that you ship with will just
be a normal distutils file on the generated `.c` files, for the basic example
we would have instead::

    from distutils.core import setup
    from distutils.extension import Extension

    setup(
        ext_modules = [Extension("example", ["example.c"])]
    ) 

