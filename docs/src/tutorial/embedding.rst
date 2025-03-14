.. highlight:: cython

.. _embedding:

**********************************************
Embedding Cython modules in C/C++ applications
**********************************************

**This is a stub documentation page. PRs very welcome.**

Quick links:

* `CPython docs <https://docs.python.org/3/extending/embedding.html>`_

* `Cython Wiki <https://github.com/cython/cython/wiki/EmbeddingCython>`_

* See the ``--embed`` option to the ``cython`` and ``cythonize`` frontends
  for generating a C main function and the
  `cython_freeze <https://github.com/cython/cython/blob/master/bin/cython_freeze>`_
  script for merging multiple extension modules into one library.

* `Embedding demo program <https://github.com/cython/cython/tree/master/Demos/embed>`_

* See the documentation of the `module init function
  <https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function>`_
  in CPython and `PEP 489 <https://www.python.org/dev/peps/pep-0489/>`_ regarding the module
  initialisation mechanism in CPython 3.5 and later.


Initialising your main module
=============================

Most importantly, DO NOT call the module init function instead of importing
the module.  This is not the right way to initialise an extension module.
(It was always wrong but used to work before, but since Python 3.5, it is
wrong *and* no longer works.)

For details, see the documentation of the
`module init function <https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function>`_
in CPython and `PEP 489 <https://www.python.org/dev/peps/pep-0489/>`_ regarding the module
initialisation mechanism in CPython 3.5 and later.

The :c:func:`PyImport_AppendInittab()`
function in CPython allows registering statically (or dynamically) linked extension
modules for later imports.  An example is given in the documentation of the module
init function that is linked above.


Embedding example code
======================

The following is a simple example that shows the main steps for embedding a
Cython module (``embedded.pyx``) in Python 3.x.

First, here is a Cython module that exports a C function to be called by external
code.  Note that the ``say_hello_from_python()`` function is declared as ``public``
to export it as a linker symbol that can be used by other C files, which in this
case is ``embedded_main.c``.

.. literalinclude:: ../../examples/tutorial/embedding/embedded.pyx

The C ``main()`` function of your program could look like this:

.. literalinclude:: ../../examples/tutorial/embedding/embedded_main.c
    :linenos:
    :language: c

(Adapted from the `CPython documentation
<https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function>`_.)

Instead of writing such a ``main()`` function yourself, you can also let
Cython generate one into your module's C file with the ``cython --embed``
option.  Or use the
`cython_freeze <https://github.com/cython/cython/blob/master/bin/cython_freeze>`_
script to embed multiple modules.  See the
`embedding demo program <https://github.com/cython/cython/tree/master/Demos/embed>`_
for a complete example setup.

Be aware that your application will not contain any external dependencies that
you use (including Python standard library modules) and so may not be truly portable.
If you want to generate a portable application we recommend using a specialized
tool (e.g. `PyInstaller <https://pyinstaller.org/en/stable/>`_
or `cx_freeze <https://cx-freeze.readthedocs.io/en/latest/index.html>`_) to find and
bundle these dependencies.

Troubleshooting
===============

Here's some of the things that can go wrong when embedding Cython code.

Not initializing the Python interpreter
---------------------------------------

Cython doesn't compile to "pure stand-alone C code". Instead Cython compiles to a bunch of
Python C API calls that depend on the Python interpreter. Therefore, in your main function
you *must* initialize the Python interpreter with ``Py_Initialize()``. You should do this
as early as possible in your ``main()`` function.

Very occasionally you may get away without it, for exceptionally simple programs. This
is pure luck, and you should not rely on it. There is no "safe subset" of Cython that's
designed to run without the interpreter.

The consequence of not initializing the Python interpreter is likely to be crashes.

You should only initialize the interpreter once - a lot of modules, including most Cython
modules and Numpy, don't currently like being imported multiple times. Therefore if you're
doing occasional Python/Cython calculations in a larger program what you *don't do* is::

   void run_calculation() {
        Py_Initialize();
        // Use Python/Cython code
        Py_Finalize();
   }
   
The chances are you will get mystery unexplained crashes.

Not setting the Python path
---------------------------

If your module imports anything (and possibly even if it doesn't) then it'll need
the Python path set so it knows where to look for modules. Unlikely the standalone
interpreter, embedded Python doesn't set this up automatically.

``PySys_SetPath(...)`` is the easiest way of doing this (just after ``Py_Initialize()``
ideally). You could also use ``PySys_GetObject("path")`` and then append to the
list that it returns.

if you forget to do this you will likely see import errors.

Not importing the Cython module
-------------------------------

Cython doesn't create standalone C code - it creates C code that's designed to be
imported as a Cython module. The "import" function sets up a lot of the basic
infrastructure necessary for you code to run. For example, strings are initialized
at import time, and built-ins like ``print`` are found and stashed within your
Cython module.

Therefore, if you decide to skip the initialization and just go straight to
running your public functions you will likely experience crashes (even for
something as simple as using a string).

InitTab
^^^^^^^

The preferred way to set up an extension module so that it's available
for import in modern Python (>=3.5) is to use the
`inittab mechanism <https://docs.python.org/3/c-api/import.html#c._inittab>`_
which is detailed in :ref:`elsewhere in the documentation <inittab_guide>`. This should be done
before ``Py_Initialize()``.

Forcing single-phase
^^^^^^^^^^^^^^^^^^^^

If for some reason you aren't able to add your module to the inittab before
Python is initialized (a common reason is trying to import another Cython
module built into a single shared library) then you can disable
multi-phase initialization by defining ``CYTHON_PEP489_MULTI_PHASE_INIT=0``
for your C compiler (for gcc this would be ``-DCYTHON_PEP489_MULTI_PHASE_INIT=0``
at the command line). If you do this then you can run the module init
function directly (``PyInit_<module_name>`` on Python 3). *This really
isn't the preferred option*.

Working with multi-phase
^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to run the multi-phase initialization manually yourself.
One of the Cython developers has written a
`guide showing how to do this <https://cython-guidelines.readthedocs.io/en/latest/troubleshooting/embedding.html#working-with-multi-phase>`_.
However, he considers it sufficiently hacky that it is only linked here,
and not reproduced directly. It is an option though, if you're unable to
use the inittab mechanism before initializing the interpreter.

Problems with multiprocessing and pickle
----------------------------------------

If you try to use ``multiprocessing`` while using a Cython module embedded into
an executable it will likely fail with errors related to the pickle module.
``multiprocessing`` often uses pickle to serialize and deserialize data to
be run in another interpreter.  What happens depends on the multiprocessing
"start method". However, on the "spawn" start method used on Windows, it starts a 
fresh copy of the **Python** interpreter (rather than a fresh copy of your embedded program)
and then tries to import your Cython module. Since your Cython module is only
available by the inittab mechanism and not be a regular import then that import
fails.

The solution likely involves setting `multiprocessing.set_executable <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_executable>`_ to point to your
embedded program then modifying that program to handle the
``--multiprocessing-fork`` command-line argument that multiprocessing passes
to the Python interpreter.  You may also need to call ``multiprocessing.freeze_support()``.

At the moment that solution is untested so you should treat multiprocessing
from an embedded Cython executable as unsupported.
