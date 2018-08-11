Building Cython code
====================

Cython code must, unlike Python, be compiled. This happens in two stages:

 - A ``.pyx`` file is compiled by Cython to a ``.c`` file, containing
   the code of a Python extension module.
 - The ``.c`` file is compiled by a C compiler to
   a ``.so`` file (or ``.pyd`` on Windows) which can be
   ``import``-ed directly into a Python session.
   Distutils or setuptools take care of this part.
   Although Cython can call them for you in certain cases.

To understand fully the Cython + distutils/setuptools build process,
one may want to read more about
`distributing Python modules <https://docs.python.org/3/distributing/index.html>`_.

There are several ways to build Cython code:

 - Write a distutils/setuptools ``setup.py``. This is the normal and recommended way.
 - Use :ref:`Pyximport<pyximport>`, importing Cython ``.pyx`` files as if they
   were ``.py`` files (using distutils to compile and build in the background).
   This method is easier than writing a ``setup.py``, but is not very flexible.
   So you'll need to write a ``setup.py`` if, for example, you need certain compilations options.
 - Run the ``cython`` command-line utility manually to produce the ``.c`` file
   from the ``.pyx`` file, then manually compiling the ``.c`` file into a shared
   object library or DLL suitable for import from Python.
   (These manual steps are mostly for debugging and experimentation.)
 - Use the [Jupyter]_ notebook or the [Sage]_ notebook,
   both of which allow Cython code inline.
   This is the easiest way to get started writing Cython code and running it.

Currently, using distutils or setuptools is the most common way Cython files are built and distributed.
The other methods are described in more detail in the :ref:`compilation` section of the reference manual.


Building a Cython module using distutils
----------------------------------------

Imagine a simple "hello world" script in a file ``hello.pyx``:

.. literalinclude:: ../../examples/quickstart/build/hello.pyx

The following could be a corresponding ``setup.py`` script:

.. literalinclude:: ../../examples/quickstart/build/setup.py

To build, run ``python setup.py build_ext --inplace``.  Then simply
start a Python session and do ``from hello import say_hello_to`` and
use the imported function as you see fit.

One caveat if you use setuptools instead of distutils, the default
action when running ``python setup.py install`` is to create a zipped
``egg`` file which will not work with ``cimport`` for ``pxd`` files
when you try to use them from a dependent package.
To prevent this, include ``zip_safe=False`` in the arguments to ``setup()``.

.. _jupyter-notebook:

Using the Jupyter notebook
--------------------------

Cython can be used conveniently and interactively from a web browser
through the Jupyter notebook.  To install Jupyter notebook, e.g. into a virtualenv,
use pip:

.. sourcecode:: bash

    (venv)$ pip install jupyter
    (venv)$ jupyter notebook

To enable support for Cython compilation, install Cython as described in :ref:`the installation guide<install>`
and load the ``Cython`` extension from within the Jupyter notebook::

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

For more information about the arguments of the ``%%cython`` magic, see
:ref:`Compiling with a Jupyter Notebook <compiling_notebook>`.

Using the Sage notebook
-----------------------

.. figure:: sage.png

  For users of the Sage math distribution, the Sage notebook allows
  transparently editing and compiling Cython code simply by typing
  ``%cython`` at the top of a cell and evaluate it.  Variables and
  functions defined in a Cython cell imported into the running session.


.. [Jupyter] http://jupyter.org/
.. [Sage] W. Stein et al., Sage Mathematics Software, http://www.sagemath.org/
