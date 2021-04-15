Welcome to Cython!
==================

Cython is a language that makes writing C extensions for
Python as easy as Python itself.  Cython is based on
Pyrex, but supports more cutting edge functionality and
optimizations.

The Cython language is very close to the Python language, but Cython
additionally supports calling C functions and declaring C types on variables
and class attributes.  This allows the compiler to generate very efficient C
code from Cython code.

This makes Cython the ideal language for wrapping external C libraries, and
for fast C modules that speed up the execution of Python code.

* Official website: https://cython.org/
* Documentation: https://docs.cython.org/
* Github repository: https://github.com/cython/cython
* Wiki: https://github.com/cython/cython/wiki

You can **support the Cython project** via
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

We are currently building the next great Cython edition:
`Cython 3.0 <https://github.com/cython/cython/milestone/58>`_.
You can help us make the life of Python 3.x users easier.


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
