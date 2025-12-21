.. _FAQ:

FAQ
+++

.. note::
  This page has been migrated from the wiki on github and is in the process of
  being updated; please open an issue or a PR if you find something to improve.

Basics
======

Do I need to rename my ``.py`` file to ``.pyx``?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: No. Cython can compile both .py and .pyx files. The difference is that the extended Cython syntax (``cdef …``) is only available in Cython .pyx files and not in Python .py files.

But you can use Cython's :ref:`pure Python mode <pure-mode>` to provide type declarations for the compilation, including Python's PEP-484 syntax for type hints.

For cases where no interaction with external C libraries is required, this is also the recommended way to type your code, since sticking to .py files with regular Python syntax keeps the whole range of debugging, linting, formatting, profiling etc. tools for Python code available for your software development needs, which usually cannot handle the syntax of .pyx files.

----------

Can Cython generate C code for classes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: A plain class becomes a fully-fledged Python class.
Cython can also generate C classes, where the class data is stored in an
efficient C structure at the cost of some additional limitations.

----------

Can I call my Python code from C?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Yes, easily. Follow the example in `Demos/callback/ <https://github.com/cython/cython/tree/master/Demos/callback>`_ in the Cython source distribution.

----------

How do I interface numpy arrays using Cython?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Follow the :ref:`example <numpy_tutorial>`.

----------

How do I compile Cython with subpackages?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: It's highly recommended to arrange Cython modules in exactly the
same Python package structure as the Python parts of the code base. As long as
you don't keep your Cython code in unusual places, everything should just work.

This is in part due to the fact that fully qualified names are resolved at
compile time, and moving ``.so`` files around or adding ``__init__`` files
between the Cython compile and the Python runtime invocation means that
cimports and imports may resolve differently. Failure to do this may result in
errors like .pxd files not found or ``'module' object has no attribute
'__pyx_capi__'``.

----------

How do I speed up the C compilation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Especially with large modules, the code that Cython generates can
take the C compiler quite some time to optimise. This is usually ok for
production builds, but during development, this can get in the way.

It can substantially speed up the C compiler runs to disable the code
optimisation, e.g. by setting the environment variable ``CFLAGS="-O0 -ggdb"``
on Linux or MacOS, which also enables full debugging symbols for better crash
reports and debugger usage.  For MSVC on Windows, you can pass the option
``/Od`` to disable all optimisations.

----------

How do I reduce the size of the binary modules?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: The Python distutils build often includes debugging symbols in the
extension modules.  The default for gcc is ``-g2``, for example. Disabling them
(``CFLAGS=-g0`` for gcc), or setting them to the bare minimum that is required
to produce stack traces on crashes (``CFLAGS=-g1`` for gcc), can visibly reduce
the size of the binaries.

Here are some more things to try:

* If you don't need pickle support for your cdef classes, memoryviews or functions,
  consider disabling auto-pickle support with a directive::

    # cython: auto_pickle=False

    # you can still enable or disable it locally for single class:
    @cython.auto_pickle(True)
    @cclass
    class MyClass:
        ...

* If you do not need C line information in exception stack traces (i.e. Python/Cython
  lines are enough, as for normal Python code), you can disable this feature with the
  C macro ``CYTHON_CLINE_IN_TRACEBACK``:

    ``-DCYTHON_CLINE_IN_TRACEBACK=0``

  In Cython versions before 3.1, you also had to pass the option ``--no-c-in-traceback``
  or set the option ``c_line_in_traceback=False`` to get the reduction in size.

* If you do not need Cython implemented functions to look and behave like Python
  functions when it comes to introspection (argument names, annotations, etc.),
  you can turn off the ``binding`` directive, either globally, or locally for classes
  or specific functions.  This will make Cython use the normal CPython implementation
  for natively implemented functions, which does not expose such functionality.

* If you do not need to expose the docstrings of Python functions and classes,
  you can exclude them from the extension module with the option
  :data:`Cython.Compiler.Options.docstrings`.

* If you use memoryviews in multiple modules, you can generate and use a shared utility module.
  This approach will allow you to have one single utility code shared between all cython modules
  instead of having them replicated in every module. See :ref:`shared_module` for more detail.

----------

