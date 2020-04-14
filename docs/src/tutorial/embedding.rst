.. highlight:: cython

.. _embedding:

**********************************************
Embedding Cython modules in C/C++ applications
**********************************************

This is a stub documentation page. PRs welcome.

* `CPython docs <https://docs.python.org/3/extending/embedding.html>`_

* `Cython Wiki <https://github.com/cython/cython/wiki/EmbeddingCython>`_

* See the ``--embed`` option to the ``cython`` and ``cythonize`` frontends
  for generating a C main function and the
  `cython_freeze <https://github.com/cython/cython/blob/master/bin/cython_freeze>`_
  script for merging multiple extension modules into one library.

* `Embedding demo program <https://github.com/cython/cython/tree/master/Demos/embed>`_

* The `PyImport_AppendInittab() <https://docs.python.org/3/c-api/import.html#c.PyImport_AppendInittab>`_
  function in CPython allows registering statically (or dynamically) linked extension modules
  for later imports.

* Also see the documentation of the
  `module init function <https://docs.python.org/3/extending/extending.html#the-module-s-method-table-and-initialization-function>`_
  in CPython and `PEP 489 <https://www.python.org/dev/peps/pep-0489/>`_ regarding the module
  initialisation mechanism in CPython 3.5 and later.
