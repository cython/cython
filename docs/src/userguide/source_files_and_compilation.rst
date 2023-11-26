.. highlight:: cython

.. _compilation:

****************************
Source Files and Compilation
****************************

Cython source file names consist of the name of the module followed by a
``.pyx`` extension, for example a module called primes would have a source
file named :file:`primes.pyx`.

Cython code, unlike Python, must be compiled.  This happens in two stages:

  * A ``.pyx`` (or ``.py``) file is compiled by Cython to a ``.c`` file.

  * The ``.c`` file is compiled by a C compiler to a ``.so`` file (or a
    ``.pyd`` file on Windows)

Once you have written your ``.pyx``/``.py`` file, there are a couple of ways
how to turn it into an extension module.

The following sub-sections describe several ways to build your
extension modules, and how to pass directives to the Cython compiler.

There are also a number of tools that process ``.pyx`` files apart from Cython, e.g.

- Linting: https://pypi.org/project/cython-lint/


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

.. code-block:: text

    $ cython primes.pyx

This will produce a file called :file:`primes.c`, which then needs to be
compiled with the C compiler using whatever options are appropriate on your
platform for generating an extension module. For these options look at the
official Python documentation.

The other, and probably better, way is to use the :mod:`setuptools` extension
provided with Cython. The benefit of this method is that it will give the
platform specific compilation options, acting like a stripped down autotools.


Compiling with the ``cythonize`` command
----------------------------------------

Run the ``cythonize`` compiler command with your options and list of
``.pyx`` files to generate an extension module.  For example:

.. code-block:: bash

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
system, for example, it might look similar to this:

.. code-block:: bash

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
          -I/usr/include/python3.5 -o yourmod.so yourmod.c

(``gcc`` will need to have paths to your included header files and paths
to libraries you want to link with.)

After compilation, a ``yourmod.so`` (:file:`yourmod.pyd` for Windows)
file is written into the target directory
and your module, ``yourmod``, is available for you to import as with any other
Python module.  Note that if you are not relying on ``cythonize`` or setuptools,
you will not automatically benefit from the platform specific file extension
that CPython generates for disambiguation, such as
``yourmod.cpython-35m-x86_64-linux-gnu.so`` on a regular 64bit Linux installation
of CPython 3.5.


.. _basic_setup.py:

Basic setup.py
===============
The setuptools extension provided with Cython allows you to pass ``.pyx`` files
directly to the ``Extension`` constructor in your setup file.

If you have a single Cython file that you want to turn into a compiled
extension, say with filename :file:`example.pyx` the associated :file:`setup.py`
would be::

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        ext_modules = cythonize("example.pyx")
    )

If your build depends directly on Cython in this way,
then you may also want to inform pip that :mod:`Cython` is required for
:file:`setup.py` to execute, following `PEP 518
<https://www.python.org/dev/peps/pep-0518/>`, creating a :file:`pyproject.toml`
file containing, at least:

.. code-block:: ini


    [build-system]
    requires = ["setuptools", "wheel", "Cython"]

To understand the :file:`setup.py` more fully look at the official `setuptools
documentation`_. To compile the extension for use in the current directory use:

.. code-block:: text

    $ python setup.py build_ext --inplace


Configuring the C-Build
------------------------

If you have include files in non-standard places you can pass an
``include_path`` parameter to ``cythonize``::

    from setuptools import setup
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

Despite this, you may still get warnings like the following from the compiler,
because Cython is not disabling the usage of the old deprecated Numpy API::

   .../include/numpy/npy_1_7_deprecated_api.h:15:2: warning: #warning "Using deprecated NumPy API, disable it by " "#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]

In Cython 3.0, you can get rid of this warning by defining the C macro
``NPY_NO_DEPRECATED_API`` as ``NPY_1_7_API_VERSION``
in your build, e.g.::

    # distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

or (see below)::

    Extension(
        ...,
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )

With older Cython releases, setting this macro will fail the C compilation,
because Cython generates code that uses this deprecated C-API.  However, the
warning has no negative effects even in recent NumPy versions including 1.18.x.
You can ignore it until you (or your library's users) switch to a newer NumPy
version that removes this long deprecated API, in which case you also need to
use Cython 3.0 or later.  Thus, the earlier you switch to Cython 3.0, the
better for your users.

If you need to specify compiler options, libraries to link with or other
linker options you will need to create ``Extension`` instances manually
(note that glob syntax can still be used to specify multiple extensions
in one line)::

    from setuptools import Extension, setup
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

Note that when using setuptools, you should import it before Cython, otherwise,
both might disagree about the class to use here.

If your options are static (for example you do not need to call a tool like
``pkg-config`` to determine them) you can also provide them directly in your
.pyx or .pxd source file using a special comment block at the start of the file::

    # distutils: libraries = spam eggs
    # distutils: include_dirs = /opt/food/include

If you cimport multiple .pxd files defining libraries, then Cython
merges the list of libraries, so this works as expected (similarly
with other options, like ``include_dirs`` above).

If you have some C files that have been wrapped with Cython and you want to
compile them into your extension, you can define the setuptools ``sources``
parameter::

    # distutils: sources = helper.c, another_helper.c

Note that these sources are added to the list of sources of the current
extension module.  Spelling this out in the :file:`setup.py` file looks
as follows::

    from setuptools import Extension, setup
    from Cython.Build import cythonize

    sourcefiles = ['example.pyx', 'helper.c', 'another_helper.c']

    extensions = [Extension("example", sourcefiles)]

    setup(
        ext_modules=cythonize(extensions)
    )

The :class:`Extension` class takes many options, and a fuller explanation can
be found in the `setuptools documentation`_. Some useful options to know about
are ``include_dirs``, ``libraries``, and ``library_dirs`` which specify where
to find the ``.h`` and library files when linking to external libraries.

.. _setuptools documentation: https://setuptools.readthedocs.io/

Sometimes this is not enough and you need finer customization of the
setuptools :class:`Extension`.
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
be a normal setuptools file on the generated `.c` files, for the basic example
we would have instead::

    from setuptools import Extension, setup

    setup(
        ext_modules = [Extension("example", ["example.c"])]
    )

This is easy to combine with :func:`cythonize` by changing the file extension
of the extension module sources::

    from setuptools import Extension, setup

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
        extensions = [Extension("*", ["*.pyx"])],
        cmdclass={'build_ext': Cython.Build.build_ext},
        ...
    )

This depends on pip knowing that :mod:`Cython` is a setup dependency, by having
a :file:`pyproject.toml` file::

    [build-system]
    requires = ["setuptools", "wheel", "Cython"]

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
something more sophisticated like informing setuptools of the dependencies
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

Pyximport does not hide the setuptools/GCC warnings and errors generated
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
efficient reuse.


Compiling with ``cython.compile``
=================================

Cython supports transparent compiling of the cython code in a function using the
``@cython.compile`` decorator::

    @cython.compile
    def plus(a, b):
        return a + b

Parameters of the decorated function cannot have type declarations. Their types are
automatically determined from values passed to the function, thus leading to one or more
specialised compiled functions for the respective argument types.
Executing example::

    import cython

    @cython.compile
    def plus(a, b):
        return a + b

    print(plus('3', '5'))
    print(plus(3, 5))

will produce following output::

    35
    8


.. _compiling_with_sage:

Compiling with Sage
===================

The Sage notebook allows transparently editing and compiling Cython
code simply by typing ``%cython`` at the top of a cell and evaluate
it. Variables and functions defined in a Cython cell are imported into the
running session.  Please check `Sage documentation
<https://www.sagemath.org/doc/>`_ for details.

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

--annotate-fullc                              Produce a colorized HTML version of the source which includes entire generated C/C++-code.

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

    from setuptools import setup

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

    Default is True.

    .. versionchanged:: 3.0.0
        Default changed from False to True 

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
    If set to True, Cython checks that
     - a memoryview is initialized whenever its elements are accessed 
       or assigned to.
     - a C++ class is initialized when it is accessed 
       (only when ``cpp_locals`` is on)

    Setting this to False disables these checks.
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

``embedsignature.format`` (``c`` / ``python`` / ``clinic``)
    If set to ``c``, Cython will generate signatures preserving
    C type declarations and Python type annotations.
    If set to ``python``, Cython will do a best attempt to use
    pure-Python type annotations in embedded signatures. For arguments
    without Python type annotations, the C type is mapped to the
    closest Python type equivalent (e.g., C ``short`` is mapped to
    Python ``int`` type and C ``double`` is mapped to Python ``float``
    type).  The specific output and type mapping are experimental and
    may change over time.
    The ``clinic`` format generates signatures that are compatible
    with those understood by CPython's Argument Clinic tool. The
    CPython runtime strips these signatures from docstrings and
    translates them into a ``__text_signature__`` attribute. This is
    mainly useful when using ``binding=False``, since the Cython
    functions generated with ``binding=True`` do not have (nor need)
    a ``__text_signature__`` attribute.
    Default is ``c``.

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
    
``cpow`` (True / False)
    ``cpow`` modifies the return type of ``a**b``, as shown in the
    table below:
    
        .. csv-table:: cpow behaviour
            :file: cpow_table.csv
            :header-rows: 1
            :class: longtable
            :widths: 1 1 3 3
    
    The ``cpow==True`` behaviour largely keeps the result type the
    same as the operand types, while the ``cpow==False`` behaviour
    follows Python and returns a flexible type depending on the
    inputs.

    Introduced in Cython 3.0 with a default of False;
    before that, the behaviour matched the ``cpow=True`` version.