How well is Unicode supported?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: The support for Unicode is as good as CPython's, but additionally
distinguishes between  the Python ``str`` (``bytes`` in Python 2.7) and
``unicode`` (always Unicode text) string type. Note that there is no equivalent
C type available for Unicode strings, but Cython can automatically convert
(encode/decode) from and to encoded C/C++ strings (``char*`` /
``std::string``).

See the :ref:`string tutorial <string_tutorial>`.


How do I ...?
=============

How do I pickle cdef classes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: See :ref:`the documentation <auto_pickle>`.

----------

How do I help Cython find numpy header files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: If you are seeing errors like these:

::

     error: numpy/arrayobject.h: No such file or directory
     error: numpy/ufuncobject.h: No such file or directory

You should modify your setup.py file to grab the numpy include directory as follows:

::

    import numpy
    ...
    setup(
        ...
        ext_modules = [Extension(..., include_dirs=[numpy.get_include()])]
    )

----------

How do I declare numeric or integer C types?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: In most cases, you don't need to. For types declared in
``stdint.h``, just ``cimport`` them from ``libc.stdint`` which comes with
Cython, e.g.

::

    from libc.stdint cimport uint32_t, int64_t
    cdef int64_t i = 5

For non-standard types, it's enough to provide Cython with a ``ctypedef`` declaration that maps them to a closely related standard C type, e.g.

::

    cdef extern from "someheader.h":
        ctypedef unsigned long MySpecialCInt_t

    cdef MySpecialCInt_t i

Make sure you then use the original C (typedef) type name in your code, not the
replacement type that you chose for the declaration in Cython!

