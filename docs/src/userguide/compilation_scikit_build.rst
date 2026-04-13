******************************************
Compiling with CMake and scikit-build-core
******************************************

CMake is a popular build system, with support for multiple languages,
including C, C++, and Cuda.  :mod:`scikit-build-core` is the official adaptor
for using CMake for a Python package.

Therefore the combination of CMake and :mod:`scikit-build-core` is a good
choice if you're wrapping or using a C/C++ library that uses CMake heavily.
But equally they can be used in their own right, independent of any
external dependencies.  

:mod:`scikit-build-core`
========================

If you want to use `scikit-build-core` then
`their docs <https://scikit-build-core.readthedocs.io/en/latest/guide/getting_started.html>`_
provides a simple, minimal example of how to build a Cython module. There is an official Cython plugin,
`cython-cmake <https://github.com/scikit-build/cython-cmake>`_.

Like most Python build backends, you need a :file:`pyproject.toml` file
to define the project metadata and set up the build backend::

    [build-system]
    requires = ["scikit-build-core", "cython", "cython-cmake"]
    build-backend = "scikit_build_core.build"

    [project]
    name = "example"
    version = "1.0.0"

The majority of the logic to build your package is in
:file:`CMakeLists.txt`:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.21...4.0)
    project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

    find_package(
      Python
      COMPONENTS Interpreter Development.Module
      REQUIRED)
    include(UseCython)
    
    cython_transpile(example.pyx LANGUAGE C OUTPUT_VARIABLE example_c)

    python_add_library(example MODULE ${example_c} WITH_SOABI)
    install(TARGETS example DESTINATION .)

Install your package by running ``pip install .``.