``always_allow_keywords`` (True / False)
    When disabled, uses the ``METH_NOARGS`` and ``METH_O`` signatures when
    constructing functions/methods which take zero or one arguments. Has no
    effect on special methods and functions with more than one argument. The
    ``METH_NOARGS`` and ``METH_O`` signatures provide slightly faster
    calling conventions but disallow the use of keywords.

``c_api_binop_methods`` (True / False)
    When enabled, makes the special binary operator methods (``__add__``, etc.)
    behave according to the low-level C-API slot semantics, i.e. only a single
    method implements both the normal and reversed operator.  This used to be
    the default in Cython 0.x and was now replaced by Python semantics, i.e. the
    default in Cython 3.x and later is ``False``.

``profile`` (True / False)
    Write hooks for Python profilers into the compiled C code.  Default
    is False.

``linetrace`` (True / False)
    Write line tracing hooks for Python profilers or coverage reporting
    into the compiled C code.  This also enables profiling.  Default is
    False.  Note that the generated module will not actually use line
    tracing, unless you additionally pass the C macro definition
    ``CYTHON_TRACE=1`` to the C compiler (e.g. using the setuptools option
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
    Globally set the Python language level to be used for module compilation.
    Default is compatibility with Python 3 in Cython 3.x and with Python 2 in Cython 0.x.
    To enable Python 3 source code semantics, set this to 3 (or 3str) at the start
    of a module or pass the "-3" or "--3str" command line options to the
    compiler.  For Python 2 semantics, use 2 and "-2" accordingly.  The ``3str``
    option enables Python 3 semantics but does
    not change the ``str`` type and unprefixed string literals to
    ``unicode`` when the compiled code runs in Python 2.x.
    Language level 2 ignores ``x: int`` type annotations due to the int/long ambiguity.
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

``annotation_typing`` (True / False)
    Uses function argument annotations to determine the type of variables. Default
    is True, but can be disabled. Since Python does not enforce types given in
    annotations, setting to False gives greater compatibility with Python code.
    From Cython 3.0, ``annotation_typing`` can be set on a per-function or
    per-class basis.

``emit_code_comments`` (True / False)
    Copy the original source code line by line into C code comments in the generated
    code file to help with understanding the output.
    This is also required for coverage analysis.

``cpp_locals`` (True / False)
    Make C++ variables behave more like Python variables by allowing them to be
    "unbound" instead of always default-constructing them at the start of a
    function.  See :ref:`cpp_locals directive` for more detail.

``legacy_implicit_noexcept`` (True / False)
    When enabled, ``cdef`` functions will not propagate raised exceptions by default. Hence,
    the function will behave in the same way as if declared with `noexcept` keyword. See
    :ref:`error_return_values` for details. Setting this directive to ``True`` will
    cause Cython 3.0 to have the same semantics as Cython 0.x. This directive was solely added
    to help migrate legacy code written before Cython 3. It will be removed in a future release.


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
   
``show_performance_hints`` (default True)
  Show performance hints during compilation pointing to places in the code which can yield performance degradation.
  Note that performance hints are not warnings and hence the directives starting with ``warn.`` above do not affect them
  and they will not trigger a failure when "error on warnings" is enabled.


.. _how_to_set_directives:

How to set directives
---------------------

Globally
:::::::::

One can set compiler directives through a special header comment near the top of the file, like this::

    # cython: language_level=3, boundscheck=False

The comment must appear before any code (but can appear after other
comments or whitespace).

One can also pass a directive on the command line by using the -X switch:

.. code-block:: bash

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

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        name="My hello app",
        ext_modules=cythonize('hello.pyx', compiler_directives={'embedsignature': True}),
    )

This will override the default directives as specified in the ``compiler_directives`` dictionary.
Note that explicit per-file or local directives as explained above take precedence over the
values passed to ``cythonize``.

C macro defines
===============

Cython has a number of C macros that can be used to control compilation. Typically, these
would be set using ``extra_compile_args`` in `setup.py` (for example
``extra_compile_args=['-DCYTHON_USE_TYPE_SPECS=1']``), however they can also be set in
other ways like using the ``CFLAGS`` environmental variable.

These macros are set automatically by Cython to sensible default values unless
you chose to explicitly override them, so they are a tool that most users
can happily ignore.  Not all combinations of macros are compatible or tested, and
some change the default value of other macros.  They are listed below in rough order from
most important to least important:

