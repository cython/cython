.. highlight:: cython

.. _compilation:

****************************
Source Files and Compilation
****************************

.. note:: See :ref:`compilation-reference` reference section for more details

Cython source file names consist of the name of the module followed by a
``.pyx`` extension, for example a module called primes would have a source
file named :file:`primes.pyx`.

Once you have written your ``.pyx`` file, there are a couple of ways of turning it
into an extension module. One way is to compile it manually with the Cython
compiler, e.g.:

.. sourcecode:: text

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

    extensions = [Extension("*", "*.pyx")]

    setup(
        ext_modules = cythonize(extensions)
    )


.. _pyximport:

Pyximport
===========

.. TODO add some text about how this is Paul Prescods code. Also change the
   tone to be more universal (i.e. remove all the I statements)

Cython is a compiler. Therefore it is natural that people tend to go
through an edit/compile/test cycle with Cython modules. But my personal
opinion is that one of the deep insights in Python's implementation is
that a language can be compiled (Python modules are compiled to ``.pyc``)
files and hide that compilation process from the end-user so that they
do not have to worry about it. Pyximport does this for Cython modules.
For instance if you write a Cython module called :file:`foo.pyx`, with
Pyximport you can import it in a regular Python module like this::


    import pyximport; pyximport.install()
    import foo

Doing so will result in the compilation of :file:`foo.pyx` (with appropriate
exceptions if it has an error in it).

If you would always like to import Cython files without building them
specially, you can also the first line above to your :file:`sitecustomize.py`.
That will install the hook every time you run Python. Then you can use
Cython modules just with simple import statements. I like to test my
Cython modules like this:

.. sourcecode:: text

    $ python -c "import foo"

Dependency Handling
--------------------

In Pyximport 1.1 it is possible to declare that your module depends on
multiple files, (likely ``.h`` and ``.pxd`` files). If your Cython module is
named ``foo`` and thus has the filename :file:`foo.pyx` then you should make
another file in the same directory called :file:`foo.pyxdep`. The
:file:`modname.pyxdep` file can be a list of filenames or "globs" (like
``*.pxd`` or ``include/*.h``). Each filename or glob must be on a separate
line. Pyximport will check the file date for each of those files before
deciding whether to rebuild the module. In order to keep track of the
fact that the dependency has been handled, Pyximport updates the
modification time of your ".pyx" source file. Future versions may do
something more sophisticated like informing distutils of the
dependencies directly.

Limitations
------------

Pyximport does not give you any control over how your Cython file is
compiled. Usually the defaults are fine. You might run into problems if
you wanted to write your program in half-C, half-Cython and build them
into a single library. Pyximport 1.2 will probably do this.

Pyximport does not hide the Distutils/GCC warnings and errors generated
by the import process. Arguably this will give you better feedback if
something went wrong and why. And if nothing went wrong it will give you
the warm fuzzy that pyximport really did rebuild your module as it was
supposed to.

For further thought and discussion
------------------------------------

I don't think that Python's :func:`reload` will do anything for changed
``.so``'s on some (all?) platforms. It would require some (easy)
experimentation that I haven't gotten around to. But reload is rarely used in
applications outside of the Python interactive interpreter and certainly not
used much for C extension modules. Info about Windows
`<http://mail.python.org/pipermail/python-list/2001-July/053798.html>`_

``setup.py install`` does not modify :file:`sitecustomize.py` for you. Should it?
Modifying Python's "standard interpreter" behaviour may be more than
most people expect of a package they install..

Pyximport puts your ``.c`` file beside your ``.pyx`` file (analogous to
``.pyc`` beside ``.py``). But it puts the platform-specific binary in a
build directory as per normal for Distutils. If I could wave a magic
wand and get Cython or distutils or whoever to put the build directory I
might do it but not necessarily: having it at the top level is *VERY*
*HELPFUL* for debugging Cython problems.

