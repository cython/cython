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

The `PyImport_AppendInittab() <https://docs.python.org/3/c-api/import.html#c.PyImport_AppendInittab>`_
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