``CYTHON_LIMITED_API``
    Turns on Cython's experimental Limited API support, meaning that one compiled module
    can be used by many Python interpreter versions (at the cost of some performance).
    At this stage many features do not work in the Limited API.  If you use this macro
    you should also set the macro ``Py_LIMITED_API`` to be the version hex for the
    minimum Python version you want to support (>=3.7).  ``0x03070000`` will support
    Python 3.7 upwards.

``CYTHON_PEP489_MULTI_PHASE_INIT``
    Uses multi-phase module initialization as described in PEP489.  This improves
    Python compatibility, especially when running the initial import of the code when it
    makes attributes such as ``__file__`` available.  It is therefore on by default
    where supported.

``CYTHON_USE_MODULE_STATE``
    Stores module data on a struct associated with the module object rather than as
    C global variables.  The advantage is that it should be possible to import the
    same module more than once (e.g. in different sub-interpreters).  At the moment
    this is experimental and not all data has been moved.  It also requires that
    ``CYTHON_PEP489_MULTI_PHASE_INIT`` is off - we plan to remove this limitation
    in the future.

``CYTHON_USE_TYPE_SPECS``
    Defines ``cdef classes`` as `"heap types" <https://docs.python.org/3/c-api/typeobj.html#heap-types>`_
    rather than "static types".  Practically this does not change a lot from a user
    point of view, but it is needed to implement Limited API support.
    
``CYTHON_EXTERN_C``
    Slightly different to the other macros, this controls how ``cdef public``
    functions appear to C++ code. See :ref:`CYTHON_EXTERN_C` for full details.
    
There is a further list of macros which turn off various optimizations or language
features.  Under normal circumstance Cython enables these automatically based on the
version of Python you are compiling for so there is no need to use them
to try to enable extra optimizations - all supported optimizations are enabled by
default.  These are mostly relevant if you're tying to get Cython working in a
new and unsupported Python interpreter where you will typically want to set
them to 0 to *disable* optimizations.  They are listed below for completeness but
hidden by default since most users will be uninterested in changing them.

.. tabs::
    .. tab:: Hide
    
    .. tab:: Show
        
        ``CYTHON_USE_TYPE_SLOTS``
            If enabled, Cython will directly access members of the ``PyTypeObject``
            struct.
            
        ``CYTHON_USE_PYTYPE_LOOKUP``
            Use the internal `_PyType_Lookup()` function for more efficient access
            to properties of C classes.
            
        ``CYTHON_USE_ASYNC_SLOTS``
            Support the ``tp_as_async`` attribute on type objects.
            
        ``CYTHON_USE_PYLONG_INTERNALS``/``CYTHON_USE_PYLIST_INTERNALS``/``CYTHON_USE_UNICODE_INTERNALS``
            Enable optimizations based on direct access into the internals of Python
            ``int``/``list``/``unicode`` objects respectively.
            
        ``CYTHON_USE_UNICODE_WRITER``
            Use a faster (but internal) mechanism for building unicode strings, for
            example in f-strings.
            
        ``CYTHON_AVOID_BORROWED_REFS``
            Avoid using "borrowed references" and ensure that Cython always holds
            a reference to objects it manipulates.  Most useful for
            non-reference-counted implementations of Python, like PyPy
            (where it is enabled by default).
            
        ``CYTHON_ASSUME_SAFE_MACROS``
            Use some C-API macros that increase performance by skipping error checking,
            which may not be safe on all Python implementations (e.g. PyPy).
            
        ``CYTHON_FAST_GIL``
            On some Python versions this speeds up getting/releasing the GIL.
            
        ``CYTHON_UNPACK_METHODS``
            Try to speed up method calls at the cost of code-size.  Linked to
            the ``optimize.unpack_method_calls`` compiler directive - this macro
            is used to selectively enable the compiler directive only on versions
            of Python that support it.
            
        ``CYTHON_METH_FASTCALL``/``CYTHON_FAST_PYCALL``
            These are used internally to incrementally enable the vectorcall calling
            mechanism on older Python versions (<3.8).
            
        ``CYTHON_PEP487_INIT_SUBCLASS``
            Enable `PEP-487 <https://peps.python.org/pep-0487/>`_ ``__init_subclass__`` behaviour.
            
        ``CYTHON_USE_TP_FINALIZE``
            Use the ``tp_finalize`` type-slot instead of ``tp_dealloc``,
            as described in `PEP-442 <https://peps.python.org/pep-0442/>`_.
            
        ``CYTHON_USE_DICT_VERSIONS``
            Try to optimize attribute lookup by using versioned dictionaries
            where supported.
            
        ``CYTHON_USE_EXC_INFO_STACK``
            Use an internal structure to track exception state,
            used in CPython 3.7 and later.
            
        ``CYTHON_UPDATE_DESCRIPTOR_DOC``
            Attempt to provide docstrings also for special (double underscore) methods.
