***************************
Compiling with scikit-build
***************************

Two related projects are :mod:`scikit-build` and :mod:`scikit-build-core`.
They are similar in approach but :mod:`scikit-build-core` is a somewhat
more recent (but possibly less complete) project that aims to
reimplement :mod:`scikit-build` with "lessons learned"-type fixes.

Currently :mod:`scikit-build` has Cython helpers while :mod:`scikit-build-core`
requires manual invocation.
The main disadvantage of :mod:`scikit-build` is that
it works with :mod:`setuptools` rather than completely replacing it,
which :mod:`scikit-build-core` is independent.

Both are based around CMake so are a good choice if you're wrapping
or using a C/C++ library that uses CMake heavily.

:mod:`scikit-build`
===================

A good place to learn from is
`the minimal Cython example in scikit-build's tests <https://github.com/scikit-build/scikit-build/tree/main/tests/samples/hello-cython>`_.

However, the initial author of this document could not persuade the line::

    find_package(Cython)

to work under any circumstances, and so no working example is presented here.

:mod:`scikit-build-core`
========================

If you want to use `scikit-build-core` then
`their docs <https://scikit-build-core.readthedocs.io/en/latest/guide/getting_started.html>`_
provide a simple, minimal example of how to build a Cython module that has been copied
for the example here.

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