The exact size of the type at C compile time is not that important because
Cython generates automatic size detection code (evaluated at C compile time).
However, when your code mixes different types in arithmetic code, Cython must
know about the correct signedness and the approximate longness in order to
infer the appropriate result type of an expression. Therefore, when using a
``ctypedef`` as above, try to come up with a good approximation of the expected
C type. Since the largest type wins in mixed arithmetic expressions, it's
usually not a problem if the type turns out to be somewhat larger than what the
C compiler eventually determines for a given platform. In the worst case, if
your replacement type is substantially larger than the real C type (say, 'long
long' instead of 'int'), you may end up with slightly slower conversion code.
However, if the type is declared too small and Cython considers it smaller than
other types it is used together with, Cython may infer the wrong type for an
expression and may end up generating incorrect coercion code. You may or may
not get a warning by the C compiler in this case.

Also note that Cython will consider large integer literals (>32 bit signed)
unsafe to use in C code and may therefore use Python objects to represent them.
You can make sure a large literal is considered a safe C literal by appending a
C suffix, such as 'LL' or 'UL'. Note that a single 'L' is not considered a C
suffix in Python 2 code.

----------

How do I declare an object of type bool?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Well, that depends on whether you want the C99/C++ ``bool`` or the
Python ``bool``. Previously, Cython always defaulted to the Python ``bool``
type, which led to hard-to-debug issues when users unsuspectingly used ``bool``
in wrapping C++ code. We decided to make the choice explicit -- you can import
whichever you'd like:

 * For the Python type, do ``from cpython cimport bool``.
 * For the C++ type, do ``from libcpp cimport bool``.

Note that there is also a type called ``bint``, which is essentially a C
``int`` but automatically coerces from and to a Python bool value, i.e. ``cdef
object x = <bint>some_c_integer_value`` gives either ``True`` or ``False``.

----------

How do I use ``const``?
^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: You can just use it in your code and in your declarations.

----------

How do I use builtins like ``len()`` with the C type ``char *``?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Cython maps ``len(char*)`` directly to ``strlen()``, which means
that it will count the number of characters up to the first 0 byte. Similarly,
``(char*).decode(...)`` is optimised into a C-API call, and applying it to
sliced ``char*`` values will skip the length counting step.

See the :ref:`string tutorial <string_tutorial>`.

For other Python operations on ``char*``, the generated code may be
inefficient, as a temporary object may have to get created. If you notice this
for your code and think that Cython can do better, please speak up on the
mailing list.

----------

How do I make a cdef'd class that derives from a builtin Python type such as list?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: You can just use the type as a base class in your cdef class declaration.

The only exception are the types bytes ('str' in Python 2) and tuple, which can
only be subtyped by Python classes (not cdef classes). This is considered a
`bug <https://github.com/cython/cython/issues/711>`_. However, you can
safely subtype 'unicode' and 'list' instead.

----------

How do I raise an exception in Cython code that will be visible to ancestor (in the callstack) CPython code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**:

If your cdef or cpdef function or method does not declare a return type (as is
normal in CPython code), then you get exceptions without any extra effort.

If your cdef or cpdef function or method declares a C-style return type, see
:ref:`error_return_values`.

----------

How do I declare a global variable?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**:

::

    global variable

----------

How do I assign to a global variable?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: You need to declare the variable to be global (see above) before
trying to assign to it. Often this occurs when one has code like

::

    cdef int *data

    def foo(n):
        data = malloc(n * sizeof(int))

This will result in an error "Cannot convert ``'int *'`` to Python object."
This is because, as in Python, assignment declares a local variable. Instead,
you must write

::

    cdef int *data

    def foo(n):
        global data
        data = malloc(n * sizeof(int))

See http://docs.python.org/tutorial/classes.html#python-scopes-and-namespaces
for more details.

----------

How do I create objects or apply operators to locally created objects as pure C code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: For methods like ``__init__`` and ``__getitem__`` the Python
calling convention is mandatory and identical for all objects, so Cython cannot
provide a major speed-up for them.

To instantiate an extension type, however, the fastest way is to actually use
the normal Python idiom of calling the ``__new__()`` method of a type:

.. code:: python

    cdef class ExampleClass:
        cdef int _value
        def __init__(self):
            # calling "__new__()" will not call "__init__()" !
            raise TypeError("This class cannot be instantiated from Python")

    cdef ExampleClass _factory():
        cdef ExampleClass instance = ExampleClass.__new__(ExampleClass)
        instance._value = 1
        return instance

Note that this has similar restrictions as the normal Python code: it will not
call the ``__init__()`` method (which makes it quite a bit faster). Also, while
all Python class members will be initialised to None, you have to take care to
initialise the C members. Either the ``__cinit__()`` method or a factory
function like the one above are good places to do so.

How do I implement a single class method in a Cython module?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: As of Cython 3.0, Cython-defined methods bind by default.
That means that the following should work:

::

    #!python
    import cython_module

    class A(object):
        method = cython_module.optimized_method

----------

How do I pass string buffers that may contain 0 bytes to Cython?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: See the :ref:`string tutorial <string_tutorial>`.

You need to use either a Python byte string object or a char*/length pair of
variables.

The normal way to convert a char* to a Python byte string is as follows:

.. code:: python

    #!python
    cdef char* s = "a normal C byte string"
    cdef bytes a_python_byte_string = s

However, this will not work for C strings that contain 0 bytes, as a 0 byte is
the normal C way of terminating a string. So the above method will cut the
string at the first 0 byte. To handle this case correctly, you have to specify
the total length of the string that you want to convert:

.. code:: python

    cdef char* s = "an unusual \0 containing C byte string"
    a_python_byte_string = s[:21]    #  take the first 21 bytes of the string, including the \0 byte

Note that this will not handle the case that the specified slice length is
longer than the actual C string. This code will crash if the allocated memory
area of the ``char*`` is shorter.

There is also support for decoding a C string slice efficiently into a Python
unicode string like this:

.. code:: python

    # -*- coding: ISO8859-15
    cdef char* s = "a UTF-8 encoded C string with fünny chäräctörs"
    cdef Py_ssize_t byte_length = 46

    a_python_unicode_string = s[:byte_length].decode('ISO8859-15')

----------

How do I pass a Python string parameter on to a C library?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `string tutorial <string_tutorial>`.

**Answer**: It depends on the semantics of the string. Imagine you have this C function:

::

    cdef extern from "something.h":
        cdef int c_handle_data(char* data, int length)

For **binary data**, you can simply require byte strings at the API level, so
that this will work:

::

    def work_with_binary_data(bytes binary_data):
        c_handle_data(binary_data, len(binary_data))

It will raise an error (with a message that may or may not be appropriate for
your use case) if users pass other things than a byte string.

For **textual data**, however, you must handle Unicode data input. What you do
with it depends on what your C function accepts. For example, if it requires
UTF-8 encoded byte sequences, this might work:

::

    def work_with_text_data(text):
        if not isinstance(text, unicode):
            raise ValueError("requires text input, got %s" % type(text))
        utf8_data = text.encode('UTF-8')
        c_handle_data( utf8_data, len(utf8_data) )

Note that this also accepts subtypes of the Python unicode type. Typing the
"text" parameter as "unicode" will not cover this case.

----------

How do I use variable args?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: For a regular function, just use ``*args`` as in Python.

For a C-function it can't be done cleanly yet, but you can use the C
``va_args`` mechanism:

::

    cdef extern from "stdarg.h":
        ctypedef struct va_list:
            pass
        ctypedef struct fake_type:
            pass
        void va_start(va_list, void* arg)
        void* va_arg(va_list, fake_type)
        void va_end(va_list)
        fake_type int_type "int"

    cdef int foo(int n, ...):
        print "starting"
        cdef va_list args
        va_start(args, <void*>n)
        while n != 0:
            print n
            n = <int>va_arg(args, int_type)
        va_end(args)
        print "done"

    def call_foo():
        foo(1, 2, 3, 0)
        foo(1, 2, 0)

----------

How do I make a standalone binary from a Python program using cython?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: You probably want a recipe something like this:

.. highlight::bash

    PYVERSION=3.9
    cython --embed foobar.py -o foobar.c
    $(CC) -I /usr/include/python$(PYVERSION) foobar.c -lpython$(PYVERSION) -o foobar

The magic is the ``--embed`` option, which embeds a copy of the Python interpreter
main in the generated C.  You'll want to change ``'foobar'`` to reflect the name of
your script, of course, and ``PYVERSION`` as appropriate.

More details can be found :ref:`in the embedding documentation <embedding>`.

----------

How do I have to wrap C code that uses the restrict qualifier?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: There currently is no way of doing this directly into C code. Cython does not understand the restrict qualifier. However you can wrap your way around it.

See the following example code:

slurp.h
-------

::

    #include <sys/types.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <regex.h>
    #include <Python.h>

    int th_match(char *, char *);

cslurp.c
--------

::

    #include "slurp.h"

    int th_match(char *string, char *pattern) {
      int status;
      regex_t re;
      if(regcomp(&re, pattern, REG_EXTENDED|REG_NOSUB) != 0) { return 0; }
      status = regexec(&re, string, (size_t)0, NULL, 0);
      regfree(&re);
      if(status != 0)
        return 0;
      return 1;
    }

slurp.pyx
---------

::

    cdef extern from "slurp.h":
        int th_match(char *st, char *pt)

    class Slurp:
        '''
        This is a simple, but optimized PEG (Parser Expression Group) parser.
        It will parse through anything you hand it provided what you hand it
        has a readline() method.

        Example:
            import sys
            from thci.ext import slurp
            o = slurp.Slurp()
            o.register_trigger('^root:.*:.*:.*:.*$', sys.stdout.write)
            o.process(open('/etc/passwd', 'r'))
        '''

        def __init__(self):
            ''' __init__(self) '''
            self.map = {}
            self.idx = 0

        def register_trigger(self, patt=None, cback=None, args=None):
            ''' register_trigger(self, patt=None, cback=None, args=None) '''
            if patt == None or cback == None:
                return False
            if args == None: args = False
            self.map[self.idx] = (patt, cback, args)
            self.idx += 0
            return True

        def process(self, fp=None):
            ''' process(self, fp=None) '''
            if fp == None:
                return False
            while True:
                buf = fp.readline()
                if not buf: break
                for patt, cback, args in self.map.values():
                    if th_match(buf, patt) == True:
                        if args == False:
                            cback(buf.strip())
                        else:
                            cback(buf.strip(), args)

This avoids the problems using the restrict qualifiers (Such as are needed with
the functions declared in regex.h on FreeBSD [at least 7.X]) by allowing the C
compiler to handle things going from C to C, Cython's support for this even
using the "const trick" doesn't seem to behave properly (at least as of 0.12).
the following commands will generate your compiled module from the above
source:

::

    cython -o slurp.c slurp.pyx
    cc -shared -I/usr/include -I./ -I/usr/local/include/python2.5 -L/usr/local/lib -lpthread -lpython2.5 cslurp.c slurp.c -o slurp.so

It is also possible to use distutils by adding the file cslurp.c (or your files
name) to the list of files to be compiled for the extension.

----------

How do I automatically generate Cython definition files from C (.h) or C++ (.hpp) header files ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Several people have created scripts to parse header files and
automatically produce Cython bindings.

**autowrap**

autowrap automatically generates python extension modules for wrapping C++
libraries based on annotated (commented) cython pxd files. Current features
include wrapping of template classes, enums, free functions and static methods
as well as converters from Python data types to (many) STL containers and back.
Finally, also manually written Cython code can be incorporated for wrapping
code.

http://github.com/uweschmitt/autowrap

**python-autopxd**

Automatically generate pxd from C headers. It uses
[pycparser](https://github.com/eliben/pycparser) to parse the definitions, so
the only requirement beyond python dependencies is a C preprocessor on PATH.

https://github.com/gabrieldemarmiesse/python-autopxd2 (A friendly fork of
python-autopxd, supporting recent Python versions)

https://github.com/tarruda/python-autopxd (original version)

----------

How do I run doctests in Cython code (pyx files)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**:

Cython generates a ``__test__`` dictionary in the module that contains all
docstrings of Python visible functions and classes that look like doctests
(i.e. that contain ``>>>``). The doctest module will properly pick this up and
run the doctests.

This module (let's call it "cydoctest") offers a Cython-compatible workaround.

::

    #!python
    """
    Cython-compatible wrapper for doctest.testmod().

    Usage example, assuming a Cython module mymod.pyx is compiled.
    This is run from the command line, passing a command to Python:
    python -c "import cydoctest, mymod; cydoctest.testmod(mymod)"

    (This still won't let a Cython module run its own doctests
    when called with "python mymod.py", but it's pretty close.
    Further options can be passed to testmod() as desired, e.g.
    verbose=True.)
    """

    import doctest
    import inspect

    def _from_module(module, object):
        """
        Return true if the given object is defined in the given module.
        """
        if module is None:
            return True
        elif inspect.getmodule(object) is not None:
            return module is inspect.getmodule(object)
        elif inspect.isfunction(object):
            return module.__dict__ is object.func_globals
        elif inspect.isclass(object):
            return module.__name__ == object.__module__
        elif hasattr(object, '__module__'):
            return module.__name__ == object.__module__
        elif isinstance(object, property):
            return True # [XX] no way not be sure.
        else:
            raise ValueError("object must be a class or function")

    def fix_module_doctest(module):
        """
        Extract docstrings from cython functions, that would be skipped by doctest
        otherwise.
        """
        module.__test__ = {}
        for name in dir(module):
           value = getattr(module, name)
           if inspect.isbuiltin(value) and isinstance(value.__doc__, str) and _from_module(module, value):
               module.__test__[name] = value.__doc__

    def testmod(m=None, *args, **kwargs):
        """
        Fix a Cython module's doctests, then call doctest.testmod()

        All other arguments are passed directly to doctest.testmod().
        """
        fix_module_doctest(m)
        doctest.testmod(m, *args, **kwargs)

----------

How do I work around the ``-Wno-long-double error`` when installing on OS X?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**:

This is a known issue in OS X with some Python installs. It has nothing to do
with Cython, and you will run on the same trouble **every** time you want to
build an C extension module.

This is the most sane (if not the only) way to fix it:

1) Enter Python prompt, and type this:

::

    >>> from distutils import sysconfig
    >>> sysconfig.get_makefile_filename()

That should output the full path of a 'Makefile'... Open that file
with any text editor and remove  all occurrences of '-Wno-long-double'
flag.

----------

How do I work around the "unable to find vcvarsall.bat" error when using MinGW as the compiler (on Windows)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: This error means that Python cannot find the C++ compiler on your
system. Normally, this is managed by distutils, but it may happen that it's not
yet up-to-date. For example, you may be using this in setup.py:

::

    from distutils.core import setup
    from distutils.extension import Extension


Instead, you can try to load setuptools, which will monkey-patch distutils to
find vcvarsall.bat:

::

    try:
        from setuptools import setup
        from setuptools import Extension
    except ImportError:
        from distutils.core import setup
       from distutils.extension import Extension


In IPython, you can just import setuptools, like this:

::

    # First cell:
        import setuptools
                %load_ext Cython

    # Second cell:
        %%cython -a
        import cython
        cimport cython

        cdef int alpha = 255
        print alpha

If this is unsuccessful, try the following workarounds.

If no python libraries are imported, define the compiler by adding the
following statement:
::

    --compiler=mingw32

Therefore, the line should read:
::

    python pyprog.py build_ext --compiler=mingw32 --inplace

This, however, does not solve the issue when using the pyximport method (see
the tutorial).  Alternatively, the following patch can be applied.

**NOTE: This is untested.**

Open the file pyximport/pyxbuild.py and add the four lines marked with "+" at
the appropriate place.

.. highlight::diff

    diff -r 7fbe931e5ab7 pyximport/pyxbuild.py
    --- a/pyximport/pyxbuild.py Wed Sep 16 15:50:00 2009 +0200
    +++ b/pyximport/pyxbuild.py Fri Sep 18 12:39:51 2009 -0300
    @@ -55,6 +55,11 @@
    build = dist.get_command_obj('build')
    build.build_base = pyxbuild_dir

    + config_files = dist.find_config_files()
    + try: config_files.remove('setup.cfg')
    + except ValueError: pass
    + dist.parse_config_files(config_files)
    +
    try:
    ok = dist.parse_command_line()
    except DistutilsArgError:

Finally, if this does not work, create a file called "pydistutils.cfg" in
notepad and give it the contents:
::

    [build_ext]
    compiler=mingw32

Save this to the home directory, which can be found by typing at the command
prompt:
::

    import os
    os.path.expanduser('~')

Explanations
============

What is the difference between a ``.pxd`` and ``.pxi`` file? When should either be used?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SHORT **Answer**:  You should always use .pxd files for declarations and .pxi
files only for code that you want to include.

MEDIUM **Answer**:  A .pxd files are lists of declarations, .pxi files are
textually included, and their use for declarations is a historical artifact of
the way common declarations were shared before .pxd files existed.

LONG **Answer**:  A .pxd file is a declaration file, and is used to declare
classes, methods, etc. in a C extension module, (typically as implemented in a
.pyx file of the same name). It can contain declarations only, i.e. no
executable statements. One can ``cimport`` things from .pxd files just as one
would import things in Python. Two separate modules cimporting from the same
.pxd file will receive identical objects.

A .pxi file is an include file and is textually included (similar to the C
``#include`` directive) and may contain any valid Cython code at the given
point in the program. It may contain implementations (e.g. common cdef inline
functions) which will be copied into both files. For example, this means that
if I have a class A declared in a.pxi, and both b.pyx and c.pyx do ``include
a.pxi`` then I will have two distinct classes b.A and c.A. Interfaces to C
libraries (including the Python/C API) have usually been declared in .pxi files
(as they are not associated to a specific module). It is also re-parsed at
every invocation.

Now that ``cimport *`` can be used, there is no reason to use .pxi files for
external declarations.

----------

What is better, a single big module or multiple separate modules?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: In short, one big module is clumsy to handle but allows broader
optimisations by the C compiler.

The compile time might actually decrease for multiple modules since the build
can be parallelised. The "build_ext" command in distutils has a "-j" option
since Py3.5. Also, smaller modules are usually faster to compile by the C
compiler, because some optimisations may involve non-linear overhead.

The distribution size, and the size per module, will probably increase when
splitting a module because there are some things that Cython has to copy into
each module. There is a
`feature request <https://github.com/cython/cython/issues/2356>`_ that would mitigate
this.

C calls between modules are slightly slower than C calls inside of a module,
simply because the C compiler cannot optimise and/or inline them. You will have
to use shared .pxd declarations for them, which will then call through a
function pointer. If modules use a functional split, however, this should not
hurt too much. It might still be a good idea to create a shared .pxd file (or
.pxi) with inline functions for performance critical code that is used in
multiple modules.

When splitting an existing module, you will also have to deal with the API
changes. Leaving some legacy imports here and there, or turning a module into a
package that merges the module namespaces back together via imports, might
prevent code breakage for users of your original module when you move names
around and redistribute them across multiple modules.

----------

What is the difference between ``PyObject*`` and ``object``?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: A variable of type ``PyObject*`` is a simple C pointer, just like
``void*``. It is not reference counted, which is sometimes referred to as a
borrowed reference. An ``object`` variable is an owned reference to a Python
object. You can convert one into the other by casting:

::

    from cpython.ref cimport PyObject

    py_object = [1,2,3]

    cdef PyObject* ptr = <PyObject*>py_object

    cdef object l = <object>ptr    # this increases the reference count to the list

Note that the lifetime of the object is only bound to its owned references, not
to any C pointers that happen to point to it. This means that ``ptr`` in the
example above becomes invalid as soon as the last reference to the object dies:

::

    py_object = [1,2,3]
    cdef PyObject* ptr = <PyObject*>py_object
    py_object = None   # last reference to list dies here

    # ptr now points to a dead object
    print(<object>ptr)   # expect a crash here!

Pointers are commonly used when passing objects through C callbacks, e.g.

::

    cdef int call_it_from_c(void* py_function, void* args):
        py_args = <tuple>args if args is not NULL else ()
        return (<object>py_function)(*py_args)

    def py_func(a,b,c):
        print(a,b,c)
        return -1

    args = [1,2,3]

    call_it_from_c(<PyObject*>py_func, <PyObject*>args)

Once again, care must be taken to keep the objects alive as long as any
pointers to them are still in use.

----------

Why does Cython not always give errors for uninitialized variables?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Cython does some static checks for variable initialization before
use during  compile time, but these are very basic, as Cython has no definite
knowledge  what paths of code will be taken at runtime:

Consider the following

.. code:: python

    def testUnboundedLocal1():
       if False:
          c = 1
       print c
    def testUnboundedLocal2():
       print c

With CPython, both functions lead to the following exception:

::

    NameError: global name 'c' is not defined

With Cython, the first variant prints "None", the second variant leads to a
compile time error. Both behaviours differ from CPython's.

This is considered a BUG and will change in the future.

----------

Why does a function with cdef'd parameters accept None?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: It is a fairly common idiom in Python to use ``None`` as a way to
mean "no value" or "invalid". This doesn't play well with C, as ``None`` is not
compatible with any C type. To accommodate for this, the default behavior is
for functions with cdefed parameters to also accept None. This behavior was
inherited from Pyrex, and while it has been proposed that it be changed, it
will likely stay (at least for a while) for backwards capability.

You have four choices for how to handle ``None`` in your code:

1. In Cython 3.x, use Python type annotations instead of Cython syntax. Python type annotations distinguish between ``func(x: MyType)`` and ``func(x: Optional[MyType])``, where the first **disallows** ``None`` and the second explicitly allows it.  ``func(x: MyType = None)`` allows it as well because it is explicitly required by the provided default value.

2. If you want to consider ``None`` invalid input, then you need to write code that checks for it, and raised an appropriate exception.

3. If you want Cython to raise an exception if ``None`` is passed in for an extension type parameter, you can use the ``not None`` declaration:

   ::

       def foo(MyClass val not None): <...>

   which is a short-hand for

   ::

       def foo(MyClass val):
           if val is None: raise <...>
           <...>

4. You can also put ``#cython: nonecheck=True`` at the top of your file and all access will be checked for None, but it will slow things down, as it is adding a check on every access, rather that once on function call.


About the project
=================

Is Cython a Python implementation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Not officially, no. However, it compiles almost all existing Python
code, which gets it pretty close to a real Python implementation. The result
depends on the CPython runtime, though, which we consider a major compatibility
advantage. In any case, it is an official goal for Cython to compile regular
Python code and run (most of) the normal Python test suite - obviously faster
than CPython. ;-)

----------

Is Cython faster than CPython?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: For most things, yes. For example, a Cython compiled pybench runs
more than 30% faster in total, while being 60-90% faster on control structures
like ``if-elif-else`` and ``for``-loops. We regularly run the tests from the
CPython benchmark suite (which includes Django templates, 2to3, computational
benchmarks and other applications) and most of them work out-of-the-box without
modifications or static typing, with a performance increase of 20-60%.

However the main advantage of Cython is that it scales very well to even
greater performance requirements. For code that operates heavily on common
builtin types (lists, dicts, strings), Cython can often speed up processing
loops by factors. For numerical code, speed-ups of 100-1000 times compared to
CPython are not unusual, and are achieved by simply adding static type
declarations to performance critical parts of the code, thus trading Python's
dynamic typing for speed. As this can be done at any granularity in the code,
Cython makes it easy to write simple Python code that is fast enough, and just
tune the critical 5% of your code into maximum performance by using static C
types in just the right places.

----------

What Python versions does Cython support?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: From Cython 0.21 on, the supported versions are 2.6, 2.7 and 3.4+,
with Python 2.6 being phased out implicitly due to lack of testing
capabilities. Cython 3.0 removes support for Python 2.6 completely and requires
either Python 2.7 or Python 3.4+. Python 2.x support is scheduled for removal
in Cython 3.1, which will probably require Python 3.6 or later at the time of
its release.

The C code generated by Cython is portable and builds in all supported Python
versions. All supported CPython release series are tested regularly. New
CPython versions are usually supported before they are released.

The source code that Cython compiles can use both Python 2 and Python 3 syntax,
defaulting to Python 2 syntax in Cython 0.x and Python 3 syntax in Cython 3.x
and later. When compiling Cython modules (.pyx files) in Python 2 mode, most
Python 3 syntax features are available by default if they do not interfere with
Python 2 syntax (as in Python 2.7), but the general language semantics are
defined as in Python 2. When compiling Python modules (.py files), the special
Cython syntax (such as the ``cdef`` keyword) is not available. For both input
types, the language level can be set to Python 3 by either passing the "-3"
option to the compiler, or by putting

::

    # cython: language_level=3

at the top of the module file (within the first comment and before any code or
empty lines). With Cython 3.x, compiling Python 2 code requires the option "-2"
or the directive ``language_level=2``. By default, with the Python 3 semantics
in Cython 3.0, ``print()`` is a function, loop variables in list comprehensions
do not leak into the outer scope, etc. This is equivalent to
``language_level=3str`` or the option ``--3str``.  If you instead select
``language_level=3``, then, additionally, unprefixed strings are always unicode
strings.

----------

What's the license situation of Cython's output?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: You can use the output of Pyrex/Cython however you like (and
license it how you like - be it BSD, public domain, GPL, all rights reserved,
whatever).

More details: The Python License is different from the GPL used for GCC, for
example. GCC requires a special exception clause for its output as it is
*linked* against the library part of GCC, i.e. against GPL software, which
triggers the GPL restrictions.

Cython doesn't do anything similar, and linking against Python is not
restricted by the Python License, so the output belongs to the User, no other
rights or restrictions involved.

Also, all of the copyright holders of Pyrex/Cython stated in mailing list that
people are allowed to use the output of Pyrex/Cython however they would like.

----------

How do I cite Cython in an academic paper?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: If you mention Cython, the simplest way to reference us is to add
the URL to our website in a footnote. You may also choose to reference our
software project
in a more formal way, such as

::

    R. Bradshaw, S. Behnel, D. S. Seljebotn, G. Ewing, et al., The Cython compiler, http://cython.org.

(the list of author names were taken from setup.py)

For a yet more formal citation, there is a `journal
paper <https://www.computer.org/csdl/magazine/cs/2011/02/mcs2011020031/13rRUx0Pqtw|journal paper>`_ on Cython.
If you wish to cite it, here's the Bibtex:

::

    @ARTICLE{ behnel2010cython,
        author={Behnel, S. and Bradshaw, R. and Citro, C. and Dalcin, L. and Seljebotn, D.S. and Smith, K.},
        journal={Computing in Science Engineering},
        title={Cython: The Best of Both Worlds},
        year={2011},
        month=march-april ,
        volume={13},
        number={2},
        pages={31 -39},
        keywords={Cython language;Fortran code;Python language extension;numerical loops;programming language;C language;numerical analysis;},
        doi={10.1109/MCSE.2010.118},
        ISSN={1521-9615},
    }

----------

What is the relation between Cython and Pyrex?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Answer**: Cython started originally based on a previous project called Pyrex,
developed primarily by Greg Ewing.

Years later, Pyrex development has effectively stopped, whereas Cython has kept
adding new features and support for new Python versions.

As of 2023, Pyrex is only of historical interest.
