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

Usage example with distutils
----------------------------

You first need to install Pythran. See its `documentation
<https://pythonhosted.org/pythran/MANUAL.html>`_ for more information.

Then, simply add ``np_pythran=True`` to the ``cythonize`` call in the related
setup.py.

Here is an example:

.. code::

  from distutils.core import setup
  from Cython.Build import cythonize
  
  setup(
      name = "My hello app",
      ext_modules = cythonize('hello_pythran.pyx', np_pythran=True)
  )


.. _Pythran: https://github.com/serge-sans-paille/pythran
