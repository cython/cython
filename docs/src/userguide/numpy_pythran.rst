.. highlight:: python

.. _numpy-pythran:

**************************
Pythran as a Numpy backend
**************************

Using the flag ``--np-pythran``, it is possible to use the `Pythran`_ numpy
implementation for numpy related operations. One advantage to use this backend
is that the Pythran implementation uses C++ expression templates to save memory
transfers and can benefit from SIMD instructions of modern CPU.

This can lead to really interesting speedup in some cases, going from 2 up to
16, depending on the targeted CPU architecture and the original algorithm.

Please note that this feature is experimental.

Usage example with setuptools
-----------------------------

You first need to install Pythran. See its `documentation
<https://pythran.readthedocs.io/>`_ for more information.

Then, simply add a ``cython: np_pythran=True`` directive at the top of the
Python files that needs to be compiled using Pythran numpy support.

Here is an example of a simple ``setup.py`` file using setuptools:

.. code::

  from setuptools import setup
  from Cython.Build import cythonize
  import numpy
  import pythran

  setup(
      name = "My hello app",
      ext_modules = cythonize('hello_pythran.pyx'),
      include_dirs = [numpy.get_include(), pythran.get_include()]
  )

Then, with the following header in ``hello_pythran.pyx``:

.. code::

  # cython: np_pythran=True

``hello_pythran.pyx`` will be compiled using Pythran numpy support.

Please note that Pythran can further be tweaked by adding settings in the
``$HOME/.pythranrc`` file. For instance, this can be used to enable `Boost.SIMD`_ support.
See the `Pythran user manual
<https://pythran.readthedocs.io/en/latest/MANUAL.html#customizing-your-pythranrc>`_ for
more information.

.. _Pythran: https://github.com/serge-sans-paille/pythran
.. _Boost.SIMD: https://github.com/NumScale/boost.simd
