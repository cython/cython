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


.. _pyximport:

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

Arguments
---------

The function ``pyximport.install()`` can take several arguments to
influence the compilation of Cython or Python files.

.. function:: pyximport.install(pyximport=True, pyimport=False, build_dir=None, build_in_temp=True, setup_args=None, reload_support=False, load_py_module_on_import_failure=False, inplace=False, language_level=None)

    :param pyximport: If set to False, does not try to import ``.pyx`` files.

    :param pyimport: You can pass ``pyimport=True`` to also install the ``.py`` import hook
                     in your meta-path.  Note, however, that it is highly experimental,
                     will not work for most ``.py`` files, and will therefore only slow
                     down your imports.  Use at your own risk.

    :param build_dir: By default, compiled modules will end up in a ``.pyxbld``
                      directory in the user's home directory.  Passing a different path
                      as ``build_dir`` will override this.

    :param build_in_temp: If ``False``, will produce the C files locally. Working
                          with complex dependencies and debugging becomes more easy. This
                          can principally interfere with existing files of the same name.

    :param setup_args: Dict of arguments for Distribution. See ``distutils.core.setup()``.

    :param reload_support: Enables support for dynamic
                           ``reload(my_module)``, e.g. after a change in the Cython code.
                           Additional files ``<so_path>.reloadNN`` may arise on that account, when
                           the previously loaded module file cannot be overwritten.

    :param load_py_module_on_import_failure: If the compilation of a ``.py``
                                             file succeeds, but the subsequent import fails for some reason,
                                             retry the import with the normal ``.py`` module instead of the
                                             compiled module.  Note that this may lead to unpredictable results
                                             for modules that change the system state during their import, as
                                             the second import will rerun these modifications in whatever state
                                             the system was left after the import of the compiled module
                                             failed.

    :param inplace: Install the compiled module (``.so`` for Linux and Mac / ``.pyd`` for Windows) next to the source file.

    :param language_level: The source language level to use: 2 or 3.
                           The default is to use the language level of the current Python
                           runtime for .py files and Py2 for ``.pyx`` files.

Dependency Handling
--------------------

Since :mod:`pyximport` does not use `cythonize()` internally, it currently
requires a different setup for dependencies.  It is possible to declare that
your module depends on multiple files, (likely ``.h`` and ``.pxd`` files).
If your Cython module is named ``foo`` and thus has the filename
:file:`foo.pyx` then you should create another file in the same directory
called :file:`foo.pyxdep`.  The :file:`modname.pyxdep` file can be a list of
filenames or "globs" (like ``*.pxd`` or ``include/*.h``).  Each filename or
glob must be on a separate line.  Pyximport will check the file date for each
of those files before deciding whether to rebuild the module.  In order to
keep track of the fact that the dependency has been handled, Pyximport updates
the modification time of your ".pyx" source file.  Future versions may do
something more sophisticated like informing distutils of the dependencies
directly.

Limitations
------------

Pyximport does not give you any control over how your Cython file is
compiled.  Usually the defaults are fine.  You might run into problems if
you wanted to write your program in half-C, half-Cython and build them
into a single library.

Pyximport does not hide the Distutils/GCC warnings and errors generated
by the import process.  Arguably this will give you better feedback if
something went wrong and why.  And if nothing went wrong it will give you
the warm fuzzy feeling that pyximport really did rebuild your module as it
was supposed to.

Basic module reloading support is available with the option ``reload_support=True``.
Note that this will generate a new module filename for each build and thus
end up loading multiple shared libraries into memory over time.  CPython does
not support reloading shared libraries as such.

Pyximport puts both your ``.c`` file and the platform-specific binary into
a separate build directory, usually ``$HOME/.pyxblx/``.  To copy it back
into the package hierarchy (usually next to the source file) for manual
reuse, you can pass the option ``inplace=True``.
