Building Cython code
====================

Cython code must, unlike Python, be compiled. This happens in two stages:

 - A ``.pyx`` file is compiled by Cython to a ``.c`` file, containing
   the code of a Python extension module
 - The ``.c`` file is compiled by a C compiler to
   a ``.so`` file (or ``.pyd`` on Windows) which can be
   ``import``-ed directly into a Python session.

There are several ways to build Cython code:

 - Write a distutils ``setup.py``. This is the normal and recommended way.
 - Use ``pyximport``, importing Cython ``.pyx`` files as if they
   were ``.py`` files (using distutils to compile and build in the background).
 - Run the ``cython`` command-line utility manually to produce the ``.c`` file
   from the ``.pyx`` file, then manually compiling the ``.c`` file into a shared
   object library or DLL suitable for import from Python.
   (These manual steps are mostly for debugging and experimentation.)
 - Use the [Jupyter]_ notebook or the [Sage]_ notebook,
   both of which allow Cython code inline.

Currently, distutils is the most common way Cython files are built and distributed. The other methods are described in more detail in the :ref:`compilation` section of the reference manual.


Building a Cython module using distutils
----------------------------------------

Imagine a simple "hello world" script in a file ``hello.pyx``::

  def say_hello_to(name):
      print("Hello %s!" % name)

The following could be a corresponding ``setup.py`` script::

  from distutils.core import setup
  from Cython.Build import cythonize

  setup(
    name = 'Hello world app',
    ext_modules = cythonize("hello.pyx"),
  )

To build, run ``python setup.py build_ext --inplace``.  Then simply
start a Python session and do ``from hello import say_hello_to`` and
use the imported function as you see fit.


Using the Jupyter notebook
--------------------------

Cython can be used conveniently and interactively from a web browser
through the Jupyter notebook.  To install Jupyter notebook, e.g. into a virtualenv,
use pip:

.. sourcecode:: bash

    (venv)$ pip install jupyter
    (venv)$ jupyter notebook

To enable support for Cython compilation, install Cython and load the
``Cython`` extension from within the Jupyter notebook::

    %load_ext Cython

Then, prefix a cell with the ``%%cython`` marker to compile it::

    %%cython

    cdef int a = 0
    for i in range(10):
        a += i
    print(a)

You can show Cython's code analysis by passing the ``--annotate`` option::

    %%cython --annotate
    ...

.. figure:: jupyter.png

Additional allowable arguments to the Cython magic are:

-a, --annotate
  Produce a colorized HTML version of the source.

--cplus, -+
  Output a C++ rather than C file

-f, --force
  Force the compilation of a new module, even if the source has been previously compiled.

-3
  Select Python 3 syntax

-2
  Select Python 2 syntax

-c=COMPILE_ARGS, --compile-args=COMPILE_ARGS
  Extra flags to pass to compiler via the extra_compile_args.

--link-args LINK_ARGS
 Extra flags to pass to linker via the extra_link_args.

-l LIB, --lib LIB
 Add a library to link the extension against (can be specified multiple times).

-L dir	
  Add a path to the list of libary directories (can be specified multiple times).

-I INCLUDE, --include INCLUDE
 Add a path to the list of include directories (can be specified multiple times).

-S, --src
  Add a path to the list of src files (can be specified multiple times).

-n NAME, --name NAME
  Specify a name for the Cython module.

--pgo
  Enable profile guided optimisation in the C compiler. Compiles the cell twice and executes it in between to generate a runtime profile.

--verbose
  Print debug information like generated .c/.cpp file location and exact gcc/g++ command invoked.

Using the Sage notebook
-----------------------

.. figure:: sage.png

  For users of the Sage math distribution, the Sage notebook allows
  transparently editing and compiling Cython code simply by typing
  ``%cython`` at the top of a cell and evaluate it.  Variables and
  functions defined in a Cython cell imported into the running session.


.. [Jupyter] http://jupyter.org/
.. [Sage] W. Stein et al., Sage Mathematics Software, http://sagemath.org
