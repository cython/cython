.. _limited_api:

******************************
The Limited API and Stable ABI
******************************

The Limited API and Stable ABI are `two related features of Python <https://docs.python.org/3/c-api/stable.html>`_.  Extension modules that only use a safe subset of the Python C API (the Limited API)
get a forward-compatibility guarantee (the Stable ABI) which means that the extension module can 
be used with any future version of Python, without recompilation.

Cython is able to compile extension modules in Limited API mode from Cython 3.1 onwards
(Cython 3.0 had some support, but not enough to be practically useful).  The Limited API
implementation in Cython 3.1 is close to feature-complete and successfully runs the majority of
Cython's own test-suite. However, you may still encounter bugs and missing features (even
beyond the known missing features described below).

From a user's point of view, the main benefit is that you only need to compile your Cython module
once and it will support a range of Python versions.  Be aware that forward compatibility isn't
necessarily perfect:

* The behaviour of some of the Limited API functions in the Python runtime has changed from
  version-to-version.
* in some cases Cython just uses an unstable Python API instead of an unstable C API, which
  may just move any incompatibility from compile-time to runtime.
* Cython itself does not test forward compatibility extensively. There is a
  prohibilitively large 3D tensor (header version, ``Py_LIMITED_API`` value, runtime version)
  of combinations to test.

Therefore you should be sure to test your own extensions on all the versions of Python that
you claim to support.

Limitations
===========

A number of features of Cython do not work in the Limited API.  Some of the important restrictions
are listed below, however this is non-exhaustive:

* Extension types (``cdef classes``) cannot inherit from builtin types (e.g. ``list``).  This
  is a limitation of the current implementation and is likely to be removed in the future.
* Features like profiling and line-tracing are not supported, and are unlikely to ever be supported.
* ``cimport cpython`` is restricted.  Support for this is likely to improve, although you will
  never be able to use functions/structures that are unavailable in the Limited API through this
  interface.  Direct access to the ``array.array`` class is an example of a feature that will
  never work.
* Some features only work on specific versions of the Limited API.  The most significant is
  :ref:`memoryviews` which requires Python 3.11+ in Limited API mode.
* In many cases, Cython substitutes private C API for private Python API.  This means that
  complete forward compatibility with future versions of Python isn't assured (and with
  errors likely to be runtime errors rather than compile-time errors).

Performance
===========

Running in the Limited API has a notable performance cost.  If this is a concern then you
should measure it for your own module.  Some rough guidelines follow:

Where the majority of the work involves C-level code the performance loss is likely to be
low.  This includes code that makes heavy use of typed memoryviews, or code that mainly calls
an external C library.

Where the majority of the work involves interacting with Python objects the cost is likely to
be more significant.  As an example, compiling the Cython compiler with the regular C API
gives a ~35% speed-up compared to not compiling the Cython compiler.  Compiling the Cython
compiler in the Limited API gives a 0-10% speed-up (depending on the exact version used).

If you are prepared to restrict yourself to Python versions 3.12+, then Cython will use
the "vectorcall" interface in Limited API mode.  This doesn't enable any new functionality,
but it does give a noticeable performance improvement. (Outside of the Limited API, Cython
almost always uses this interface).

Building with the Limited API
=============================

Cython's usage of the Limited API is controlled by setting the ``Py_LIMITED_API`` macro
when running the C compiler.  This macro should be set to the version-hex for the
minimum Python version that you want to support.  Useful version-hexes are:

* ``0x03070000`` - Python 3.7 - the minimum version that Cython supports.
* ``0x030B0000`` - Python 3.11 - the first version to support typed memoryviews.
* ``0x030C0000`` - Python 3.12 - the first version to support vectorcall (performance
  improvement).
  
As well as setting the ``Py_LIMITED_API`` macro, you should also name the compiled
extension modules to indicate their use of the Stable ABI.  On OS X and Linux, this
means the extension modules names should end with ``.abi3.so``.

A number of examples are shown below for different build systems, but the
same basic principles apply to any other build system.

Setuptools and setup.py
-----------------------

Using setup.py to control the compilation (as shown in the main :ref:`compilation`
documentation)::

    from setuptools import Extension, setup
    from Cython.Build import cythonize
    
    setup(
        ext_modules=cythonize([
            Extension(
                name="cy_code",
                sources=["cy_code.pyx"],
                define_macros=[
                    ("Py_LIMITED_API", 0x03070000),
                ],
                py_limited_api=True
            ),
        ]))
        
The key differences are two arguments to ``Extension``:  ``define_macros`` and ``py_limited_api``.
The ``py_limited_api`` argument controls the naming of the extension module.

Scikit-build
------------

.. highlight:: cmake

`Scikit-build <https://scikit-build.readthedocs.io>`_ uses CMake to control compilation::

    cmake_minimum_required(VERSION 3.5.0)
    project(hello_cython)
    find_package(Cython REQUIRED)
    find_package(PythonExtensions REQUIRED)
    add_cython_target(cy_code)
    add_library(cy_code MODULE ${cy_code})
    python_extension_module(cy_code)
    
    target_compile_definitions(cy_code PUBLIC -DPy_LIMITED_API=0x03070000)
    set_target_properties(cy_code PROPERTIES SUFFIX .abi3.so)
    
    install(TARGETS cy_code LIBRARY DESTINATION .)
    
The majority of this example is a lightly modified version of the example from
`their own documentation <https://scikit-build.readthedocs.io/en/latest/cmake-modules/Cython.html>`_
- for full details users should refer to that.
The Limited API specific changes are ``target_compile_definitions`` (which sets
the ``Py_LIMITED_API`` macro) and ``set_target_properties`` (which controls the
name of the generated extension module).

Meson
-----

.. highlight:: meson

`Meson <https://mesonbuild.com/>`_ is another modern build system that can be used
to generate Python modules::

    project(
        'some_package', 'c', 'cython', meson_version: '>= 1.3.0',
    )
    
    py = import('python').find_installation()
    
    py.extension_module(
        'cy_code',
        'cy_code.pyx',
        limited_api: '3.7'
    )
    
Again, this example is adapted from
`the Meson documentation <https://mesonbuild.com/Cython.html#cython>`_ and more complete
details are available there.  The Limited API modification is the argument ``limited_api: '3.7'``,
which both sets the version hex and names the generated module correctly.
