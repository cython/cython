Welcome to Cython!
==================

Cython is a Python compiler that makes writing C extensions for
Python as easy as Python itself.  Cython is based on Pyrex,
but supports more cutting edge functionality and optimizations.

Cython translates Python code to C/C++ code, but additionally supports calling
C functions and declaring C types on variables and class attributes.
This allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for wrapping external C libraries, and
for fast C modules that speed up the execution of Python code.

* Official website: https://cython.org/
* Documentation: https://docs.cython.org/
* Github repository: https://github.com/cython/cython
* Wiki: https://github.com/cython/cython/wiki

Cython has `about 30 million downloads <https://pypistats.org/packages/cython>`_
per month on PyPI.  You can **support the Cython project** via
`Github Sponsors <https://github.com/users/scoder/sponsorship>`_ or
`Tidelift <https://tidelift.com/subscription/pkg/pypi-cython>`_.


Installation:
-------------

If you already have a C compiler, just run following command::

   pip install Cython

otherwise, see `the installation page <https://docs.cython.org/en/latest/src/quickstart/install.html>`_.


License:
--------

The original Pyrex program was licensed "free of restrictions" (see below).
Cython itself is licensed under the permissive **Apache License**.

See `LICENSE.txt <https://github.com/cython/cython/blob/master/LICENSE.txt>`_.


Contributing:
-------------

Want to contribute to the Cython project?
Here is some `help to get you started <https://github.com/cython/cython/blob/master/docs/CONTRIBUTING.rst>`_.


Differences to other Python compilers
-------------------------------------

Started as a project in the early 2000s, Cython has outlived
`most other attempts <https://wiki.python.org/moin/PythonImplementations#Compilers>`_
at producing static compilers for the Python language.

Similar projects that have a relevance today include:

* `PyPy <https://www.pypy.org/>`_, a Python implementation with a JIT compiler.

  * Pros: JIT compilation with runtime optimisations, fully language compliant,
    good integration with external C/C++ code
  * Cons: non-CPython runtime, relatively large resource usage of the runtime,
    limited compatibility with CPython extensions, non-obvious performance results

* `Numba <http://numba.pydata.org/>`_, a Python extension that features a
  JIT compiler for a subset of the language, based on the LLVM compiler
  infrastructure (probably best known for its ``clang`` C compiler).
  It mostly targets numerical code that uses NumPy.

  * Pros: JIT compilation with runtime optimisations
  * Cons: limited language support, relatively large runtime dependency (LLVM),
    non-obvious performance results

* `Pythran <https://pythran.readthedocs.io/>`_, a static Python-to-C++
  extension compiler for a subset of the language, mostly targeted
  at numerical computation.  Pythran can be (and is probably best) used
  as an additional
  `backend for NumPy code <https://cython.readthedocs.io/en/latest/src/userguide/numpy_pythran.html>`_
  in Cython.

* `mypyc <https://mypyc.readthedocs.io/>`_, a static Python-to-C extension
  compiler, based on the `mypy <http://www.mypy-lang.org/>`_ static Python
  analyser.  Like Cython's
  `pure Python mode <https://cython.readthedocs.io/en/latest/src/tutorial/pure.html>`_,
  mypyc can make use of PEP-484 type annotations to optimise code for static types.

  * Pros: good support for language and PEP-484 typing, good type inference,
    reasonable performance gains
  * Cons: no support for low-level optimisations and typing,
    opinionated Python type interpretation, reduced Python compatibility
    and introspection after compilation

* `Nuitka <https://nuitka.net/>`_, a static Python-to-C extension compiler.

  * Pros: highly language compliant, reasonable performance gains,
    support for static application linking (similar to
    `cython_freeze <https://github.com/cython/cython/blob/master/bin/cython_freeze>`_
    but with the ability to bundle library dependencies into a self-contained
    executable)
  * Cons: no support for low-level optimisations and typing

In comparison to the above, Cython provides

* fast, efficient and highly compliant support for almost all
  Python language features, including dynamic features and introspection
* full runtime compatibility with all still-in-use and future versions
  of CPython
* "generate once, compile everywhere" C code generation that allows for
  reproducible performance results and testing
* C compile time adaptation to the target platform and Python version
* support for other C-API implementations, including PyPy and Pyston
* seamless integration with C/C++ code
* broad support for manual optimisation and tuning down to the C level
* a large user base with thousands of libraries, packages and tools
* almost two decades of bug fixing and static code optimisations


Get the full source history:
----------------------------

Note that Cython used to ship the full version control repository in its source
distribution, but no longer does so due to space constraints.  To get the
full source history from a downloaded source archive, make sure you have git
installed, then step into the base directory of the Cython source distribution
and type::

    make repo


The following is from Pyrex:
------------------------------------------------------
This is a development version of Pyrex, a language
for writing Python extension modules.

For more info, take a look at:

* Doc/About.html for a description of the language
* INSTALL.txt    for installation instructions
* USAGE.txt      for usage instructions
* Demos          for usage examples

Comments, suggestions, bug reports, etc. are most
welcome!

Copyright stuff: Pyrex is free of restrictions. You
may use, redistribute, modify and distribute modified
versions.

The latest version of Pyrex can be found `here <https://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/>`_.

| Greg Ewing, Computer Science Dept
| University of Canterbury
| Christchurch, New Zealand

 A citizen of NewZealandCorp, a wholly-owned subsidiary of USA Inc.
