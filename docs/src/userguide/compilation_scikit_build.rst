********************************
Compiling with scikit-build-core
********************************

Two related projects are :mod:`scikit-build` and :mod:`scikit-build-core`.
:mod:`scikit-build` should be considered a legacy project while
:mod:`scikit-build-core` is a modern and more fully-featured replacement.

Both are based around CMake and so are a good choice if you're wrapping
or using a C/C++ library that uses CMake heavily.

If you want to use one of these build backends, our recommendation is
to use :mod:`scikit-build-core`.  However, the main remaining advantage
of :mod:`scikit-build` is that it comes with builtin utilities to
handle invoke Cython while for :mod:`scikit-build-core` you must
invoke Cython manually through CMake.  

:mod:`scikit-build-core`
========================

If you want to use `scikit-build-core` then
`their docs <https://scikit-build-core.readthedocs.io/en/latest/guide/getting_started.html>`_
provides a simple, minimal example of how to build a Cython module. There is an official Cython plugin, `cython-cmake <https://github.com/scikit-build/cython-cmake>`_.

Like most Python build backends, you need a :file:`pyproject.toml`::

    [build-system]
    requires = ["scikit-build-core", "cython", "cython-cmake"]
    build-backend = "scikit_build_core.build"

    [project]
    name = "example"
    version = "1.0.0"

Then you need a :file:`CMakeLists.txt`:

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

