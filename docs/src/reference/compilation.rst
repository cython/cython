.. highlight:: cython

.. _compilation-reference:

=============
Compilation
=============

Cython code, unlike Python, must be compiled.  This happens in two stages:

  * A ``.pyx`` file is compiled by Cython to a ``.c`` file.

  * The ``.c`` file is compiled by a C compiler to a ``.so`` file (or a
    ``.pyd`` file on Windows)


The following sub-sections describe several ways to build your
extension modules, and how to pass directives to the Cython compiler.

Compiling from the command line
===============================

Run the Cython compiler command with your options and list of ``.pyx``
files to generate.  For example::

    $ cython -a yourmod.pyx

This creates a ``yourmod.c`` file, and the -a switch produces a
generated html file.  Pass the ``-h`` flag for a complete list of
supported flags.

Compiling your ``.c`` files will vary depending on your operating
system.  Python documentation for writing extension modules should
have some details for your system.  Here we give an example on a Linux
system::

    $ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
          -I/usr/include/python2.5 -o yourmod.so yourmod.c

[``gcc`` will need to have paths to your included header files and
paths to libraries you need to link with]

A ``yourmod.so`` file is now in the same directory and your module,
``yourmod``, is available for you to import as you normally would.


Compiling with ``distutils``
============================

First, make sure that ``distutils`` package is installed in your
system.  It normally comes as part of the standard library.
The following assumes a Cython file to be compiled called
*hello.pyx*.  Now, create a ``setup.py`` script::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        name = "My hello app",
        ext_modules = cythonize('hello.pyx'), # accepts a glob pattern
    )

Run the command ``python setup.py build_ext --inplace`` in your
system's command shell and you are done.  Import your new extension
module into your python shell or script as normal.

The ``cythonize`` command also allows for multi-threaded compilation and
dependency resolution.  Recompilation will be skipped if the target file
is up to date with its main source file and dependencies.


Configuring the C-Build
------------------------

If you have include files in non-standard places you can pass an
``include_path`` parameter to ``cythonize``::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        name = "My hello app",
        ext_modules = cythonize("src/*.pyx", include_path = [...]),
    )

Often, Python packages that offer a C-level API provide a way to find
the necessary include files, e.g. for NumPy::

    include_path = [numpy.get_include()]

If you need to specify compiler options, libraries to link with or other
linker options you will need to create ``Extension`` instances manually
(note that glob syntax can still be used to specify multiple extensions
in one line)::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Build import cythonize

    extensions = [
        Extension("primes", ["primes.pyx"],
            include_dirs = [...],
            libraries = [...],
            library_dirs = [...]),
        # Everything but primes.pyx is included here.
        Extension("*", ["*.pyx"],
            include_dirs = [...],
            libraries = [...],
            library_dirs = [...]),
    ]
    setup(
        name = "My hello app",
        ext_modules = cythonize(extensions),
    )

If your options are static (for example you do not need to call a tool like
``pkg-config`` to determine them) you can also provide them directly in your
.pyx source file using a special comment block at the start of the file::

    # distutils: libraries = spam eggs
    # distutils: include_dirs = /opt/food/include

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
        ext_modules = cythonize(extensions)
    )

The :class:`Extension` class takes many options, and a fuller explanation can
be found in the `distutils documentation`_. Some useful options to know about
are ``include_dirs``, ``libraries``, and ``library_dirs`` which specify where
to find the ``.h`` and library files when linking to external libraries.

.. _distutils documentation: http://docs.python.org/extending/building.html


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


Compiling with ``pyximport``
=============================

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

Compiling with Sage
===================

The Sage notebook allows transparently editing and compiling Cython
code simply by typing ``%cython`` at the top of a cell and evaluate
it. Variables and functions defined in a Cython cell are imported into the
running session.  Please check `Sage documentation
<http://www.sagemath.org/doc/>`_ for details.

You can tailor the behavior of the Cython compiler by specifying the
directives below.

Compiler directives
====================

Compiler directives are instructions which affect the behavior of
Cython code.  Here is the list of currently supported directives:

``boundscheck``  (True / False)
    If set to False, Cython is free to assume that indexing operations
    ([]-operator) in the code will not cause any IndexErrors to be
    raised. Lists, tuples, and strings are affected only if the index
    can be determined to be non-negative (or if ``wraparound`` is False). 
    Conditions
    which would normally trigger an IndexError may instead cause
    segfaults or data corruption if this is set to False.
    Default is True.

``wraparound``  (True / False)
    In Python arrays can be indexed relative to the end. For example
    A[-1] indexes the last value of a list. In C negative indexing is
    not supported. If set to False, Cython will neither check for nor
    correctly handle negative indices, possibly causing segfaults or
    data corruption.
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
    `CEP 516 <http://wiki.cython.org/enhancements/division>`_.  Default
    is False.

``cdivision_warnings`` (True / False)
    If set to True, Cython will emit a runtime warning whenever
    division is performed with negative operands.  See `CEP 516
    <http://wiki.cython.org/enhancements/division>`_.  Default is
    False.

``always_allow_keywords`` (True / False)
    Avoid the ``METH_NOARGS`` and ``METH_O`` when constructing
    functions/methods which take zero or one arguments. Has no effect
    on special methods and functions with more than one argument. The
    ``METH_NOARGS`` and ``METH_O`` signatures provide faster
    calling conventions but disallow the use of keywords.

``profile`` (True / False)
    Add hooks for Python profilers into the compiled C code.  Default
    is False.

``linetrace`` (True / False)
    Add line tracing hooks for Python profilers into the compiled C code.
    This also enables profiling.  Default is False.  Note that the
    generated module will not actually use line tracing, unless you
    additionally pass the C macro definition ``CYTHON_TRACE=1`` to the
    C compiler (e.g. using the distutils option ``define_macros``).

    Note that this feature is currently EXPERIMENTAL.  It will slow down
    your code, may not work at all for what you want to do with it, and
    may even crash arbitrarily.

``infer_types`` (True / False)
    Infer types of untyped variables in function bodies. Default is
    None, indicating that on safe (semantically-unchanging) inferences
    are allowed.

``language_level`` (2/3)
    Globally set the Python language level to be used for module
    compilation.  Default is compatibility with Python 2.  To enable
    Python 3 source code semantics, set this to 3 at the start of a
    module or pass the "-3" command line option to the compiler.
    Note that cimported and included source files inherit this
    setting from the module being compiled, unless they explicitly
    set their own language level.

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


How to set directives
---------------------

Globally
:::::::::

One can set compiler directives through a special header comment at the top of the file, like this::

    #!python
    #cython: language_level=3, boundscheck=False

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
