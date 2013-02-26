.. highlight:: cython

.. _compilation-reference:

=============
Compilation
=============

Cython code, unlike Python, must be compiled.  This happens in two stages:

  * A ``.pyx`` file is compiles by Cython to a ``.c`` file.

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

How to set directives
---------------------

Globally
:::::::::

One can set compiler directives through a special header comment at the top of the file, like this::

    #!python
    #cython: boundscheck=False

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
    	with cython.boundscheck(True): # turn it temporarily on again for this block
            ...

.. Warning:: These two methods of setting directives are **not**
    affected by overriding the directive on the command-line using the
    -X option.
