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

.. _compiling_command_line:

Compiling from the command line
===============================

There are two ways of compiling from the command line.

* The ``cython`` command takes a ``.py`` or ``.pyx`` file and
  compiles it into a C/C++ file.

* The ``cythonize`` command takes a ``.py`` or ``.pyx`` file and
  compiles it into a C/C++ file.  It then compiles the C/C++ file into
  an extension module which is directly importable from Python.


Compiling with the ``cython`` command
-------------------------------------

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


Compiling with the ``cythonize`` command
----------------------------------------

Run the ``cythonize`` compiler command with your options and list of
``.pyx`` files to generate an extension module.  For example::

    $ cythonize -a -i yourmod.pyx

This creates a ``yourmod.c`` file (or ``yourmod.cpp`` in C++ mode), compiles it,
and puts the resulting extension module (``.so`` or ``.pyd``, depending on your
platform) next to the source file for direct import (``-i`` builds "in place").
The ``-a`` switch additionally produces an annotated html file of the source code.

The ``cythonize`` command accepts multiple source files and glob patterns like
``**/*.pyx`` as argument and also understands the common ``-j`` option for
running multiple parallel build jobs.  When called without further options, it
will only translate the source files to ``.c`` or ``.cpp`` files.  Pass the
``-h`` flag for a complete list of supported options.

There simpler command line tool ``cython`` only invokes the source code translator.

In the case of manual compilation, how to compile your ``.c`` files will vary
depending on your operating system and compiler.  The Python documentation for
writing extension modules should have some details for your system.  On a Linux
system, for example, it might look similar to this::

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
          -I/usr/include/python3.5 -o yourmod.so yourmod.c

(``gcc`` will need to have paths to your included header files and paths
to libraries you want to link with.)

After compilation, a ``yourmod.so`` (:file:`yourmod.pyd` for Windows)
file is written into the target directory
and your module, ``yourmod``, is available for you to import as with any other
Python module.  Note that if you are not relying on ``cythonize`` or distutils,
you will not automatically benefit from the platform specific file extension
that CPython generates for disambiguation, such as
``yourmod.cpython-35m-x86_64-linux-gnu.so`` on a regular 64bit Linux installation
of CPython 3.5.

.. _basic_setup.py:

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

Configuring the C-Build
------------------------

If you have include files in non-standard places you can pass an
``include_path`` parameter to ``cythonize``::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        name="My hello app",
        ext_modules=cythonize("src/*.pyx", include_path=[...]),
    )

Often, Python packages that offer a C-level API provide a way to find
the necessary include files, e.g. for NumPy::

    include_path = [numpy.get_include()]

.. note::

    Using memoryviews or importing NumPy with ``import numpy`` does not mean that
    you have to add the path to NumPy include files. You need to add this path only
    if you use ``cimport numpy``.

Despite this, you will still get warnings like the
following from the compiler, because Cython is using a deprecated Numpy API::

   .../include/numpy/npy_1_7_deprecated_api.h:15:2: warning: #warning "Using deprecated NumPy API, disable it by " "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]

For the time being, it is just a warning that you can ignore.

If you need to specify compiler options, libraries to link with or other
linker options you will need to create ``Extension`` instances manually
(note that glob syntax can still be used to specify multiple extensions
in one line)::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Build import cythonize

    extensions = [
        Extension("primes", ["primes.pyx"],
            include_dirs=[...],
            libraries=[...],
            library_dirs=[...]),
        # Everything but primes.pyx is included here.
        Extension("*", ["*.pyx"],
            include_dirs=[...],
            libraries=[...],
            library_dirs=[...]),
    ]
    setup(
        name="My hello app",
        ext_modules=cythonize(extensions),
    )

Note that when using setuptools, you should import it before Cython as
setuptools may replace the ``Extension`` class in distutils.  Otherwise,
both might disagree about the class to use here.

Note also that if you use setuptools instead of distutils, the default
action when running ``python setup.py install`` is to create a zipped
``egg`` file which will not work with ``cimport`` for ``pxd`` files
when you try to use them from a dependent package.
To prevent this, include ``zip_safe=False`` in the arguments to ``setup()``.

If your options are static (for example you do not need to call a tool like
``pkg-config`` to determine them) you can also provide them directly in your
.pyx or .pxd source file using a special comment block at the start of the file::

    # distutils: libraries = spam eggs
    # distutils: include_dirs = /opt/food/include

If you cimport multiple .pxd files defining libraries, then Cython
merges the list of libraries, so this works as expected (similarly
with other options, like ``include_dirs`` above).

If you have some C files that have been wrapped with Cython and you want to
compile them into your extension, you can define the distutils ``sources``
parameter::

    # distutils: sources = helper.c, another_helper.c

Note that these sources are added to the list of sources of the current
extension module.  Spelling this out in the :file:`setup.py` file looks
as follows::

    from distutils.core import setup
    from Cython.Build import cythonize
    from distutils.extension import Extension

    sourcefiles = ['example.pyx', 'helper.c', 'another_helper.c']

    extensions = [Extension("example", sourcefiles)]

    setup(
        ext_modules=cythonize(extensions)
    )

The :class:`Extension` class takes many options, and a fuller explanation can
be found in the `distutils documentation`_. Some useful options to know about
are ``include_dirs``, ``libraries``, and ``library_dirs`` which specify where
to find the ``.h`` and library files when linking to external libraries.

.. _distutils documentation: https://docs.python.org/extending/building.html

Sometimes this is not enough and you need finer customization of the
distutils :class:`Extension`.
To do this, you can provide a custom function ``create_extension``
to create the final :class:`Extension` object after Cython has processed
the sources, dependencies and ``# distutils`` directives but before the
file is actually Cythonized.
This function takes 2 arguments ``template`` and ``kwds``, where
``template`` is the :class:`Extension` object given as input to Cython
and ``kwds`` is a :class:`dict` with all keywords which should be used
to create the :class:`Extension`.
The function ``create_extension`` must return a 2-tuple
``(extension, metadata)``, where ``extension`` is the created
:class:`Extension` and ``metadata`` is metadata which will be written
as JSON at the top of the generated C files. This metadata is only used
for debugging purposes, so you can put whatever you want in there
(as long as it can be converted to JSON).
The default function (defined in ``Cython.Build.Dependencies``) is::

    def default_create_extension(template, kwds):
        if 'depends' in kwds:
            include_dirs = kwds.get('include_dirs', []) + ["."]
            depends = resolve_depends(kwds['depends'], include_dirs)
            kwds['depends'] = sorted(set(depends + template.depends))

        t = template.__class__
        ext = t(**kwds)
        metadata = dict(distutils=kwds, module_name=kwds['name'])
        return ext, metadata

In case that you pass a string instead of an :class:`Extension` to
``cythonize()``, the ``template`` will be an :class:`Extension` without
sources. For example, if you do ``cythonize("*.pyx")``,
the ``template`` will be ``Extension(name="*.pyx", sources=[])``.

Just as an example, this adds ``mylib`` as library to every extension::

    from Cython.Build.Dependencies import default_create_extension

    def my_create_extension(template, kwds):
        libs = kwds.get('libraries', []) + ["mylib"]
        kwds['libraries'] = libs
        return default_create_extension(template, kwds)

    ext_modules = cythonize(..., create_extension=my_create_extension)

.. note::

    If you Cythonize in parallel (using the ``nthreads`` argument),
    then the argument to ``create_extension`` must be pickleable.
    In particular, it cannot be a lambda function.

.. _cythonize_arguments:

Cythonize arguments
-------------------

The function :func:`cythonize` can take extra arguments which will allow you to
customize your build.

.. autofunction:: Cython.Build.cythonize


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


.. _distributing_cython_modules:

Distributing Cython modules
----------------------------

It is strongly recommended that you distribute the generated ``.c`` files as well
as your Cython sources, so that users can install your module without needing
to have Cython available.

It is also recommended that Cython compilation not be enabled by default in the
version you distribute. Even if the user has Cython installed, he/she probably
doesn't want to use it just to install your module. Also, the installed version
may not be the same one you used, and may not compile your sources correctly.

This simply means that the :file:`setup.py` file that you ship with will just
be a normal distutils file on the generated `.c` files, for the basic example
we would have instead::

    from distutils.core import setup
    from distutils.extension import Extension

    setup(
        ext_modules = [Extension("example", ["example.c"])]
    )

This is easy to combine with :func:`cythonize` by changing the file extension
of the extension module sources::

    from distutils.core import setup
    from distutils.extension import Extension

    USE_CYTHON = ...   # command line option, try-import, ...

    ext = '.pyx' if USE_CYTHON else '.c'

    extensions = [Extension("example", ["example"+ext])]

    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)

    setup(
        ext_modules = extensions
    )

If you have many extensions and want to avoid the additional complexity in the
declarations, you can declare them with their normal Cython sources and then
call the following function instead of ``cythonize()`` to adapt the sources
list in the Extensions when not using Cython::

    import os.path

    def no_cythonize(extensions, **_ignore):
        for extension in extensions:
            sources = []
            for sfile in extension.sources:
                path, ext = os.path.splitext(sfile)
                if ext in ('.pyx', '.py'):
                    if extension.language == 'c++':
                        ext = '.cpp'
                    else:
                        ext = '.c'
                    sfile = path + ext
                sources.append(sfile)
            extension.sources[:] = sources
        return extensions

Another option is to make Cython a setup dependency of your system and use
Cython's build_ext module which runs ``cythonize`` as part of the build process::

    setup(
        setup_requires=[
            'cython>=0.x',
        ],
        extensions = [Extension("*", ["*.pyx"])],
        cmdclass={'build_ext': Cython.Build.build_ext},
        ...
    )

If you want to expose the C-level interface of your library for other
libraries to cimport from, use package_data to install the ``.pxd`` files,
e.g.::

    setup(
        package_data = {
            'my_package': ['*.pxd'],
            'my_package/sub_package': ['*.pxd'],
        },
        ...
    )

These ``.pxd`` files need not have corresponding ``.pyx``
modules if they contain purely declarations of external libraries.

Remember that if you use setuptools instead of distutils, the default
action when running ``python setup.py install`` is to create a zipped
``egg`` file which will not work with ``cimport`` for ``pxd`` files
when you try to use them from a dependent package.
To prevent this, include ``zip_safe=False`` in the arguments to ``setup()``.


.. _integrating_multiple_modules:

Integrating multiple modules
============================

In some scenarios, it can be useful to link multiple Cython modules
(or other extension modules) into a single binary, e.g. when embedding
Python in another application.  This can be done through the inittab
import mechanism of CPython.

Create a new C file to integrate the extension modules and add this
macro to it::

    #if PY_MAJOR_VERSION < 3
    # define MODINIT(name)  init ## name
    #else
    # define MODINIT(name)  PyInit_ ## name
    #endif

If you are only targeting Python 3.x, just use ``PyInit_`` as prefix.

Then, for each of the modules, declare its module init function
as follows, replacing ``some_module_name`` with the name of the module::

    PyMODINIT_FUNC  MODINIT(some_module_name) (void);

In C++, declare them as ``extern C``.

If you are not sure of the name of the module init function, refer
to your generated module source file and look for a function name
starting with ``PyInit_``.

Next, before you start the Python runtime from your application code
with ``Py_Initialize()``, you need to initialise the modules at runtime
using the ``PyImport_AppendInittab()`` C-API function, again inserting
the name of each of the modules::

    PyImport_AppendInittab("some_module_name", MODINIT(some_module_name));

This enables normal imports for the embedded extension modules.

In order to prevent the joined binary from exporting all of the module
init functions as public symbols, Cython 0.28 and later can hide these
symbols if the macro ``CYTHON_NO_PYINIT_EXPORT`` is defined while
C-compiling the module C files.

Also take a look at the `cython_freeze
<https://github.com/cython/cython/blob/master/bin/cython_freeze>`_ tool.
It can generate the necessary boilerplate code for linking one or more
modules into a single Python executable.


.. _pyximport:

Compiling with :mod:`pyximport`
===============================

For building Cython modules during development without explicitly
running ``setup.py`` after each change, you can use :mod:`pyximport`::

    >>> import pyximport; pyximport.install()
    >>> import helloworld
    Hello World

This allows you to automatically run Cython on every ``.pyx`` that
Python is trying to import.  You should use this for simple Cython
builds only where no extra C libraries and no special building setup
is needed.

It is also possible to compile new ``.py`` modules that are being
imported (including the standard library and installed packages).  For
using this feature, just tell that to :mod:`pyximport`::

    >>> pyximport.install(pyimport=True)

In the case that Cython fails to compile a Python module, :mod:`pyximport`
will fall back to loading the source modules instead.

Note that it is not recommended to let :mod:`pyximport` build code
on end user side as it hooks into their import system.  The best way
to cater for end users is to provide pre-built binary packages in the
`wheel <https://wheel.readthedocs.io/>`_ packaging format.


Arguments
---------

The function ``pyximport.install()`` can take several arguments to
influence the compilation of Cython or Python files.

.. autofunction:: pyximport.install


Dependency Handling
--------------------

Since :mod:`pyximport` does not use :func:`cythonize()` internally, it currently
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

:mod:`pyximport` does not use :func:`cythonize()`. Thus it is not
possible to do things like using compiler directives at
the top of Cython files or compiling Cython code to C++.

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
end up loading multiple shared libraries into memory over time. CPython has limited
support for reloading shared libraries as such,
see `PEP 489 <https://www.python.org/dev/peps/pep-0489/>`_.

Pyximport puts both your ``.c`` file and the platform-specific binary into
a separate build directory, usually ``$HOME/.pyxblx/``.  To copy it back
into the package hierarchy (usually next to the source file) for manual
reuse, you can pass the option ``inplace=True``.


.. _compiling_with_cython_inline:

Compiling with ``cython.inline``
=================================

One can also compile Cython in a fashion similar to SciPy's ``weave.inline``.
For example::

    >>> import cython
    >>> def f(a):
    ...     ret = cython.inline("return a+b", b=3)
    ...

Unbound variables are automatically pulled from the surrounding local
and global scopes, and the result of the compilation is cached for
efficient re-use.

.. _compiling_with_sage:

Compiling with Sage
===================

The Sage notebook allows transparently editing and compiling Cython
code simply by typing ``%cython`` at the top of a cell and evaluate
it. Variables and functions defined in a Cython cell are imported into the
running session.  Please check `Sage documentation
<http://www.sagemath.org/doc/>`_ for details.

You can tailor the behavior of the Cython compiler by specifying the
directives below.

.. _compiling_notebook:

Compiling with a Jupyter Notebook
=================================

It's possible to compile code in a notebook cell with Cython.
For this you need to load the Cython magic::

    %load_ext cython

Then you can define a Cython cell by writing ``%%cython`` on top of it.
Like this::

    %%cython

    cdef int a = 0
    for i in range(10):
        a += i
    print(a)

Note that each cell will be compiled into a separate extension module. So if you use a package in a Cython
cell, you will have to import this package in the same cell. It's not enough to
have imported the package in a previous cell. Cython will tell you that there are
"undefined global names" at compilation time if you don't comply.

The global names (top level functions, classes, variables and modules) of the
cell are then loaded into the global namespace of the notebook. So in the
end, it behaves as if you executed a Python cell.

Additional allowable arguments to the Cython magic are listed below.
You can see them also by typing ```%%cython?`` in IPython or a Jupyter notebook.

============================================  =======================================================================================================================================

-a, --annotate                                Produce a colorized HTML version of the source.

-+, --cplus                                   Output a C++ rather than C file.

-f, --force                                   Force the compilation of a new module, even if the source has been previously compiled.

-3                                            Select Python 3 syntax

-2                                            Select Python 2 syntax

-c=COMPILE_ARGS, --compile-args=COMPILE_ARGS  Extra flags to pass to compiler via the extra_compile_args.

--link-args LINK_ARGS                         Extra flags to pass to linker via the extra_link_args.

-l LIB, --lib LIB                             Add a library to link the extension against (can be specified multiple times).

-L dir                                        Add a path to the list of library directories (can be specified multiple times).

-I INCLUDE, --include INCLUDE                 Add a path to the list of include directories (can be specified multiple times).

-S, --src                                     Add a path to the list of src files (can be specified multiple times).

-n NAME, --name NAME                          Specify a name for the Cython module.

--pgo                                         Enable profile guided optimisation in the C compiler. Compiles the cell twice and executes it in between to generate a runtime profile.

--verbose                                     Print debug information like generated .c/.cpp file location and exact gcc/g++ command invoked.
============================================  =======================================================================================================================================


.. _compiler_options:

Compiler options
----------------

Compiler options can be set in the :file:`setup.py`, before calling :func:`cythonize`,
like this::

    from distutils.core import setup

    from Cython.Build import cythonize
    from Cython.Compiler import Options

    Options.docstrings = False

    setup(
        name = "hello",
        ext_modules = cythonize("lib.pyx"),
    )

Here are the options that are available:

.. autodata:: Cython.Compiler.Options.docstrings
.. autodata:: Cython.Compiler.Options.embed_pos_in_docstring
.. autodata:: Cython.Compiler.Options.emit_code_comments
.. pre_import
.. autodata:: Cython.Compiler.Options.generate_cleanup_code
.. autodata:: Cython.Compiler.Options.clear_to_none
.. autodata:: Cython.Compiler.Options.annotate
.. annotate_coverage_xml
.. autodata:: Cython.Compiler.Options.fast_fail
.. autodata:: Cython.Compiler.Options.warning_errors
.. autodata:: Cython.Compiler.Options.error_on_unknown_names
.. autodata:: Cython.Compiler.Options.error_on_uninitialized
.. autodata:: Cython.Compiler.Options.convert_range
.. autodata:: Cython.Compiler.Options.cache_builtins
.. autodata:: Cython.Compiler.Options.gcc_branch_hints
.. autodata:: Cython.Compiler.Options.lookup_module_cpdef
.. autodata:: Cython.Compiler.Options.embed
.. old_style_globals
.. autodata:: Cython.Compiler.Options.cimport_from_pyx
.. autodata:: Cython.Compiler.Options.buffer_max_dims
.. autodata:: Cython.Compiler.Options.closure_freelist_size


.. _compiler-directives:

Compiler directives
====================

Compiler directives are instructions which affect the behavior of
Cython code.  Here is the list of currently supported directives:

``binding`` (True / False)
    Controls whether free functions behave more like Python's CFunctions
    (e.g. :func:`len`) or, when set to True, more like Python's functions.
    When enabled, functions will bind to an instance when looked up as a
    class attribute (hence the name) and will emulate the attributes
    of Python functions, including introspections like argument names and
    annotations.
    Default is False.

``boundscheck``  (True / False)
    If set to False, Cython is free to assume that indexing operations
    ([]-operator) in the code will not cause any IndexErrors to be
    raised. Lists, tuples, and strings are affected only if the index
    can be determined to be non-negative (or if ``wraparound`` is False).
    Conditions which would normally trigger an IndexError may instead cause
    segfaults or data corruption if this is set to False.
    Default is True.

``wraparound``  (True / False)
    In Python, arrays and sequences can be indexed relative to the end.
    For example, A[-1] indexes the last value of a list.
    In C, negative indexing is not supported.
    If set to False, Cython is allowed to neither check for nor correctly
    handle negative indices, possibly causing segfaults or data corruption.
    If bounds checks are enabled (the default, see ``boundschecks`` above),
    negative indexing will usually raise an ``IndexError`` for indices that
    Cython evaluates itself.
    However, these cases can be difficult to recognise in user code to
    distinguish them from indexing or slicing that is evaluated by the
    underlying Python array or sequence object and thus continues to support
    wrap-around indices.
    It is therefore safest to apply this option only to code that does not
    process negative indices at all.
    Default is True.

``initializedcheck`` (True / False)
    If set to True, Cython checks that a memoryview is initialized
    whenever its elements are accessed or assigned to. Setting this
    to False disables these checks.
    Default is True.

``nonecheck``  (True / False)
    If set to False, Cython is free to assume that native field
    accesses on variables typed as an extension type, or buffer
    accesses on a buffer variable, never occurs when the variable is
    set to ``None``. Otherwise a check is inserted and the
    appropriate exception is raised. This is off by default for
    performance reasons.  Default is False.

``overflowcheck`` (True / False)
    If set to True, raise errors on overflowing C integer arithmetic
    operations.  Incurs a modest runtime penalty, but is much faster than
    using Python ints.  Default is False.

``overflowcheck.fold`` (True / False)
    If set to True, and overflowcheck is True, check the overflow bit for
    nested, side-effect-free arithmetic expressions once rather than at every
    step.  Depending on the compiler, architecture, and optimization settings,
    this may help or hurt performance.  A simple suite of benchmarks can be
    found in ``Demos/overflow_perf.pyx``.  Default is True.

``embedsignature`` (True / False)
    If set to True, Cython will embed a textual copy of the call
    signature in the docstring of all Python visible functions and
    classes. Tools like IPython and epydoc can thus display the
    signature, which cannot otherwise be retrieved after
    compilation.  Default is False.

``cdivision`` (True / False)
    If set to False, Cython will adjust the remainder and quotient
    operators C types to match those of Python ints (which differ when
    the operands have opposite signs) and raise a
    ``ZeroDivisionError`` when the right operand is 0. This has up to
    a 35% speed penalty. If set to True, no checks are performed.  See
    `CEP 516 <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default
    is False.

``cdivision_warnings`` (True / False)
    If set to True, Cython will emit a runtime warning whenever
    division is performed with negative operands.  See `CEP 516
    <https://github.com/cython/cython/wiki/enhancements-division>`_.  Default is
    False.

``always_allow_keywords`` (True / False)
    Avoid the ``METH_NOARGS`` and ``METH_O`` when constructing
    functions/methods which take zero or one arguments. Has no effect
    on special methods and functions with more than one argument. The
    ``METH_NOARGS`` and ``METH_O`` signatures provide faster
    calling conventions but disallow the use of keywords.

``profile`` (True / False)
    Write hooks for Python profilers into the compiled C code.  Default
    is False.

``linetrace`` (True / False)
    Write line tracing hooks for Python profilers or coverage reporting
    into the compiled C code.  This also enables profiling.  Default is
    False.  Note that the generated module will not actually use line
    tracing, unless you additionally pass the C macro definition
    ``CYTHON_TRACE=1`` to the C compiler (e.g. using the distutils option
    ``define_macros``).  Define ``CYTHON_TRACE_NOGIL=1`` to also include
    ``nogil`` functions and sections.

``infer_types`` (True / False)
    Infer types of untyped variables in function bodies. Default is
    None, indicating that only safe (semantically-unchanging) inferences
    are allowed.
    In particular, inferring *integral* types for variables *used in arithmetic
    expressions* is considered unsafe (due to possible overflow) and must be
    explicitly requested.

``language_level`` (2/3/3str)
    Globally set the Python language level to be used for module
    compilation.  Default is compatibility with Python 2.  To enable
    Python 3 source code semantics, set this to 3 (or 3str) at the start
    of a module or pass the "-3" or "--3str" command line options to the
    compiler.  The ``3str`` option enables Python 3 semantics but does
    not change the ``str`` type and unprefixed string literals to
    ``unicode`` when the compiled code runs in Python 2.x.
    Note that cimported files inherit this setting from the module
    being compiled, unless they explicitly set their own language level.
    Included source files always inherit this setting.

``c_string_type`` (bytes / str / unicode)
    Globally set the type of an implicit coercion from char* or std::string.

``c_string_encoding`` (ascii, default, utf-8, etc.)
    Globally set the encoding to use when implicitly coercing char* or std:string
    to a unicode object.  Coercion from a unicode object to C type is only allowed
    when set to ``ascii`` or ``default``, the latter being utf-8 in Python 3 and
    nearly-always ascii in Python 2.

``type_version_tag`` (True / False)
    Enables the attribute cache for extension types in CPython by setting the
    type flag ``Py_TPFLAGS_HAVE_VERSION_TAG``.  Default is True, meaning that
    the cache is enabled for Cython implemented types.  To disable it
    explicitly in the rare cases where a type needs to juggle with its ``tp_dict``
    internally without paying attention to cache consistency, this option can
    be set to False.

``unraisable_tracebacks`` (True / False)
    Whether to print tracebacks when suppressing unraisable exceptions.

``iterable_coroutine`` (True / False)
    `PEP 492 <https://www.python.org/dev/peps/pep-0492/>`_ specifies that async-def
    coroutines must not be iterable, in order to prevent accidental misuse in
    non-async contexts.  However, this makes it difficult and inefficient to write
    backwards compatible code that uses async-def coroutines in Cython but needs to
    interact with async Python code that uses the older yield-from syntax, such as
    asyncio before Python 3.5.  This directive can be applied in modules or
    selectively as decorator on an async-def coroutine to make the affected
    coroutine(s) iterable and thus directly interoperable with yield-from.


.. _configurable_optimisations:

Configurable optimisations
--------------------------

``optimize.use_switch`` (True / False)
    Whether to expand chained if-else statements (including statements like
    ``if x == 1 or x == 2:``) into C switch statements.  This can have performance
    benefits if there are lots of values but cause compiler errors if there are any
    duplicate values (which may not be detectable at Cython compile time for all
    C constants).  Default is True.

``optimize.unpack_method_calls`` (True / False)
    Cython can generate code that optimistically checks for Python method objects
    at call time and unpacks the underlying function to call it directly.  This
    can substantially speed up method calls, especially for builtins, but may also
    have a slight negative performance impact in some cases where the guess goes
    completely wrong.
    Disabling this option can also reduce the code size.  Default is True.

.. _warnings:

Warnings
--------

All warning directives take True / False as options
to turn the warning on / off.

``warn.undeclared`` (default False)
    Warns about any variables that are implicitly declared without a ``cdef`` declaration

``warn.unreachable`` (default True)
    Warns about code paths that are statically determined to be unreachable, e.g.
    returning twice unconditionally.

``warn.maybe_uninitialized`` (default False)
    Warns about use of variables that are conditionally uninitialized.

``warn.unused`` (default False)
    Warns about unused variables and declarations

``warn.unused_arg`` (default False)
    Warns about unused function arguments

``warn.unused_result`` (default False)
    Warns about unused assignment to the same name, such as
    ``r = 2; r = 1 + 2``

``warn.multiple_declarators`` (default True)
   Warns about multiple variables declared on the same line with at least one pointer type.
   For example ``cdef double* a, b`` - which, as in C, declares ``a`` as a pointer, ``b`` as
   a value type, but could be mininterpreted as declaring two pointers.


.. _how_to_set_directives:

How to set directives
---------------------

Globally
:::::::::

One can set compiler directives through a special header comment near the top of the file, like this::

    # cython: language_level=3, boundscheck=False

The comment must appear before any code (but can appear after other
comments or whitespace).

One can also pass a directive on the command line by using the -X switch::

    $ cython -X boundscheck=True ...

Directives passed on the command line will override directives set in
header comments.

Locally
::::::::

For local blocks, you need to cimport the special builtin ``cython``
module::

    #!python
    cimport cython

Then you can use the directives either as decorators or in a with
statement, like this::

    #!python
    @cython.boundscheck(False) # turn off boundscheck for this function
    def f():
        ...
        # turn it temporarily on again for this block
        with cython.boundscheck(True):
            ...

.. Warning:: These two methods of setting directives are **not**
    affected by overriding the directive on the command-line using the
    -X option.

In :file:`setup.py`
:::::::::::::::::::

Compiler directives can also be set in the :file:`setup.py` file by passing a keyword
argument to ``cythonize``::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        name="My hello app",
        ext_modules=cythonize('hello.pyx', compiler_directives={'embedsignature': True}),
    )

This will override the default directives as specified in the ``compiler_directives`` dictionary.
Note that explicit per-file or local directives as explained above take precedence over the
values passed to ``cythonize``.
