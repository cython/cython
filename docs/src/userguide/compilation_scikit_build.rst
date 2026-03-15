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
provides a simple, minimal example of how to build a Cython module that has been adapted here.

Like most Python build backends, you need a :file:`pyproject.toml`::

    [build-system]
    requires = ["scikit-build-core", "cython"]
    build-backend = "scikit_build_core.build"

    [project]
    name = "example"
    version = "1.0.0"

Then you need a :file:`CMakeLists.txt`:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.15...3.26)
    project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

    find_package(
    Python
    COMPONENTS Interpreter Development.Module
    REQUIRED)

    add_custom_command(
    OUTPUT example.c
    COMMENT
        "Making ${CMAKE_CURRENT_BINARY_DIR}/example.c from ${CMAKE_CURRENT_SOURCE_DIR}/example.pyx"
    COMMAND Python::Interpreter -m cython
            "${CMAKE_CURRENT_SOURCE_DIR}/example.pyx" --output-file example.c
    DEPENDS example.pyx
    VERBATIM)

    python_add_library(example MODULE example.c WITH_SOABI)

    install(TARGETS example DESTINATION .)

Currently the Cython command is invoked manually as a custom CMake command,
which is a bit verbose but fairly simple.

Install your package by running ``pip install .``.

:mod:`scikit-build`
===================

If you do want to use the legacy :mod:`scikit-build` then
A good place to learn from is
`the minimal Cython example in their tests <https://github.com/scikit-build/scikit-build/tree/main/tests/samples/hello-cython>`_.
