================
Cython Changelog
================

3.0.12 (2025-02-11)
===================

Bugs fixed
----------

* Release 3.0.11 introduced some incorrect ``noexcept`` warnings.
  (Github issue :issue:`6335`)

* Conditional assignments to variables using the walrus operator could crash.
  (Github issue :issue:`6094`)

* Dict assignments to struct members with reserved C names could generate invalid C code.

* Fused ctuples with the same entry types but different sizes could fail to compile.
  (Github issue :issue:`6328`)

* In Py3, `pyximport` was not searching `sys.path` when looking for importable source files.
  (Github issue :issue:`5615`)

* Using `& 0` on integers produced with `int.from_bytes()` could read invalid memory on Python 3.10.
  (Github issue :issue:`6480`)

* Modules could fail to compile in PyPy 3.11 due to missing CPython specific header files.
  Patch by Matti Picus.  (Github issue :issue:`6482`)

* Minor fix in C++ ``partial_sum()`` declaration.


3.0.11 (2024-08-05)
===================

Features added
--------------

* The C++11 ``emplace*`` methods were added to ``libcpp.deque``.
  Patch by Somin An.  (Github issue :issue:`6159`)

Bugs fixed
----------

* The exception check value of functions declared in pxd files was not always applied in 3.0.10.
  (Github issue :issue:`6122`)

* A crash on exception deallocations was fixed.
  (Github issue :issue:`6022`)

* A crash was fixed when assigning a zero-length slice to a memoryview.
  Patch by Michael Man.  (Github issue :issue:`6227`)

* ``libcpp.optional.value()`` could crash if it raised a C++ exception.
  Patch by Alexander Condello.  (Github issue :issue:`6190`)

* The return type of ``str()`` was mishandled, leading to crashes with ``language_level=3``.
  (Github issue :issue:`6166`)

* ``bytes.startswith/endswith()`` failed for non-bytes substrings (e.g. ``bytearray``).
  (Github issue :issue:`6168`)

* Fused ctuples crashed Cython.
  (Github issue :issue:`6068`)

* A compiler crash was fixed when using extension types in fused types.
  (Github issue :issue:`6204`)

* The module cleanup code was incorrect for globally defined memory view slices.
  (Github issue :issue:`6276`)

* Some adaptations were made to enable compilation in Python 3.13.
  (Github issues :issue:`5997`, :issue:`6182`, :issue:`6251`)


3.0.10 (2024-03-30)
===================

Bugs fixed
----------

* Cython generated incorrect self-casts when directly calling final methods of subtypes.
  Patch by Lisandro Dalcin.  (Github issue :issue:`2747`)

* Internal C names generated from C function signatures could become too long for MSVC.
  (Github issue :issue:`6052`)

* The ``noexcept`` warnings could be misleading in some cases.
  Patch by Gonzalo Tornaría.  (Github issue :issue:`6087`)

* The ``@cython.ufunc`` implementation could generate incomplete C code.
  (Github issue :issue:`6064`)

* The ``libcpp.complex`` declarations could result in incorrect C++ code.
  Patch by Raffi Enficiaud.  (Github issue :issue:`6037`)

* Several tests were adapted to work with both NumPy 1.x and 2.0.
  Patch by Matti Picus.  (Github issues :issue:`6076`, :issue:`6100`)

* C compiler warnings when the freelist implementation is disabled (e.g. on PyPy) were fixed.
  It can now be disabled explicitly with the C macro guard ``CYTHON_USE_FREELISTS=0``.
  (Github issue :issue:`6099`)

* Some C macro guards for feature flags were missing from the NOGIL Python configuration.

* Some recently added builtins were unconditionally looked up at module import time
  (if used by user code) that weren't available on all Python versions and could thus
  fail the import.

* A performance hint regarding exported pxd declarations was improved.
  (Github issue :issue:`6001`)


3.0.9 (2024-03-05)
==================

Features added
--------------

* Assigning ``const`` values to non-const variables now issues a warning.
  (Github issue :issue:`5639`)

* Using ``noexcept`` on a function returning Python objects now issues a warning.
  (Github issue :issue:`5661`)

* Some C-API usage was updated for the upcoming CPython 3.13.
  Patches by Victor Stinner et al.  (Github issues :issue:`6003`, :issue:`6020`)

* The deprecated ``Py_UNICODE`` type is no longer used, unless required by user code.
  (Github issue :issue:`5982`)

* ``std::string.replace()`` declarations were added to libcpp.string.
  Patch by Kieran Geary.  (Github issue :issue:`6037`)

Bugs fixed
----------

* Cython generates incorrect (but harmless) self-casts when directly calling
  final methods of subtypes.  Lacking a better solution, the errors that recent
  gcc versions produce have been silenced for the time being.
  Original patch by Michał Górny.  (Github issue :issue:`2747`)

* Unused variable warnings about clineno were fixed when C lines in tracebacks are disabled.
  (Github issue :issue:`6035`)

* Subclass deallocation of extern classes could crash if the base class uses GC.
  Original patch by Jason Fried.  (Github issue :issue:`5971`)

* Type checks for Python ``memoryview`` could use an invalid C function.
  Patch by Xenia Lu.  (Github issue :issue:`5988`)

* Calling final fused functions could generate invalid C code.
  (Github issue :issue:`5989`)

* Declaring extern enums multiple times could generate invalid C code.
  (Github issue :issue:`5905`)

* ``pyximport`` used relative paths incorrectly.
  Patch by Stefano Rivera.  (Github issue :issue:`5957`)

* Running Cython with globbing characters (``[]*?``) in the module search path could fail.
  Patch by eewanco.  (Github issue :issue:`5942`)

* Literal strings that include braces could change the C code indentation.

Other changes
-------------

* The "enum class not importable" warning is now only issued once per enum type.
  (Github issue :issue:`5941`)


3.0.8 (2024-01-10)
==================

Bugs fixed
----------

* Using ``const`` together with defined fused types could fail to compile.
  (Github issue :issue:`5230`)

* A "use after free" bug was fixed in parallel sections.
  (Github issue :issue:`5922`)

* Several types were not available as ``cython.*`` types in pure Python code.

* The generated code is now correct C89 again, removing some C++ style ``//`` comments
  and C99-style declaration-after-code code ordering.  This is still relevant for some
  ols C compilers, specifically ones that match old Python 2.7 installations.


3.0.7 (2023-12-19)
==================

Bugs fixed
----------

* In the iterator of generator expressions, ``await`` and ``yield`` were not correctly analysed.
  (Github issue :issue:`5851`)

* ``cpdef`` enums with the same name cimported from different modules could lead to
  invalid C code.
  (Github issue :issue:`5887`)

* Some declarations in ``cpython.unicode`` were fixed and extended.
  (Github issue :issue:`5902`)

* Compiling fused types used in pxd files could crash Cython in Python 3.11+.
  (Github issues :issue:`5894`,  :issue:`5588`)

* Source files with non-ASCII file names could crash Cython.
  (Github issue :issue:`5873`)

* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the :ref:`0.29.37` release.


3.0.6 (2023-11-26)
==================

Features added
--------------

* Fused def function dispatch is a bit faster.

* Declarations for the ``wchar`` PyUnicode API were added.
  (Github issue :issue:`5836`)

* The Python "nogil" fork is now also detected with the new ``Py_GIL_DISABLED`` macro.
  Patch by Hugo van Kemenade.  (Github issue :issue:`5852`)

Bugs fixed
----------

* Comparing dataclasses could give different results than Python.
  (Github issue :issue:`5857`)

* ``float(std::string)`` generated invalid C code.
  (Github issue :issue:`5818`)

* Using ``cpdef`` functions with ``cimport_from_pyx`` failed.
  (Github issue :issue:`5795`)

* A crash was fixed when string-formatting a Python value fails.
  (Github issue :issue:`5787`)

* On item access, Cython could try the sequence protocol before the mapping protocol
  in some cases if an object supports both.
  (Github issue :issue:`5776`)

* A C compiler warning was resolved.
  (Github issue :issue:`5794`)

* Complex numbers failed to compile in MSVC with C11.
  Patch by Lysandros Nikolaou.  (Github issue :issue:`5809`)

* Some issues with the Limited API and with PyPy were resolved.
  (Github issues :issue:`5695`, :issue:`5696`)

* A C++ issue in Python 3.13 was resolved.
  (Github issue :issue:`5790`)

* Several directives are now also available (as no-ops) in Python code.
  (Github issue :issue:`5803`)

* An error message was corrected.
  Patch by Mads Ynddal.  (Github issue :issue:`5805`)


3.0.5 (2023-10-31)
==================

Features added
--------------

* Preliminary support for CPython 3.13a1 was added to allow early testing.
  (Github issue :issue:`5767`)

Bugs fixed
----------

* A compiler crash was fixed.
  (Github issue :issue:`5771`)

* A typo in the ``always_allow_keywords`` directive for Python code was fixed.
  Patch by lk-1984.  (Github issue :issue:`5772`)

* Some C compiler warnings were resolved.
  Patch by Pierre Jolivet.  (Github issue :issue:`5780`)


3.0.4 (2023-10-17)
==================

Features added
--------------

* A new compiler directive ``show_performance_hints`` was added to disable the
  newly added performance hint output.
  (Github issue :issue:`5748`)

Bugs fixed
----------

* ```cythonize` required ``distutils`` even for operations that did not build binaries.
  (Github issue :issue:`5751`)

* A regression in 3.0.3 was fixed that prevented calling inline functions
  from another inline function in ``.pxd`` files.
  (Github issue :issue:`5748`)

* Some C compiler warnings were resolved.
  Patch by Pierre Jolivet.  (Github issue :issue:`5756`)


3.0.3 (2023-10-05)
==================

Features added
--------------

* More warnings were added to help users migrate and avoid bugs.
  (Github issue :issue:`5650`)

* A warning-like category for performance hints was added that bypasses ``-Werror``.
  (Github issue :issue:`5673`)

* FastGIL now uses standard ``thread_local`` in C++.
  (Github issue :issue:`5640`)

* ``reference_wrapper`` was added to ``libcpp.functional``.
  Patch by Vyas Ramasubramani.  (Github issue :issue:`5671`)

* The ``cythonize`` command now supports the ``--cplus`` option known from the ``cython`` command.
  (Github issue :issue:`5736`)

Bugs fixed
----------

* Performance regressions where the GIL was needlessly acquired were fixed.
  (Github issues :issue:`5670`, :issue:`5700`)

* A reference leak for exceptions in Python 3.12 was resolved.
  Patch by Eric Johnson.  (Github issue :issue:`5724`)

* ``fastcall`` calls with keyword arguments generated incorrect C code.
  (Github issue :issue:`5665`)

* Assigning the type converted result of a conditional (if-else) expression
  to ``int`` or ``bool`` variables could lead to incorrect C code.
  (Github issue :issue:`5731`)

* Early (unlikely) failures in Python function wrappers no longer set a
  traceback in order to simplify the C code flow.  Being mostly memory
  allocation errors, they probably would never have created a traceback anyway.
  (Github issue :issue:`5681`)

* Relative cimports from packages with ``__init__.py`` files could fail.
  (Github issue :issue:`5715`)

* Several issues with the Limited API support were resolved.
  (Github issues :issue:`5641`, :issue:`5648`, :issue:`5689`)

* The code generated for special-casing both Cython functions and PyCFunctions was cleaned up
  to avoid calling C-API functions that were not meant for the other type respectively.
  This could previously trigger assertions in CPython debug builds and now also plays better
  with the Limited API.
  (Github issues :issue:`4804`, :issue:`5739`)

* Fix some C compiler warnings.
  Patches by Ralf Gommers, Oleksandr Pavlyk, Sebastian Koslowski et al.
  (Github issues :issue:`5651`, :issue:`5663`, :issue:`5668`, :issue:`5717`, :issue:`5726`, :issue:`5734`)

* Generating gdb debugging information failed when using generator expressions.
  Patch by Oleksandr Pavlyk.  (Github issue :issue:`5552`)

* Passing a ``setuptools.Extension`` into ``cythonize()`` instead of a
  ``distutils.Extension`` could make it miss the matching extensions.

* ``cython -M`` needlessly required ``distutils``, which made it fail in Python 3.12.
  (Github issue :issue:`5681`)

Other changes
-------------

* The visible deprecation warning for ``DEF`` was removed again since it proved
  difficult for some users to migrate away from it.  The statement is still
  meant to be removed at some point (and thus, like ``IF``, should not be
  used in new code), but the time for sunset is probably not around the corner.
  (Github issue :issue:`4310`)

* The ``np_pythran`` option raise a ``DeprecationWarning`` if it receives other values
  than ``True`` and ``False``.  This will eventually be disallowed (in line with all
  other boolean options).


3.0.2 (2023-08-27)
==================

Bugs fixed
----------

* Using ``None`` as default value for arguments annotated as ``int`` could crash Cython.
  (Github issue :issue:`5643`)

* Default values of fused types that include ``complex`` could generate invalid C code
  with ``-DCYTHON_CCOMPLEX=0``.
  (Github issue :issue:`5644`)

* Using C++ enum class types in extension type method signatures could generate invalid C code.
  (Github issue :issue:`5637`)


3.0.1 (2023-08-25)
==================

Features added
--------------

* The error messages regarding exception declarations were improved in order to give
  better help about possible reasons and fixes.
  (Github issue :issue:`5547`)

Bugs fixed
----------

* Memory view types in Python argument annotations no longer accept ``None``.  They now
  require an explicit ``Optional[]`` or a ``None`` default value in order to allow ``None``
  to be passed.  This was an oversight in the 3.0.0 release and is a BACKWARDS INCOMPATIBLE
  change.  However, since it only applies to code using Python syntax, it probably only
  applies to newly written code that was written for Cython 3.0 and can easily be adapted.
  In most cases, we expect that this change will avoid bugs in user code rather than
  produce problems.
  (Github issue :issue:`5612`)

* ``nogil`` functions using parallel code could freeze when called with the GIL held.
  (Github issues :issue:`5564`, :issue:`5573`)

* Relative cimports could end up searching globally and find the same package installed
  elsewhere, potentially in another version.
  (Github issue :issue:`5511`)

* Attribute lookups on known standard library modules could accidentally search
  in the module namespace instead.
  (Github issue :issue:`5536`)

* Using constructed C++ default arguments could generate invalid C++ code.
  (Github issue :issue:`5553`)

* ``libcpp.memory.make_unique()`` was lacking C++ exception handling.
  (Github issue :issue:`5560`)

* Some non-public and deprecated CAPI usages were replaced by public
  (and thus more future proof) API code.

* Many issues with the Limited API support were resolved.
  Patches by Lisandro Dalcin et al.
  (Github issues :issue:`5549`, :issue:`5550`, :issue:`5556`, :issue:`5605`, :issue:`5617`)

* Some C compiler warnings were resolved.
  Patches by Matti Picus et al.  (Github issues :issue:`5557`, :issue:`5555`)

* Large Python integers are now stored in hex instead of decimal strings to work around
  security limits in Python and generally speed up their Python object creation.

* ``NULL`` could not be used as default for fused type pointer arguments.
  (Github issue :issue:`5554`)

* C functions that return pointer types now return ``NULL`` as default exception value.
  Previously, calling code wasn't aware of this and always tested for raised exceptions.
  (Github issue :issue:`5554`)

* Untyped literal default arguments in fused functions could generate invalid C code.
  (Github issue :issue:`5614`)

* C variables declared as ``const`` could generate invalid C code when used in closures,
  generator expressions, ctuples, etc.
  (Github issues :issue:`5558`,  :issue:`5333`)

* Enums could not refer to previously defined enums in their definition.
  (Github issue :issue:`5602`)

* The Python conversion code for anonymous C enums conflicted with regular int conversion.
  (Github issue :issue:`5623`)

* Using memory views for property methods (and other special methods) could lead to
  refcounting problems.
  (Github issue :issue:`5571`)

* Star-imports could generate code that tried to assign to constant C macros like
  ``PY_SSIZE_T_MAX`` and ``PY_SSIZE_T_MIN``.
  Patch by Philipp Wagner.  (Github issue :issue:`5562`)

* ``CYTHON_USE_TYPE_SPECS`` can now be (explicitly) enabled in PyPy.

* The template parameter "delimeters" in the Tempita ``Template`` class was corrected
  to "delimiters".  The old spelling is still available in the main template API but
  now issues a ``DeprecationWarning``.
  (Github issue :issue:`5608`)

* The ``cython --version`` output is now  less likely to reach both stdout and stderr.
  Patch by Eli Schwartz.  (Github issue :issue:`5504`)

* The sdist was missing the `Shadow.pyi` stub file.


3.0.0 unified release notes
===========================

Cython 3.0.0 has been a very large effort that cleaned up many old warts,
introduced many new features, and introduces a couple of intentional
behaviour changes, even though the goal remained to stay compatible as
much as possible with Cython 0.29.x. For details, see the `migration guide`_.

.. _`migration guide`: https://cython.readthedocs.io/en/latest/src/userguide/migrating_to_cy30.html

As the development was spread out over several years, a lot of things have
happened in the meantime. Many crucial bugfixes and some features were
backported to 0.29.x and are not strictly speaking "new" in Cython 3.0.0.

Major themes in 3.0.0
=====================

Compatibility with CPython and the Python C API
-----------------------------------------------

Since Cython 3.0.0 started development, CPython 3.8-3.11 were released.
All these are supported in Cython, including experimental support for the
in-development CPython 3.12. On the other end of the spectrum, support for
Python 2.6 was dropped.

Cython interacts very closely with the C-API of Python, which is where most
of the adaptation work happens.


Related changes
^^^^^^^^^^^^^^^

* The long deprecated include files ``python_*``, ``stdio``, ``stdlib`` and
  ``stl`` in ``Cython/Includes/Deprecated/`` were removed.  Use the ``libc.*``
  and ``cpython.*`` pxd modules instead.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2904`)

* The ``Py_hash_t`` type failed to accept arbitrary "index" values.
  (Github issue :issue:`2752`)

* ``@cython.trashcan(True)`` can be used on an extension type to enable the
  CPython :ref:`trashcan`. This allows deallocating deeply recursive objects
  without overflowing the stack. Patch by Jeroen Demeyer.  (Github issue :issue:`2842`)

* ``PyEval_InitThreads()`` is no longer used in Py3.7+ where it is a no-op.

* A low-level inline function ``total_seconds(timedelta)`` was added to
  ``cpython.datetime`` to bypass the Python method call.  Note that this function
  is not guaranteed to give exactly the same results for very large time intervals.
  Patch by Brock Mendel.  (Github issue :issue:`3616`)

* The internal CPython macro ``Py_ISSPACE()`` is no longer used.
  Original patch by Andrew Jones.  (Github issue :issue:`4111`)

* The value ``PyBUF_MAX_NDIM`` was added to the ``cpython.buffer`` module.
  Patch by John Kirkham.  (Github issue :issue:`3811`)

* A new module ``cpython.time`` was added with some low-level alternatives to
  Python's ``time`` module.
  Patch by Brock Mendel.  (Github issue :issue:`3767`)

* More C-API declarations for ``cpython.datetime``  were added.
  Patch by Bluenix2.  (Github issue :issue:`4128`)

* C-API declarations for context variables in Python 3.7 were added.
  Original patch by Zolisa Bleki.  (Github issue :issue:`2281`)

* C-API declarations for ``cpython.fileobject`` were added.
  Patch by Zackery Spytz.  (Github issue :issue:`3906`)

* The signature of ``PyFloat_FromString()`` in ``cpython.float`` was changed
  to match the signature in Py3.  It still has an automatic fallback for Py2.
  (Github issue :issue:`3909`)

* ``PyMem_[Raw]Calloc()`` was added to the ``cpython.mem`` declarations.
  Note that the ``Raw`` versions are no longer #defined by Cython.  The previous
  macros were not considered safe.
  Patch by William Schwartz and David Woods.  (Github issue :issue:`3047`)

* The runtime size check for imported ``PyVarObject`` types was improved
  to reduce false positives and adapt to Python 3.11.
  Patch by David Woods.  (Github issues :issue:`4827`, :issue:`4894`)

* The generated C code failed to compile in CPython 3.11a4 and later.
  (Github issue :issue:`4500`)

* ``pyximport`` no longer uses the deprecated ``imp`` module.
  Patch by Matúš Valo.  (Github issue :issue:`4560`)

* Improvements to ``PyTypeObject`` definitions in pxd wrapping of libpython.
  Patch by John Kirkham. (Github issue :issue:`4699`)

* Some old usages of the deprecated Python ``imp`` module were replaced with ``importlib``.
  Patch by Matúš Valo.  (Github issue :issue:`4640`)

* ``cpdef`` enums no longer use ``OrderedDict`` but ``dict`` in Python 3.6 and later.
  Patch by GalaxySnail.  (Github issue :issue:`5180`)

* Several problems with CPython 3.12 were resolved.
  (Github issue :issue:`5238`)

* The exception handling code was adapted to CPython 3.12.
  (Github issue :issue:`5442`)

* The Python ``int`` handling code was adapted to make use of the new ``PyLong``
  internals in CPython 3.12.
  (Github issue :issue:`5353`)

* A compile error when using ``__debug__`` was resolved.

* The deprecated ``_PyGC_FINALIZED()`` C-API macro is no longer used.
  Patch by Thomas Caswell and Matúš Valo.  (Github issue :issue:`5481`)

* A crash in Python 2.7 was fixed when cleaning up extension type instances
  at program end.


Compatibility with other Python implementations
-----------------------------------------------

Cython tries to support other Python implementations, largely on a best-effort
basis. The most advanced support exists for PyPy, which is tested in our CI
and considered supported.

Related changes
^^^^^^^^^^^^^^^

* An unsupported C-API call in PyPy was fixed.
  Patch by Max Bachmann.  (Github issue :issue:`4055`)

* Support for the now unsupported Pyston V1 was removed in favour of Pyston V2.
  Patch by Marius Wachtler.  (Github issue :issue:`4211`)

* A C compiler warning in PyPy3 regarding ``PyEval_EvalCode()`` was resolved.

* Some compatibility issues with PyPy were resolved.
  Patches by Max Bachmann, Matti Picus.
  (Github issues :issue:`4454`, :issue:`4477`, :issue:`4478`, :issue:`4509`, :issue:`4517`)

* An initial set of adaptations for GraalVM Python was implemented.  Note that
  this does not imply any general support for this target or that your code
  will work at all in this environment.  But testing should be possible now.
  Patch by David Woods.  (Github issue :issue:`4328`)

* A work-around for StacklessPython < 3.8 was disabled in Py3.8 and later.
  (Github issue :issue:`4329`)


Initial support for Limited API
-------------------------------

CPython provides a stable, limited subset of its C-API as the so-called Limited API.
This C-API comes with the guarantee of a stable ABI, meaning that extensions modules
that were compiled for one version of CPython can also be imported in later versions
without recompilation.

There is initial support for this in Cython.  By defining the ``CYTHON_LIMITED_API``
macro, Cython cuts down its C-API usage and tries to adhere to the Limited C-API,
probably at the cost of a bit of performance.
In order to get full benefit from the limited API you will also need to define the
CPython macro ``Py_LIMITED_API`` to a specific CPython compatibility version,
which additionally restricts the C-API during the C compilation,
thus enforcing the forward compatibility of the extension module.

Note that "initial support" in Cython really means that setting the ``Py_LIMITED_API``
macro will almost certainly not yet work for your specific code.
There are limitations in the Limited C-API
that are difficult for Cython to generate C code for, so some advanced Python features
(like async code) may not lead to C code that cannot adhere to the Limited C-API, or
where Cython simply does not know yet how to adhere to it.  Basically, if you get your
code to compile with both macros set, and it passes your test suite, then it should be
possible to import the extension module also in later CPython versions.

The experimental feature flags ``CYTHON_USE_MODULE_STATE`` and
``CYTHON_USE_TYPE_SPECS`` enable some individual aspects of the Limited API
implementation independently.

Related changes
^^^^^^^^^^^^^^^

* Preliminary support for the CPython's ``Py_LIMITED_API`` (stable ABI) is
  available by setting the  ``CYTHON_LIMITED_API`` C macro.  Note that the
  support is currently in an early stage and many features do not yet work.
  You currently still have to define ``Py_LIMITED_API`` externally in order
  to restrict the API usage.  This will change when the feature stabilises.
  Patches by Eddie Elizondo and David Woods.  (Github issues :issue:`3223`,
  :issue:`3311`, :issue:`3501`)

* Limited API support was improved.
  Patches by Matthias Braun.  (Github issues :issue:`3693`, :issue:`3707`)

* New C feature flags: ``CYTHON_USE_MODULE_STATE``, ``CYTHON_USE_TYPE_SPECS``
  Both are currently considered experimental.
  (Github issue :issue:`3611`)

* ``_Py_TPFLAGS_HAVE_VECTORCALL`` was always set on extension types when using the limited API.
  Patch by David Woods.  (Github issue :issue:`4453`)

* Limited API C preprocessor warning is compatible with MSVC. Patch by
  Victor Molina Garcia.  (Github issue :issue:`4826`)

* The embedding code no longer calls deprecated C-API functions but uses the new ``PyConfig``
  API instead on CPython versions that support it (3.8+).
  Patch by Alexander Shadchin.  (Github issue :issue:`4895`)

* Some C code issue were resolved for the Limited API target.
  (Github issues :issue:`5264`, :issue:`5265`, :issue:`5266`)

* Conversion of Python ints to C ``int128`` is now always supported, although slow
  if dedicated C-API support is missing (``_PyLong_AsByteArray()``), specifically in
  the Limited C-API.
  (Github issue :issue:`5419`)

* Custom buffer slot methods are now supported in the Limited C-API of Python 3.9+.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5422`)


Improved fidelity to Python semantics
-------------------------------------

Implemented PEPs
^^^^^^^^^^^^^^^^

* `PEP-3131`_: Supporting Non-ASCII Identifiers (Github issue :issue:`2601`)
* `PEP-479`_: `generator_stop` (enabled by default for `language_level=3`) (Github issue :issue:`2580`)
* `PEP-487`_: Simpler customisation of class creation (Github issue :issue:`2781`)
* `PEP-563`_: Postponed Evaluation of Annotations (Github issue :issue:`3285`)
* `PEP-570`_: Positional-Only Parameters (Github issue :issue:`2915`)
* `PEP-572`_: Assignment Expressions (a.k.a. the walrus operator `:=`) (Github issue :issue:`2636`)
* `PEP-590`_: Vectorcall protocol (Github issue :issue:`2263`)
* `PEP-614`_: Relaxing Grammar Restrictions On Decorators (Github issue :issue:`4570`)

Typing support in the sense of `PEP-484`_ (Github issues :issue:`3949`, :issue:`4243`)
and `PEP-560`_ (Github issues :issue:`2753`, :issue:`3537`, :issue:`3764`) was also improved.

.. _`PEP-3131`: https://www.python.org/dev/peps/pep-3131
.. _`PEP-479`: https://www.python.org/dev/peps/pep-0479
.. _`PEP-484`: https://www.python.org/dev/peps/pep-0484
.. _`PEP-487`: https://www.python.org/dev/peps/pep-0487
.. _`PEP-560`: https://www.python.org/dev/peps/pep-0560
.. _`PEP-563`: https://www.python.org/dev/peps/pep-0563
.. _`PEP-570`: https://www.python.org/dev/peps/pep-0570
.. _`PEP-572`: https://www.python.org/dev/peps/pep-0572
.. _`PEP-590`: https://www.python.org/dev/peps/pep-0590
.. _`PEP-614`: https://www.python.org/dev/peps/pep-0614

The default language level was changed to ``3str``, i.e. Python 3 semantics,
but with ``str`` literals (also in Python 2.7).  This is a backwards incompatible
change from the previous default of Python 2 semantics.  The previous behaviour
is available through the directive ``language_level=2``.
(Github issue :issue:`2565`).  This covers changes such as using the
``print``-function instead of the ``print``-statement, and integer-integer
division giving a floating point answer. Most of these changes were available
in earlier versions of Cython but are now the default.

Cython 3.0.0 also aligns its own language semantics more closely with Python, in particular:

* the power operator has changed to give a result matching what Python does rather than
  keeping the same types as the input (as in C),
* operator overloading of ``cdef classes`` behaves much more like Python classes,
* Cython's behaviour when using type annotations aligns more closely with their
  standard use in Python.

Related changes
^^^^^^^^^^^^^^^

* Cython no longer generates ``__qualname__`` attributes for classes in Python
  2.x since they are problematic there and not correctly maintained for subclasses.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2772`)

* Binding staticmethods of Cython functions were not behaving like Python methods.
  Patch by Jeroen Demeyer.  (Github issue :issue:`3106`, :issue:`3102`)

* Compiling package ``__init__`` files could fail under Windows due to an
  undefined export symbol.  (Github issue :issue:`2968`)

* ``__init__.pyx`` files were not always considered as package indicators.
  (Github issue :issue:`2665`)

* Setting ``language_level=2`` in a file did not work if ``language_level=3``
  was enabled globally before.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2791`)

* ``__doc__`` was not available inside of the class body during class creation.
  (Github issue :issue:`1635`)

* The first function line number of functions with decorators pointed to the
  signature line and not the first decorator line, as in Python.
  Patch by Felix Kohlgrüber.  (Github issue :issue:`2536`)

* Pickling unbound methods of Python classes failed.
  Patch by Pierre Glaser.  (Github issue :issue:`2972`)

* Item access (subscripting) with integer indices/keys always tried the
  Sequence protocol before the Mapping protocol, which diverged from Python
  semantics.  It now passes through the Mapping protocol first when supported.
  (Github issue :issue:`1807`)

* Nested dict literals in function call kwargs could incorrectly raise an
  error about duplicate keyword arguments, which are allowed when passing
  them from dict literals.
  (Github issue :issue:`2963`)

* Diverging from the usual behaviour, ``len(memoryview)``, ``len(char*)``
  and ``len(Py_UNICODE*)`` returned an unsigned ``size_t`` value.  They now
  return a signed ``Py_ssize_t``, like other usages of ``len()``.

* The unicode methods ``.upper()``, ``.lower()`` and ``.title()`` were
  incorrectly optimised for single character input values and only returned
  the first character if multiple characters should have been returned.
  They now use the original Python methods again.

* The ``cython.view.array`` type supports inheritance.
  Patch by David Woods.  (Github issue :issue:`3413`)

* The builtin ``abs()`` function can now be used on C numbers in nogil code.
  Patch by Elliott Sales de Andrade.  (Github issue :issue:`2748`)

* The attributes ``gen.gi_frame`` and ``coro.cr_frame`` of Cython compiled
  generators and coroutines now return an actual frame object for introspection.
  (Github issue :issue:`2306`)

* Inlined properties can be defined for external extension types.
  Patch by Matti Picus. (Github issue :issue:`2640`, redone later in :issue:`3571`)

* Unicode module names and imports are supported.
  Patch by David Woods.  (Github issue :issue:`3119`)

* ``__arg`` argument names in methods were not mangled with the class name.
  Patch by David Woods.  (Github issue :issue:`1382`)

* With ``language_level=3/3str``, Python classes without explicit base class
  are now new-style (type) classes also in Py2.  Previously, they were created
  as old-style (non-type) classes.
  (Github issue :issue:`3530`)

* Conditional blocks in Python code that depend on ``cython.compiled`` are
  eliminated at an earlier stage, which gives more freedom in writing
  replacement Python code.
  Patch by David Woods.  (Github issue :issue:`3507`)

* Python private name mangling now falls back to unmangled names for non-Python
  globals, since double-underscore names are not uncommon in C.  Unmangled Python
  names are also still found as a legacy fallback but produce a warning.
  Patch by David Woods.  (Github issue :issue:`3548`)

* The ``print`` statement (not the ``print()`` function) is allowed in
  ``nogil`` code without an explicit ``with gil`` section.

* ``repr()`` was assumed to return ``str`` instead of ``unicode`` with ``language_level=3``.
  (Github issue :issue:`3736`)

* Type inference now understands that ``a, *b = x`` assigns a list to ``b``.

* No/single argument functions now accept keyword arguments by default in order
  to comply with Python semantics.  The marginally faster calling conventions
  ``METH_NOARGS`` and ``METH_O`` that reject keyword arguments are still available
  with the directive ``@cython.always_allow_keywords(False)``.
  (Github issue :issue:`3090`)

* Special methods for binary operators now follow Python semantics.
  Rather than e.g. a single ``__add__`` method for cdef classes, where
  "self" can be either the first or second argument, one can now define
  both ``__add__`` and ``__radd__`` as for standard Python classes.
  This behavior can be disabled with the ``c_api_binop_methods`` directive
  to return to the previous semantics in Cython code (available from Cython
  0.29.20), or the reversed method (``__radd__``) can be implemented in
  addition to an existing two-sided operator method (``__add__``) to get a
  backwards compatible implementation.
  (Github issue :issue:`2056`)

* Generator expressions in pxd-overridden ``cdef`` functions could
  fail to compile.
  Patch by Matúš Valo.  (Github issue :issue:`3477`)

* Calls to ``.__class__()`` of a known extension type failed.
  Patch by David Woods.  (Github issue :issue:`3954`)

* Structs could not be instantiated with positional arguments in
  pure Python mode.

* Annotations were not exposed on annotated (data-)classes.
  Patch by matsjoyce.  (Github issue :issue:`4151`)

* Docstrings of ``cpdef`` enums are now copied to the enum class.
  Patch by matham.  (Github issue :issue:`3805`)

* ``asyncio.iscoroutinefunction()`` now recognises coroutine functions
  also when compiled by Cython.
  Patch by Pedro Marques da Luz.  (Github issue :issue:`2273`)

* Self-documenting f-strings (``=``) were implemented.
  Patch by davfsa.  (Github issue :issue:`3796`)

* ``cython.array`` supports simple, non-strided views.
  (Github issue :issue:`3775`)

* Attribute annotations in Python classes are now ignored, because they are
  just Python objects in a dict (as opposed to the fields of extension types).
  Patch by David Woods.  (Github issues :issue:`4196`, :issue:`4198`)

* A warning was added when ``__defaults__`` or ``__kwdefaults__`` of Cython compiled
  functions were re-assigned, since this does not current have an effect.
  Patch by David Woods.  (Github issue :issue:`2650`)

* The ``self`` argument of static methods in .pxd files was incorrectly typed.
  Patch by David Woods.  (Github issue :issue:`3174`)

* Default values for memory views arguments were not properly supported.
  Patch by Corentin Cadiou.  (Github issue :issue:`4313`)

* Python object types were not allowed as ``->`` return type annotations.
  Patch by Matúš Valo.  (Github issue :issue:`4433`)

* The excess arguments in a for-in-range loop with more than 3 arguments to `range()`
  were silently ignored.
  Original patch by Max Bachmann. (Github issue :issue:`4550`)

* Unsupported decorators on cdef functions were not rejected in recent releases.
  Patch by David Woods.  (Github issue :issue:`4322`)

* Fused functions were binding unnecessarily, which prevented them from being pickled.
  Patch by David Woods.  (Github issue :issue:`4370`)

* Decorators on inner functions were not evaluated in the right scope.
  Patch by David Woods.  (Github issue :issue:`4367`)

* Cython did not type the ``self`` argument in special binary methods.
  Patch by David Woods.  (Github issue :issue:`4434`)

* Circular imports of compiled modules could fail needlessly even when the import
  could already be resolved from ``sys.modules``.
  Patch by Syam Gadde.  (Github issue :issue:`4390`)

* ``__del__(self)`` on extension types now maps to ``tp_finalize`` in Python 3.
  Original patch by ax487.  (Github issue :issue:`3612`)

* Reusing an extension type attribute name as a method name is now an error.
  Patch by 0dminnimda.  (Github issue :issue:`4661`)

* When using type annotations, ``func(x: list)`` or ``func(x: ExtType)`` (and other
  Python builtin or extension types) no longer allow ``None`` as input argument to ``x``.
  This is consistent with the normal typing semantics in Python, and was a common gotcha
  for users who did not expect ``None`` to be allowed as input.  To allow ``None``, use
  ``typing.Optional`` as in ``func(x: Optional[list])``.  ``None`` is also automatically
  allowed when it is used as default argument, i.e. ``func(x: list = None)``.
  ``int`` and ``float`` are now also recognised in type annotations and restrict the
  value type at runtime.  They were previously ignored.
  Note that, for backwards compatibility reasons, the new behaviour does not apply when using
  Cython's C notation, as in ``func(list x)``.  Here, ``None`` is still allowed, as always.
  Also, the ``annotation_typing`` directive can now be enabled and disabled more finely
  within the module.
  (Github issues :issue:`2696`, :issue:`3883`, :issue:`4606`, :issue:`4669`, :issue:`4886`)

* The parser allowed some invalid spellings of ``...``.
  Patch by 0dminnimda.  (Github issue :issue:`4868`)

* The ``__self__`` attribute of fused functions reports its availability correctly
  with ``hasattr()``.  Patch by David Woods.
  (Github issue :issue:`4808`)

* Several optimised string methods failed to accept ``None`` as arguments to their options.
  Test patch by Kirill Smelkov.  (Github issue :issue:`4737`)

* Cython generators and coroutines now identify as ``CO_ASYNC_GENERATOR``,
  ``CO_COROUTINE`` and ``CO_GENERATOR`` accordingly.
  (Github issue :issue:`4902`)

* Memory views and the internal Cython array type now identify as ``collections.abc.Sequence``.
  Patch by David Woods.  (Github issue :issue:`4817`)

* Context managers can be written in parentheses.
  Patch by David Woods.  (Github issue :issue:`4814`)

* Some parser issues were resolved.
  (Github issue :issue:`4992`)

* Unused ``**kwargs`` arguments did not show up in ``locals()``.
  (Github issue :issue:`4899`)

* Relative imports failed in compiled ``__init__.py`` package modules.
  Patch by Matúš Valo.  (Github issue :issue:`3442`)

* Extension types are now explicitly marked as immutable types to prevent them from
  being considered mutable.
  Patch by Max Bachmann.  (Github issue :issue:`5023`)

* ``int(Py_UCS4)`` returned the code point instead of the parsed digit value.
  (Github issue :issue:`5216`)

* Calling bound classmethods of builtin types could fail trying to call the unbound method.
  (Github issue :issue:`5051`)

* Generator expressions and comprehensions now look up their outer-most iterable
  on creation, as Python does, and not later on start, as they did previously.
  (Github issue :issue:`1159`)

* Bound C methods can now coerce to Python objects.
  (Github issues :issue:`4890`, :issue:`5062`)

* ``cpdef`` enums can now be pickled.
  (Github issue :issue:`5120`)

* The Python Enum of a ``cpdef enum`` now inherits from ``IntFlag`` to better match
  both Python and C semantics of enums.
  (Github issue :issue:`2732`)

* The special ``__*pow__`` methods now support the 2- and 3-argument variants.
  (Github issue :issue:`5160`)

* The ``**`` power operator now behaves more like in Python by returning the correct complex
  result if required by math.  A new ``cpow`` directive was added to turn on the previous
  C-like behaviour.
  (Github issue :issue:`4936`)

* With ``language_level=2``, imports of modules in packages could return the wrong module in Python 3.
  (Github issue :issue:`5308`)

* Function signatures containing a type like `tuple[()]` could not be printed.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5355`)

* ``__qualname__`` and ``__module__`` were not available inside of class bodies.
  (Github issue :issue:`4447`)

* A new directive ``embedsignature.format`` was added to select the format of the
  docstring embedded signatures between ``python``, ``c`` and argument ``clinic``.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5415`)

* ctuples can now be assigned from arbitrary sequences, not just Python tuples.


Improvements in Pure Python mode
--------------------------------

Cython strives to be able to
parse newer Python constructs for use with its `pure python`_ mode, which
has been a focus. In short, this allows to compile a wider range of Python
code into optimized C code.

.. _`pure python`: https://cython.readthedocs.io/en/latest/src/tutorial/pure.html

Pure python mode gained many new features and was generally overhauled to make
it as capable as the Cython syntax.  Except for using external C/C++ libraries,
it should now be possible to express all Cython code and use all features in
regular Python syntax.  The very few remaining exceptions or bugs are noted in
the documentation.

Additionally, the documentation has been substantially updated
(primarily by Matúš Valo and 0dminnimda) to show both the older Cython syntax
and pure Python syntax.

Related changes
^^^^^^^^^^^^^^^

* The ``cython.declare()`` and ``cython.cast()`` functions could fail in pure mode.
  Patch by Dmitry Shesterkin.  (Github issue :issue:`3244`)

* Fused argument types were not correctly handled in type annotations and
  ``cython.locals()``.
  Patch by David Woods.  (Github issues :issue:`3391`, :issue:`3142`)

* ``nogil`` functions now avoid acquiring the GIL on function exit if possible
  even if they contain ``with gil`` blocks.
  (Github issue :issue:`3554`)

* The ``@returns()`` decorator propagates exceptions by default for suitable C
  return types when no ``@exceptval()`` is defined.
  (Github issues :issue:`3625`, :issue:`3664`)

* Extension types inheriting from Python classes could not safely
  be exposed in ``.pxd``  files.
  (Github issue :issue:`4106`)

* Default arguments of methods were not exposed for introspection.
  Patch by Vladimir Matveev.  (Github issue :issue:`4061`)

* Literal list assignments to pointer variables declared in PEP-526
  notation failed to compile.

* The type ``cython.Py_hash_t`` is available in Python mode.

* A ``cimport`` is now supported in pure Python code by prefixing the
  imported module name with ``cython.cimports.``, e.g.
  ``from cython.cimports.libc.math import sin``.
  (GIthub issue :issue:`4190`)

* Directives starting with ``optimization.*`` in pure Python mode were incorrectly named.
  It should have been ``optimize.*``.
  Patch by David Woods.  (Github issue :issue:`4258`)

* Invalid and misspelled ``cython.*`` module names were not reported as errors.
  (Github issue :issue:`4947`)

* The ``annotation_typing`` directive was missing in pure Python mode.
  Patch by 0dminnimda.  (Github issue :issue:`5194`)

* Memoryviews with ``object`` item type were not supported in Python type declarations.
  (Github issue :issue:`4907`)

* Subscripted builtin types in type declarations (like ``list[float]``) are now
  better supported.
  (Github issue :issue:`5058`)

* Unknown type annotations (e.g. because of typos) now emit a warning at compile time.
  Patch by Matúš Valo.  (Github issue :issue:`5070`)

* ``typing.Optional`` could fail on tuple types.
  (Github issue :issue:`5263`)

* ``from cython cimport … as …`` could lead to imported names not being found in annotations.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5235`)

* Simple tuple types like ``(int, int)`` are no longer accepted in Python annotations
  and require the Python notation instead (e.g. ``tuple[cython.int, cython.int]``).
  (Github issue :issue:`5397`)

* The Python implementation of ``cimport cython.cimports…`` could raise an ``ImportError``
  instead of an ``AttributeError`` when looking up package variable names.
  Patch by Matti Picus.  (Github issue :issue:`5411`)

* A new decorator ``@cython.with_gil`` is available in Python code to match the ``with gil``
  function declaration in Cython syntax.

* ``with gil`` and ``with nogil(flag)`` now accept their flag argument also in Python code.
  Patch by Matúš Valo.  (Github issue :issue:`5113`)


Code generation changes
-----------------------

Cython has gained several major new features that speed up both the development
and the code. Dataclasses have gained an extension type equivalent that implements
the dataclass features in C code.  Similarly, the ``@functools.total_ordering``
decorator to an extension type will implement the comparison functions in C.

Finally, NumPy ufuncs can be generated from simple computation functions with the
new ``@cython.ufunc`` decorator.

Related changes
^^^^^^^^^^^^^^^

* ``with gil/nogil`` statements can be conditional based on compile-time
  constants, e.g. fused type checks.
  Patch by Noam Hershtig.  (Github issue :issue:`2579`)

* The names of Cython's internal types (functions, generator, coroutine, etc.)
  are now qualified with the module name of the internal Cython module that is
  used for sharing them across Cython implemented modules, for example
  ``_cython_3_0a5.coroutine``.  This was done to avoid making them look like
  homeless builtins, to help with debugging, and in order to avoid a CPython
  warning according to https://bugs.python.org/issue20204

* A ``@cython.total_ordering`` decorator has been added to automatically
  implement all comparison operators, similar to ``functools.total_ordering``.
  Patch by Spencer Brown.  (Github issue :issue:`2090`)

* A new decorator ``@cython.dataclasses.dataclass`` was implemented that provides
  compile time dataclass generation capabilities to ``cdef`` classes (extension types).
  Patch by David Woods.  (Github issue :issue:`2903`).  ``kw_only`` dataclasses
  added by Yury Sokov.  (Github issue :issue:`4794`)

* A new function decorator ``@cython.ufunc`` automatically generates a (NumPy) ufunc that
  applies the calculation function to an entire memoryview.
  (Github issue :issue:`4758`)

* Generated NumPy ufuncs could crash for large arrays due to incorrect GIL handling.
  (Github issue :issue:`5328`)

* Some invalid directive usages are now detected and rejected, e.g. using ``@ccall``
  together with ``@cfunc``, and applying ``@cfunc`` to a ``@ufunc``.  Cython also
  warns now when a directive is applied needlessly.
  (Github issue :issue:`5399` et al.)

* The normal ``@dataclasses.dataclass`` and ``@functools.total_ordering`` decorators
  can now be used on extension types.  Using the corresponding ``@cython.*`` decorator
  will automatically turn a Python class into an extension type (no need for ``@cclass``).
  (Github issue :issue:`5292`)


Interaction with numpy
----------------------

The NumPy declarations (``cimport numpy``) were moved over to the NumPy project in order
to allow version specific changes on their side.

One effect is that Cython does not use deprecated NumPy C-APIs any more.  Thus, you
can define the respective NumPy C macro to get rid of the compatibility warning at
C compile time.

Related changes
^^^^^^^^^^^^^^^

* ``cython.inline()`` now sets the ``NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION``
  C macro automatically when ``numpy`` is imported in the code, to avoid C compiler
  warnings about deprecated NumPy C-API usage.

* Deprecated NumPy API usages were removed from ``numpy.pxd``.
  Patch by Matti Picus.  (Github issue :issue:`3365`)

* ``numpy.import_array()`` is automatically called if ``numpy`` has been cimported
  and it has not been called in the module code.  This is intended as a hidden
  fail-safe so user code should continue to call ``numpy.import_array``.
  Patch by David Woods.  (Github issue :issue:`3524`)

* The outdated getbuffer/releasebuffer implementations in the NumPy
  declarations were removed so that buffers declared as ``ndarray``
  now use the normal implementation in NumPy.

* Several macros/functions declared in the NumPy API are now usable without
  holding the GIL.

* The ``numpy`` declarations were updated.
  Patch by Brock Mendel.  (Github issue :issue:`3630`)

* ``ndarray.shape`` failed to compile with Pythran and recent NumPy.
  Patch by Serge Guelton.  (Github issue :issue:`3762`)

* A C-level compatibility issue with recent NumPy versions was resolved.
  Patch by David Woods.  (Github issue :issue:`4396`)

* The generated modules no longer import NumPy internally when using
  fused types but no memoryviews.
  Patch by David Woods.  (Github issue :issue:`4935`)

* ``np.long_t`` and ``np.ulong_t`` were removed from the NumPy declarations,
  syncing Cython with upstream NumPy v1.25.0.  The aliases were confusing
  since they could mean different things on different platforms.


Exception handling
------------------

Cython-implemented C functions now propagate exceptions by default, rather than
swallowing them in non-object returning function if the user forgot to add an
``except`` declaration to the signature.  This was a long-standing source of bugs,
but can require adding the ``noexcept`` declaration to existing functions if
exception propagation is really undesired.
(Github issue :issue:`4280`)

To ease the transition for this break in behaviour, it is possible to set
``legacy_implicit_noexcept=True``.

Related changes
^^^^^^^^^^^^^^^

* The ``assert`` statement is allowed in ``nogil`` sections.  Here, the GIL is
  only acquired if the ``AssertionError`` is really raised, which means that the
  evaluation of the asserted condition only allows C expressions.

* The exception handling annotation ``except +*`` was broken.
  Patch by David Woods.  (Github issues :issue:`3065`, :issue:`3066`)

* Improve conversion between function pointers with non-identical but
  compatible exception specifications.  Patches by David Woods.
  (Github issues :issue:`4770`, :issue:`4689`)

* Exceptions within for-loops that run over memoryviews could lead to a ref-counting error.
  Patch by David Woods.  (Github issue :issue:`4662`)

* To opt out of the new, safer exception handling behaviour, legacy code can set the new
  directive ``legacy_implicit_noexcept=True`` for a transition period to keep the
  previous, unsafe behaviour.  This directive will eventually be removed in a later release.
  Patch by Matúš Valo.  (Github issue :issue:`5094`)

* Cython implemented C functions now propagate exceptions by default, rather than
  swallowing them in non-object returning function if the user forgot to add an
  ``except`` declaration to the signature.  This was a long-standing source of bugs,
  but can require adding the ``noexcept`` declaration to existing functions if
  exception propagation is really undesired.
  (Github issue :issue:`4280`)

* The code ``except +nogil`` (declaring a C++ exception handler function called ``nogil``)
  is now rejected because it is almost certainly a typo from ``except + nogil``.
  (Github issue :issue:`5430`)

* Handling freshly raised exceptions that didn't have a traceback yet could crash.
  (Github issue :issue:`5495`)


Optimizations
-------------

Generating efficient code has long been a goal of Cython, and 3.0 continues that.
Probably the most significant change is that Cython functions use the PEP-590 vectorcall
protocol on Python 3.7 and higher.

Related changes
^^^^^^^^^^^^^^^

* Name lookups in class bodies no longer go through an attribute lookup.
  Patch by Jeroen Demeyer.  (Github issue :issue:`3100`)

* Extension types that do not need their own ``tp_new`` implementation (because
  they have no object attributes etc.) directly inherit the implementation of
  their parent type if possible.
  (Github issue :issue:`1555`)

* Some list copying is avoided internally when a new list needs to be created
  but we already have a fresh one.
  (Github issue :issue:`3494`)

* Multiplication of Python numbers with small constant integers is faster.
  (Github issue :issue:`2808`)

* String concatenation can now happen in place if possible, by extending the
  existing string rather than always creating a new one.
  Patch by David Woods.  (Github issue :issue:`3453`)

* The ``str()`` builtin now calls ``PyObject_Str()`` instead of going
  through a Python call.
  Patch by William Ayd.  (Github issue :issue:`3279`)

* Reimports of already imported modules are substantially faster.
  (Github issue :issue:`2854`)

* The dispatch to fused functions is now linear in the number of arguments,
  which makes it much faster, often 2x or more, and several times faster for
  larger fused types with many specialisations.
  Patch by will-ca.  (Github issue :issue:`1385`)

* The fastcall/vectorcall protocols are used for several internal Python calls.
  (Github issue :issue:`3540`)

* ``nogil`` functions now avoid acquiring the GIL on function exit if possible
  even if they contain ``with gil`` blocks.
  (Github issue :issue:`3554`)

* Type inference now works for memory views and slices.
  Patch by David Woods.  (Github issue :issue:`2227`)

* For-in-loop iteration over ``bytearray`` and memory views is optimised.
  Patch by David Woods.  (Github issue :issue:`2227`)

* For-in-loop iteration over ``bytearray`` and memory views is optimised.
  Patch by David Woods.  (Github issue :issue:`2227`)

* ``float(…)`` is optimised for string arguments (str/bytes/bytearray).

* ``[...] * N`` is optimised for C integer multipliers ``N``.
  (Github issue :issue:`3922`)

* Some constant tuples containing strings were not deduplicated.
  Patch by David Woods.  (Github issue :issue:`4353`)

* Memory views can use atomic CPU instructions instead of locks in more cases.
  Patch by Sam Gross.  (Github issue :issue:`4912`)

* Cython avoids raising ``StopIteration`` in ``__next__`` methods when possible.
  Patch by David Woods.  (Github issue :issue:`3447`)

* Larger numbers of extension types with multiple subclasses could take very long to compile.
  Patch by Scott Wolchok.  (Github issue :issue:`5139`)

* Integer comparisons avoid Python coercions if possible.
  (Github issue :issue:`4821`)

* The call-time dispatch for fused memoryview types is less slow.
  (Github issue :issue:`5073`)

* Python's ``memoryview`` is now a known builtin type with optimised properties.
  (Github issue :issue:`3798`)

* Multiplying a sequence by a C integer avoids creating and intermediate Python integer.

* The reference counting of memory views involved useless overhead.
  (Github issue :issue:`5510`)


Compatibility with C
--------------------

The support for C features like ``const`` or ``volatile`` was substantially improved.

The generated code has been cleared up to reduce the number of C compiler warnings emitted.

Related changes
^^^^^^^^^^^^^^^

* A C compiler cast warning was resolved.
  Patch by Michael Buesch.  (Github issue :issue:`2775`)

* Constant integer expressions that used a negative exponent were evaluated
  as integer 0 instead of the expected float value.
  Patch by Kryštof Pilnáček.  (Github issue :issue:`2133`)

* Several declarations in ``cpython.*``, ``libc.*`` and ``libcpp.*`` were added.
  Patches by Jeroen Demeyer, Matthew Edwards, Chris Gyurgyik, Jerome Kieffer
  and Zackery Spytz.
  (Github issues :issue:`3468`, :issue:`3332`, :issue:`3202`, :issue:`3188`,
  :issue:`3179`, :issue:`2891`, :issue:`2826`, :issue:`2713`)

* The ``volatile`` C modifier is supported in Cython code.
  Patch by Jeroen Demeyer.  (Github issue :issue:`1667`)

* ``const`` can be used together with fused types.
  Patch by Thomas Vincent.  (Github issue :issue:`1772`)

* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods.  (Github issues :issue:`3430`, :issue:`3522`)

* The C property feature has been rewritten and now requires C property methods
  to be declared ``inline`` (:issue:`3571`).

* Cython generates C compiler branch hints for unlikely user defined if-clauses
  in more cases, when they end up raising exceptions unconditionally. This now
  includes exceptions being raised in ``nogil``/``with gil`` sections.

* Several issues with arithmetic overflow handling were resolved, including
  undefined behaviour in C.
  Patch by Sam Sneddon.  (Github issue :issue:`3588`)

* `libc.math` was extended to include all C99 function declarations.
  Patch by Dean Scarff.  (Github issue :issue:`3570`)

* Some C compiler warninge were resolved.
  Patches by Max Bachmann.  (Github issue :issue:`4053`, :issue:`4059`, :issue:`4054`, :issue:`4148`, :issue:`4162`)

* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue :issue:`2749`)

* A C compiler warning about unused code was resolved.
  (Github issue :issue:`3763`)

* Some compiler problems and warnings were resolved.
  Patches by David Woods, 0dminnimda, Nicolas Pauss and others.
  (Github issues :issue:`4317`, :issue:`4324`, :issue:`4361`, :issue:`4357`)

* Some C compiler warnings were fixed.
  Patch by mwtian.  (Github issue :issue:`4831`)

* A case of undefined C behaviour was resolved in the list slicing code.
  Patch by Richard Barnes.  (Github issue :issue:`4734`)

* Typedefs for the ``bint`` type did not always behave like ``bint``.
  Patch by Nathan Manville and 0dminnimda.  (Github issue :issue:`4660`)

* Intel C compilers could complain about unsupported gcc pragmas.
  Patch by Ralf Gommers.  (Github issue :issue:`5052`)

* Structs that contained an array field resulted in incorrect C code.  Their initialisation
  now uses ``memcpy()``.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5178`)

* The module state struct was not initialised in correct C (before C23), leading to
  compile errors on Windows.
  Patch by yudonglin.  (Github issue :issue:`5169`)

* ``cdef public`` functions declared in .pxd files could use an incorrectly mangled C name.
  Patch by EpigeneMax.  (Github issue :issue:`2940`)

* ``const`` types could not be returned from functions.
  Patch by Mike Graham.  (Github issue :issue:`5135`)

* C11 ``complex.h`` is now properly detected.
  (Github issue :issue:`2513`)

* Standard C/C++ atomic operations are now used for memory views, if available.
  (Github issue :issue:`4925`)

* C arrays can be initialised inside of nogil functions.
  Patch by Matúš Valo.  (Github issue :issue:`1662`)

* Very long Python integer constants could exceed the maximum C name length of MSVC.
  Patch by 0dminnimda.  (Github issue :issue:`5290`)

* Some C compiler warnings were resolved.
  Patches by Matt Tyson, Lisandro Dalcin, Philipp Wagner, Matti Picus et al.
  (Github issues :issue:`5417`, :issue:`5418`, :issue:`5421`, :issue:`5437`, :issue:`5438`, :issue:`5443`)

* Some typedef declarations for libc function types were fixed.
  (Github issue :issue:`5498`)

* With MSVC, Cython no longer enables C-Complex support by accident (which is not supported there).
  (Github issue :issue:`5512`)


Compatibility with C++
----------------------

Many C++ features like forwarding references or ``std::move`` are now supported or even used
internally, if possible.

Cython's wrapping of the C++ standard library has been extended.

A new `cpp_locals`` directive enables C++ local variables to initialized when assigned to
rather than at the start of the function, making them behave more like Python variables,
and also removing the requirement for them to be default constructible.

Related changes
^^^^^^^^^^^^^^^

* C++ ``typeid()`` failed for fused types.
  Patch by David Woods.  (Github issue :issue:`3203`)

* ``std::move()`` is now used in C++ mode for internal temp variables to
  make them work without copying values.
  Patch by David Woods.  (Github issues :issue:`3253`, :issue:`1612`)

* The C++ ``typeid()`` function was allowed in C mode.
  Patch by Celelibi.  (Github issue :issue:`3637`)

* C++ references failed to compile when used as Python object indexes.
  Patch by David Woods.  (Github issue :issue:`3754`)

* The construct ``for x in cpp_function_call()`` failed to compile.
  Patch by David Woods.  (Github issue :issue:`3663`)

* Some C++ STL methods did not propagate exceptions.
  Patch by Max Bachmann.  (Github issue :issue:`4079`)

* A compile failure for C++ enums in Py3.4 / MSVC was resolved.
  Patch by Ashwin Srinath.  (Github issue :issue:`3782`)

* Cython compiled functions always provided a ``__self__`` attribute,
  regardless of being used as a method or not.
  Patch by David Woods.  (Github issue :issue:`4036`)

* Overloaded C++ static methods were lost.
  Patch by Ashwin Srinath.  (Github :issue:`1851`)

* Nested C++ types were not usable through ctypedefs.
  Patch by Vadim Pushtaev.  (Github issue :issue:`4039`)

* More declarations for C++ string methods were added.

* Converting C++ containers to Python lists uses less memory allocations.
  Patch by Max Bachmann.  (Github issue :issue:`4081`)

* ``std::move()`` is now also called for temps during ``yield``.
  Patch by Yu Feng.  (Github issue :issue:`4154`)

* The destructor is now called for fields in C++ structs.
  Patch by David Woods.  (Github issue :issue:`3226`)

* Conversion from Python dicts to ``std::map`` was broken.
  Patch by David Woods and Mikkel Skofelt.  (Github issues :issue:`4228`, :issue:`4231`)

* Code optimisations were not applied to methods of Cython implemented C++ classes.
  Patch by David Woods.  (Github issue :issue:`4212`)

* C++17 execution policies are supported in ``libcpp.algorithm``.
  Patch by Ashwin Srinath.  (Github issue :issue:`3790`)

* A new directive ``cpp_locals`` was added that allows local C++ variables to
  be lazily initialised (without default constructor), thus making them behave
  more like Python variables.
  Patch by David Woods.  (Github issue :issue:`4160`)

* Generated utility code for C++ conversions no longer depends on several user
  definable directives that may make it behave incorrectly.
  Patch by David Woods.  (Github issue :issue:`4206`)

* Several issues with the new ``cpp_locals`` directive were resolved and
  its test coverage improved.
  Patch by David Woods.  (Github issues :issue:`4265`, :issue:`4266`)

* Declarations for ``libcpp.algorithms``, ``libcpp.set`` and ``libcpp.unordered_set``
  were extended.
  Patch by David Woods.  (Github issues :issue:`4271`, :issue:`4273`)

* Several C++ library declarations were added and fixed.
  Patches by Dobatymo, account-login, Jonathan Helgert, Evgeny Yakimov, GalaxySnail, Max Bachmann.
  (Github issues :issue:`4408`, :issue:`4419`, :issue:`4410`, :issue:`4395`,
  :issue:`4423`, :issue:`4448`, :issue:`4462`, :issue:`3293`, :issue:`4522`,
  :issue:`2171`, :issue:`4531`)

* Templating C++ classes with memory view types lead to buggy code and is now rejected.
  Patch by David Woods.  (Github issue :issue:`3085`)

* ``prange`` loops generated incorrect code when ``cpp_locals`` is enabled.
  Patch by David Woods.  (Github issue :issue:`4354`)

* Direct assignments to C++ references are now allowed.
  Patch by David Woods.  (Github issue :issue:`1863`)

* Conversion from Python dict to C++ map now supports arbitrary Python mappings,
  not just dicts.

* Some C++ and CPython library declarations were extended and fixed.
  Patches by Max Bachmann, Till Hoffmann, Julien Jerphanion, Wenjun Si.
  (Github issues :issue:`4530`, :issue:`4528`, :issue:`4710`, :issue:`4746`,
  :issue:`4751`, :issue:`4818`, :issue:`4762`, :issue:`4910`)

* Some C/C++ warnings were resolved.
  Patches by Max Bachmann, Alexander Shadchin, at al.
  (Github issues :issue:`5004`, :issue:`5005`, :issue:`5019`, :issue:`5029`, :issue:`5096`)

* C++ references did not work on fused types.
  (Github issue :issue:`4717`)

* C++ iteration more safely stores the iterable in temporary variables.
  Patch by Xavier.  (Github issue :issue:`3828`)

* C++ post-increment/-decrement operators were not correctly looked up on declared C++
  classes, thus allowing Cython declarations to be missing for them and incorrect C++
  code to be generated.
  Patch by Max Bachmann.  (Github issue :issue:`4536`)

* ``cdef public`` functions used an incorrect linkage declaration in C++.
  Patch by Maximilien Colange.  (Github issue :issue:`1839`)

* Declarations were added for the C++ bit operations, some other parts of C++20 and CPython APIs.
  Patches by Jonathan Helgert, Dobatymo, William Ayd and Max Bachmann.
  (Github issues :issue:`4962`, :issue:`5101`, :issue:`5157`, :issue:`5163`, :issue:`5257`)

* ``cpp_locals`` no longer have to be "assignable".
  (Github issue :issue:`4558`)

* Nested ``cppclass`` definitions are supported.
  Patch by samaingw.  (Github issue :issue:`1218`)

* ``reversed()`` can now be used together with C++ iteration.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5002`)

* Some C++ warnings regarding ``const`` usage in internally generated utility code were resolved.
  Patch by Max Bachmann.  (Github issue :issue:`5301`)

* Cython generated C++ code accidentally used C++11 features in some cases.
  (Github issue :issue:`5316`)

* Fully qualified C++ names prefixed by a cimported module name could fail to compile.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5229`)

* C++ declarations for ``<cmath>``, ``<numbers>`` and ``std::any`` were added.
  Patches by Jonathan Helgert and Maximilien Colange.
  (Github issues :issue:`5262`, :issue:`5309`, :issue:`5314`)

* The ``extern "C"`` and ``extern "C++"`` markers that Cython generates for
  ``public`` functions can now be controlled by setting the C macro ``CYTHON_EXTERN_C``.

* C++ containers of item type ``bint`` could conflict with those of item type ``int``.
  (Github issue :issue:`5516`)

* Reverse iteration in C++ no longer removes the ``const`` qualifier from the item type.
  Patch by Isuru Fernando.  (Github issue :issue:`5478`)


Commandline Interface
---------------------

A number of new options were added to the ``cython`` and ``cythonize``
commands.

Related changes
^^^^^^^^^^^^^^^

* The command line parser was rewritten and modernised using ``argparse``.
  Patch by Egor Dranischnikow.  (Github issue :issue:`2952`, :issue:`3001`)

* ``cygdb`` gives better error messages when it fails to initialise the
  Python runtime support in gdb.
  Patch by Volker Weissmann.  (Github issue :issue:`3489`)

* ``--no-docstrings`` option added to ``cythonize`` script.
  Original patch by mo-han.  (Github issue :issue:`2889`)

* Code annotation accepts a new debugging argument ``--annotate-fullc`` that
  will include the complete syntax highlighted C file in the HTML output.
  (Github issue :issue:`2855`)

* ``cygdb`` has a new option ``--skip-interpreter`` that allows using a different
  Python runtime than the one used to generate the debugging information.
  Patch by Alessandro Molina.  (Github issue :issue:`4186`)

* ``cythonize()`` and the corresponding CLI command now regenerate the output files
  also when they already exist but were generated by a different Cython version.

* The ``cython`` and ``cythonize`` commands ignored non-existing input files without error.
  Patch by Matúš Valo.  (Github issue :issue:`4629`)

* ``cythonize --help`` now also prints information about the supported environment variables.
  Patch by Matúš Valo.  (Github issue :issue:`1711`)

* Using the ``--working`` option could lead to sources not being found.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5365`)

* Passing a language level and directives on the command line lost the language level setting.
  Patch by Matúš Valo.  (Github issue :issue:`5484`)

* ``cython --version`` now prints the version to both stdout and stderr (unless that is a TTY).
  (Github issue :issue:`5504`)


Build integration
-----------------

Cython has made a number of improvements both to how it compiles itself
and how it integrates with external build tools.  Most notably Cython
has been moving to use ``setuptools`` instead of the deprecated/removed
``distutils`` where possible.

The new ``--depfile`` option generates dependency files to help integrate
Cython with other build tools.

Related changes
^^^^^^^^^^^^^^^

* Binary Linux wheels now follow the manylinux2010 standard.
  Patch by Alexey Stepanov.  (Github issue :issue:`3355`)

* The search order for include files was changed. Previously it was
  ``include_directories``, ``Cython/Includes``, ``sys.path``. Now it is
  ``include_directories``, ``sys.path``, ``Cython/Includes``. This was done to
  allow third-party ``*.pxd`` files to override the ones in Cython.
  Patch by Matti Picus.  (Github issue :issue:`2905`)

* Source file fingerprinting now uses SHA-1 instead of MD5 since the latter
  tends to be slower and less widely supported these days.
  (Github issue :issue:`2790`)

* The Cython AST code serialiser class ``CodeWriter`` in ``Cython.CodeWriter``
  supports more syntax nodes.

* Parallel builds of Cython itself (``setup.py build_ext -j N``) failed on Windows.

* When importing the old Cython ``build_ext`` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha.  (Github issue :issue:`2209`)

* ``.pxd`` files can now be :ref:`versioned <versioning>` by adding an
  extension like "``.cython-30.pxd``" to prevent older Cython versions (than
  3.0 in this case) from picking them up.  (Github issue :issue:`3577`)

* The Cython ``CodeWriter`` can now handle more syntax constructs.
  Patch by Tao He.  (Github issue :issue:`3514`)

* The Cython ``CodeWriter`` mishandled no-argument ``return`` statements.
  Patch by Tao He.  (Github issue :issue:`3795`)

* Cython now detects when existing output files were not previously generated
  by itself and refuses to overwrite them.  It is a common mistake to name
  the module file of a wrapper after the library (source file) that it wraps,
  which can lead to surprising errors when the file gets overwritten.

* The ``Cython.Build.BuildExecutable`` tool no longer executes the program automatically.
  Use ``cythonrun`` for that.

* Python modules were not automatically recompiled when only their ``.pxd`` file changed.
  Patch by Golden Rockefeller.  (Github issue :issue:`1428`)

* An unnecessary slow-down at import time was removed from ``Cython.Distutils``.
  Original patch by Anthony Sottile.  (Github issue :issue:`4224`)

* A compiler crash when running Cython thread-parallel from distutils was resolved.
  (Github issue :issue:`4503`)

* An incompatibility with recent coverage.py versions was resolved.
  Patch by David Woods.  (Github issue :issue:`4440`)

* ``pyximport`` now uses ``cythonize()`` internally.
  Patch by Matúš Valo.  (Github issue :issue:`2304`)

* ``Cython.Distutils.build_ext`` now uses ``cythonize()`` internally (previously
  known as ``new_build_ext``), while still supporting the options that were
  available in the old implementation (``old_build_ext``).
  Patch by Matúš Valo.  (Github issue :issue:`3541`)

* Improve compatibility between classes pickled in Cython 3.0 and 0.29.x
  by accepting MD5, SHA-1 and SHA-256 checksums.
  (Github issue :issue:`4680`)

* ``pyximport`` failed for long filenames on Windows.
  Patch by Matti Picus.  (Github issue :issue:`4630`)

* A new Cython build option ``--cython-compile-minimal`` was added to compile only a
  smaller set of Cython's own modules, which can be used to reduce the package
  and install size.

* The environment variable ``CYTHON_FORCE_REGEN=1`` can be used to force ``cythonize``
  to regenerate the output files regardless of modification times and changes.

* The ``cythonize`` and ``cython`` commands have a new option ``-M`` / ``--depfile``
  to generate ``.dep`` dependency files for the compilation unit.  This can be used
  by external build tools to track these dependencies.
  The ``cythonize`` option was already available in Cython :ref:`0.29.27`.
  Patches by Evgeni Burovski and Eli Schwartz.  (Github issue :issue:`1214`)

* Wheels now include a compiled parser again, which increases their size a little
  but gives about a 10% speed-up when running Cython.

* The wheel building process was migrated to use the ``cibuildwheel`` tool.
  Patch by Thomas Li.  (Github issue :issue:`4736`)

* ``setup.cfg`` was missing from the source distribution.
  (Github issue :issue:`5199`)

* Extended glob paths with ``/**/`` and ``\**\`` for finding source files failed on Windows.

* Coverage analysis failed in projects with a separate source subdirectory.
  Patch by Sviatoslav Sydorenko and Ruben Vorderman.  (Github issue :issue:`3636`)

* Cython could crash when finding import files with dots in their names.
  Patch by Matúš Valo.  (Github issue :issue:`5396`)

* A module loading problem with ``cython.inline()`` on Windows was resolved.


Deprecations
------------

Some older features of Cython have been deprecated. Most notable are the
compile time ``DEF`` and ``IF`` statements, although we emphasise that
they will remain until a good alternative exists for all their use-cases.

Related changes
^^^^^^^^^^^^^^^

* Dotted filenames for qualified module names (``pkg.mod.pyx``) are deprecated.
  Use the normal Python package directory layout instead.
  (Github issue :issue:`2686`)

* "Declaration after use" is now an error for variables.
  Patch by David Woods.  (Github issue :issue:`3976`)

* Variables can no longer be declared with ``cpdef``.
  Patch by David Woods.  (Github issue :issue:`887`)

* The compile-time ``DEF`` and ``IF`` statements are deprecated and generate a warning.
  They should be replaced with normal constants, code generation or C macros.
  (Github issue :issue:`4310`)

* C-style array declarations (``cdef int a[4]``) are now (silently) deprecated in
  favour of the Java-style ``cdef int[4] a`` form.  The latter was always available
  and the Python type declaration syntax already used it exclusively (``a: int[4]``).
  Patch by Matúš Valo.  (Github issue :issue:`5248`)

* The undocumented, untested and apparently useless syntax
  ``from somemodule cimport class/struct/union somename`` was removed.  The type
  modifier is not needed here and a plain ``cimport`` of the name will do.
  (Github issue :issue:`4904`)


Editor support
--------------

Related changes
^^^^^^^^^^^^^^^

* C compiler warnings and errors are now shown in Jupyter notebooks.
  Patch by Egor Dranischnikow.  (Github issue :issue:`3751`)

* An endless loop in ``cython-mode.el`` was resolved.
  Patch by Johannes Mueller.  (Github issue :issue:`3218`)

* The Emacs Cython mode file ``cython-mode.el`` is now maintained in a separate repo:
  https://github.com/cython/emacs-cython-mode

* The C code shown in the annotated HTML output could lack the last C code line(s).


Other changes
-------------

* Memoryviews failed to compile when the ``cache_builtins`` feature was disabled.
  Patch by David Woods.  (Github issue :issue:`3406`)

* Broadcast assignments to a multi-dimensional memory view slice could end
  up in the wrong places when the underlying memory view is known to be
  contiguous but the slice is not.
  (Github issue :issue:`2941`)

* The Pythran ``shape`` attribute is supported.
  Patch by Serge Guelton.  (Github issue :issue:`3307`)

* ``--no-capture`` added to ``runtests.py`` to prevent stdout/stderr capturing
  during srctree tests.
  Patch by Matti Picus.  (Github issue :issue:`2701`)

* Decoding an empty bytes/char* slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3534`)

* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3531`)

* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch.  (Github issue :issue:`1407`)

* Error handling in ``cython.array`` creation was improved to avoid calling
  C-API functions with an error held.

* Error handling early in the module init code could lead to a crash.

* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.

* A reference leak on import failures was resolved.
  Patch by Max Bachmann.  (Github issue :issue:`4056`)

* Casting to ctuples is now allowed.
  Patch by David Woods.  (Github issue :issue:`3808`)

* Some issues were resolved that could lead to duplicated C names.
  Patch by David Woods.  (Github issue :issue:`3716`, :issue:`3741`, :issue:`3734`)

* Inline functions and other code in ``.pxd`` files could accidentally
  inherit the compiler directives of the ``.pyx`` file that imported them.
  Patch by David Woods.  (Github issue :issue:`1071`)

* Parts of the documentation were (and are being) rewritten to show the
  Cython language syntax next to the equivalent Python syntax.
  Patches by 0dminnimda and Matúš Valo.  (Github issue :issue:`4187`)

* A name collision when including multiple generated API header files was resolved.
  Patch by David Woods.  (Github issue :issue:`4308`)

* Very early errors during module initialisation could lead to crashes.
  Patch by David Woods.  (Github issue :issue:`4377`)

* Type errors when passing memory view arguments could leak buffer references.
  Patch by David Woods.  (Github issue :issue:`4296`)

* The GIL can now safely be released inside of ``nogil`` functions (which may actually
  be called with the GIL held at runtime).
  Patch by David Woods.  (Github issue :issue:`4137`)

* The return type of a fused function is no longer ignored for function pointers,
  since it is relevant when passing them e.g. as argument into other fused functions.
  Patch by David Woods.  (Github issue :issue:`4644`)

* Using memoryview arguments in closures of inner functions could lead to ref-counting errors.
  Patch by David Woods.  (Github issue :issue:`4798`)

* Decorators like ``@cfunc`` and ``@ccall`` could leak into nested functions and classes.
  Patch by David Woods.  (Github issue :issue:`4092`)

* Cython now uses a ``.dev0`` version suffix for unreleased source installations.

* The ``Tempita`` module no longer contains HTML processing capabilities, which
  were found to be broken in Python 3.8 and later.
  Patch by Marcel Stimberg.  (Github issue :issue:`3309`)

* Nesting fused types in other fused types could fail to specialise the inner type.
  (Github issue :issue:`4725`)

* Iterating over memoryviews in generator expressions could leak a buffer reference.
  (Github issue :issue:`4968`)

* The C ``float`` type was not inferred on assignments.
  (Github issue :issue:`5234`)

* Type checks for Python's ``memoryview`` type generated incorrect C code.
  (Github issues :issue:`5268`, :issue:`5270`)

* Auto-generated utility code didn't always have all required user defined types available.
  (Github issue :issue:`5269`)

* ``cimport_from_pyx`` could miss some declarations.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5318`)

* For-loops now release the internal reference to their list/tuple iterable before
  instead of after the ``else:`` clause.  This probably has no practical impact.
  (Github issue :issue:`5347`)

* Extension type hierarchies were generated in the wrong order, thus leading to compile issues.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5395`)

* The FAQ page was moved from the GitHub Wiki to the regular documentation
  to make it more visible.


3.0.0 (2023-07-17)
==================

Bugs fixed
----------

* A crash in Python 2.7 was fixed when cleaning up extension type instances
  at program end.


3.0.0 rc 2 (2023-07-13)
=======================

Bugs fixed
----------

* Parser crash on hex/oct enum values.
  (Github issue :issue:`5524`)

* ``cython --version`` now prints the version to both stdout and stderr (unless that is a TTY).
  (Github issue :issue:`5504`)


3.0.0 rc 1 (2023-07-12)
=======================

Features added
--------------

* ``with gil`` and ``with nogil(flag)`` now accept their flag argument also in Python code.
  Patch by Matúš Valo.  (Github issue :issue:`5113`)

* A new decorator ``@cython.with_gil`` is available in Python code to match the ``with gil``
  function declaration in Cython syntax.

* Assigning a list to a ctuple is slightly faster.

Bugs fixed
----------

* The reference counting of memory views involved useless overhead.
  (Github issue :issue:`5510`)

* Duplicate values in a ``cpdef`` enum could lead to invalid switch statements.
  (Github issue :issue:`5400`)

* Handling freshly raised exceptions that didn't have a traceback yet could crash.
  (Github issue :issue:`5495`)

* Reverse iteration in C++ no longer removes the ``const`` qualifier from the item type.
  Patch by Isuru Fernando.  (Github issue :issue:`5478`)

* C++ containers of item type ``bint`` could conflict with those of item type ``int``.
  (Github issue :issue:`5516`)

* With MSVC, Cython no longer enables C-Complex support by accident (which is not supported there).
  (Github issue :issue:`5512`)

* The Python implementation of ``cimport cython.cimports…`` could raise an ``ImportError``
  instead of an ``AttributeError`` when looking up package variable names.
  Patch by Matti Picus.  (Github issue :issue:`5411`)

* Passing a language level and directives on the command line lost the language level setting.
  Patch by Matúš Valo.  (Github issue :issue:`5484`)

* Some typedef declarations for libc function types were fixed.
  (Github issue :issue:`5498`)

* Some C compiler warnings and errors in CPython 3.12 were resolved.

* The deprecated ``_PyGC_FINALIZED()`` C-API macro is no longer used.
  Patch by Thomas Caswell and Matúš Valo.  (Github issue :issue:`5481`)

* A compile error when using ``__debug__`` was resolved.

* A module loading problem with ``cython.inline()`` on Windows was resolved.

* ``cython --version`` now prints the version to stdout instead of stderr.
  (Github issue :issue:`5504`)

* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the :ref:`0.29.36` release.

Other changes
-------------

* The FAQ page was moved from the GitHub Wiki to the regular documentation
  to make it more visible.

* ``np.long_t`` and ``np.ulong_t`` were removed from the NumPy declarations,
  syncing Cython with upstream NumPy v1.25.0.  The aliases were confusing
  since they could mean different things on different platforms.


3.0.0 beta 3 (2023-05-24)
=========================

Features added
--------------

* Custom buffer slot methods are now supported in the Limited C-API of Python 3.9+.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5422`)

* The ``extern "C"`` and ``extern "C++"`` markers that Cython generates for
  ``public`` functions can now be controlled by setting the C macro ``CYTHON_EXTERN_C``.

* The Python ``int`` handling code was adapted to make use of the new ``PyLong``
  internals in CPython 3.12.
  (Github issue :issue:`5353`)

* Conversion of Python ints to C ``int128`` is now always supported, although slow
  if dedicated C-API support is missing (``_PyLong_AsByteArray()``), specifically in
  the Limited C-API.
  (Github issue :issue:`5419`)

* The exception handling code was adapted to CPython 3.12.
  (Github issue :issue:`5442`)

* The dataclass implementation was adapted to support Python 3.12.
  (Github issue :issue:`5346`)

* The normal ``@dataclasses.dataclass`` and ``@functools.total_ordering`` decorators
  can now be used on extension types.  Using the corresponding ``@cython.*`` decorator
  will automatically turn a Python class into an extension type (no need for ``@cclass``).
  (Github issue :issue:`5292`)

* Multiplying a sequence by a C integer avoids creating and intermediate Python integer.

* ctuples can now be assigned from arbitrary sequences, not just Python tuples.

* A new directive ``embedsignature.format`` was added to select the format of the
  docstring embedded signatures between ``python``, ``c`` and argument ``clinic``.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5415`)

* Some invalid directive usages are now detected and rejected, e.g. using ``@ccall``
  together with ``@cfunc``, and applying ``@cfunc`` to a ``@ufunc``.  Cython also
  warns now when a directive is applied needlessly.
  (Github issue :issue:`5399` et al.)

* Unicode identifier names now allow all letters defined in CPython 3.12.

Bugs fixed
----------

* Some C compile failures in CPython 3.12.0a6/a7 were resolved.

* Cascaded comparisons between integer constants and Python types could fail to compile.
  (Github issue :issue:`5354`)

* The internal macro ``__PYX_IS_UNSIGNED`` was accidentally duplicated in beta 2
  which lead to C compile errors.
  Patch by 0dminnimda.  (Github issue :issue:`5356`)

* Memoryviews with typedef item types could fail to match the non-typedef item types.
  Patch by Yue Yang.  (Github issue :issue:`5373`)

* Fused memory views could raise a ``TypeError`` instead of a ``ValueError`` on creation.
  Patch by Matúš Valo.  (Github issue :issue:`5401`)

* Cython could crash when finding import files with dots in their names.
  Patch by Matúš Valo.  (Github issue :issue:`5396`)

* Selecting a context manager in parentheses and then calling it directly failed to parse.
  (Github issue :issue:`5403`)

* ``__qualname__`` and ``__module__`` were not available inside of class bodies.
  (Github issue :issue:`4447`)

* ``noexcept`` was not automatically applied to function pointer attributes in extern structs.
  Patch by Matúš Valo.  (Github issue :issue:`5359`)

* Function signatures containing a type like `tuple[()]` could not be printed.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5355`)

* Extension type hierarchies were generated in the wrong order, thus leading to compile issues.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5395`)

* Using the ``--working`` option could lead to sources not being found.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5365`)

* Some C compiler warnings were resolved.
  Patches by Matt Tyson, Lisandro Dalcin, Philipp Wagner, Matti Picus et al.
  (Github issues :issue:`5417`, :issue:`5418`, :issue:`5421`, :issue:`5437`, :issue:`5438`, :issue:`5443`)

* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the :ref:`0.29.35` release.

Other changes
-------------

* For-loops now release the internal reference to their list/tuple iterable before
  instead of after the ``else:`` clause.  This probably has no practical impact.
  (Github issue :issue:`5347`)

* Simple tuple types like ``(int, int)`` are no longer accepted in Python annotations
  and require the Python notation instead (e.g. ``tuple[cython.int, cython.int]``).
  (Github issue :issue:`5397`)

* The code ``except +nogil`` (declaring a C++ exception handler function called ``nogil``)
  is now rejected because it is almost certainly a typo from ``except + nogil``.
  (Github issue :issue:`5430`)


3.0.0 beta 2 (2023-03-27)
=========================

Features added
--------------

* C++ declarations for ``<cmath>``, ``<numbers>`` and ``std::any`` were added.
  Patches by Jonathan Helgert and Maximilien Colange.
  (Github issues :issue:`5262`, :issue:`5309`, :issue:`5314`)

Bugs fixed
----------

* Unintended internal exception handling lead to a visible performance regression
  for ``nogil`` memoryview code in 3.0.0b1.
  (Github issue :issue:`5324`)

* ``None`` default arguments for arguments with fused memoryview types could select a different
  implementation in 3.0 than in 0.29.x.  The selection behaviour is generally considered
  suboptimal but was at least reverted to the old behaviour for now.
  (Github issue :issue:`5297`)

* The new complex vs. floating point behaviour of the ``**`` power operator accidentally
  added a dependency on the GIL, which was really only required on failures.
  (Github issue :issue:`5287`)

* ``from cython cimport … as …`` could lead to imported names not being found in annotations.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5235`)

* Generated NumPy ufuncs could crash for large arrays due to incorrect GIL handling.
  (Github issue :issue:`5328`)

* Very long Python integer constants could exceed the maximum C name length of MSVC.
  Patch by 0dminnimda.  (Github issue :issue:`5290`)

* ``cimport_from_pyx`` could miss some declarations.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5318`)

* Fully qualified C++ names prefixed by a cimported module name could fail to compile.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5229`)

* Cython generated C++ code accidentally used C++11 features in some cases.
  (Github issue :issue:`5316`)

* Some C++ warnings regarding ``const`` usage in internally generated utility code were resolved.
  Patch by Max Bachmann.  (Github issue :issue:`5301`)

* With ``language_level=2``, imports of modules in packages could return the wrong module in Python 3.
  (Github issue :issue:`5308`)

* ``typing.Optional`` could fail on tuple types.
  (Github issue :issue:`5263`)

* Auto-generated utility code didn't always have all required user defined types available.
  (Github issue :issue:`5269`)

* Type checks for Python's ``memoryview`` type generated incorrect C code.
  (Github issues :issue:`5268`, :issue:`5270`)

* Some issues with ``depfile`` generation were resolved.
  Patches by Eli Schwartz.  (Github issues :issue:`5279`, :issue:`5291`)

* Some C code issue were resolved for the Limited API target.
  (Github issues :issue:`5264`, :issue:`5265`, :issue:`5266`)

* The C code shown in the annotated HTML output could lack the last C code line(s).


3.0.0 beta 1 (2023-02-25)
=========================

Features added
--------------

* Cython implemented C functions now propagate exceptions by default, rather than
  swallowing them in non-object returning function if the user forgot to add an
  ``except`` declaration to the signature.  This was a long-standing source of bugs,
  but can require adding the ``noexcept`` declaration to existing functions if
  exception propagation is really undesired.
  (Github issue :issue:`4280`)

* To opt out of the new, safer exception handling behaviour, legacy code can set the new
  directive ``legacy_implicit_noexcept=True`` for a transition period to keep the
  previous, unsafe behaviour.  This directive will eventually be removed in a later release.
  Patch by Matúš Valo.  (Github issue :issue:`5094`)

* A new function decorator ``@cython.ufunc`` automatically generates a (NumPy) ufunc that
  applies the calculation function to an entire memoryview.
  (Github issue :issue:`4758`)

* The ``**`` power operator now behaves more like in Python by returning the correct complex
  result if required by math.  A new ``cpow`` directive was added to turn on the previous
  C-like behaviour.
  (Github issue :issue:`4936`)

* The special ``__*pow__`` methods now support the 2- and 3-argument variants.
  (Github issue :issue:`5160`)

* Unknown type annotations (e.g. because of typos) now emit a warning at compile time.
  Patch by Matúš Valo.  (Github issue :issue:`5070`)

* Subscripted builtin types in type declarations (like ``list[float]``) are now
  better supported.
  (Github issue :issue:`5058`)

* Python's ``memoryview`` is now a known builtin type with optimised properties.
  (Github issue :issue:`3798`)

* The call-time dispatch for fused memoryview types is less slow.
  (Github issue :issue:`5073`)

* Integer comparisons avoid Python coercions if possible.
  (Github issue :issue:`4821`)

* The Python Enum of a ``cpdef enum`` now inherits from ``IntFlag`` to better match
  both Python and C semantics of enums.
  (Github issue :issue:`2732`)

* `PEP-614 <https://peps.python.org/pep-0614/>`_:
  decorators can now be arbitrary Python expressions.
  (Github issue :issue:`4570`)

* ``cpdef`` enums can now be pickled.
  (Github issue :issue:`5120`)

* Bound C methods can now coerce to Python objects.
  (Github issues :issue:`4890`, :issue:`5062`)

* C arrays can be initialised inside of nogil functions.
  Patch by Matúš Valo.  (Github issue :issue:`1662`)

* ``reversed()`` can now be used together with C++ iteration.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5002`)

* Standard C/C++ atomic operations are now used for memory views, if available.
  (Github issue :issue:`4925`)

* C11 ``complex.h`` is now properly detected.
  (Github issue :issue:`2513`)

* Nested ``cppclass`` definitions are supported.
  Patch by samaingw.  (Github issue :issue:`1218`)

* ``cpp_locals`` no longer have to be "assignable".
  (Github issue :issue:`4558`)

* ``cythonize --help`` now also prints information about the supported environment variables.
  Patch by Matúš Valo.  (Github issue :issue:`1711`)

* Declarations were added for the C++ bit operations, some other parts of C++20 and CPython APIs.
  Patches by Jonathan Helgert, Dobatymo, William Ayd and Max Bachmann.
  (Github issues :issue:`4962`, :issue:`5101`, :issue:`5157`, :issue:`5163`, :issue:`5257`)

Bugs fixed
----------

* Generator expressions and comprehensions now look up their outer-most iterable
  on creation, as Python does, and not later on start, as they did previously.
  (Github issue :issue:`1159`)

* Type annotations for Python ``int`` rejected ``long`` under Py2 in the alpha-11 release.
  They are now ignored again (as always before) when ``language_level=2``, and accept
  both ``int`` and ``long`` in Py2 (and only ``int`` in Py3) otherwise.
  (Github issue :issue:`4944`)

* Calling bound classmethods of builtin types could fail trying to call the unbound method.
  (Github issue :issue:`5051`)

* ``int(Py_UCS4)`` returned the code point instead of the parsed digit value.
  (Github issue :issue:`5216`)

* Several problems with CPython 3.12 were resolved.
  (Github issue :issue:`5238`)

* The C ``float`` type was not inferred on assignments.
  (Github issue :issue:`5234`)

* Memoryviews with ``object`` item type were not supported in Python type declarations.
  (Github issue :issue:`4907`)

* Iterating over memoryviews in generator expressions could leak a buffer reference.
  (Github issue :issue:`4968`)

* Memory views and the internal Cython array type now identify as ``collections.abc.Sequence``
  by setting the ``Py_TPFLAGS_SEQUENCE`` type flag directly.
  (Github issue :issue:`5187`)

* ``__del__`` finaliser methods were not always called if they were only inherited.
  (Github issue :issue:`4995`)

* Extension types are now explicitly marked as immutable types to prevent them from
  being considered mutable.
  Patch by Max Bachmann.  (Github issue :issue:`5023`)

* ``const`` types could not be returned from functions.
  Patch by Mike Graham.  (Github issue :issue:`5135`)

* ``cdef public`` functions declared in .pxd files could use an incorrectly mangled C name.
  Patch by EpigeneMax.  (Github issue :issue:`2940`)

* ``cdef public`` functions used an incorrect linkage declaration in C++.
  Patch by Maximilien Colange.  (Github issue :issue:`1839`)

* C++ post-increment/-decrement operators were not correctly looked up on declared C++
  classes, thus allowing Cython declarations to be missing for them and incorrect C++
  code to be generated.
  Patch by Max Bachmann.  (Github issue :issue:`4536`)

* C++ iteration more safely stores the iterable in temporary variables.
  Patch by Xavier.  (Github issue :issue:`3828`)

* C++ references did not work on fused types.
  (Github issue :issue:`4717`)

* The module state struct was not initialised in correct C (before C23), leading to
  compile errors on Windows.
  Patch by yudonglin.  (Github issue :issue:`5169`)

* Structs that contained an array field resulted in incorrect C code.  Their initialisation
  now uses ``memcpy()``.
  Patch by Chia-Hsiang Cheng.  (Github issue :issue:`5178`)

* Nesting fused types in other fused types could fail to specialise the inner type.
  (Github issue :issue:`4725`)

* The special methods ``__matmul__``, ``__truediv__``, ``__floordiv__`` failed to type
  their ``self`` argument.
  (Github issue :issue:`5067`)

* Coverage analysis failed in projects with a separate source subdirectory.
  Patch by Sviatoslav Sydorenko and Ruben Vorderman.  (Github issue :issue:`3636`)

* The ``annotation_typing`` directive was missing in pure Python mode.
  Patch by 0dminnimda.  (Github issue :issue:`5194`)

* The ``@dataclass`` directive was accidentally inherited by methods and subclasses.
  (Github issue :issue:`4953`)

* Some issues with Cython ``@dataclass`` arguments, hashing, inheritance and ``repr()``
  were resolved.  (Github issues :issue:`4956`, :issue:`5046`)

* ``cpdef`` enums no longer use ``OrderedDict`` but ``dict`` in Python 3.6 and later.
  Patch by GalaxySnail.  (Github issue :issue:`5180`)

* Larger numbers of extension types with multiple subclasses could take very long to compile.
  Patch by Scott Wolchok.  (Github issue :issue:`5139`)

* Relative imports failed in compiled ``__init__.py`` package modules.
  Patch by Matúš Valo.  (Github issue :issue:`3442`)

* Some old usages of the deprecated Python ``imp`` module were replaced with ``importlib``.
  Patch by Matúš Valo.  (Github issue :issue:`4640`)

* The ``cython`` and ``cythonize`` commands ignored non-existing input files without error.
  Patch by Matúš Valo.  (Github issue :issue:`4629`)

* Invalid and misspelled ``cython.*`` module names were not reported as errors.
  (Github issue :issue:`4947`)

* Unused ``**kwargs`` arguments did not show up in ``locals()``.
  (Github issue :issue:`4899`)

* Extended glob paths with ``/**/`` and ``\**\`` for finding source files failed on Windows.

* Annotated HTML generation was missing newlines in 3.0.0a11.
  (Github issue :issue:`4945`)

* Some parser issues were resolved.
  (Github issue :issue:`4992`)

* ``setup.cfg`` was missing from the source distribution.
  (Github issue :issue:`5199`)

* Some C/C++ warnings were resolved.
  Patches by Max Bachmann, Alexander Shadchin, at al.
  (Github issues :issue:`5004`, :issue:`5005`, :issue:`5019`, :issue:`5029`, :issue:`5096`)

* The embedding code no longer calls deprecated C-API functions but uses the new ``PyConfig``
  API instead on CPython versions that support it (3.8+).
  Patch by Alexander Shadchin.  (Github issue :issue:`4895`)

* Intel C compilers could complain about unsupported gcc pragmas.
  Patch by Ralf Gommers.  (Github issue :issue:`5052`)

* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the :ref:`0.29.33` release.

Other changes
-------------

* The undocumented, untested and apparently useless syntax
  ``from somemodule cimport class/struct/union somename`` was removed.  The type
  modifier is not needed here and a plain ``cimport`` of the name will do.
  (Github issue :issue:`4904`)

* C-style array declarations (``cdef int a[4]``) are now (silently) deprecated in
  favour of the Java-style ``cdef int[4] a`` form.  The latter was always available
  and the Python type declaration syntax already used it exclusively (``a: int[4]``).
  Patch by Matúš Valo.  (Github issue :issue:`5248`)

* The wheel building process was migrated to use the ``cibuildwheel`` tool.
  Patch by Thomas Li.  (Github issue :issue:`4736`)

* Wheels now include a compiled parser again, which increases their size a little
  but gives about a 10% speed-up when running Cython.

* The ``Tempita`` module no longer contains HTML processing capabilities, which
  were found to be broken in Python 3.8 and later.
  Patch by Marcel Stimberg.  (Github issue :issue:`3309`)

* The Emacs Cython mode file ``cython-mode.el`` is now maintained in a separate repo:
  https://github.com/cython/emacs-cython-mode

* Cython now uses a ``.dev0`` version suffix for unreleased source installations.


3.0.0 alpha 11 (2022-07-31)
===========================

Features added
--------------

* A new decorator ``@cython.dataclasses.dataclass`` was implemented that provides
  compile time dataclass generation capabilities to ``cdef`` classes (extension types).
  Patch by David Woods.  (Github issue :issue:`2903`).  ``kw_only`` dataclasses
  added by Yury Sokov.  (Github issue :issue:`4794`)

* Named expressions (PEP 572) aka. assignment expressions (aka. the walrus operator
  ``:=``) were implemented.
  Patch by David Woods.  (Github issue :issue:`2636`)

* Context managers can be written in parentheses.
  Patch by David Woods.  (Github issue :issue:`4814`)

* Cython avoids raising ``StopIteration`` in ``__next__`` methods when possible.
  Patch by David Woods.  (Github issue :issue:`3447`)

* Some C++ and CPython library declarations were extended and fixed.
  Patches by Max Bachmann, Till Hoffmann, Julien Jerphanion, Wenjun Si.
  (Github issues :issue:`4530`, :issue:`4528`, :issue:`4710`, :issue:`4746`,
  :issue:`4751`, :issue:`4818`, :issue:`4762`, :issue:`4910`)

* The ``cythonize`` and ``cython`` commands have a new option ``-M`` / ``--depfile``
  to generate ``.dep`` dependency files for the compilation unit.  This can be used
  by external build tools to track these dependencies.
  The ``cythonize`` option was already available in Cython :ref:`0.29.27`.
  Patches by Evgeni Burovski and Eli Schwartz.  (Github issue :issue:`1214`)

* ``cythonize()`` and the corresponding CLI command now regenerate the output files
  also when they already exist but were generated by a different Cython version.

* Memory views and the internal Cython array type now identify as ``collections.abc.Sequence``.
  Patch by David Woods.  (Github issue :issue:`4817`)

* Cython generators and coroutines now identify as ``CO_ASYNC_GENERATOR``,
  ``CO_COROUTINE`` and ``CO_GENERATOR`` accordingly.
  (Github issue :issue:`4902`)

* Memory views can use atomic CPU instructions instead of locks in more cases.
  Patch by Sam Gross.  (Github issue :issue:`4912`)

* The environment variable ``CYTHON_FORCE_REGEN=1`` can be used to force ``cythonize``
  to regenerate the output files regardless of modification times and changes.

* A new Cython build option ``--cython-compile-minimal`` was added to compile only a
  smaller set of Cython's own modules, which can be used to reduce the package
  and install size.

* Improvements to ``PyTypeObject`` definitions in pxd wrapping of libpython.
  Patch by John Kirkham. (Github issue :issue:`4699`)


Bugs fixed
----------

* Decorators like ``@cfunc`` and ``@ccall`` could leak into nested functions and classes.
  Patch by David Woods.  (Github issue :issue:`4092`)

* Exceptions within for-loops that run over memoryviews could lead to a ref-counting error.
  Patch by David Woods.  (Github issue :issue:`4662`)

* Using memoryview arguments in closures of inner functions could lead to ref-counting errors.
  Patch by David Woods.  (Github issue :issue:`4798`)

* Several optimised string methods failed to accept ``None`` as arguments to their options.
  Test patch by Kirill Smelkov.  (Github issue :issue:`4737`)

* A regression in 3.0.0a10 was resolved that prevented property setter methods from
  having the same name as their value argument.
  Patch by David Woods.  (Github issue :issue:`4836`)

* Typedefs for the ``bint`` type did not always behave like ``bint``.
  Patch by Nathan Manville and 0dminnimda.  (Github issue :issue:`4660`)

* The return type of a fused function is no longer ignored for function pointers,
  since it is relevant when passing them e.g. as argument into other fused functions.
  Patch by David Woods.  (Github issue :issue:`4644`)

* The ``__self__`` attribute of fused functions reports its availability correctly
  with ``hasattr()``.  Patch by David Woods.
  (Github issue :issue:`4808`)

* ``pyximport`` no longer uses the deprecated ``imp`` module.
  Patch by Matúš Valo.  (Github issue :issue:`4560`)

* ``pyximport`` failed for long filenames on Windows.
  Patch by Matti Picus.  (Github issue :issue:`4630`)

* The generated C code failed to compile in CPython 3.11a4 and later.
  (Github issue :issue:`4500`)

* A case of undefined C behaviour was resolved in the list slicing code.
  Patch by Richard Barnes.  (Github issue :issue:`4734`)

* Using the Limited API could report incorrect line numbers in tracebacks.

* A work-around for StacklessPython < 3.8 was disabled in Py3.8 and later.
  (Github issue :issue:`4329`)

* Improve conversion between function pointers with non-identical but
  compatible exception specifications.  Patches by David Woods.
  (Github issues :issue:`4770`, :issue:`4689`)

* The runtime size check for imported ``PyVarObject`` types was improved
  to reduce false positives and adapt to Python 3.11.
  Patch by David Woods.  (Github issues :issue:`4827`, :issue:`4894`)

* The generated modules no longer import NumPy internally when using
  fused types but no memoryviews.
  Patch by David Woods.  (Github issue :issue:`4935`)

* Improve compatibility with forthcoming CPython 3.12 release.

* Limited API C preprocessor warning is compatible with MSVC. Patch by
  Victor Molina Garcia.  (Github issue :issue:`4826`)

* Some C compiler warnings were fixed.
  Patch by mwtian.  (Github issue :issue:`4831`)

* The parser allowed some invalid spellings of ``...``.
  Patch by 0dminnimda.  (Github issue :issue:`4868`)

* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the :ref:`0.29.32` release.

Other changes
-------------

* When using type annotations, ``func(x: list)`` or ``func(x: ExtType)`` (and other
  Python builtin or extension types) no longer allow ``None`` as input argument to ``x``.
  This is consistent with the normal typing semantics in Python, and was a common gotcha
  for users who did not expect ``None`` to be allowed as input.  To allow ``None``, use
  ``typing.Optional`` as in ``func(x: Optional[list])``.  ``None`` is also automatically
  allowed when it is used as default argument, i.e. ``func(x: list = None)``.
  ``int`` and ``float`` are now also recognised in type annotations and restrict the
  value type at runtime.  They were previously ignored.
  Note that, for backwards compatibility reasons, the new behaviour does not apply when using
  Cython's C notation, as in ``func(list x)``.  Here, ``None`` is still allowed, as always.
  Also, the ``annotation_typing`` directive can now be enabled and disabled more finely
  within the module.
  (Github issues :issue:`3883`, :issue:`2696`, :issue:`4669`, :issue:`4606`, :issue:`4886`)

* The compile-time ``DEF`` and ``IF`` statements are deprecated and generate a warning.
  They should be replaced with normal constants, code generation or C macros.
  (Github issue :issue:`4310`)

* Reusing an extension type attribute name as a method name is now an error.
  Patch by 0dminnimda.  (Github issue :issue:`4661`)

* Improve compatibility between classes pickled in Cython 3.0 and 0.29.x
  by accepting MD5, SHA-1 and SHA-256 checksums.
  (Github issue :issue:`4680`)


3.0.0 alpha 10 (2022-01-06)
===========================

Features added
--------------

* ``Cython.Distutils.build_ext`` now uses ``cythonize()`` internally (previously
  known as ``new_build_ext``), while still supporting the options that were
  available in the old implementation (``old_build_ext``).
  Patch by Matúš Valo.  (Github issue :issue:`3541`)

* ``pyximport`` now uses ``cythonize()`` internally.
  Patch by Matúš Valo.  (Github issue :issue:`2304`)

* ``__del__(self)`` on extension types now maps to ``tp_finalize`` in Python 3.
  Original patch by ax487.  (Github issue :issue:`3612`)

* Conversion from Python dict to C++ map now supports arbitrary Python mappings,
  not just dicts.

* Direct assignments to C++ references are now allowed.
  Patch by David Woods.  (Github issue :issue:`1863`)

* An initial set of adaptations for GraalVM Python was implemented.  Note that
  this does not imply any general support for this target or that your code
  will work at all in this environment.  But testing should be possible now.
  Patch by David Woods.  (Github issue :issue:`4328`)

* ``PyMem_[Raw]Calloc()`` was added to the ``cpython.mem`` declarations.
  Note that the ``Raw`` versions are no longer #defined by Cython.  The previous
  macros were not considered safe.
  Patch by William Schwartz and David Woods.  (Github issue :issue:`3047`)

Bugs fixed
----------

* Circular imports of compiled modules could fail needlessly even when the import
  could already be resolved from ``sys.modules``.
  Patch by Syam Gadde.  (Github issue :issue:`4390`)

* The GIL can now safely be released inside of ``nogil`` functions (which may actually
  be called with the GIL held at runtime).
  Patch by David Woods.  (Github issue :issue:`4137`)

* Type errors when passing memory view arguments could leak buffer references.
  Patch by David Woods.  (Github issue :issue:`4296`)

* Cython did not type the ``self`` argument in special binary methods.
  Patch by David Woods.  (Github issue :issue:`4434`)

* An incompatibility with recent coverage.py versions was resolved.
  Patch by David Woods.  (Github issue :issue:`4440`)

* Fused typed default arguments generated incorrect code.
  Patch by David Woods.  (Github issue :issue:`4413`)

* ``prange`` loops generated incorrect code when ``cpp_locals`` is enabled.
  Patch by David Woods.  (Github issue :issue:`4354`)

* A C-level compatibility issue with recent NumPy versions was resolved.
  Patch by David Woods.  (Github issue :issue:`4396`)

* Decorators on inner functions were not evaluated in the right scope.
  Patch by David Woods.  (Github issue :issue:`4367`)

* Very early errors during module initialisation could lead to crashes.
  Patch by David Woods.  (Github issue :issue:`4377`)

* Fused functions were binding unnecessarily, which prevented them from being pickled.
  Patch by David Woods.  (Github issue :issue:`4370`)

* Some constant tuples containing strings were not deduplicated.
  Patch by David Woods.  (Github issue :issue:`4353`)

* Unsupported decorators on cdef functions were not rejected in recent releases.
  Patch by David Woods.  (Github issue :issue:`4322`)

* The excess arguments in a for-in-range loop with more than 3 arguments to `range()`
  were silently ignored.
  Original patch by Max Bachmann. (Github issue :issue:`4550`)

* Python object types were not allowed as ``->`` return type annotations.
  Patch by Matúš Valo.  (Github issue :issue:`4433`)

* Default values for memory views arguments were not properly supported.
  Patch by Corentin Cadiou.  (Github issue :issue:`4313`)

* Templating C++ classes with memory view types lead to buggy code and is now rejected.
  Patch by David Woods.  (Github issue :issue:`3085`)

* Several C++ library declarations were added and fixed.
  Patches by Dobatymo, account-login, Jonathan Helgert, Evgeny Yakimov, GalaxySnail, Max Bachmann.
  (Github issues :issue:`4408`, :issue:`4419`, :issue:`4410`, :issue:`4395`,
  :issue:`4423`, :issue:`4448`, :issue:`4462`, :issue:`3293`, :issue:`4522`,
  :issue:`2171`, :issue:`4531`)

* Some compiler problems and warnings were resolved.
  Patches by David Woods, 0dminnimda, Nicolas Pauss and others.
  (Github issues :issue:`4317`, :issue:`4324`, :issue:`4361`, :issue:`4357`)

* The ``self`` argument of static methods in .pxd files was incorrectly typed.
  Patch by David Woods.  (Github issue :issue:`3174`)

* A name collision when including multiple generated API header files was resolved.
  Patch by David Woods.  (Github issue :issue:`4308`)

* An endless loop in ``cython-mode.el`` was resolved.
  Patch by Johannes Mueller.  (Github issue :issue:`3218`)

* ``_Py_TPFLAGS_HAVE_VECTORCALL`` was always set on extension types when using the limited API.
  Patch by David Woods.  (Github issue :issue:`4453`)

* Some compatibility issues with PyPy were resolved.
  Patches by Max Bachmann, Matti Picus.
  (Github issues :issue:`4454`, :issue:`4477`, :issue:`4478`, :issue:`4509`, :issue:`4517`)

* A compiler crash when running Cython thread-parallel from distutils was resolved.
  (Github issue :issue:`4503`)

* Includes all bug-fixes from the :ref:`0.29.26` release.

Other changes
-------------

* A warning was added when ``__defaults__`` or ``__kwdefaults__`` of Cython compiled
  functions were re-assigned, since this does not current have an effect.
  Patch by David Woods.  (Github issue :issue:`2650`)


3.0.0 alpha 9 (2021-07-21)
==========================

Features added
--------------

* Declarations for ``libcpp.algorithms``, ``libcpp.set`` and ``libcpp.unordered_set``
  were extended.
  Patch by David Woods.  (Github issues :issue:`4271`, :issue:`4273`)

* ``cygdb`` has a new option ``--skip-interpreter`` that allows using a different
  Python runtime than the one used to generate the debugging information.
  Patch by Alessandro Molina.  (Github issue :issue:`4186`)

Bugs fixed
----------

* Several issues with the new ``cpp_locals`` directive were resolved and
  its test coverage improved.
  Patch by David Woods.  (Github issues :issue:`4266`, :issue:`4265`)

* Generated utility code for C++ conversions no longer depends on several user
  definable directives that may make it behave incorrectly.
  Patch by David Woods.  (Github issue :issue:`4206`)

* A reference counting bug in the new ``@cython.total_ordering`` decorator was fixed.

* Includes all bug-fixes from the :ref:`0.29.24` release.

Other changes
-------------

* Parts of the documentation were (and are being) rewritten to show the
  Cython language syntax next to the equivalent Python syntax.
  Patches by 0dminnimda and Matúš Valo.  (Github issue :issue:`4187`)


3.0.0 alpha 8 (2021-07-02)
==========================

Features added
--------------

* A ``@cython.total_ordering`` decorator has been added to automatically
  implement all comparison operators, similar to ``functools.total_ordering``.
  Patch by Spencer Brown.  (Github issue :issue:`2090`)

* A new directive ``cpp_locals`` was added that allows local C++ variables to
  be lazily initialised (without default constructor), thus making them behave
  more like Python variables.
  Patch by David Woods.  (Github issue :issue:`4160`)

* C++17 execution policies are supported in ``libcpp.algorithm``.
  Patch by Ashwin Srinath.  (Github issue :issue:`3790`)

* New C feature flags: ``CYTHON_USE_MODULE_STATE``, ``CYTHON_USE_TYPE_SPECS``
  Both are currently considered experimental.
  (Github issue :issue:`3611`)

* ``[...] * N`` is optimised for C integer multipliers ``N``.
  (Github issue :issue:`3922`)

Bugs fixed
----------

* The dispatch code for binary operators to special methods could run into infinite recursion.
  Patch by David Woods.  (Github issue :issue:`4172`)

* Code optimisations were not applied to methods of Cython implemented C++ classes.
  Patch by David Woods.  (Github issue :issue:`4212`)

* The special ``cython`` module was not always detected in PEP-484 type annotations.
  Patch by David Woods.  (Github issue :issue:`4243`)

* Conversion from Python dicts to ``std::map`` was broken.
  Patch by David Woods and Mikkel Skofelt.  (Github issues :issue:`4231`, :issue:`4228`)

* The exception handling annotation ``except +*`` was broken.
  Patch by David Woods.  (Github issues :issue:`3065`, :issue:`3066`)

* Attribute annotations in Python classes are now ignored, because they are
  just Python objects in a dict (as opposed to the fields of extension types).
  Patch by David Woods.  (Github issues :issue:`4196`, :issue:`4198`)

* An unnecessary slow-down at import time was removed from ``Cython.Distutils``.
  Original patch by Anthony Sottile.  (Github issue :issue:`4224`)

* Python modules were not automatically recompiled when only their ``.pxd`` file changed.
  Patch by Golden Rockefeller.  (Github issue :issue:`1428`)

* The signature of ``PyFloat_FromString()`` in ``cpython.float`` was changed
  to match the signature in Py3.  It still has an automatic fallback for Py2.
  (Github issue :issue:`3909`)

* A compile error on MSVC was resolved.
  Patch by David Woods.  (Github issue :issue:`4202`)

* A C compiler warning in PyPy3 regarding ``PyEval_EvalCode()`` was resolved.

* Directives starting with ``optimization.*`` in pure Python mode were incorrectly named.
  It should have been ``optimize.*``.
  Patch by David Woods.  (Github issue :issue:`4258`)

Other changes
-------------

* Variables can no longer be declared with ``cpdef``.
  Patch by David Woods.  (Github issue :issue:`887`)

* Support for the now unsupported Pyston V1 was removed in favour of Pyston V2.
  Patch by Marius Wachtler.  (Github issue :issue:`4211`)

* The ``Cython.Build.BuildExecutable`` tool no longer executes the program automatically.
  Use ``cythonrun`` for that.


3.0.0 alpha 7 (2021-05-24)
==========================

Features added
--------------

* A ``cimport`` is now supported in pure Python code by prefixing the
  imported module name with ``cython.cimports.``, e.g.
  ``from cython.cimports.libc.math import sin``.
  (GIthub issue :issue:`4190`)

* ``__class_getitem__`` (`PEP-560`_) is supported for cdef classes.
  Patch by Kmol Yuan.  (Github issue :issue:`3764`)

* ``__mro_entries__`` (`PEP-560`_) is supported for Python classes.
  Patch by David Woods.  (Github issue :issue:`3537`)

* ``cython.array`` supports simple, non-strided views.
  (Github issue :issue:`3775`)

* Self-documenting f-strings (``=``) were implemented.
  Patch by davfsa.  (Github issue :issue:`3796`)

* The destructor is now called for fields in C++ structs.
  Patch by David Woods.  (Github issue :issue:`3226`)

* ``std::move()`` is now also called for temps during ``yield``.
  Patch by Yu Feng.  (Github issue :issue:`4154`)

* ``asyncio.iscoroutinefunction()`` now recognises coroutine functions
  also when compiled by Cython.
  Patch by Pedro Marques da Luz.  (Github issue :issue:`2273`)

* C compiler warnings and errors are now shown in Jupyter notebooks.
  Patch by Egor Dranischnikow.  (Github issue :issue:`3751`)

* ``float(…)`` is optimised for string arguments (str/bytes/bytearray).

* Converting C++ containers to Python lists uses less memory allocations.
  Patch by Max Bachmann.  (Github issue :issue:`4081`)

* Docstrings of ``cpdef`` enums are now copied to the enum class.
  Patch by matham.  (Github issue :issue:`3805`)

* The type ``cython.Py_hash_t`` is available in Python mode.

* C-API declarations for ``cpython.fileobject`` were added.
  Patch by Zackery Spytz.  (Github issue :issue:`3906`)

* C-API declarations for context variables in Python 3.7 were added.
  Original patch by Zolisa Bleki.  (Github issue :issue:`2281`)

* More C-API declarations for ``cpython.datetime``  were added.
  Patch by Bluenix2.  (Github issue :issue:`4128`)

* A new module ``cpython.time`` was added with some low-level alternatives to
  Python's ``time`` module.
  Patch by Brock Mendel.  (Github issue :issue:`3767`)

* The value ``PyBUF_MAX_NDIM`` was added to the ``cpython.buffer`` module.
  Patch by John Kirkham.  (Github issue :issue:`3811`)

* "Declaration after use" is now an error for variables.
  Patch by David Woods.  (Github issue :issue:`3976`)

* More declarations for C++ string methods were added.

* Cython now detects when existing output files were not previously generated
  by itself and refuses to overwrite them.  It is a common mistake to name
  the module file of a wrapper after the library (source file) that it wraps,
  which can lead to surprising errors when the file gets overwritten.

Bugs fixed
----------

* Annotations were not exposed on annotated (data-)classes.
  Patch by matsjoyce.  (Github issue :issue:`4151`)

* Inline functions and other code in ``.pxd`` files could accidentally
  inherit the compiler directives of the ``.pyx`` file that imported them.
  Patch by David Woods.  (Github issue :issue:`1071`)

* Some issues were resolved that could lead to duplicated C names.
  Patch by David Woods.  (Github issue :issue:`3716`, :issue:`3741`, :issue:`3734`)

* Modules with unicode names failed to build on Windows.
  Patch by David Woods.  (Github issue :issue:`4125`)

* ``ndarray.shape`` failed to compile with Pythran and recent NumPy.
  Patch by Serge Guelton.  (Github issue :issue:`3762`)

* Casting to ctuples is now allowed.
  Patch by David Woods.  (Github issue :issue:`3808`)

* Structs could not be instantiated with positional arguments in
  pure Python mode.

* Literal list assignments to pointer variables declared in PEP-526
  notation failed to compile.

* Nested C++ types were not usable through ctypedefs.
  Patch by Vadim Pushtaev.  (Github issue :issue:`4039`)

* Overloaded C++ static methods were lost.
  Patch by Ashwin Srinath.  (Github :issue:`1851`)

* Cython compiled functions always provided a ``__self__`` attribute,
  regardless of being used as a method or not.
  Patch by David Woods.  (Github issue :issue:`4036`)

* Calls to ``.__class__()`` of a known extension type failed.
  Patch by David Woods.  (Github issue :issue:`3954`)

* Generator expressions in pxd-overridden ``cdef`` functions could
  fail to compile.
  Patch by Matúš Valo.  (Github issue :issue:`3477`)

* A reference leak on import failures was resolved.
  Patch by Max Bachmann.  (Github issue :issue:`4056`)

* A C compiler warning about unused code was resolved.
  (Github issue :issue:`3763`)

* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue :issue:`2749`)

* Some C compiler warninge were resolved.
  Patches by Max Bachmann.  (Github issue :issue:`4053`, :issue:`4059`, :issue:`4054`, :issue:`4148`, :issue:`4162`)

* A compile failure for C++ enums in Py3.4 / MSVC was resolved.
  Patch by Ashwin Srinath.  (Github issue :issue:`3782`)

* Some C++ STL methods did not propagate exceptions.
  Patch by Max Bachmann.  (Github issue :issue:`4079`)

* An unsupported C-API call in PyPy was fixed.
  Patch by Max Bachmann.  (Github issue :issue:`4055`)

* The Cython ``CodeWriter`` mishandled no-argument ``return`` statements.
  Patch by Tao He.  (Github issue :issue:`3795`)

* ``complex`` wasn't supported in PEP-484 type annotations.
  Patch by David Woods.  (Github issue :issue:`3949`)

* Default arguments of methods were not exposed for introspection.
  Patch by Vladimir Matveev.  (Github issue :issue:`4061`)

* Extension types inheriting from Python classes could not safely
  be exposed in ``.pxd``  files.
  (Github issue :issue:`4106`)

* The profiling/tracing code was adapted to work with Python 3.10b1.

* The internal CPython macro ``Py_ISSPACE()`` is no longer used.
  Original patch by Andrew Jones.  (Github issue :issue:`4111`)

* Includes all bug-fixes from the :ref:`0.29.23` release.


3.0.0 alpha 6 (2020-07-31)
==========================

Features added
--------------

* Special methods for binary operators now follow Python semantics.
  Rather than e.g. a single ``__add__`` method for cdef classes, where
  "self" can be either the first or second argument, one can now define
  both ``__add__`` and ``__radd__`` as for standard Python classes.
  This behavior can be disabled with the ``c_api_binop_methods`` directive
  to return to the previous semantics in Cython code (available from Cython
  0.29.20), or the reversed method (``__radd__``) can be implemented in
  addition to an existing two-sided operator method (``__add__``) to get a
  backwards compatible implementation.
  (Github issue :issue:`2056`)

* No/single argument functions now accept keyword arguments by default in order
  to comply with Python semantics.  The marginally faster calling conventions
  ``METH_NOARGS`` and ``METH_O`` that reject keyword arguments are still available
  with the directive ``@cython.always_allow_keywords(False)``.
  (Github issue :issue:`3090`)

* For-in-loop iteration over ``bytearray`` and memory views is optimised.
  Patch by David Woods.  (Github issue :issue:`2227`)

* Type inference now works for memory views and slices.
  Patch by David Woods.  (Github issue :issue:`2227`)

* The ``@returns()`` decorator propagates exceptions by default for suitable C
  return types when no ``@exceptval()`` is defined.
  (Github issues :issue:`3625`, :issue:`3664`)

* A low-level inline function ``total_seconds(timedelta)`` was added to
  ``cpython.datetime`` to bypass the Python method call.  Note that this function
  is not guaranteed to give exactly the same results for very large time intervals.
  Patch by Brock Mendel.  (Github issue :issue:`3616`)

* Type inference now understands that ``a, *b = x`` assigns a list to ``b``.

* Limited API support was improved.
  Patches by Matthias Braun.  (Github issues :issue:`3693`, :issue:`3707`)

* The Cython ``CodeWriter`` can now handle more syntax constructs.
  Patch by Tao He.  (Github issue :issue:`3514`)

Bugs fixed
----------

* The construct ``for x in cpp_function_call()`` failed to compile.
  Patch by David Woods.  (Github issue :issue:`3663`)

* C++ references failed to compile when used as Python object indexes.
  Patch by David Woods.  (Github issue :issue:`3754`)

* The C++ ``typeid()`` function was allowed in C mode.
  Patch by Celelibi.  (Github issue :issue:`3637`)

* ``repr()`` was assumed to return ``str`` instead of ``unicode`` with ``language_level=3``.
  (Github issue :issue:`3736`)

* Includes all bug-fixes from the :ref:`0.29.21` release.

Other changes
-------------

* The ``numpy`` declarations were updated.
  Patch by Brock Mendel.  (Github issue :issue:`3630`)

* The names of Cython's internal types (functions, generator, coroutine, etc.)
  are now qualified with the module name of the internal Cython module that is
  used for sharing them across Cython implemented modules, for example
  ``_cython_3_0a5.coroutine``.  This was done to avoid making them look like
  homeless builtins, to help with debugging, and in order to avoid a CPython
  warning according to https://bugs.python.org/issue20204

3.0.0 alpha 5 (2020-05-19)
==========================

Features added
--------------

* ``.pxd`` files can now be :ref:`versioned <versioning>` by adding an
  extension like "``.cython-30.pxd``" to prevent older Cython versions (than
  3.0 in this case) from picking them up.  (Github issue :issue:`3577`)

* Several macros/functions declared in the NumPy API are now usable without
  holding the GIL.

* `libc.math` was extended to include all C99 function declarations.
  Patch by Dean Scarff.  (Github issue :issue:`3570`)

Bugs fixed
----------

* Several issues with arithmetic overflow handling were resolved, including
  undefined behaviour in C.
  Patch by Sam Sneddon.  (Github issue :issue:`3588`)

* The improved GIL handling in ``nogil`` functions introduced in 3.0a3
  could fail to acquire the GIL in some cases on function exit.
  (Github issue :issue:`3590` etc.)

* A reference leak when processing keyword arguments in Py2 was resolved,
  that appeared in 3.0a1.
  (Github issue :issue:`3578`)

* The outdated getbuffer/releasebuffer implementations in the NumPy
  declarations were removed so that buffers declared as ``ndarray``
  now use the normal implementation in NumPy.

* Includes all bug-fixes from the :ref:`0.29.18` release.


3.0.0 alpha 4 (2020-05-05)
==========================

Features added
--------------

* The ``print`` statement (not the ``print()`` function) is allowed in
  ``nogil`` code without an explicit ``with gil`` section.

* The ``assert`` statement is allowed in ``nogil`` sections.  Here, the GIL is
  only acquired if the ``AssertionError`` is really raised, which means that the
  evaluation of the asserted condition only allows C expressions.

* Cython generates C compiler branch hints for unlikely user defined if-clauses
  in more cases, when they end up raising exceptions unconditionally. This now
  includes exceptions being raised in ``nogil``/``with gil`` sections.

* Some internal memoryview functions were tuned to reduce object overhead.

Bugs fixed
----------

* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.

* Error handling early in the module init code could lead to a crash.

* Error handling in ``cython.array`` creation was improved to avoid calling
  C-API functions with an error held.

* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch.  (Github issue :issue:`1407`)

* When importing the old Cython ``build_ext`` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha.  (Github issue :issue:`2209`)

* The improved GIL handling in ``nogil`` functions introduced in 3.0a3
  could generate invalid C code.
  (Github issue :issue:`3558`)

* ``PyEval_InitThreads()`` is no longer used in Py3.7+ where it is a no-op.

* Parallel builds of Cython itself (``setup.py build_ext -j N``) failed on Windows.

Other changes
-------------

* The C property feature has been rewritten and now requires C property methods
  to be declared ``inline`` (:issue:`3571`).


3.0.0 alpha 3 (2020-04-27)
==========================

Features added
--------------

* ``nogil`` functions now avoid acquiring the GIL on function exit if possible
  even if they contain ``with gil`` blocks.
  (Github issue :issue:`3554`)

* Python private name mangling now falls back to unmangled names for non-Python
  globals, since double-underscore names are not uncommon in C.  Unmangled Python
  names are also still found as a legacy fallback but produce a warning.
  Patch by David Woods.  (Github issue :issue:`3548`)

Bugs fixed
----------

* Includes all bug-fixes from the :ref:`0.29.17` release.


3.0.0 alpha 2 (2020-04-23)
==========================

Features added
--------------

* ``std::move()`` is now used in C++ mode for internal temp variables to
  make them work without copying values.
  Patch by David Woods.  (Github issues :issue:`3253`, :issue:`1612`)

* ``__class_getitem__`` is supported for types on item access (`PEP-560`_).
  Patch by msg555.  (Github issue :issue:`2753`)

* The simplified Py3.6 customisation of class creation is implemented (`PEP-487`_).
  (Github issue :issue:`2781`)

* Conditional blocks in Python code that depend on ``cython.compiled`` are
  eliminated at an earlier stage, which gives more freedom in writing
  replacement Python code.
  Patch by David Woods.  (Github issue :issue:`3507`)

* ``numpy.import_array()`` is automatically called if ``numpy`` has been cimported
  and it has not been called in the module code.  This is intended as a hidden
  fail-safe so user code should continue to call ``numpy.import_array``.
  Patch by David Woods.  (Github issue :issue:`3524`)

* The Cython AST code serialiser class ``CodeWriter`` in ``Cython.CodeWriter``
  supports more syntax nodes.

* The fastcall/vectorcall protocols are used for several internal Python calls.
  (Github issue :issue:`3540`)

Bugs fixed
----------

* With ``language_level=3/3str``, Python classes without explicit base class
  are now new-style (type) classes also in Py2.  Previously, they were created
  as old-style (non-type) classes.
  (Github issue :issue:`3530`)

* C++ ``typeid()`` failed for fused types.
  Patch by David Woods.  (Github issue :issue:`3203`)

* ``__arg`` argument names in methods were not mangled with the class name.
  Patch by David Woods.  (Github issue :issue:`1382`)

* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3531`)

* Decoding an empty bytes/char* slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3534`)

* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods.  (Github issues :issue:`3430`, :issue:`3522`)

* Several C compiler warnings were fixed.


3.0.0 alpha 1 (2020-04-12)
==========================

Features added
--------------

* Cython functions now use the `PEP-590`_ vectorcall protocol in Py3.7+.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2263`)

* Unicode identifiers are supported in Cython code (`PEP-3131`_).
  Patch by David Woods.  (Github issue :issue:`2601`)

* Unicode module names and imports are supported.
  Patch by David Woods.  (Github issue :issue:`3119`)

* Annotations are no longer parsed, keeping them as strings following `PEP-563`_.
  Patch by David Woods.  (Github issue :issue:`3285`)

* Preliminary support for the CPython's ``Py_LIMITED_API`` (stable ABI) is
  available by setting the  ``CYTHON_LIMITED_API`` C macro.  Note that the
  support is currently in an early stage and many features do not yet work.
  You currently still have to define ``Py_LIMITED_API`` externally in order
  to restrict the API usage.  This will change when the feature stabilises.
  Patches by Eddie Elizondo and David Woods.  (Github issues :issue:`3223`,
  :issue:`3311`, :issue:`3501`)

* The dispatch to fused functions is now linear in the number of arguments,
  which makes it much faster, often 2x or more, and several times faster for
  larger fused types with many specialisations.
  Patch by will-ca.  (Github issue :issue:`1385`)

* ``with gil/nogil`` statements can be conditional based on compile-time
  constants, e.g. fused type checks.
  Patch by Noam Hershtig.  (Github issue :issue:`2579`)

* ``const`` can be used together with fused types.
  Patch by Thomas Vincent.  (Github issue :issue:`1772`)

* Reimports of already imported modules are substantially faster.
  (Github issue :issue:`2854`)

* Positional-only arguments are supported in Python functions (`PEP-570`_).
  Patch by Josh Tobin.  (Github issue :issue:`2915`)

* The ``volatile`` C modifier is supported in Cython code.
  Patch by Jeroen Demeyer.  (Github issue :issue:`1667`)

* ``@cython.trashcan(True)`` can be used on an extension type to enable the
  CPython :ref:`trashcan`. This allows deallocating deeply recursive objects
  without overflowing the stack. Patch by Jeroen Demeyer.  (Github issue :issue:`2842`)

* Inlined properties can be defined for external extension types.
  Patch by Matti Picus. (Github issue :issue:`2640`, redone later in :issue:`3571`)

* The ``str()`` builtin now calls ``PyObject_Str()`` instead of going
  through a Python call.
  Patch by William Ayd.  (Github issue :issue:`3279`)

* String concatenation can now happen in place if possible, by extending the
  existing string rather than always creating a new one.
  Patch by David Woods.  (Github issue :issue:`3453`)

* Multiplication of Python numbers with small constant integers is faster.
  (Github issue :issue:`2808`)

* Some list copying is avoided internally when a new list needs to be created
  but we already have a fresh one.
  (Github issue :issue:`3494`)

* Extension types that do not need their own ``tp_new`` implementation (because
  they have no object attributes etc.) directly inherit the implementation of
  their parent type if possible.
  (Github issue :issue:`1555`)

* The attributes ``gen.gi_frame`` and ``coro.cr_frame`` of Cython compiled
  generators and coroutines now return an actual frame object for introspection.
  (Github issue :issue:`2306`)

* Several declarations in ``cpython.*``, ``libc.*`` and ``libcpp.*`` were added.
  Patches by Jeroen Demeyer, Matthew Edwards, Chris Gyurgyik, Jerome Kieffer
  and Zackery Spytz.
  (Github issues :issue:`3468`, :issue:`3332`, :issue:`3202`, :issue:`3188`,
  :issue:`3179`, :issue:`2891`, :issue:`2826`, :issue:`2713`)

* Deprecated NumPy API usages were removed from ``numpy.pxd``.
  Patch by Matti Picus.  (Github issue :issue:`3365`)

* ``cython.inline()`` now sets the ``NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION``
  C macro automatically when ``numpy`` is imported in the code, to avoid C compiler
  warnings about deprecated NumPy C-API usage.

* The builtin ``abs()`` function can now be used on C numbers in nogil code.
  Patch by Elliott Sales de Andrade.  (Github issue :issue:`2748`)

* `PEP-479`_ (``generator_stop``) is now enabled by default with language level 3.
  (Github issue :issue:`2580`)

* The ``cython.view.array`` type supports inheritance.
  Patch by David Woods.  (Github issue :issue:`3413`)

* Code annotation accepts a new debugging argument ``--annotate-fullc`` that
  will include the complete syntax highlighted C file in the HTML output.
  (Github issue :issue:`2855`)

* ``--no-capture`` added to ``runtests.py`` to prevent stdout/stderr capturing
  during srctree tests.
  Patch by Matti Picus.  (Github issue :issue:`2701`)

* ``--no-docstrings`` option added to ``cythonize`` script.
  Original patch by mo-han.  (Github issue :issue:`2889`)

* ``cygdb`` gives better error messages when it fails to initialise the
  Python runtime support in gdb.
  Patch by Volker Weissmann.  (Github issue :issue:`3489`)

* The Pythran ``shape`` attribute is supported.
  Patch by Serge Guelton.  (Github issue :issue:`3307`)

Bugs fixed
----------

* The unicode methods ``.upper()``, ``.lower()`` and ``.title()`` were
  incorrectly optimised for single character input values and only returned
  the first character if multiple characters should have been returned.
  They now use the original Python methods again.

* Fused argument types were not correctly handled in type annotations and
  ``cython.locals()``.
  Patch by David Woods.  (Github issues :issue:`3391`, :issue:`3142`)

* Diverging from the usual behaviour, ``len(memoryview)``, ``len(char*)``
  and ``len(Py_UNICODE*)`` returned an unsigned ``size_t`` value.  They now
  return a signed ``Py_ssize_t``, like other usages of ``len()``.

* Nested dict literals in function call kwargs could incorrectly raise an
  error about duplicate keyword arguments, which are allowed when passing
  them from dict literals.
  (Github issue :issue:`2963`)

* Item access (subscripting) with integer indices/keys always tried the
  Sequence protocol before the Mapping protocol, which diverged from Python
  semantics.  It now passes through the Mapping protocol first when supported.
  (Github issue :issue:`1807`)

* Name lookups in class bodies no longer go through an attribute lookup.
  Patch by Jeroen Demeyer.  (Github issue :issue:`3100`)

* Broadcast assignments to a multi-dimensional memory view slice could end
  up in the wrong places when the underlying memory view is known to be
  contiguous but the slice is not.
  (Github issue :issue:`2941`)

* Pickling unbound methods of Python classes failed.
  Patch by Pierre Glaser.  (Github issue :issue:`2972`)

* The ``Py_hash_t`` type failed to accept arbitrary "index" values.
  (Github issue :issue:`2752`)

* The first function line number of functions with decorators pointed to the
  signature line and not the first decorator line, as in Python.
  Patch by Felix Kohlgrüber.  (Github issue :issue:`2536`)

* Constant integer expressions that used a negative exponent were evaluated
  as integer 0 instead of the expected float value.
  Patch by Kryštof Pilnáček.  (Github issue :issue:`2133`)

* The ``cython.declare()`` and ``cython.cast()`` functions could fail in pure mode.
  Patch by Dmitry Shesterkin.  (Github issue :issue:`3244`)

* ``__doc__`` was not available inside of the class body during class creation.
  (Github issue :issue:`1635`)

* Setting ``language_level=2`` in a file did not work if ``language_level=3``
  was enabled globally before.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2791`)

* ``__init__.pyx`` files were not always considered as package indicators.
  (Github issue :issue:`2665`)

* Compiling package ``__init__`` files could fail under Windows due to an
  undefined export symbol.  (Github issue :issue:`2968`)

* A C compiler cast warning was resolved.
  Patch by Michael Buesch.  (Github issue :issue:`2775`)

* Binding staticmethods of Cython functions were not behaving like Python methods.
  Patch by Jeroen Demeyer.  (Github issue :issue:`3106`, :issue:`3102`)

* Memoryviews failed to compile when the ``cache_builtins`` feature was disabled.
  Patch by David Woods.  (Github issue :issue:`3406`)

Other changes
-------------

* The default language level was changed to ``3str``, i.e. Python 3 semantics,
  but with ``str`` literals (also in Python 2.7).  This is a backwards incompatible
  change from the previous default of Python 2 semantics.  The previous behaviour
  is available through the directive ``language_level=2``.
  (Github issue :issue:`2565`)

* Cython no longer generates ``__qualname__`` attributes for classes in Python
  2.x since they are problematic there and not correctly maintained for subclasses.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2772`)

* Source file fingerprinting now uses SHA-1 instead of MD5 since the latter
  tends to be slower and less widely supported these days.
  (Github issue :issue:`2790`)

* The long deprecated include files ``python_*``, ``stdio``, ``stdlib`` and
  ``stl`` in ``Cython/Includes/Deprecated/`` were removed.  Use the ``libc.*``
  and ``cpython.*`` pxd modules instead.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2904`)

* The search order for include files was changed. Previously it was
  ``include_directories``, ``Cython/Includes``, ``sys.path``. Now it is
  ``include_directories``, ``sys.path``, ``Cython/Includes``. This was done to
  allow third-party ``*.pxd`` files to override the ones in Cython.
  Patch by Matti Picus.  (Github issue :issue:`2905`)

* The command line parser was rewritten and modernised using ``argparse``.
  Patch by Egor Dranischnikow.  (Github issue :issue:`2952`, :issue:`3001`)

* Dotted filenames for qualified module names (``pkg.mod.pyx``) are deprecated.
  Use the normal Python package directory layout instead.
  (Github issue :issue:`2686`)

* Binary Linux wheels now follow the manylinux2010 standard.
  Patch by Alexey Stepanov.  (Github issue :issue:`3355`)

* Support for Python 2.6 was removed.

.. _`PEP-560`: https://www.python.org/dev/peps/pep-0560
.. _`PEP-570`: https://www.python.org/dev/peps/pep-0570
.. _`PEP-487`: https://www.python.org/dev/peps/pep-0487
.. _`PEP-590`: https://www.python.org/dev/peps/pep-0590
.. _`PEP-3131`: https://www.python.org/dev/peps/pep-3131
.. _`PEP-563`: https://www.python.org/dev/peps/pep-0563
.. _`PEP-479`: https://www.python.org/dev/peps/pep-0479


.. _0.29.37:

0.29.37 (2023-12-18)
====================

Bugs fixed
----------

* Fix a potential crash while cleaning up subtypes of externally imported extension
  types when terminating Python.  This was introduced in Cython 0.29.35.

* Fix a ``complex`` related compile error on Windows.
  (Github issue :issue:`5512`)

* Compiling fused types used in pxd files could crash Cython in Python 3.11+.
  (Github issues :issue:`5894`, :issue:`5588`)

* ``cythonize`` failed to consider the ``CYTHON_FORCE_REGEN`` env variable.
  Patch by Harmen Stoppels.  (Github issue :issue:`5712`)


.. _0.29.36:

0.29.36 (2023-07-04)
====================

Bugs fixed
----------

* Async generators lost their return value in PyPy.
  (Github issue :issue:`5465`)

* The outdated C macro ``_PyGC_FINALIZED()`` is no longer used in Py3.9+.

* The deprecated ``Py_OptimizeFlag`` is no longer used in Python 3.9+.
  (Github issue :issue:`5343`)

* Using the global ``__debug__`` variable but not assertions could lead to compile errors.

* The broken HTML template support was removed from Tempita.
  (Github issue :issue:`3309`)


.. _0.29.35:

0.29.35 (2023-05-24)
====================

Bugs fixed
----------

* A garbage collection enabled subtype of a non-GC extension type could call into the
  deallocation function of the super type with GC tracking enabled.  This could lead
  to crashes during deallocation if GC was triggered on the type at the same time.
  (Github issue :issue:`5432`)

* Some C compile failures and crashes in CPython 3.12 were resolved.

* ``except + nogil`` was syntactically not allowed.
  ``except +nogil`` (i.e. defining a C++ exception handling function called ``nogil``)
  is now disallowed to prevent typos.
  (Github issue :issue:`5430`)

* A C compile failure in PyPy 3.10 was resolved.
  Patch by Matti Picus.  (Github issue :issue:`5408`)

* Cython modules now use PEP-489 multi-phase init by default in PyPy 3.9 and later.
  Original patch by Matti Picus.  (Github issue :issue:`5413`)

* API header files generated by different Cython versions can now be included in the
  same C file.
  (Github issue :issue:`5383`)

* Function signatures containing a type like `tuple[()]` could not be printed.
  Patch by Lisandro Dalcin.  (Github issue :issue:`5355`)


.. _0.29.34:

0.29.34 (2023-04-02)
====================

Bugs fixed
----------

* A reference leak of the for-loop list/tuple iterable was resolved if the for-loop's
  ``else:`` branch executes a ``break`` for an outer loop.
  (Github issue :issue:`5347`)

* Some C compile failures in CPython 3.12 were resolved.

* Some old usages of the deprecated Python ``imp`` module were replaced with ``importlib``.
  Patch by Matúš Valo.  (Github issue :issue:`5300`)

* Some issues with ``depfile`` generation were resolved.
  Patches by Eli Schwartz.  (Github issues :issue:`5279`, :issue:`5291`)


.. _0.29.33:

0.29.33 (2023-01-06)
====================

Features added
--------------

* The ``cythonize`` and ``cython`` commands have a new option ``-M`` / ``--depfile``
  to generate ``.dep`` dependency files for the compilation unit.  This can be used
  by external build tools to track these dependencies.
  The ``cythonize`` option was already available in Cython :ref:`0.29.27`.
  Patches by Evgeni Burovski and Eli Schwartz.  (Github issue :issue:`1214`)

Bugs fixed
----------

* ``const`` fused types could not be used with memory views.
  Patch by Thomas Vincent.  (Github issue :issue:`1772`)

* ``wstr`` usage was removed in Python 3.12 and later (PEP-623).
  (Github issue :issue:`5145`)

* A type check assertion for Cython functions failed in debug Python builds.
  (Github issue :issue:`5031`)

* Fixed various compiler warnings.
  Patches by Lisandro Dalcin et al.  (Github issues :issue:`4948`, :issue:`5086`)

* Fixed error when calculating complex powers of negative numbers.
  (Github issue :issue:`5014`)

* Corrected a small mis-formatting of exception messages on Python 2.
  (Github issue :issue:`5018`)

* The ``PyUnicode_AsUTF8AndSize()`` C-API function was missing from the CPython declarations.
  (Github issue :issue:`5163`)

* A performance problem in the compiler was resolved when nesting conditional expressions.
  (Github issue :issue:`5197`)

* Test suite problems with recent NumPy and CPython versions were resolved.
  (Github issues :issue:`5183`, :issue:`5190`)

Other changes
-------------

* The undocumented, untested and apparently useless syntax
  ``from somemodule cimport class/struct/union somename`` was deprecated
  in anticipation of its removal in Cython 3.  The type
  modifier is not needed here and a plain ``cimport`` of the name will do.
  (Github issue :issue:`4905`)

* Properly disable generation of descriptor docstrings on PyPy since they cause crashes.
  It was previously disabled, but only accidentally via a typo.
  Patch by Matti Picus.  (Github issue :issue:`5083`)

* The ``cpow`` directive of Cython 3.0 is available as a no-op.
  (Github issue :issue:`5016`)


.. _0.29.32:

0.29.32 (2022-07-29)
====================

Bugs fixed
----------

* Revert "Using memoryview typed arguments in inner functions is now rejected as unsupported."
  Patch by David Woods.  (Github issue :issue:`4798`)

* ``from module import *`` failed in 0.29.31 when using memoryviews.
  Patch by David Woods.  (Github issue :issue:`4927`)


.. _0.29.31:

0.29.31 (2022-07-27)
====================

Features added
--------------

* A new argument ``--module-name`` was added to the ``cython`` command to
  provide the (one) exact target module name from the command line.
  Patch by Matthew Brett and h-vetinari.  (Github issue :issue:`4906`)

* A new keyword ``noexcept`` was added for forward compatibility with Cython 3.
  Patch by David Woods.  (Github issue :issue:`4903`)

Bugs fixed
----------

* Use ``importlib.util.find_spec()`` instead of the deprecated ``importlib.find_loader()``
  function when setting up the package path at import-time.
  Patch by Matti Picus.  (Github issue :issue:`4764`)

* Require the C compiler to support the two-arg form of ``va_start``
  on Python 3.10 and higher.
  Patch by Thomas Caswell.  (Github issue :issue:`4820`)

* Make ``fused_type`` subscriptable in Shadow.py.
  Patch by Pfebrer.  (Github issue :issue:`4842`)

* Fix the incorrect code generation of the target type in ``bytearray`` loops.
  Patch by Kenrick Everett.  (Github issue :issue:`4108`)

* Atomic refcounts for memoryviews were not used on some GCC versions by accident.
  Patch by Sam Gross.  (Github issue :issue:`4915`)

* Silence some GCC ``-Wconversion`` warnings in C utility code.
  Patch by Lisandro Dalcin.  (Github issue :issue:`4854`)

* Tuple multiplication was ignored in expressions such as ``[*(1,) * 2]``.
  Patch by David Woods.  (Github issue :issue:`4864`)

* Calling ``append`` methods on extension types could fail to find the method
  in some cases.
  Patch by David Woods.  (Github issue :issue:`4828`)

* Ensure that object buffers (e.g. ``ndarray[object, ndim=1]``) containing
  ``NULL``  pointers are safe to use, returning ``None`` instead of the ``NULL``
  pointer.
  Patch by Sebastian Berg.  (Github issue :issue:`4859`)

* Using memoryview typed arguments in inner functions is now rejected as unsupported.
  Patch by David Woods.  (Github issue :issue:`4798`)

* Compilation could fail on systems (e.g. FIPS) that block MD5 checksums at runtime.
  (Github issue :issue:`4909`)

* Experimental adaptations for the CPython "nogil" fork was added.
  Note that there is no official support for this in Cython 0.x.
  Patch by Sam Gross.  (Github issue :issue:`4912`)


.. _0.29.30:

0.29.30 (2022-05-16)
====================

Bugs fixed
----------

* The GIL handling changes in 0.29.29 introduced a regression where
  objects could be deallocated without holding the GIL.
  (Github issue :issue:`4796`)


.. _0.29.29:

0.29.29 (2022-05-16)
====================

Features added
--------------

* Avoid acquiring the GIL at the end of nogil functions.
  This change was backported in order to avoid generating wrong C code
  that would trigger C compiler warnings with tracing support enabled.
  Backport by Oleksandr Pavlyk.  (Github issue :issue:`4637`)

Bugs fixed
----------

* Function definitions in ``finally:`` clauses were not correctly generated.
  Patch by David Woods.  (Github issue :issue:`4651`)

* A case where C-API functions could be called with a live exception set was fixed.
  Patch by Jakub Kulík.  (Github issue :issue:`4722`)

* Pickles can now be exchanged again with those generated from Cython 3.0 modules.
  (Github issue :issue:`4680`)

* Cython now correctly generates Python methods for both the provided regular and
  reversed special numeric methods of extension types.
  Patch by David Woods.  (Github issue :issue:`4750`)

* Calling unbound extension type methods without arguments could raise an
  ``IndexError`` instead of a ``TypeError``.
  Patch by David Woods.  (Github issue :issue:`4779`)

* Calling unbound ``.__contains__()`` super class methods on some builtin base
  types could trigger an infinite recursion.
  Patch by David Woods.  (Github issue :issue:`4785`)

* The C union type in pure Python mode mishandled some field names.
  Patch by Jordan Brière.  (Github issue :issue:`4727`)

* Allow users to overwrite the C macro ``_USE_MATH_DEFINES``.
  Patch by Yuriy Chernyshov. (Github issue :issue:`4690`)

* Improved compatibility with CPython 3.10/11.
  Patches by Thomas Caswell, David Woods.
  (Github issues :issue:`4609`, :issue:`4667`, :issue:`4721`, :issue:`4730`, :issue:`4777`)

* Docstrings of descriptors are now provided in PyPy 7.3.9.
  Patch by Matti Picus.  (Github issue :issue:`4701`)


.. _0.29.28:

0.29.28 (2022-02-17)
====================

Bugs fixed
----------

* Due to backwards incompatible changes in CPython 3.11a4, the feature flags
  ``CYTHON_FAST_THREAD_STATE`` and ``CYTHON_USE_EXC_INFO_STACK`` are now disabled
  in Python 3.11 and later.  They are enabled again in Cython 3.0.
  Patch by David Woods.  (Github issue :issue:`4610`)

* A C compiler warning in older PyPy versions was resolved.
  Patch by Matti Picus.  (Github issue :issue:`4236`)


.. _0.29.27:

0.29.27 (2022-01-28)
====================

Features added
--------------

* The ``cythonize`` command has a new option ``-M`` to generate ``.dep`` dependency
  files for the compilation unit.  This can be used by external build tools to track
  these dependencies.
  Patch by Evgeni Burovski.  (Github issue :issue:`1214`)

Bugs fixed
----------

* Compilation failures on PyPy were resolved.
  Patches by Matti Picus.  (Github issues :issue:`4509`, :issue:`4517`)

* Calls to ``range()`` with more than three arguments did not fail.
  Original patch by Max Bachmann.  (Github issue :issue:`4550`)

* Some C compiler warnings about missing type struct initialisers in Py3.10 were resolved.

* Cython no longer warns about using OpenMP 3.0 features since they are now
  considered generally available.


.. _0.29.26:

0.29.26 (2021-12-16)
====================

Bugs fixed
----------

* An incompatibility with CPython 3.11.0a3 was resolved.
  (Github issue :issue:`4499`)

* The ``in`` operator failed on literal lists with starred expressions.
  Patch by Arvind Natarajan.  (Github issue :issue:`3938`)

* A C compiler warning in PyPy about a missing struct field initialisation was resolved.


.. _0.29.25:

0.29.25 (2021-12-06)
====================

Bugs fixed
----------

* Several incompatibilities with CPython 3.11 were resolved.
  Patches by David Woods, Victor Stinner, Thomas Caswell.
  (Github issues :issue:`4411`, :issue:`4414`, :issue:`4415`, :issue:`4416`, :issue:`4420`,
  :issue:`4428`, :issue:`4473`, :issue:`4479`, :issue:`4480`)

* Some C compiler warnings were resolved.
  Patches by Lisandro Dalcin and others.  (Github issue :issue:`4439`)

* C++ ``std::move()`` should only be used automatically in MSVC versions that support it.
  Patch by Max Bachmann.  (Github issue :issue:`4191`)

 * The ``Py_hash_t`` type failed to accept arbitrary "index" values.
   (Github issue :issue:`2752`)

* Avoid copying unaligned 16-bit values since some platforms require them to be aligned.
  Use memcpy() instead to let the C compiler decide how to do it.
  (Github issue :issue:`4343`)

* Cython crashed on invalid truthiness tests on C++ types without ``operator bool``.
  Patch by David Woods.  (Github issue :issue:`4348`)

* The declaration of ``PyUnicode_CompareWithASCIIString()`` in ``cpython.unicode`` was incorrect.
  Patch by Max Bachmann.  (Github issue :issue:`4344`)


.. _0.29.24:

0.29.24 (2021-07-14)
====================

Bugs fixed
----------

* Inline functions in pxd files that used memory views could lead to invalid
  C code if the module that imported from them does not use memory views.
  Patch by David Woods.  (Github issue :issue:`1415`)

* Several declarations in ``libcpp.string`` were added and corrected.
  Patch by Janek Bevendorff.  (Github issue :issue:`4268`)

* Pickling unbound Cython compiled methods failed.
  Patch by Pierre Glaser.  (Github issue :issue:`2972`)

* The tracing code was adapted to work with CPython 3.10.

* The optimised ``in`` operator failed on unicode strings in Py3.9 and later
  that were constructed from an external ``wchar_t`` source.
  Also, related C compiler warnings about deprecated C-API usage were resolved.
  (Github issue :issue:`3925`)

* Some compiler crashes were resolved.
  Patch by David Woods.  (Github issues :issue:`4214`, :issue:`2811`)

* An incorrect warning about 'unused' generator expressions was removed.
  (GIthub issue :issue:`1699`)

* The attributes ``gen.gi_frame`` and ``coro.cr_frame`` of Cython compiled
  generators and coroutines now return an actual frame object for introspection,
  instead of ``None``.
  (Github issue :issue:`2306`)


.. _0.29.23:

0.29.23 (2021-04-14)
====================

Bugs fixed
----------

* Some problems with Python 3.10 were resolved.
  Patches by Victor Stinner and David Woods.  (Github issues :issue:`4046`, :issue:`4100`)

* An incorrect "optimisation" was removed that allowed changes to a keyword
  dict to leak into keyword arguments passed into a function.
  Patch by Peng Weikang.  (Github issue :issue:`3227`)

* Multiplied str constants could end up as bytes constants with language_level=2.
  Patch by Alphadelta14 and David Woods.  (Github issue :issue:`3951`)

* ``PY_SSIZE_T_CLEAN`` does not get defined any more if it is already defined.
  Patch by Andrew Jones.  (Github issue :issue:`4104`)


.. _0.29.22:

0.29.22 (2021-02-20)
====================

Features added
--------------

* Some declarations were added to the provided pxd includes.
  Patches by Zackery Spytz and John Kirkham.
  (Github issues :issue:`3811`, :issue:`3882`, :issue:`3899`, :issue:`3901`)

Bugs fixed
----------

* A crash when calling certain functions in Py3.9 and later was resolved.
  (Github issue :issue:`3917`)

* ``const`` memory views of structs failed to compile.
  (Github issue :issue:`2251`)

* ``const`` template declarations could not be nested.
  Patch by Ashwin Srinath.  (Github issue :issue:`1355`)

* The declarations in the ``cpython.pycapsule`` module were missing their
  ``const`` modifiers and generated incorrect C code.
  Patch by Warren Weckesser.  (Github issue :issue:`3964`)

* Casts to memory views failed for fused dtypes.
  Patch by David Woods.  (Github issue :issue:`3881`)

* ``repr()`` was assumed to return ``str`` instead of ``unicode`` with ``language_level=3``.
  (Github issue :issue:`3736`)

* Calling ``cpdef`` functions from cimported modules crashed the compiler.
  Patch by David Woods.  (Github issue :issue:`4000`)

* Cython no longer validates the ABI size of the NumPy classes it compiled against.
  See the discussion in https://github.com/numpy/numpy/pull/432

* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue :issue:`2749`)

* Coverage reporting in the annotated HTML file failed in Py3.9.
  Patch by Nick Pope.  (Github issue :issue:`3865`)

* The embedding code now reports Python errors as exit status.

* Long type declarations could lead to (harmless) random changes in the
  C file when used in auto-generated Python wrappers or pickled classes.

Other changes
-------------

* Variables defined as ``cpdef`` now generate a warning since this
  is currently useless and thus does not do what users would expect.
  Patch by David Woods.  (Github issue :issue:`3959`)


.. _0.29.21:

0.29.21 (2020-07-09)
====================

Bugs fixed
----------

* Fix a regression in 0.29.20 where ``__div__`` failed to be found in extension types.
  (Github issue :issue:`3688`)

* Fix a regression in 0.29.20 where a call inside of a finally clause could fail to compile.
  Patch by David Woods.  (Github issue :issue:`3712`)

* Zero-sized buffers could fail to validate as C/Fortran-contiguous.
  Patch by Clemens Hofreither.  (Github issue :issue:`2093`)

* ``exec()`` did not allow recent Python syntax features in Py3.8+ due to
  https://bugs.python.org/issue35975.
  (Github issue :issue:`3695`)

* Binding staticmethods of Cython functions were not behaving like Python methods in Py3.
  Patch by Jeroen Demeyer and Michał Górny.  (Github issue :issue:`3106`)

* Pythran calls to NumPy methods no longer generate useless method lookup code.

* The ``PyUnicode_GET_LENGTH()`` macro was missing from the ``cpython.*`` declarations.
  Patch by Thomas Caswell.  (Github issue :issue:`3692`)

* The deprecated ``PyUnicode_*()`` C-API functions are no longer used, except for Unicode
  strings that contain lone surrogates.  Unicode strings that contain non-BMP characters
  or surrogate pairs now generate different C code on 16-bit Python 2.x Unicode deployments
  (such as MS-Windows).  Generating the C code on Python 3.x is recommended in this case.
  Original patches by Inada Naoki and Victor Stinner.
  (Github issues :issue:`3677`, :issue:`3721`, :issue:`3697`)

* Some template parameters were missing from the C++ ``std::unordered_map`` declaration.
  Patch by will.  (Github issue :issue:`3685`)

* Several internal code generation issues regarding temporary variables were resolved.
  (Github issue :issue:`3708`)


.. _0.29.20:

0.29.20 (2020-06-10)
====================

Bugs fixed
----------

* Nested try-except statements with multiple ``return`` statements could crash
  due to incorrect deletion of the ``except as`` target variable.
  (Github issue :issue:`3666`)

* The ``@classmethod`` decorator no longer rejects unknown input from other decorators.
  Patch by David Woods.  (Github issue :issue:`3660`)

* Fused types could leak into unrelated usages.
  Patch by David Woods.  (Github issue :issue:`3642`)

* Now uses ``Py_SET_SIZE()`` and ``Py_SET_REFCNT()`` in Py3.9+ to avoid low-level
  write access to these object fields.
  Patch by Victor Stinner.  (Github issue :issue:`3639`)

* The built-in ``abs()`` function could lead to undefined behaviour when used on
  the negative-most value of a signed C integer type.
  Patch by Serge Guelton.  (Github issue :issue:`1911`)

* Usages of ``sizeof()`` and ``typeid()`` on uninitialised variables no longer
  produce a warning.
  Patch by Celelibi.  (Github issue :issue:`3575`)

* The C++ ``typeid()`` function was allowed in C mode.
  Patch by Celelibi.  (Github issue :issue:`3637`)

* The error position reported for errors found in f-strings was misleading.
  (Github issue :issue:`3674`)

* The new ``c_api_binop_methods`` directive was added for forward compatibility, but can
  only be set to True (the current default value).  It can be disabled in Cython 3.0.


.. _0.29.19:

0.29.19 (2020-05-20)
====================

Bugs fixed
----------

* A typo in Windows specific code in 0.29.18 was fixed that broke "libc.math".
  (Github issue :issue:`3622`)

* A platform specific test failure in 0.29.18 was fixed.
  Patch by smutch.  (Github issue :issue:`3620`)


.. _0.29.18:

0.29.18 (2020-05-18)
====================

Bugs fixed
----------

* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.

* Error handling early in the module init code could lead to a crash.

* Error handling in ``cython.array`` creation was improved to avoid calling
  C-API functions with an error held.

* A memory corruption was fixed when garbage collection was triggered during calls
  to ``PyType_Ready()`` of extension type subclasses.
  (Github issue :issue:`3603`)

* Memory view slicing generated unused error handling code which could negatively
  impact the C compiler optimisations for parallel OpenMP code etc.  Also, it is
  now helped by static branch hints.
  (Github issue :issue:`2987`)

* Cython's built-in OpenMP functions were not translated inside of call arguments.
  Original patch by Celelibi and David Woods.  (Github issue :issue:`3594`)

* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch.  (Github issue :issue:`1407`)

* Decorators were not allowed on nested `async def` functions.
  (Github issue :issue:`1462`)

* C-tuples could use invalid C struct casting.
  Patch by MegaIng.  (Github issue :issue:`3038`)

* Optimised ``%d`` string formatting into f-strings failed on float values.
  (Github issue :issue:`3092`)

* Optimised aligned string formatting (``%05s``, ``%-5s``) failed.
  (Github issue :issue:`3476`)

* When importing the old Cython ``build_ext`` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha.  (Github issue :issue:`2209`)

* When using the ``CYTHON_NO_PYINIT_EXPORT`` option in C++, the module init function
  was not declared as ``extern "C"``.
  (Github issue :issue:`3414`)

* Three missing timedelta access macros were added in ``cpython.datetime``.

* The signature of the NumPy C-API function ``PyArray_SearchSorted()`` was fixed.
  Patch by Brock Mendel.  (Github issue :issue:`3606`)


.. _0.29.17:

0.29.17 (2020-04-26)
====================

Features added
--------------

* ``std::move()`` is now available from ``libcpp.utility``.
  Patch by Omer Ozarslan.  (Github issue :issue:`2169`)

* The ``@cython.binding`` decorator is available in Python code.
  (Github issue :issue:`3505`)

Bugs fixed
----------

* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3531`)

* Decoding an empty bytes/char* slice with large bounds could crash.
  Patch by Sam Sneddon.  (Github issue :issue:`3534`)

* Re-importing a Cython extension no longer raises the error
  "``__reduce_cython__ not found``".
  (Github issue :issue:`3545`)

* Unused C-tuples could generate incorrect code in 0.29.16.
  Patch by Kirk Meyer.  (Github issue :issue:`3543`)

* Creating a fused function attached it to the garbage collector before it
  was fully initialised, thus risking crashes in rare failure cases.
  Original patch by achernomorov.  (Github issue :issue:`3215`)

* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods.  (Github issues :issue:`3430`, :issue:`3522`)

* The compilation cache in ``cython.inline("…")`` failed to take the language
  level into account.
  Patch by will-ca.  (Github issue :issue:`3419`)

* The deprecated ``PyUnicode_GET_SIZE()`` function is no longer used in Py3.


.. _0.29.16:

0.29.16 (2020-03-24)
====================

Bugs fixed
----------

* Temporary internal variables in nested prange loops could leak into other
  threads.  Patch by Frank Schlimbach.  (Github issue :issue:`3348`)

* Default arguments on fused functions could crash.
  Patch by David Woods.  (Github issue :issue:`3370`)

* C-tuples declared in ``.pxd`` files could generate incomplete C code.
  Patch by Kirk Meyer.  (Github issue :issue:`1427`)

* Fused functions were not always detected and optimised as Cython
  implemented functions.
  Patch by David Woods.  (Github issue :issue:`3384`)

* Valid Python object concatenation of (iterable) strings to non-strings
  could fail with an exception.
  Patch by David Woods.  (Github issue :issue:`3433`)

* Using C functions as temporary values lead to invalid C code.
  Original patch by David Woods.  (Github issue :issue:`3418`)

* Fix an unhandled C++ exception in comparisons.
  Patch by David Woods.  (Github issue :issue:`3361`)

* Fix deprecated import of "imp" module.
  Patch by Matti Picus.  (Github issue :issue:`3350`)

* Fix compatibility with Pythran 0.9.6 and later.
  Patch by Serge Guelton.  (Github issue :issue:`3308`)

* The ``_Py_PyAtExit()`` function in ``cpython.pylifecycle`` was misdeclared.
  Patch by Zackery Spytz.  (Github issue :issue:`3382`)

* Several missing declarations in ``cpython.*`` were added.
  Patches by Zackery Spytz.  (Github issue :issue:`3452`, :issue:`3421`, :issue:`3411`, :issue:`3402`)

* A declaration for ``libc.math.fpclassify()`` was added.
  Patch by Zackery Spytz.  (Github issue :issue:`2514`)

* Avoid "undeclared" warning about automatically generated pickle methods.
  Patch by David Woods.  (Github issue :issue:`3353`)

* Avoid C compiler warning about unreachable code in ``prange()``.

* Some C compiler warnings in PyPy were resolved.
  Patch by Matti Picus.  (Github issue :issue:`3437`)


.. _0.29.15:


0.29.15 (2020-02-06)
====================

Bugs fixed
----------

* Crash when returning a temporary Python object from an async-def function.
  (Github issue :issue:`3337`)

* Crash when using ``**kwargs`` in generators.
  Patch by David Woods.  (Github issue :issue:`3265`)

* Double reference free in ``__class__`` cell handling for ``super()`` calls.
  (Github issue :issue:`3246`)

* Compile error when using ``*args`` as Python class bases.
  (Github issue :issue:`3338`)

* Import failure in IPython 7.11.
  (Github issue :issue:`3297`)

* Fixed C name collision in the auto-pickle code.
  Patch by ThePrez.  (Github issue :issue:`3238`)

* Deprecated import failed in Python 3.9.
  (Github issue :issue:`3266`)


.. _0.29.14:

0.29.14 (2019-11-01)
====================

Bugs fixed
----------

* The generated code failed to initialise the ``tp_print`` slot in CPython 3.8.
  Patches by Pablo Galindo and Orivej Desh.  (Github issues :issue:`3171`, :issue:`3201`)

* ``?`` for ``bool`` was missing from the supported NumPy dtypes.
  Patch by Max Klein.  (Github issue :issue:`2675`)

* ``await`` was not allowed inside of f-strings.
  Patch by Dmitro Getz.  (Github issue :issue:`2877`)

* Coverage analysis failed for projects where the code resides in separate
  source sub-directories.
  Patch by Antonio Valentino.  (Github issue :issue:`1985`)

* An incorrect compiler warning was fixed in automatic C++ string conversions.
  Patch by Gerion Entrup.  (Github issue :issue:`3108`)

* Error reports in the Jupyter notebook showed unhelpful stack traces.
  Patch by Matthew Edwards (Github issue :issue:`3196`).

* ``Python.h`` is now also included explicitly from ``public`` header files.
  (Github issue :issue:`3133`).

* Distutils builds with ``--parallel`` did not work when using Cython's
  deprecated ``build_ext`` command.
  Patch by Alphadelta14 (Github issue :issue:`3187`).

Other changes
-------------

* The ``PyMemoryView_*()`` C-API is available in ``cpython.memoryview``.
  Patch by Nathan Manville.  (Github issue :issue:`2541`)


0.29.13 (2019-07-26)
====================

Bugs fixed
----------

* A reference leak for ``None`` was fixed when converting a memoryview
  to a Python object.  (Github issue :issue:`3023`)

* The declaration of ``PyGILState_STATE`` in ``cpython.pystate`` was unusable.
  Patch by Kirill Smelkov.  (Github issue :issue:`2997`)

Other changes
-------------

* The declarations in ``posix.mman`` were extended.
  Patches by Kirill Smelkov.  (Github issues :issue:`2893`, :issue:`2894`, :issue:`3012`)


0.29.12 (2019-07-07)
====================

Bugs fixed
----------

* Fix compile error in CPython 3.8b2 regarding the ``PyCode_New()`` signature.
  (Github issue :issue:`3031`)

* Fix a C compiler warning about a missing ``int`` downcast.
  (Github issue :issue:`3028`)

* Fix reported error positions of undefined builtins and constants.
  Patch by Orivej Desh.  (Github issue :issue:`3030`)

* A 32 bit issue in the Pythran support was resolved.
  Patch by Serge Guelton.  (Github issue :issue:`3032`)


0.29.11 (2019-06-30)
====================

Bugs fixed
----------

* Fix compile error in CPython 3.8b2 regarding the ``PyCode_New()`` signature.
  Patch by Nick Coghlan. (Github issue :issue:`3009`)

* Invalid C code generated for lambda functions in cdef methods.
  Patch by Josh Tobin.  (Github issue :issue:`2967`)

* Support slice handling in newer Pythran versions.
  Patch by Serge Guelton.  (Github issue :issue:`2989`)

* A reference leak in power-of-2 calculation was fixed.
  Patch by Sebastian Berg.  (Github issue :issue:`3022`)

* The search order for include files was changed. Previously it was
  ``include_directories``, ``Cython/Includes``, ``sys.path``. Now it is
  ``include_directories``, ``sys.path``, ``Cython/Includes``. This was done to
  allow third-party ``*.pxd`` files to override the ones in Cython.
  Original patch by Matti Picus.  (Github issue :issue:`2905`)

* Setting ``language_level=2`` in a file did not work if ``language_level=3``
  was enabled globally before.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2791`)


0.29.10 (2019-06-02)
====================

Bugs fixed
----------

* Fix compile errors in CPython 3.8b1 due to the new "tp_vectorcall" slots.
  (Github issue :issue:`2976`)


0.29.9 (2019-05-29)
===================

Bugs fixed
----------

* Fix a crash regression in 0.29.8 when creating code objects fails.

* Remove an incorrect cast when using true-division in C++ operations.
  (Github issue :issue:`1950`)


0.29.8 (2019-05-28)
===================

Bugs fixed
----------

* C compile errors with CPython 3.8 were resolved.
  Patch by Marcel Plch.  (Github issue :issue:`2938`)

* Python tuple constants that compare equal but have different item
  types could incorrectly be merged into a single constant.
  (Github issue :issue:`2919`)

* Non-ASCII characters in unprefixed strings could crash the compiler when
  used with language level ``3str``.

* Starred expressions in %-formatting tuples could fail to compile for
  unicode strings.  (Github issue :issue:`2939`)

* Passing Python class references through ``cython.inline()`` was broken.
  (Github issue :issue:`2936`)


0.29.7 (2019-04-14)
===================

Bugs fixed
----------

* Crash when the shared Cython config module gets unloaded and another Cython
  module reports an exceptions.  Cython now makes sure it keeps an owned reference
  to the module.
  (Github issue :issue:`2885`)

* Resolved a C89 compilation problem when enabling the fast-gil sharing feature.

* Coverage reporting did not include the signature line of ``cdef`` functions.
  (Github issue :issue:`1461`)

* Casting a GIL-requiring function into a nogil function now issues a warning.
  (Github issue :issue:`2879`)

* Generators and coroutines were missing their return type annotation.
  (Github issue :issue:`2884`)


0.29.6 (2019-02-27)
===================

Bugs fixed
----------

* Fix a crash when accessing the ``__kwdefaults__`` special attribute of
  fused functions.  (Github issue :issue:`1470`)

* Fix the parsing of buffer format strings that contain numeric sizes, which
  could lead to incorrect input rejections.  (Github issue :issue:`2845`)

* Avoid a C #pragma in old gcc versions that was only added in GCC 4.6.
  Patch by Michael Anselmi.  (Github issue :issue:`2838`)

* Auto-encoding of Unicode strings to UTF-8 C/C++ strings failed in Python 3,
  even though the default encoding there is UTF-8.
  (Github issue :issue:`2819`)


0.29.5 (2019-02-09)
===================

Bugs fixed
----------

* Crash when defining a Python subclass of an extension type and repeatedly calling
  a cpdef method on it.  (Github issue :issue:`2823`)

* Compiler crash when ``prange()`` loops appear inside of with-statements.
  (Github issue :issue:`2780`)

* Some C compiler warnings were resolved.
  Patches by Christoph Gohlke.  (Github issues :issue:`2815`, :issue:`2816`, :issue:`2817`, :issue:`2822`)

* Python conversion of C++ enums failed in 0.29.
  Patch by Orivej Desh.  (Github issue :issue:`2767`)


0.29.4 (2019-02-01)
===================

Bugs fixed
----------

* Division of numeric constants by a runtime value of 0 could fail to raise a
  ``ZeroDivisionError``.  (Github issue :issue:`2820`)


0.29.3 (2019-01-19)
===================

Bugs fixed
----------

* Some C code for memoryviews was generated in a non-deterministic order.
  Patch by Martijn van Steenbergen.  (Github issue :issue:`2779`)

* C89 compatibility was accidentally lost since 0.28.
  Patches by gastineau and true-pasky.  (Github issues :issue:`2778`, :issue:`2801`)

* A C compiler cast warning was resolved.
  Patch by Michael Buesch.  (Github issue :issue:`2774`)

* An compilation failure with complex numbers under MSVC++ was resolved.
  (Github issue :issue:`2797`)

* Coverage reporting could fail when modules were moved around after the build.
  Patch by Wenjun Si.  (Github issue :issue:`2776`)


0.29.2 (2018-12-14)
===================

Bugs fixed
----------

* The code generated for deduplicated constants leaked some references.
  (Github issue :issue:`2750`)

* The declaration of ``sigismember()`` in ``libc.signal`` was corrected.
  (Github issue :issue:`2756`)

* Crashes in compiler and test runner were fixed.
  (Github issue :issue:`2736`, :issue:`2755`)

* A C compiler warning about an invalid safety check was resolved.
  (Github issue :issue:`2731`)


0.29.1 (2018-11-24)
===================

Bugs fixed
----------

* Extensions compiled with MinGW-64 under Windows could misinterpret integer
  objects larger than 15 bit and return incorrect results.
  (Github issue :issue:`2670`)

* Cython no longer requires the source to be writable when copying its data
  into a memory view slice.
  Patch by Andrey Paramonov.  (Github issue :issue:`2644`)

* Line tracing of ``try``-statements generated invalid C code.
  (Github issue :issue:`2274`)

* When using the ``warn.undeclared`` directive, Cython's own code generated
  warnings that are now fixed.
  Patch by Nicolas Pauss.  (Github issue :issue:`2685`)

* Cython's memoryviews no longer require strides for setting the shape field
  but only the ``PyBUF_ND`` flag to be set.
  Patch by John Kirkham.  (Github issue :issue:`2716`)

* Some C compiler warnings about unused memoryview code were fixed.
  Patch by Ho Cheuk Ting.  (Github issue :issue:`2588`)

* A C compiler warning about implicit signed/unsigned conversion was fixed.
  (Github issue :issue:`2729`)

* Assignments to C++ references returned by ``operator[]`` could fail to compile.
  (Github issue :issue:`2671`)

* The power operator and the support for NumPy math functions were fixed
  in Pythran expressions.
  Patch by Serge Guelton.  (Github issues :issue:`2702`, :issue:`2709`)

* Signatures with memory view arguments now show the expected type
  when embedded in docstrings.
  Patch by Matthew Chan and Benjamin Weigel.  (Github issue :issue:`2634`)

* Some ``from ... cimport ...`` constructs were not correctly considered
  when searching modified dependencies in ``cythonize()`` to decide
  whether to recompile a module.
  Patch by Kryštof Pilnáček.  (Github issue :issue:`2638`)

* A struct field type in the ``cpython.array`` declarations was corrected.
  Patch by John Kirkham.  (Github issue :issue:`2712`)


0.29 (2018-10-14)
=================

Features added
--------------

* PEP-489 multi-phase module initialisation has been enabled again.  Module
  reloads in other subinterpreters raise an exception to prevent corruption
  of the static module state.

* A set of ``mypy`` compatible PEP-484 declarations were added for Cython's C data
  types to integrate with static analysers in typed Python code.  They are available
  in the ``Cython/Shadow.pyi`` module and describe the types in the special ``cython``
  module that can be used for typing in Python code.
  Original patch by Julian Gethmann. (Github issue :issue:`1965`)

* Memoryviews are supported in PEP-484/526 style type declarations.
  (Github issue :issue:`2529`)

* ``@cython.nogil`` is supported as a C-function decorator in Python code.
  (Github issue :issue:`2557`)

* Raising exceptions from nogil code will automatically acquire the GIL, instead
  of requiring an explicit ``with gil`` block.

* C++ functions can now be declared as potentially raising both C++ and Python
  exceptions, so that Cython can handle both correctly.
  (Github issue :issue:`2615`)

* ``cython.inline()`` supports a direct ``language_level`` keyword argument that
  was previously only available via a directive.

* A new language level name ``3str`` was added that mostly corresponds to language
  level 3, but keeps unprefixed string literals as type 'str' in both Py2 and Py3,
  and the builtin 'str' type unchanged.  This will become the default in the next
  Cython release and is meant to help user code a) transition more easily to this
  new default and b) migrate to Python 3 source code semantics without making support
  for Python 2.x difficult.

* In CPython 3.6 and later, looking up globals in the module dict is almost
  as fast as looking up C globals.
  (Github issue :issue:`2313`)

* For a Python subclass of an extension type, repeated method calls to non-overridden
  cpdef methods can avoid the attribute lookup in Py3.6+, which makes them 4x faster.
  (Github issue :issue:`2313`)

* (In-)equality comparisons of objects to integer literals are faster.
  (Github issue :issue:`2188`)

* Some internal and 1-argument method calls are faster.

* Modules that cimport many external extension types from other Cython modules
  execute less import requests during module initialisation.

* Constant tuples and slices are deduplicated and only created once per module.
  (Github issue :issue:`2292`)

* The coverage plugin considers more C file extensions such as ``.cc`` and ``.cxx``.
  (Github issue :issue:`2266`)

* The ``cythonize`` command accepts compile time variable values (as set by ``DEF``)
  through the new ``-E`` option.
  Patch by Jerome Kieffer.  (Github issue :issue:`2315`)

* ``pyximport`` can import from namespace packages.
  Patch by Prakhar Goel.  (Github issue :issue:`2294`)

* Some missing numpy and CPython C-API declarations were added.
  Patch by John Kirkham. (Github issues :issue:`2523`, :issue:`2520`, :issue:`2537`)

* Declarations for the ``pylifecycle`` C-API functions were added in a new .pxd file
  ``cpython.pylifecycle``.

* The Pythran support was updated to work with the latest Pythran 0.8.7.
  Original patch by Adrien Guinet.  (Github issue :issue:`2600`)

* ``%a`` is included in the string formatting types that are optimised into f-strings.
  In this case, it is also automatically mapped to ``%r`` in Python 2.x.

* New C macro ``CYTHON_HEX_VERSION`` to access Cython's version in the same style as
  ``PY_VERSION_HEX``.

* Constants in ``libc.math`` are now declared as ``const`` to simplify their handling.

* An additional ``check_size`` clause was added to the ``ctypedef class`` name
  specification to allow suppressing warnings when importing modules with
  backwards-compatible ``PyTypeObject`` size changes.
  Patch by Matti Picus.  (Github issue :issue:`2627`)

Bugs fixed
----------

* The exception handling in generators and coroutines under CPython 3.7 was adapted
  to the newly introduced exception stack.  Users of Cython 0.28 who want to support
  Python 3.7 are encouraged to upgrade to 0.29 to avoid potentially incorrect error
  reporting and tracebacks.  (Github issue :issue:`1958`)

* Crash when importing a module under Stackless Python that was built for CPython.
  Patch by Anselm Kruis.  (Github issue :issue:`2534`)

* 2-value slicing of typed sequences failed if the start or stop index was None.
  Patch by Christian Gibson.  (Github issue :issue:`2508`)

* Multiplied string literals lost their factor when they are part of another
  constant expression (e.g. 'x' * 10 + 'y' => 'xy').

* String formatting with the '%' operator didn't call the special ``__rmod__()``
  method if the right side is a string subclass that implements it.
  (Python issue 28598)

* The directive ``language_level=3`` did not apply to the first token in the
  source file.  (Github issue :issue:`2230`)

* Overriding cpdef methods did not work in Python subclasses with slots.
  Note that this can have a performance impact on calls from Cython code.
  (Github issue :issue:`1771`)

* Fix declarations of builtin or C types using strings in pure python mode.
  (Github issue :issue:`2046`)

* Generator expressions and lambdas failed to compile in ``@cfunc`` functions.
  (Github issue :issue:`459`)

* Global names with ``const`` types were not excluded from star-import assignments
  which could lead to invalid C code.
  (Github issue :issue:`2621`)

* Several internal function signatures were fixed that lead to warnings in gcc-8.
  (Github issue :issue:`2363`)

* The numpy helper functions ``set_array_base()`` and ``get_array_base()``
  were adapted to the current numpy C-API recommendations.
  Patch by Matti Picus. (Github issue :issue:`2528`)

* Some NumPy related code was updated to avoid deprecated API usage.
  Original patch by jbrockmendel.  (Github issue :issue:`2559`)

* Several C++ STL declarations were extended and corrected.
  Patch by Valentin Valls. (Github issue :issue:`2207`)

* C lines of the module init function were unconditionally not reported in
  exception stack traces.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2492`)

* When PEP-489 support is enabled, reloading the module overwrote any static
  module state. It now raises an exception instead, given that reloading is
  not actually supported.

* Object-returning, C++ exception throwing functions were not checking that
  the return value was non-null.
  Original patch by Matt Wozniski (Github issue :issue:`2603`)

* The source file encoding detection could get confused if the
  ``c_string_encoding`` directive appeared within the first two lines.
  (Github issue :issue:`2632`)

* Cython generated modules no longer emit a warning during import when the
  size of the NumPy array type is larger than what was found at compile time.
  Instead, this is assumed to be a backwards compatible change on NumPy side.

Other changes
-------------

* Cython now emits a warning when no ``language_level`` (2, 3 or '3str') is set
  explicitly, neither as a ``cythonize()`` option nor as a compiler directive.
  This is meant to prepare the transition of the default language level from
  currently Py2 to Py3, since that is what most new users will expect these days.
  The future default will, however, not enforce unicode literals, because this
  has proven a major obstacle in the support for both Python 2.x and 3.x.  The
  next major release is intended to make this change, so that it will parse all
  code that does not request a specific language level as Python 3 code, but with
  ``str`` literals.  The language level 2 will continue to be supported for an
  indefinite time.

* The documentation was restructured, cleaned up and examples are now tested.
  The NumPy tutorial was also rewritten to simplify the running example.
  Contributed by Gabriel de Marmiesse.  (Github issue :issue:`2245`)

* Cython compiles less of its own modules at build time to reduce the installed
  package size to about half of its previous size.  This makes the compiler
  slightly slower, by about 5-7%.


0.28.6 (2018-11-01)
===================

Bugs fixed
----------

* Extensions compiled with MinGW-64 under Windows could misinterpret integer
  objects larger than 15 bit and return incorrect results.
  (Github issue :issue:`2670`)

* Multiplied string literals lost their factor when they are part of another
  constant expression (e.g. 'x' * 10 + 'y' => 'xy').


0.28.5 (2018-08-03)
===================

Bugs fixed
----------

* The discouraged usage of GCC's attribute ``optimize("Os")`` was replaced by the
  similar attribute ``cold`` to reduce the code impact of the module init functions.
  (Github issue :issue:`2494`)

* A reference leak in Py2.x was fixed when comparing str to unicode for equality.


0.28.4 (2018-07-08)
===================

Bugs fixed
----------

* Reallowing ``tp_clear()`` in a subtype of an ``@no_gc_clear`` extension type
  generated an invalid C function call to the (non-existent) base type implementation.
  (Github issue :issue:`2309`)

* Exception catching based on a non-literal (runtime) tuple could fail to match the
  exception.  (Github issue :issue:`2425`)

* Compile fix for CPython 3.7.0a2.  (Github issue :issue:`2477`)


0.28.3 (2018-05-27)
===================

Bugs fixed
----------

* Set iteration was broken in non-CPython since 0.28.

* ``UnicodeEncodeError`` in Py2 when ``%s`` formatting is optimised for
  unicode strings.  (Github issue :issue:`2276`)

* Work around a crash bug in g++ 4.4.x by disabling the size reduction setting
  of the module init function in this version.  (Github issue :issue:`2235`)

* Crash when exceptions occur early during module initialisation.
  (Github issue :issue:`2199`)


0.28.2 (2018-04-13)
===================

Features added
--------------

* ``abs()`` is faster for Python long objects.

* The C++11 methods ``front()`` and ``end()`` were added to the declaration of
  ``libcpp.string``.  Patch by Alex Huszagh.  (Github issue :issue:`2123`)

* The C++11 methods ``reserve()`` and ``bucket_count()`` are declared for
  ``libcpp.unordered_map``.  Patch by Valentin Valls.  (Github issue :issue:`2168`)

Bugs fixed
----------

* The copy of a read-only memoryview was considered read-only as well, whereas
  a common reason to copy a read-only view is to make it writable.  The result
  of the copying is now a writable buffer by default.
  (Github issue :issue:`2134`)

* The ``switch`` statement generation failed to apply recursively to the body of
  converted if-statements.

* ``NULL`` was sometimes rejected as exception return value when the returned
  type is a fused pointer type.
  Patch by Callie LeFave.  (Github issue :issue:`2177`)

* Fixed compatibility with PyPy 5.11.
  Patch by Matti Picus.  (Github issue :issue:`2165`)

Other changes
-------------

* The NumPy tutorial was rewritten to use memoryviews instead of the older
  buffer declaration syntax.
  Contributed by Gabriel de Marmiesse.  (Github issue :issue:`2162`)


0.28.1 (2018-03-18)
===================

Bugs fixed
----------

* ``PyFrozenSet_New()`` was accidentally used in PyPy where it is missing
  from the C-API.

* Assignment between some C++ templated types were incorrectly rejected
  when the templates mix ``const`` with ``ctypedef``.
  (Github issue :issue:`2148`)

* Undeclared C++ no-args constructors in subclasses could make the compilation
  fail if the base class constructor was declared without ``nogil``.
  (Github issue :issue:`2157`)

* Bytes %-formatting inferred ``basestring`` (bytes or unicode) as result type
  in some cases where ``bytes`` would have been safe to infer.
  (Github issue :issue:`2153`)

* ``None`` was accidentally disallowed as typed return value of ``dict.pop()``.
  (Github issue :issue:`2152`)


0.28 (2018-03-13)
=================

Features added
--------------

* Cdef classes can now multiply inherit from ordinary Python classes.
  (The primary base must still be a c class, possibly ``object``, and
  the other bases must *not* be cdef classes.)

* Type inference is now supported for Pythran compiled NumPy expressions.
  Patch by Nils Braun.  (Github issue :issue:`1954`)

* The ``const`` modifier can be applied to memoryview declarations to allow
  read-only buffers as input.  (Github issues :issue:`1605`, :issue:`1869`)

* C code in the docstring of a ``cdef extern`` block is copied verbatimly
  into the generated file.
  Patch by Jeroen Demeyer.  (Github issue :issue:`1915`)

* When compiling with gcc, the module init function is now tuned for small
  code size instead of whatever compile flags were provided externally.
  Cython now also disables some code intensive optimisations in that function
  to further reduce the code size.  (Github issue :issue:`2102`)

* Decorating an async coroutine with ``@cython.iterable_coroutine`` changes its
  type at compile time to make it iterable.  While this is not strictly in line
  with PEP-492, it improves the interoperability with old-style coroutines that
  use ``yield from`` instead of ``await``.

* The IPython magic has preliminary support for JupyterLab.
  (Github issue :issue:`1775`)

* The new TSS C-API in CPython 3.7 is supported and has been backported.
  Patch by Naotoshi Seo.  (Github issue :issue:`1932`)

* Cython knows the new ``Py_tss_t`` type defined in PEP-539 and automatically
  initialises variables declared with that type to ``Py_tss_NEEDS_INIT``,
  a value which cannot be used outside of static assignments.

* The set methods ``.remove()`` and ``.discard()`` are optimised.
  Patch by Antoine Pitrou.  (Github issue :issue:`2042`)

* ``dict.pop()`` is optimised.
  Original patch by Antoine Pitrou.  (Github issue :issue:`2047`)

* Iteration over sets and frozensets is optimised.
  (Github issue :issue:`2048`)

* Safe integer loops (< range(2^30)) are automatically optimised into C loops.

* ``alist.extend([a,b,c])`` is optimised into sequential ``list.append()`` calls
  for short literal sequences.

* Calls to builtin methods that are not specifically optimised into C-API calls
  now use a cache that avoids repeated lookups of the underlying C function.
  (Github issue :issue:`2054`)

* Single argument function calls can avoid the argument tuple creation in some cases.

* Some redundant extension type checks are avoided.

* Formatting C enum values in f-strings is faster, as well as some other special cases.

* String formatting with the '%' operator is optimised into f-strings in simple cases.

* Subscripting (item access) is faster in some cases.

* Some ``bytearray`` operations have been optimised similar to ``bytes``.

* Some PEP-484/526 container type declarations are now considered for
  loop optimisations.

* Indexing into memoryview slices with ``view[i][j]`` is now optimised into
  ``view[i, j]``.

* Python compatible ``cython.*`` types can now be mixed with type declarations
  in Cython syntax.

* Name lookups in the module and in classes are faster.

* Python attribute lookups on extension types without instance dict are faster.

* Some missing signals were added to ``libc/signal.pxd``.
  Patch by Jeroen Demeyer.  (Github issue :issue:`1914`)

* The warning about repeated extern declarations is now visible by default.
  (Github issue :issue:`1874`)

* The exception handling of the function types used by CPython's type slot
  functions was corrected to match the de-facto standard behaviour, so that
  code that uses them directly benefits from automatic and correct exception
  propagation.  Patch by Jeroen Demeyer.  (Github issue :issue:`1980`)

* Defining the macro ``CYTHON_NO_PYINIT_EXPORT`` will prevent the module init
  function from being exported as symbol, e.g. when linking modules statically
  in an embedding setup.  Patch by AraHaan.  (Github issue :issue:`1944`)

Bugs fixed
----------

* If a module name is explicitly provided for an ``Extension()`` that is compiled
  via ``cythonize()``, it was previously ignored and replaced by the source file
  name.  It can now be used to override the target module name, e.g. for compiling
  prefixed accelerator modules from Python files.  (Github issue :issue:`2038`)

* The arguments of the ``num_threads`` parameter of parallel sections
  were not sufficiently validated and could lead to invalid C code.
  (Github issue :issue:`1957`)

* Catching exceptions with a non-trivial exception pattern could call into
  CPython with a live exception set.  This triggered incorrect behaviour
  and crashes, especially in CPython 3.7.

* The signature of the special ``__richcmp__()`` method was corrected to recognise
  the type of the first argument as ``self``.  It was previously treated as plain
  object, but CPython actually guarantees that it always has the correct type.
  Note: this can change the semantics of user code that previously relied on
  ``self`` being untyped.

* Some Python 3 exceptions were not recognised as builtins when running Cython
  under Python 2.

* Some async helper functions were not defined in the generated C code when
  compiling simple async code.  (Github issue :issue:`2075`)

* Line tracing did not include generators and coroutines.
  (Github issue :issue:`1949`)

* C++ declarations for ``unordered_map`` were corrected.
  Patch by Michael Schatzow.  (Github issue :issue:`1484`)

* Iterator declarations in C++ ``deque`` and ``vector`` were corrected.
  Patch by Alex Huszagh.  (Github issue :issue:`1870`)

* The const modifiers in the C++ ``string`` declarations were corrected, together
  with the coercion behaviour of string literals into C++ strings.
  (Github issue :issue:`2132`)

* Some declaration types in ``libc.limits`` were corrected.
  Patch by Jeroen Demeyer.  (Github issue :issue:`2016`)

* ``@cython.final`` was not accepted on Python classes with an ``@cython.cclass``
  decorator.  (Github issue :issue:`2040`)

* Cython no longer creates useless and incorrect ``PyInstanceMethod`` wrappers for
  methods in Python 3.  Patch by Jeroen Demeyer.  (Github issue :issue:`2105`)

* The builtin ``bytearray`` type could not be used as base type of cdef classes.
  (Github issue :issue:`2106`)

Other changes
-------------


0.27.3 (2017-11-03)
===================

Bugs fixed
----------

* String forward references to extension types like ``@cython.locals(x="ExtType")``
  failed to find the named type.  (Github issue :issue:`1962`)

* NumPy slicing generated incorrect results when compiled with Pythran.
  Original patch by Serge Guelton (Github issue :issue:`1946`).

* Fix "undefined reference" linker error for generators on Windows in Py3.3-3.5.
  (Github issue :issue:`1968`)

* Adapt to recent C-API change of ``PyThreadState`` in CPython 3.7.

* Fix signature of ``PyWeakref_GetObject()`` API declaration.
  Patch by Jeroen Demeyer (Github issue :issue:`1975`).


0.27.2 (2017-10-22)
===================

Bugs fixed
----------

* Comprehensions could incorrectly be optimised away when they appeared in boolean
  test contexts.  (Github issue :issue:`1920`)

* The special methods ``__eq__``, ``__lt__`` etc. in extension types did not type
  their first argument as the type of the class but ``object``.  (Github issue :issue:`1935`)

* Crash on first lookup of "cline_in_traceback" option during exception handling.
  (Github issue :issue:`1907`)

* Some nested module level comprehensions failed to compile.
  (Github issue :issue:`1906`)

* Compiler crash on some complex type declarations in pure mode.
  (Github issue :issue:`1908`)

* ``std::unordered_map.erase()`` was declared with an incorrect ``void`` return
  type in ``libcpp.unordered_map``.  (Github issue :issue:`1484`)

* Invalid use of C++ ``fallthrough`` attribute before C++11 and similar issue in clang.
  (Github issue :issue:`1930`)

* Compiler crash on misnamed properties. (Github issue :issue:`1905`)


0.27.1 (2017-10-01)
===================

Features added
--------------

* The Jupyter magic has a new debug option ``--verbose`` that shows details about
  the distutils invocation.  Patch by Boris Filippov (Github issue :issue:`1881`).

Bugs fixed
----------

* Py3 list comprehensions in class bodies resulted in invalid C code.
  (Github issue :issue:`1889`)

* Modules built for later CPython 3.5.x versions failed to import in 3.5.0/3.5.1.
  (Github issue :issue:`1880`)

* Deallocating fused types functions and methods kept their GC tracking enabled,
  which could potentially lead to recursive deallocation attempts.

* Crash when compiling in C++ mode with old setuptools versions.
  (Github issue :issue:`1879`)

* C++ object arguments for the constructor of Cython implemented C++ are now
  passed by reference and not by value to allow for non-copyable arguments, such
  as ``unique_ptr``.

* API-exported C++ classes with Python object members failed to compile.
  (Github issue :issue:`1866`)

* Some issues with the new relaxed exception value handling were resolved.

* Python classes as annotation types could prevent compilation.
  (Github issue :issue:`1887`)

* Cython annotation types in Python files could lead to import failures
  with a "cython undefined" error.  Recognised types are now turned into strings.

* Coverage analysis could fail to report on extension modules on some platforms.

* Annotations could be parsed (and rejected) as types even with
  ``annotation_typing=False``.

Other changes
-------------

* PEP 489 support has been disabled by default to counter incompatibilities with
  import setups that try to reload or reinitialise modules.


0.27 (2017-09-23)
=================

Features added
--------------

* Extension module initialisation follows
  `PEP 489 <https://www.python.org/dev/peps/pep-0489/>`_ in CPython 3.5+, which
  resolves several differences with regard to normal Python modules.  This makes
  the global names ``__file__`` and ``__path__`` correctly available to module
  level code and improves the support for module-level relative imports.
  (Github issues :issue:`1715`, :issue:`1753`, :issue:`1035`)

* Asynchronous generators (`PEP 525 <https://www.python.org/dev/peps/pep-0525/>`_)
  and asynchronous comprehensions (`PEP 530 <https://www.python.org/dev/peps/pep-0530/>`_)
  have been implemented.  Note that async generators require finalisation support
  in order to allow for asynchronous operations during cleanup, which is only
  available in CPython 3.6+.  All other functionality has been backported as usual.

* Variable annotations are now parsed according to
  `PEP 526 <https://www.python.org/dev/peps/pep-0526/>`_.  Cython types (e.g.
  ``cython.int``) are evaluated as C type declarations and everything else as Python
  types.  This can be disabled with the directive ``annotation_typing=False``.
  Note that most complex PEP-484 style annotations are currently ignored.  This will
  change in future releases. (Github issue :issue:`1850`)

* Extension types (also in pure Python mode) can implement the normal special methods
  ``__eq__``, ``__lt__`` etc. for comparisons instead of the low-level ``__richcmp__``
  method.  (Github issue :issue:`690`)

* New decorator ``@cython.exceptval(x=None, check=False)`` that makes the signature
  declarations ``except x``, ``except? x`` and ``except *`` available to pure Python
  code.  Original patch by Antonio Cuni.  (Github issue :issue:`1653`)

* Signature annotations are now included in the signature docstring generated by
  the ``embedsignature`` directive.  Patch by Lisandro Dalcin (Github issue :issue:`1781`).

* The gdb support for Python code (``libpython.py``) was updated to the latest
  version in CPython 3.7 (git rev 5fe59f8).

* The compiler tries to find a usable exception return value for cdef functions
  with ``except *`` if the returned type allows it.  Note that this feature is subject
  to safety limitations, so it is still better to provide an explicit declaration.

* C functions can be assigned to function pointers with a compatible exception
  declaration, not only with exact matches.  A side-effect is that certain compatible
  signature overrides are now allowed and some more mismatches of exception signatures
  are now detected and rejected as errors that were not detected before.

* The IPython/Jupyter magic integration has a new option ``%%cython --pgo`` for profile
  guided optimisation. It compiles the cell with PGO settings for the C compiler,
  executes it to generate a runtime profile, and then compiles it again using that
  profile for C compiler optimisation.  Currently only tested with gcc.

* ``len(memoryview)`` can be used in nogil sections to get the size of the
  first dimension of a memory view (``shape[0]``). (Github issue :issue:`1733`)

* C++ classes can now contain (properly refcounted) Python objects.

* NumPy dtype subarrays are now accessible through the C-API.
  Patch by Gerald Dalley (Github issue :issue:`245`).

* Resolves several issues with PyPy and uses faster async slots in PyPy3.
  Patch by Ronan Lamy (Github issues :issue:`1871`, :issue:`1878`).

Bugs fixed
----------

* Extension types that were cimported from other Cython modules could disagree
  about the order of fused cdef methods in their call table.  This could lead
  to wrong methods being called and potentially also crashes.  The fix required
  changes to the ordering of fused methods in the call table, which may break
  existing compiled modules that call fused cdef methods across module boundaries,
  if these methods were implemented in a different order than they were declared
  in the corresponding .pxd file. (Github issue :issue:`1873`)

* The exception state handling in generators and coroutines could lead to
  exceptions in the caller being lost if an exception was raised and handled
  inside of the coroutine when yielding. (Github issue :issue:`1731`)

* Loops over ``range(enum)`` were not converted into C for-loops.  Note that it
  is still recommended to use an explicit cast to a C integer type in this case.

* Error positions of names (e.g. variables) were incorrectly reported after the
  name and not at the beginning of the name.

* Compile time ``DEF`` assignments were evaluated even when they occur inside of
  falsy ``IF`` blocks. (Github issue :issue:`1796`)

* Disabling the line tracing from a trace function could fail.
  Original patch by Dmitry Trofimov. (Github issue :issue:`1769`)

* Several issues with the Pythran integration were resolved.

* abs(signed int) now returns a signed rather than unsigned int.
  (Github issue :issue:`1837`)

* Reading ``frame.f_locals`` of a Cython function (e.g. from a debugger or profiler
  could modify the module globals. (Github issue :issue:`1836`)

* Buffer type mismatches in the NumPy buffer support could leak a reference to the
  buffer owner.

* Using the "is_f_contig" and "is_c_contig" memoryview methods together could leave
  one of them undeclared. (Github issue :issue:`1872`)

* Compilation failed if the for-in-range loop target was not a variable but a more
  complex expression, e.g. an item assignment. (Github issue :issue:`1831`)

* Compile time evaluations of (partially) constant f-strings could show incorrect
  results.

* Escape sequences in raw f-strings (``fr'...'``) were resolved instead of passing
  them through as expected.

* Some ref-counting issues in buffer error handling have been resolved.

Other changes
-------------

* Type declarations in signature annotations are now parsed according to
  `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_
  typing.  Only Cython types (e.g. ``cython.int``) and Python builtin types are
  currently considered as type declarations.  Everything else is ignored, but this
  will change in a future Cython release.
  (Github issue :issue:`1672`)

* The directive ``annotation_typing`` is now ``True`` by default, which enables
  parsing type declarations from annotations.

* This release no longer supports Python 3.2.


0.26.1 (2017-08-29)
===================

Features added
--------------

Bugs fixed
----------

* ``cython.view.array`` was missing ``.__len__()``.

* Extension types with a ``.pxd`` override for their ``__releasebuffer__`` slot
  (e.g. as provided by Cython for the Python ``array.array`` type) could leak
  a reference to the buffer owner on release, thus not freeing the memory.
  (Github issue :issue:`1638`)

* Auto-decoding failed in 0.26 for strings inside of C++ containers.
  (Github issue :issue:`1790`)

* Compile error when inheriting from C++ container types.
  (Github issue :issue:`1788`)

* Invalid C code in generators (declaration after code).
  (Github issue :issue:`1801`)

* Arithmetic operations on ``const`` integer variables could generate invalid code.
  (Github issue :issue:`1798`)

* Local variables with names of special Python methods failed to compile inside of
  closures. (Github issue :issue:`1797`)

* Problem with indirect Emacs buffers in cython-mode.
  Patch by Martin Albrecht (Github issue :issue:`1743`).

* Extension types named ``result`` or ``PickleError`` generated invalid unpickling code.
  Patch by Jason Madden (Github issue :issue:`1786`).

* Bazel integration failed to compile ``.py`` files.
  Patch by Guro Bokum (Github issue :issue:`1784`).

* Some include directories and dependencies were referenced with their absolute paths
  in the generated files despite lying within the project directory.

* Failure to compile in Py3.7 due to a modified signature of ``_PyCFunctionFast()``


0.26 (2017-07-19)
=================

Features added
--------------

* Pythran can be used as a backend for evaluating NumPy array expressions.
  Patch by Adrien Guinet (Github issue :issue:`1607`).

* cdef classes now support pickling by default when possible.
  This can be disabled with the ``auto_pickle`` directive.

* Speed up comparisons of strings if their hash value is available.
  Patch by Claudio Freire (Github issue :issue:`1571`).

* Support pyximport from zip files.
  Patch by Sergei Lebedev (Github issue :issue:`1485`).

* IPython magic now respects the ``__all__`` variable and ignores
  names with leading-underscore (like ``import *`` does).
  Patch by Syrtis Major (Github issue :issue:`1625`).

* ``abs()`` is optimised for C complex numbers.
  Patch by David Woods (Github issue :issue:`1648`).

* The display of C lines in Cython tracebacks can now be enabled at runtime
  via ``import cython_runtime; cython_runtime.cline_in_traceback=True``.
  The default has been changed to False.

* The overhead of calling fused types generic functions was reduced.

* "cdef extern" include files are now also searched relative to the current file.
  Patch by Jeroen Demeyer (Github issue :issue:`1654`).

* Optional optimization for re-acquiring the GIL, controlled by the
  `fast_gil` directive.

Bugs fixed
----------

* Item lookup/assignment with a unicode character as index that is typed
  (explicitly or implicitly) as ``Py_UCS4`` or ``Py_UNICODE`` used the
  integer value instead of the Unicode string value. Code that relied on
  the previous behaviour now triggers a warning that can be disabled by
  applying an explicit cast. (Github issue :issue:`1602`)

* f-string processing was adapted to changes in PEP 498 and CPython 3.6.

* Invalid C code when decoding from UTF-16(LE/BE) byte strings.
  (Github issue :issue:`1696`)

* Unicode escapes in 'ur' raw-unicode strings were not resolved in Py2 code.
  Original patch by Aaron Gallagher (Github issue :issue:`1594`).

* File paths of code objects are now relative.
  Original patch by Jelmer Vernooij (Github issue :issue:`1565`).

* Decorators of cdef class methods could be executed twice.
  Patch by Jeroen Demeyer (Github issue :issue:`1724`).

* Dict iteration using the Py2 ``iter*`` methods failed in PyPy3.
  Patch by Armin Rigo (Github issue :issue:`1631`).

* Several warnings in the generated code are now suppressed.

Other changes
-------------

* The ``unraisable_tracebacks`` option now defaults to ``True``.

* Coercion of C++ containers to Python is no longer automatic on attribute
  access (Github issue :issue:`1521`).

* Access to Python attributes of cimported modules without the corresponding
  import is now a compile-time (rather than runtime) error.

* Do not use special dll linkage for "cdef public" functions.
  Patch by Jeroen Demeyer (Github issue :issue:`1687`).

* cdef/cpdef methods must match their declarations.  See Github issue :issue:`1732`.
  This is now a warning and will be an error in future releases.


0.25.2 (2016-12-08)
===================

Bugs fixed
----------

* Fixes several issues with C++ template deduction.

* Fixes a issue with bound method type inference (Github issue :issue:`551`).

* Fixes a bug with cascaded tuple assignment (Github issue :issue:`1523`).

* Fixed or silenced many Clang warnings.

* Fixes bug with powers of pure real complex numbers (Github issue :issue:`1538`).


0.25.1 (2016-10-26)
===================

Bugs fixed
----------

* Fixes a bug with ``isinstance(o, Exception)`` (Github issue :issue:`1496`).

* Fixes bug with ``cython.view.array`` missing utility code in some cases
  (Github issue :issue:`1502`).

Other changes
-------------

* The distutils extension ``Cython.Distutils.build_ext`` has been reverted,
  temporarily, to be ``old_build_ext`` to give projects time to migrate.
  The new build_ext is available as ``new_build_ext``.


0.25 (2016-10-25)
=================

Features added
--------------

* def/cpdef methods of cdef classes benefit from Cython's internal function
  implementation, which enables introspection and line profiling for them.
  Implementation sponsored by Turbostream (www.turbostream-cfd.com).

* Calls to Python functions are faster, following the recent "FastCall"
  optimisations that Victor Stinner implemented for CPython 3.6.
  See https://bugs.python.org/issue27128 and related issues.

* The new METH_FASTCALL calling convention for PyCFunctions is supported
  in CPython 3.6.  See https://bugs.python.org/issue27810

* Initial support for using Cython modules in Pyston.
  Patch by Boxiang Sun.

* Dynamic Python attributes are allowed on cdef classes if an attribute
  ``cdef dict __dict__`` is declared in the class.  Patch by empyrical.

* Cython implemented C++ classes can make direct calls to base class methods.
  Patch by empyrical.

* C++ classes can now have typedef members. STL containers updated with
  value_type.

* New directive ``cython.no_gc`` to fully disable GC for a cdef class.
  Patch by Claudio Freire.

* Buffer variables are no longer excluded from ``locals()``.
  Patch by David Woods.

* Building f-strings is faster, especially when formatting C integers.

* for-loop iteration over "std::string".

* ``libc/math.pxd`` provides ``e`` and ``pi`` as alias constants to simplify
  usage as a drop-in replacement for Python's math module.

* Speed up cython.inline().

* Binary lshift operations with small constant Python integers are faster.

* Some integer operations on Python long objects are faster in Python 2.7.

* Support for the C++ ``typeid`` operator.

* Support for bazel using a the pyx_library rule in //Tools:rules.bzl.

Significant Bugs fixed
----------------------

* Division of complex numbers avoids overflow by using Smith's method.

* Some function signatures in ``libc.math`` and ``numpy.pxd`` were incorrect.
  Patch by Michael Seifert.

Other changes
-------------

* The "%%cython" IPython/jupyter magic now defaults to the language level of
  the current jupyter kernel.  The language level can be set explicitly with
  "%%cython -2" or "%%cython -3".

* The distutils extension ``Cython.Distutils.build_ext`` has now been updated
  to use cythonize which properly handles dependencies.  The old extension can
  still be found in ``Cython.Distutils.old_build_ext`` and is now deprecated.

* ``directive_defaults`` is no longer available in ``Cython.Compiler.Options``,
  use ``get_directive_defaults()`` instead.


0.24.1 (2016-07-15)
===================

Bugs fixed
----------

* IPython cell magic was lacking a good way to enable Python 3 code semantics.
  It can now be used as "%%cython -3".

* Follow a recent change in `PEP 492 <https://www.python.org/dev/peps/pep-0492/>`_
  and CPython 3.5.2 that now requires the ``__aiter__()`` method of asynchronous
  iterators to be a simple ``def`` method instead of an ``async def`` method.

* Coroutines and generators were lacking the ``__module__`` special attribute.

* C++ ``std::complex`` values failed to auto-convert from and to Python complex
  objects.

* Namespaced C++ types could not be used as memory view types due to lack of
  name mangling.  Patch by Ivan Smirnov.

* Assignments between identical C++ types that were declared with differently
  typedefed template types could fail.

* Rebuilds could fail to evaluate dependency timestamps in C++ mode.
  Patch by Ian Henriksen.

* Macros defined in the ``distutils`` compiler option do not require values
  anymore.  Patch by Ian Henriksen.

* Minor fixes for MSVC, Cygwin and PyPy.


0.24 (2016-04-04)
=================

Features added
--------------

* `PEP 498 <https://www.python.org/dev/peps/pep-0498/>`_:
  Literal String Formatting (f-strings).
  Original patch by Jelle Zijlstra.

* `PEP 515 <https://www.python.org/dev/peps/pep-0515/>`_:
  Underscores as visual separators in number literals.

* Parser was adapted to some minor syntax changes in Py3.6, e.g.
  https://bugs.python.org/issue9232

* The embedded C code comments that show the original source code
  can be discarded with the new directive ``emit_code_comments=False``.

* Cpdef enums are now first-class iterable, callable types in Python.

* Ctuples can now be declared in pure Python code.

* Posix declarations for DLL loading and stdio extensions were added.
  Patch by Lars Buitinck.

* The Py2-only builtins ``unicode()``, ``xrange()``, ``reduce()`` and
  ``long`` are now also available in compile time ``DEF`` expressions
  when compiling with Py3.

* Exception type tests have slightly lower overhead.
  This fixes ticket 868.

* @property syntax fully supported in cdef classes, old syntax deprecated.

* C++ classes can now be declared with default template parameters.

Bugs fixed
----------

* C++ exceptions raised by overloaded C++ operators were not always
  handled.  Patch by Ian Henriksen.

* C string literals were previously always stored as non-const global
  variables in the module.  They are now stored as global constants
  when possible, and otherwise as non-const C string literals in the
  generated code that uses them.  This improves compatibility with
  strict C compiler options and prevents non-const strings literals
  with the same content from being incorrectly merged.

* Compile time evaluated ``str`` expressions (``DEF``) now behave in a
  more useful way by turning into Unicode strings when compiling under
  Python 3.  This allows using them as intermediate values in expressions.
  Previously, they always evaluated to bytes objects.

* ``isinf()`` declarations in ``libc/math.pxd`` and ``numpy/math.pxd`` now
  reflect the actual tristate ``int`` return value instead of using ``bint``.

* Literal assignments to ctuples avoid Python tuple round-trips in some
  more corner cases.

* Iteration over ``dict(...).items()`` failed to get optimised when dict
  arguments included keyword arguments.

* cProfile now correctly profiles cpdef functions and methods.


0.23.5 (2016-03-26)
===================

* Compile errors and warnings in integer type conversion code.  This fixes
  ticket 877.  Patches by Christian Neukirchen, Nikolaus Rath, Ian Henriksen.

* Reference leak when ``*args`` argument was reassigned in closures.

* Truth-testing Unicode strings could waste time and memory in Py3.3+.

* Return values of async functions could be ignored and replaced by ``None``.

* Compiler crash in CPython 3.6.

* Fix prange() to behave identically to range().  The end condition was
  miscalculated when the range was not exactly divisible by the step.

* Optimised ``all(genexpr)``/``any(genexpr)`` calls could warn about unused
  code.  This fixes ticket 876.


0.23.4 (2015-10-10)
===================

Bugs fixed
----------

* Memory leak when calling Python functions in PyPy.

* Compilation problem with MSVC in C99-ish mode.

* Warning about unused values in a helper macro.


0.23.3 (2015-09-29)
===================

Bugs fixed
----------

* Invalid C code for some builtin methods.  This fixes ticket 856 again.

* Incorrect C code in helper functions for PyLong conversion and string
  decoding.  This fixes ticket 863, ticket 864 and ticket 865.
  Original patch by Nikolaus Rath.

* Large folded or inserted integer constants could use too small C
  integer types and thus trigger a value wrap-around.

Other changes
-------------

* The coroutine and generator types of Cython now also register directly
  with the ``Coroutine`` and ``Generator`` ABCs in the ``backports_abc``
  module if it can be imported.  This fixes ticket 870.


0.23.2 (2015-09-11)
===================

Bugs fixed
----------

* Compiler crash when analysing some optimised expressions.

* Coverage plugin was adapted to coverage.py 4.0 beta 2.

* C++ destructor calls could fail when '&' operator is overwritten.

* Incorrect C literal generation for large integers in compile-time
  evaluated DEF expressions and constant folded expressions.

* Byte string constants could end up as Unicode strings when originating
  from compile-time evaluated DEF expressions.

* Invalid C code when caching known builtin methods.
  This fixes ticket 860.

* ``ino_t`` in ``posix.types`` was not declared as ``unsigned``.

* Declarations in ``libcpp/memory.pxd`` were missing ``operator!()``.
  Patch by Leo Razoumov.

* Static cdef methods can now be declared in .pxd files.


0.23.1 (2015-08-22)
===================

Bugs fixed
----------

* Invalid C code for generators.  This fixes ticket 858.

* Invalid C code for some builtin methods.  This fixes ticket 856.

* Invalid C code for unused local buffer variables.
  This fixes ticket 154.

* Test failures on 32bit systems.  This fixes ticket 857.

* Code that uses ``from xyz import *`` and global C struct/union/array
  variables could fail to compile due to missing helper functions.
  This fixes ticket 851.

* Misnamed PEP 492 coroutine property ``cr_yieldfrom`` renamed to
  ``cr_await`` to match CPython.

* Missing deallocation code for C++ object attributes in certain
  extension class hierarchies.

* Crash when async coroutine was not awaited.

* Compiler crash on ``yield`` in signature annotations and default
  argument values.  Both are forbidden now.

* Compiler crash on certain constructs in ``finally`` clauses.

* Cython failed to build when CPython's pgen is installed.


0.23 (2015-08-08)
=================

Features added
--------------

* `PEP 492 <https://www.python.org/dev/peps/pep-0492/>`_
  (async/await) was implemented.

* `PEP 448 <https://www.python.org/dev/peps/pep-0448/>`_
  (Additional Unpacking Generalizations) was implemented.

* Support for coverage.py 4.0+ can be enabled by adding the plugin
  "Cython.Coverage" to the ".coveragerc" config file.

* Annotated HTML source pages can integrate (XML) coverage reports.

* Tracing is supported in ``nogil`` functions/sections and module init code.

* When generators are used in a Cython module and the module imports the
  modules "inspect" and/or "asyncio", Cython enables interoperability by
  patching these modules during the import to recognise Cython's internal
  generator and coroutine types. This can be disabled by C compiling the
  module with "-D CYTHON_PATCH_ASYNCIO=0" or "-D CYTHON_PATCH_INSPECT=0"

* When generators or coroutines are used in a Cython module, their types
  are registered with the ``Generator`` and ``Coroutine`` ABCs in the
  ``collections`` or ``collections.abc`` stdlib module at import time to
  enable interoperability with code that needs to detect and process Python
  generators/coroutines.  These ABCs were added in CPython 3.5 and are
  available for older Python versions through the ``backports_abc`` module
  on PyPI.  See https://bugs.python.org/issue24018

* Adding/subtracting/dividing/modulus and equality comparisons with
  constant Python floats and small integers are faster.

* Binary and/or/xor/rshift operations with small constant Python integers
  are faster.

* When called on generator expressions, the builtins ``all()``, ``any()``,
  ``dict()``, ``list()``, ``set()``, ``sorted()`` and ``unicode.join()``
  avoid the generator iteration overhead by inlining a part of their
  functionality into the for-loop.

* Keyword argument dicts are no longer copied on function entry when they
  are not being used or only passed through to other function calls (e.g.
  in wrapper functions).

* The ``PyTypeObject`` declaration in ``cpython.object`` was extended.

* The builtin ``type`` type is now declared as PyTypeObject in source,
  allowing for extern functions taking type parameters to have the correct
  C signatures.  Note that this might break code that uses ``type`` just
  for passing around Python types in typed variables.  Removing the type
  declaration provides a backwards compatible fix.

* ``wraparound()`` and ``boundscheck()`` are available as no-ops in pure
  Python mode.

* Const iterators were added to the provided C++ STL declarations.

* Smart pointers were added to the provided C++ STL declarations.
  Patch by Daniel Filonik.

* ``NULL`` is allowed as default argument when embedding signatures.
  This fixes ticket 843.

* When compiling with ``--embed``, the internal module name is changed to
  ``__main__`` to allow arbitrary program names, including those that would
  be invalid for modules.  Note that this prevents reuse of the generated
  C code as an importable module.

* External C++ classes that overload the assignment operator can be used.
  Patch by Ian Henriksen.

* Support operator bool() for C++ classes so they can be used in if statements.

Bugs fixed
----------

* Calling "yield from" from Python on a Cython generator that returned a
  value triggered a crash in CPython.  This is now being worked around.
  See https://bugs.python.org/issue23996

* Language level 3 did not enable true division (a.k.a. float division)
  for integer operands.

* Functions with fused argument types that included a generic 'object'
  fallback could end up using that fallback also for other explicitly
  listed object types.

* Relative cimports could accidentally fall back to trying an absolute
  cimport on failure.

* The result of calling a C struct constructor no longer requires an
  intermediate assignment when coercing to a Python dict.

* C++ exception declarations with mapping functions could fail to compile
  when pre-declared in .pxd files.

* ``cpdef void`` methods are now permitted.

* ``abs(cint)`` could fail to compile in MSVC and used sub-optimal code
  in C++.  Patch by David Vierra, original patch by Michael Enßlin.

* Buffer index calculations using index variables with small C integer
  types could overflow for large buffer sizes.
  Original patch by David Vierra.

* C unions use a saner way to coerce from and to Python dicts.

* When compiling a module ``foo.pyx``, the directories in ``sys.path``
  are no longer searched when looking for ``foo.pxd``.
  Patch by Jeroen Demeyer.

* Memory leaks in the embedding main function were fixed.
  Original patch by Michael Enßlin.

* Some complex Python expressions could fail to compile inside of finally
  clauses.

* Unprefixed 'str' literals were not supported as C varargs arguments.

* Fixed type errors in conversion enum types to/from Python.  Note that
  this imposes stricter correctness requirements on enum declarations.


Other changes
-------------

* Changed mangling scheme in header files generated by ``cdef api``
  declarations.

* Installation under CPython 3.3+ no longer requires a pass of the
  2to3 tool.  This also makes it possible to run Cython in Python
  3.3+ from a source checkout without installing it first.
  Patch by Petr Viktorin.

* ``jedi-typer.py`` (in ``Tools/``) was extended and renamed to
  ``jedityper.py`` (to make it importable) and now works with and
  requires Jedi 0.9.  Patch by Tzer-jen Wei.


0.22.1 (2015-06-20)
===================

Bugs fixed
----------

* Crash when returning values on generator termination.

* In some cases, exceptions raised during internal isinstance() checks were
  not propagated.

* Runtime reported file paths of source files (e.g for profiling and tracing)
  are now relative to the build root directory instead of the main source file.

* Tracing exception handling code could enter the trace function with an active
  exception set.

* The internal generator function type was not shared across modules.

* Comparisons of (inferred) ctuples failed to compile.

* Closures inside of cdef functions returning ``void`` failed to compile.

* Using ``const`` C++ references in intermediate parts of longer expressions
  could fail to compile.

* C++ exception declarations with mapping functions could fail to compile when
  pre-declared in .pxd files.

* C++ compilation could fail with an ambiguity error in recent MacOS-X Xcode
  versions.

* C compilation could fail in pypy3.

* Fixed a memory leak in the compiler when compiling multiple modules.

* When compiling multiple modules, external library dependencies could leak
  into later compiler runs.  Fix by Jeroen Demeyer.  This fixes ticket 845.


0.22 (2015-02-11)
=================

Features added
--------------

* C functions can coerce to Python functions, which allows passing them
  around as callable objects.

* C arrays can be assigned by value and auto-coerce from Python iterables
  and to Python lists (and tuples).

* Extern C functions can now be declared as cpdef to export them to
  the module's Python namespace.  Extern C functions in pxd files export
  their values to their own module, iff it exists.

* Anonymous C tuple types can be declared as (ctype1, ctype2, ...).

* `PEP 479 <https://www.python.org/dev/peps/pep-0479/>`_:
  turn accidental StopIteration exceptions that exit generators
  into a RuntimeError, activated with future import "generator_stop".

* Looping over ``reversed(range())`` is optimised in the same way as
  ``range()``.  Patch by Favian Contreras.

Bugs fixed
----------

* Mismatching 'except' declarations on signatures in .pxd and .pyx files failed
  to produce a compile error.

* Failure to find any files for the path pattern(s) passed into ``cythonize()``
  is now an error to more easily detect accidental typos.

* The ``logaddexp`` family of functions in ``numpy.math`` now has correct
  declarations.

* In Py2.6/7 and Py3.2, simple Cython memory views could accidentally be
  interpreted as non-contiguous by CPython, which could trigger a CPython
  bug when copying data from them, thus leading to data corruption.
  See CPython issues 12834 and 23349.

Other changes
-------------

* Preliminary support for defining the Cython language with a formal grammar.
  To try parsing your files against this grammar, use the --formal_grammar directive.
  Experimental.

* ``_`` is no longer considered a cacheable builtin as it could interfere with
  gettext.

* Cythonize-computed metadata now cached in the generated C files.

* Several corrections and extensions in numpy, cpython, and libcpp pxd files.


0.21.2 (2014-12-27)
===================

Bugs fixed
----------

* Crash when assigning a C value to both a Python and C target at the same time.

* Automatic coercion from C++ strings to ``str`` generated incomplete code that
  failed to compile.

* Declaring a constructor in a C++ child class erroneously required a default
  constructor declaration in the super class.

* ``resize_smart()`` in ``cpython.array`` was broken.

* Functions in ``libcpp.cast`` are now declared as ``nogil``.

* Some missing C-API declarations were added.

* Py3 main code in embedding program code was lacking casts.

* Exception related to distutils "Distribution" class type in pyximport under
  latest CPython 2.7 and 3.4 releases when setuptools is being imported later.


0.21.1 (2014-10-18)
===================

Features added
--------------

* New ``cythonize`` option ``-a`` to generate the annotated HTML source view.

* Missing C-API declarations in ``cpython.unicode`` were added.

* Passing ``language='c++'`` into cythonize() globally enables C++ mode for
  all modules that were not passed as Extension objects (i.e. only source
  files and file patterns).

* ``Py_hash_t`` is a known type (used in CPython for hash values).

* ``PySlice_*()`` C-API functions are available from the ``cpython.slice``
  module.

* Allow arrays of C++ classes.

Bugs fixed
----------

* Reference leak for non-simple Python expressions in boolean and/or expressions.

* To fix a name collision and to reflect availability on host platforms,
  standard C declarations [ clock(), time(), struct tm and tm* functions ]
  were moved from posix/time.pxd to a new libc/time.pxd.  Patch by Charles
  Blake.

* Rerunning unmodified modules in IPython's cython support failed.
  Patch by Matthias Bussonier.

* Casting C++ ``std::string`` to Python byte strings failed when
  auto-decoding was enabled.

* Fatal exceptions in global module init code could lead to crashes
  if the already created module was used later on (e.g. through a
  stale reference in sys.modules or elsewhere).

* ``cythonize.py`` script was not installed on MS-Windows.

Other changes
-------------

* Compilation no longer fails hard when unknown compilation options are
  passed.  Instead, it raises a warning and ignores them (as it did silently
  before 0.21).  This will be changed back to an error in a future release.


0.21 (2014-09-10)
=================

Features added
--------------

* C (cdef) functions allow inner Python functions.

* Enums can now be declared as cpdef to export their values to
  the module's Python namespace.  Cpdef enums in pxd files export
  their values to their own module, iff it exists.

* Allow @staticmethod decorator to declare static cdef methods.
  This is especially useful for declaring "constructors" for
  cdef classes that can take non-Python arguments.

* Taking a ``char*`` from a temporary Python string object is safer
  in more cases and can be done inside of non-trivial expressions,
  including arguments of a function call.  A compile time error
  is raised only when such a pointer is assigned to a variable and
  would thus exceed the lifetime of the string itself.

* Generators have new properties ``__name__`` and ``__qualname__``
  that provide the plain/qualified name of the generator function
  (following CPython 3.5).  See https://bugs.python.org/issue21205

* The ``inline`` function modifier is available as a decorator
  ``@cython.inline`` in pure mode.

* When cygdb is run in a virtualenv, it enables the same virtualenv
  inside of the debugger. Patch by Marc Abramowitz.

* PEP 465: dedicated infix operator for matrix multiplication (A @ B).

* HTML output of annotated code uses Pygments for code highlighting
  and generally received a major overhaul by Matthias Bussonier.

* IPython magic support is now available directly from Cython with
  the command "%load_ext cython".  Cython code can directly be
  executed in a cell when marked with "%%cython".  Code analysis
  is available with "%%cython -a".  Patch by Martín Gaitán.

* Simple support for declaring Python object types in Python signature
  annotations.  Currently requires setting the compiler directive
  ``annotation_typing=True``.

* New directive ``use_switch`` (defaults to True) to optionally disable
  the optimization of chained if statement to C switch statements.

* Defines dynamic_cast et al. in ``libcpp.cast`` and C++ heap data
  structure operations in ``libcpp.algorithm``.

* Shipped header declarations in ``posix.*`` were extended to cover
  more of the POSIX API.  Patches by Lars Buitinck and Mark Peek.

Optimizations
-------------

* Simple calls to C implemented Python functions/methods are faster.
  This also speeds up many operations on builtins that Cython cannot
  otherwise optimise.

* The "and"/"or" operators try to avoid unnecessary coercions of their
  arguments.  They now evaluate the truth value of each argument
  independently and only coerce the final result of the whole expression
  to the target type (e.g. the type on the left side of an assignment).
  This also avoids reference counting overhead for Python values during
  evaluation and generally improves the code flow in the generated C code.

* The Python expression "2 ** N" is optimised into bit shifting.
  See https://bugs.python.org/issue21420

* Cascaded assignments (a = b = ...) try to minimise the number of
  type coercions.

* Calls to ``slice()`` are translated to a straight C-API call.

Bugs fixed
----------

* Crash when assigning memory views from ternary conditional expressions.

* Nested C++ templates could lead to unseparated ">>" characters being
  generated into the C++ declarations, which older C++ compilers could
  not parse.

* Sending SIGINT (Ctrl-C) during parallel cythonize() builds could
  hang the child processes.

* No longer ignore local setup.cfg files for distutils in pyximport.
  Patch by Martin Teichmann.

* Taking a ``char*`` from an indexed Python string generated unsafe
  reference counting code.

* Set literals now create all of their items before trying to add them
  to the set, following the behaviour in CPython.  This makes a
  difference in the rare case that the item creation has side effects
  and some items are not hashable (or if hashing them has side effects,
  too).

* Cython no longer generates the cross product of C functions for code
  that uses memory views of fused types in function signatures (e.g.
  ``cdef func(floating[:] a, floating[:] b)``).  This is considered the
  expected behaviour by most users and was previously inconsistent with
  other structured types like C arrays.  Code that really wants all type
  combinations can create the same fused memoryview type under different
  names and use those in the signature to make it clear which types are
  independent.

* Names that were unknown at compile time were looked up as builtins at
  runtime but not as global module names.  Trying both lookups helps with
  globals() manipulation.

* Fixed stl container conversion for typedef element types.

* ``obj.pop(x)`` truncated large C integer values of x to ``Py_ssize_t``.

* ``__init__.pyc`` is recognised as marking a package directory
  (in addition to .py, .pyx and .pxd).

* Syntax highlighting in ``cython-mode.el`` for Emacs no longer
  incorrectly highlights keywords found as part of longer names.

* Correctly handle ``from cython.submodule cimport name``.

* Fix infinite recursion when using super with cpdef methods.

* No-args ``dir()`` was not guaranteed to return a sorted list.

Other changes
-------------

* The header line in the generated C files no longer contains the
  timestamp but only the Cython version that wrote it.  This was
  changed to make builds more reproducible.

* Removed support for CPython 2.4, 2.5 and 3.1.

* The licensing implications on the generated code were clarified
  to avoid legal constraints for users.


0.20.2 (2014-06-16)
===================

Features added
--------------

* Some optimisations for set/frozenset instantiation.

* Support for C++ unordered_set and unordered_map.

Bugs fixed
----------

* Access to attributes of optimised builtin methods (e.g.
  ``[].append.__name__``) could fail to compile.

* Memory leak when extension subtypes add a memory view as attribute
  to those of the parent type without having Python object attributes
  or a user provided dealloc method.

* Compiler crash on readonly properties in "binding" mode.

* Auto-encoding with ``c_string_encoding=ascii`` failed in Py3.3.

* Crash when subtyping freelist enabled Cython extension types with
  Python classes that use ``__slots__``.

* Freelist usage is restricted to CPython to avoid problems with other
  Python implementations.

* Memory leak in memory views when copying overlapping, contiguous slices.

* Format checking when requesting non-contiguous buffers from
  ``cython.array`` objects was accidentally omitted in Py3.

* C++ destructor calls in extension types could fail to compile in clang.

* Buffer format validation failed for sequences of strings in structs.

* Docstrings on extension type attributes in .pxd files were rejected.


0.20.1 (2014-02-11)
===================

Bugs fixed
----------

* Build error under recent MacOS-X versions where ``isspace()`` could not be
  resolved by clang.

* List/Tuple literals multiplied by more than one factor were only multiplied
  by the last factor instead of all.

* Lookups of special methods (specifically for context managers) could fail
  in Python <= 2.6/3.1.

* Local variables were erroneously appended to the signature introspection
  of Cython implemented functions with keyword-only arguments under Python 3.

* In-place assignments to variables with inferred Python builtin/extension
  types could fail with type errors if the result value type was incompatible
  with the type of the previous value.

* The C code generation order of cdef classes, closures, helper code,
  etc. was not deterministic, thus leading to high code churn.

* Type inference could fail to deduce C enum types.

* Type inference could deduce unsafe or inefficient types from integer
  assignments within a mix of inferred Python variables and integer
  variables.


0.20 (2014-01-18)
=================

Features added
--------------

* Support for CPython 3.4.

* Support for calling C++ template functions.

* ``yield`` is supported in ``finally`` clauses.

* The C code generated for finally blocks is duplicated for each exit
  case to allow for better optimisations by the C compiler.

* Cython tries to undo the Python optimisationism of assigning a bound
  method to a local variable when it can generate better code for the
  direct call.

* Constant Python float values are cached.

* String equality comparisons can use faster type specific code in
  more cases than before.

* String/Unicode formatting using the '%' operator uses a faster
  C-API call.

* ``bytearray`` has become a known type and supports coercion from and
  to C strings.  Indexing, slicing and decoding is optimised. Note that
  this may have an impact on existing code due to type inference.

* Using ``cdef basestring stringvar`` and function arguments typed as
  ``basestring`` is now meaningful and allows assigning exactly
  ``str`` and ``unicode`` objects, but no subtypes of these types.

* Support for the ``__debug__`` builtin.

* Assertions in Cython compiled modules are disabled if the running
  Python interpreter was started with the "-O" option.

* Some types that Cython provides internally, such as functions and
  generators, are now shared across modules if more than one Cython
  implemented module is imported.

* The type inference algorithm works more fine granular by taking the
  results of the control flow analysis into account.

* A new script in ``bin/cythonize`` provides a command line frontend
  to the cythonize() compilation function (including distutils build).

* The new extension type decorator ``@cython.no_gc_clear`` prevents
  objects from being cleared during cyclic garbage collection, thus
  making sure that object attributes are kept alive until deallocation.

* During cyclic garbage collection, attributes of extension types that
  cannot create reference cycles due to their type (e.g. strings) are
  no longer considered for traversal or clearing.  This can reduce the
  processing overhead when searching for or cleaning up reference cycles.

* Package compilation (i.e. ``__init__.py`` files) now works, starting
  with Python 3.3.

* The cython-mode.el script for Emacs was updated.  Patch by Ivan Andrus.

* An option common_utility_include_dir was added to cythonize() to save
  oft-used utility code once in a separate directory rather than as
  part of each generated file.

* ``unraisable_tracebacks`` directive added to control printing of
  tracebacks of unraisable exceptions.

Bugs fixed
----------

* Abstract Python classes that subtyped a Cython extension type
  failed to raise an exception on instantiation, and thus ended
  up being instantiated.

* ``set.add(a_tuple)`` and ``set.discard(a_tuple)`` failed with a
  TypeError in Py2.4.

* The PEP 3155 ``__qualname__`` was incorrect for nested classes and
  inner classes/functions declared as ``global``.

* Several corner cases in the try-finally statement were fixed.

* The metaclass of a Python class was not inherited from its parent
  class(es).  It is now extracted from the list of base classes if not
  provided explicitly using the Py3 ``metaclass`` keyword argument.
  In Py2 compilation mode, a ``__metaclass__`` entry in the class
  dict will still take precedence if not using Py3 metaclass syntax,
  but only *after* creating the class dict (which may have been done
  by a metaclass of a base class, see PEP 3115).  It is generally
  recommended to use the explicit Py3 syntax to define metaclasses
  for Python types at compile time.

* The automatic C switch statement generation behaves more safely for
  heterogeneous value types (e.g. mixing enum and char), allowing for
  a slightly wider application and reducing corner cases.  It now always
  generates a 'default' clause to avoid C compiler warnings about
  unmatched enum values.

* Fixed a bug where class hierarchies declared out-of-order could result
  in broken generated code.

* Fixed a bug which prevented overriding const methods of C++ classes.

* Fixed a crash when converting Python objects to C++ strings fails.

Other changes
-------------

* In Py3 compilation mode, Python2-style metaclasses declared by a
  ``__metaclass__`` class dict entry are ignored.

* In Py3.4+, the Cython generator type uses ``tp_finalize()`` for safer
  cleanup instead of ``tp_del()``.


0.19.2 (2013-10-13)
===================

Features added
--------------

Bugs fixed
----------

* Some standard declarations were fixed or updated, including the previously
  incorrect declaration of ``PyBuffer_FillInfo()`` and some missing bits in
  ``libc.math``.

* Heap allocated subtypes of ``type`` used the wrong base type struct at the
  C level.

* Calling the unbound method dict.keys/value/items() in dict subtypes could
  call the bound object method instead of the unbound supertype method.

* "yield" wasn't supported in "return" value expressions.

* Using the "bint" type in memory views lead to unexpected results.
  It is now an error.

* Assignments to global/closure variables could catch them in an illegal state
  while deallocating the old value.

Other changes
-------------


0.19.1 (2013-05-11)
===================

Features added
--------------

* Completely empty C-API structs for extension type slots (protocols like
  number/mapping/sequence) are no longer generated into the C code.

* Docstrings that directly follow a public/readonly attribute declaration
  in a cdef class will be used as docstring of the auto-generated property.
  This fixes ticket 206.

* The automatic signature documentation tries to preserve more semantics
  of default arguments and argument types.  Specifically, ``bint`` arguments
  now appear as type ``bool``.

* A warning is emitted when negative literal indices are found inside of
  a code section that disables ``wraparound`` handling.  This helps with
  fixing invalid code that might fail in the face of future compiler
  optimisations.

* Constant folding for boolean expressions (and/or) was improved.

* Added a build_dir option to cythonize() which allows one to place
  the generated .c files outside the source tree.

Bugs fixed
----------

* ``isinstance(X, type)`` failed to get optimised into a call to
  ``PyType_Check()``, as done for other builtin types.

* A spurious ``from datetime cimport *`` was removed from the "cpython"
  declaration package. This means that the "datetime" declarations
  (added in 0.19) are no longer available directly from the "cpython"
  namespace, but only from "cpython.datetime". This is the correct
  way of doing it because the declarations refer to a standard library
  module, not the core CPython C-API itself.

* The C code for extension types is now generated in topological order
  instead of source code order to avoid C compiler errors about missing
  declarations for subtypes that are defined before their parent.

* The ``memoryview`` type name no longer shows up in the module dict of
  modules that use memory views.  This fixes trac ticket 775.

* Regression in 0.19 that rejected valid C expressions from being used
  in C array size declarations.

* In C++ mode, the C99-only keyword ``restrict`` could accidentally be
  seen by the GNU C++ compiler. It is now specially handled for both
  GCC and MSVC.

* Testing large (> int) C integer values for their truth value could fail
  due to integer wrap-around.

Other changes
-------------


0.19 (2013-04-19)
=================

Features added
--------------

* New directives ``c_string_type`` and ``c_string_encoding`` to more easily
  and automatically convert between C strings and the different Python string
  types.

* The extension type flag ``Py_TPFLAGS_HAVE_VERSION_TAG`` is enabled by default
  on extension types and can be disabled using the ``type_version_tag`` compiler
  directive.

* EXPERIMENTAL support for simple Cython code level line tracing.  Enabled by
  the "linetrace" compiler directive.

* Cython implemented functions make their argument and return type annotations
  available through the ``__annotations__`` attribute (PEP 3107).

* Access to non-cdef module globals and Python object attributes is faster.

* ``Py_UNICODE*`` coerces from and to Python unicode strings.  This is
  helpful when talking to Windows APIs, which use compatible wchar_t
  arrays for strings.  Note that the ``Py_UNICODE`` type is otherwise
  deprecated as of CPython 3.3.

* ``isinstance(obj, basestring)`` is optimised.  In Python 3 it only tests
  for instances of ``str`` (i.e. Py2 ``unicode``).

* The ``basestring`` builtin is mapped to ``str`` (i.e. Py2 ``unicode``) when
  compiling the generated C code under Python 3.

* Closures use freelists, which can speed up their creation quite substantially.
  This is also visible for short running generator expressions, for example.

* A new class decorator ``@cython.freelist(N)`` creates a static freelist of N
  instances for an extension type, thus avoiding the costly allocation step if
  possible. This can speed up object instantiation by 20-30% in suitable
  scenarios. Note that freelists are currently only supported for base types,
  not for types that inherit from others.

* Fast extension type instantiation using the ``Type.__new__(Type)`` idiom has
  gained support for passing arguments.  It is also a bit faster for types defined
  inside of the module.

* The Python2-only dict methods ``.iter*()`` and ``.view*()`` (requires Python 2.7)
  are automatically mapped to the equivalent keys/values/items methods in Python 3
  for typed dictionaries.

* Slicing unicode strings, lists and tuples is faster.

* list.append() is faster on average.

* ``raise Exception() from None`` suppresses the exception context in Py3.3.

* Py3 compatible ``exec(tuple)`` syntax is supported in Py2 code.

* Keyword arguments are supported for cdef functions.

* External C++ classes can be declared nogil.  Patch by John Stumpo.  This fixes
  trac ticket 805.

Bugs fixed
----------

* 2-value slicing of unknown objects passes the correct slice when the ``getitem``
  protocol is used instead of the ``getslice`` protocol (especially in Python 3),
  i.e. ``None`` values for missing bounds instead of ``[0,maxsize]``.  It is also
  a bit faster in some cases, e.g. for constant bounds.  This fixes trac ticket 636.

* Cascaded assignments of None values to extension type variables failed with
  a ``TypeError`` at runtime.

* The ``__defaults__`` attribute was not writable for Cython implemented
  functions.

* Default values of keyword-only arguments showed up in ``__defaults__`` instead
  of ``__kwdefaults__`` (which was not implemented).  Both are available for
  Cython implemented functions now, as specified in Python 3.x.

* ``yield`` works inside of ``with gil`` sections.  It previously lead to a crash.
  This fixes trac ticket 803.

* Static methods without explicitly named positional arguments (e.g. having only
  ``*args``) crashed when being called.  This fixes trac ticket 804.

* ``dir()`` without arguments previously returned an unsorted list, which now
  gets sorted as expected.

* ``dict.items()``, ``dict.keys()`` and ``dict.values()`` no longer return lists
  in Python 3.

* Exiting from an ``except-as`` clause now deletes the exception in Python 3 mode.

* The declarations of ``frexp()`` and ``ldexp()`` in ``math.pxd`` were incorrect.

Other changes
-------------


0.18 (2013-01-28)
=================

Features added
--------------

* Named Unicode escapes ("\N{...}") are supported.

* Python functions/classes provide the special attribute "__qualname__"
  as defined by PEP 3155.

* Added a directive ``overflowcheck`` which raises an OverflowException when
  arithmetic with C ints overflow.  This has a modest performance penalty, but
  is much faster than using Python ints.

* Calls to nested Python functions are resolved at compile time.

* Type inference works across nested functions.

* ``py_bytes_string.decode(...)`` is optimised.

* C ``const`` declarations are supported in the language.

Bugs fixed
----------

* Automatic C++ exception mapping didn't work in nogil functions (only in
  "with nogil" blocks).

Other changes
-------------


0.17.4 (2013-01-03)
===================

Bugs fixed
----------

* Garbage collection triggered during deallocation of container classes could lead to a double-deallocation.


0.17.3 (2012-12-14)
===================

Features added
--------------

Bugs fixed
----------

* During final interpreter cleanup (with types cleanup enabled at compile time), extension types that inherit from base types over more than one level that were cimported from other modules could lead to a crash.

* Weak-reference support in extension types (with a ``cdef __weakref__`` attribute) generated incorrect deallocation code.

* In CPython 3.3, converting a Unicode character to the Py_UNICODE type could fail to raise an overflow for non-BMP characters that do not fit into a wchar_t on the current platform.

* Negative C integer constants lost their longness suffix in the generated C code.

Other changes
-------------


0.17.2 (2012-11-20)
===================

Features added
--------------

* ``cythonize()`` gained a best effort compile mode that can be used to simply ignore .py files that fail to compile.

Bugs fixed
----------

* Replacing an object reference with the value of one of its cdef attributes could generate incorrect C code that accessed the object after deleting its last reference.

* C-to-Python type coercions during cascaded comparisons could generate invalid C code, specifically when using the 'in' operator.

* "obj[1,]" passed a single integer into the item getter instead of a tuple.

* Cyclic imports at module init time did not work in Py3.

* The names of C++ destructors for template classes were built incorrectly.

* In pure mode, type casts in Cython syntax and the C ampersand operator are now rejected. Use the pure mode replacements instead.

* In pure mode, C type names and the sizeof() function are no longer recognised as such and can be used as normal Python names.

* The extended C level support for the CPython array type was declared too late to be used by user defined classes.

* C++ class nesting was broken.

* Better checking for required nullary constructors for stack-allocated C++ instances.

* Remove module docstring in no-docstring mode.

* Fix specialization for varargs function signatures.

* Fix several compiler crashes.

Other changes
-------------

* An experimental distutils script for compiling the CPython standard library was added as Tools/cystdlib.py.


0.17.1 (2012-09-26)
===================

Features added
--------------

Bugs fixed
----------

* A reference leak was fixed in the new dict iteration code when the loop target was not a plain variable but an unpacked tuple.

* Memory views did not handle the special case of a NULL buffer strides value, as allowed by PEP3118.

Other changes
-------------


0.17 (2012-09-01)
=================

Features added
--------------

* Alpha quality support for compiling and running Cython generated extension modules in PyPy (through cpyext). Note that this requires at least PyPy 1.9 and in many cases also adaptations in user code, especially to avoid borrowed references when no owned reference is being held directly in C space (a reference in a Python list or dict is not enough, for example). See the documentation on porting Cython code to PyPy.

* "yield from" is supported (PEP 380) and a couple of minor problems with generators were fixed.

* C++ STL container classes automatically coerce from and to the equivalent Python container types on typed assignments and casts. Note that the data in the containers is copied during this conversion.

* C++ iterators can now be iterated over using "for x in cpp_container" whenever cpp_container has begin() and end() methods returning objects satisfying the iterator pattern (that is, it can be incremented, dereferenced, and compared (for non-equality)).

* cdef classes can now have C++ class members (provided a zero-argument constructor exists)

* A new cpython.array standard cimport file allows to efficiently talk to the stdlib array.array data type in Python 2. Since CPython does not export an official C-API for this module, it receives special casing by the compiler in order to avoid setup overhead on user side. In Python 3, both buffers and memory views on the array type already worked out of the box with earlier versions of Cython due to the native support for the buffer interface in the Py3 array module.

* Fast dict iteration is now enabled optimistically also for untyped variables when the common iteration methods are used.

* The unicode string processing code was adapted for the upcoming CPython 3.3 (PEP 393, new Unicode buffer layout).

* Buffer arguments and memory view arguments in Python functions can be declared "not None" to raise a TypeError on None input.

* c(p)def functions in pure mode can specify their return type with "@cython.returns()".

* Automatic dispatch for fused functions with memoryview arguments

* Support newaxis indexing for memoryviews

* Support decorators for fused functions

Bugs fixed
----------

* Old-style Py2 imports did not work reliably in Python 3.x and were broken in Python 3.3. Regardless of this fix, it's generally best to be explicit about relative and global imports in Cython code because old-style imports have a higher overhead. To this end, "from __future__ import absolute_import" is supported in Python/Cython 2.x code now (previous versions of Cython already used it when compiling Python 3 code).

* Stricter constraints on the "inline" and "final" modifiers. If your code does not compile due to this change, chances are these modifiers were previously being ignored by the compiler and can be removed without any performance regression.

* Exceptions are always instantiated while raising them (as in Python), instead of risking to instantiate them in potentially unsafe situations when they need to be handled or otherwise processed.

* locals() properly ignores names that do not have Python compatible types (including automatically inferred types).

* Some garbage collection issues of memory views were fixed.

* numpy.pxd compiles in Python 3 mode.

* Several C compiler warnings were fixed.

* Several bugs related to memoryviews and fused types were fixed.

* Several bug-fixes and improvements related to cythonize(), including ccache-style caching.

Other changes
-------------

* libc.string provides a convenience declaration for const uchar in addition to const char.

* User declared char* types are now recognised as such and auto-coerce to and from Python bytes strings.

* callable() and next() compile to more efficient C code.

* list.append() is faster on average.

* Modules generated by @cython.inline() are written into the directory pointed to by the environment variable CYTHON_CACHE_DIR if set.


0.16 (2012-04-21)
=================

Features added
--------------

* Enhancements to Cython's function type (support for weak references, default arguments, code objects, dynamic attributes, classmethods, staticmethods, and more)

* Fused Types - Template-like support for functions and methods CEP 522 (docs)

* Typed views on memory - Support for efficient direct and indirect buffers (indexing, slicing, transposing, ...) CEP 517 (docs)

* super() without arguments

* Final cdef methods (which translate into direct calls on known instances)

Bugs fixed
----------

* fix alignment handling for record types in buffer support

Other changes
-------------

* support default arguments for closures

* search sys.path for pxd files

* support C++ template casting

* faster traceback building and faster generator termination

* support inplace operators on indexed buffers

* allow nested prange sections


0.15.1 (2011-09-19)
===================

Features added
--------------

Bugs fixed
----------

Other changes
-------------


0.15 (2011-08-05)
=================

Features added
--------------

* Generators (yield) - Cython has full support for generators, generator expressions and PEP 342 coroutines.

* The nonlocal keyword is supported.

* Re-acquiring the gil: with gil - works as expected within a nogil context.

* OpenMP support: prange.

* Control flow analysis prunes dead code and emits warnings and errors about uninitialised variables.

* Debugger command cy set to assign values of expressions to Cython variables and cy exec counterpart $cy_eval().

* Exception chaining PEP 3134.

* Relative imports PEP 328.

* Improved pure syntax including cython.cclass, cython.cfunc, and cython.ccall.

* The with statement has its own dedicated and faster C implementation.

* Support for del.

* Boundschecking directives implemented for builtin Python sequence types.

* Several updates and additions to the shipped standard library .pxd files.

* Forward declaration of types is no longer required for circular references.

Bugs fixed
----------

Other changes
-------------

* Uninitialized variables are no longer initialized to None and accessing them has the same semantics as standard Python.

* globals() now returns a read-only dict of the Cython module's globals, rather than the globals of the first non-Cython module in the stack

* Many C++ exceptions are now special cased to give closer Python counterparts. This means that except+ functions that formerly raised generic RuntimeErrors may raise something else such as ArithmeticError.

* The inlined generator expressions (introduced in Cython 0.13) were disabled in favour of full generator expression support. This breaks code that previously used them inside of cdef functions (usage in def functions continues to work) and induces a performance regression for cases that continue to work but that were previously inlined. We hope to reinstate this feature in the near future.


0.14.1 (2011-02-04)
===================

Features added
--------------

* The gdb debugging support was extended to include all major Cython features, including closures.

* raise MemoryError() is now safe to use as Cython replaces it with the correct C-API call.

Bugs fixed
----------

Other changes
-------------

* Decorators on special methods of cdef classes now raise a compile time error rather than being ignored.

* In Python 3 language level mode (-3 option), the 'str' type is now mapped to 'unicode', so that cdef str s declares a Unicode string even when running in Python 2.


0.14 (2010-12-14)
=================

Features added
--------------

* Python classes can now be nested and receive a proper closure at definition time.

* Redefinition is supported for Python functions, even within the same scope.

* Lambda expressions are supported in class bodies and at the module level.

* Metaclasses are supported for Python classes, both in Python 2 and Python 3 syntax. The Python 3 syntax (using a keyword argument in the type declaration) is preferred and optimised at compile time.

* "final" extension classes prevent inheritance in Python space. This feature is available through the new "cython.final" decorator. In the future, these classes may receive further optimisations.

* "internal" extension classes do not show up in the module dictionary. This feature is available through the new "cython.internal" decorator.

* Extension type inheritance from builtin types, such as "cdef class MyUnicode(unicode)", now works without further external type redeclarations (which are also strongly discouraged now and continue to issue a warning).

* GDB support. https://docs.cython.org/src/userguide/debugging.html

* A new build system with support for inline distutils directives, correct dependency tracking, and parallel compilation. https://github.com/cython/cython/wiki/enhancements-distutils_preprocessing

* Support for dynamic compilation at runtime via the new cython.inline function and cython.compile decorator. https://github.com/cython/cython/wiki/enhancements-inline

* "nogil" blocks are supported when compiling pure Python code by writing "with cython.nogil".

* Iterating over arbitrary pointer types is now supported, as is an optimized version of the in operator, e.g. x in ptr[a:b].

Bugs fixed
----------

* In parallel assignments, the right side was evaluated in reverse order in 0.13. This could result in errors if it had side effects (e.g. function calls).

* In some cases, methods of builtin types would raise a SystemError instead of an AttributeError when called on None.

Other changes
-------------

* Constant tuples are now cached over the lifetime of an extension module, just like CPython does. Constant argument tuples of Python function calls are also cached.

* Closures have tightened to include exactly the names used in the inner functions and classes. Previously, they held the complete locals of the defining function.

* The builtin "next()" function in Python 2.6 and later is now implemented internally and therefore available in all Python versions. This makes it the preferred and portable way of manually advancing an iterator.

* In addition to the previously supported inlined generator expressions in 0.13, "sorted(genexpr)" can now be used as well. Typing issues were fixed in "sum(genexpr)" that could lead to invalid C code being generated. Other known issues with inlined generator expressions were also fixed that make upgrading to 0.14 a strong recommendation for code that uses them. Note that general generators and generator expressions continue to be not supported.

* Inplace arithmetic operators now respect the cdivision directive and are supported for complex types.

* Typing a variable as type "complex" previously gave it the Python object type. It now uses the appropriate C/C++ double complex type. A side-effect is that assignments and typed function parameters now accept anything that Python can coerce to a complex, including integers and floats, and not only complex instances.

* Large integer literals pass through the compiler in a safer way. To prevent truncation in C code, non 32-bit literals are turned into Python objects if not used in a C context. This context can either be given by a clear C literal suffix such as "UL" or "LL" (or "L" in Python 3 code), or it can be an assignment to a typed variable or a typed function argument, in which case it is up to the user to take care of a sufficiently large value space of the target.

* Python functions are declared in the order they appear in the file, rather than all being created at module creation time. This is consistent with Python and needed to support, for example, conditional or repeated declarations of functions. In the face of circular imports this may cause code to break, so a new --disable-function-redefinition flag was added to revert to the old behavior. This flag will be removed in a future release, so should only be used as a stopgap until old code can be fixed.


0.13 (2010-08-25)
=================

Features added
--------------

* Closures are fully supported for Python functions. Cython supports inner functions and lambda expressions. Generators and generator expressions are not supported in this release.

* Proper C++ support. Cython knows about C++ classes, templates and overloaded function signatures, so that Cython code can interact with them in a straight forward way.

* Type inference is enabled by default for safe C types (e.g. double, bint, C++ classes) and known extension types. This reduces the need for explicit type declarations and can improve the performance of untyped code in some cases. There is also a verbose compile mode for testing the impact on user code.

* Cython's for-in-loop can iterate over C arrays and sliced pointers. The type of the loop variable will be inferred automatically in this case.

* The Py_UNICODE integer type for Unicode code points is fully supported, including for-loops and 'in' tests on unicode strings. It coerces from and to single character unicode strings. Note that untyped for-loop variables will automatically be inferred as Py_UNICODE when iterating over a unicode string. In most cases, this will be much more efficient than yielding sliced string objects, but can also have a negative performance impact when the variable is used in a Python context multiple times, so that it needs to coerce to a unicode string object more than once. If this happens, typing the loop variable as unicode or object will help.

* The built-in functions any(), all(), sum(), list(), set() and dict() are inlined as plain for loops when called on generator expressions. Note that generator expressions are not generally supported apart from this feature. Also, tuple(genexpr) is not currently supported - use tuple([listcomp]) instead.

* More shipped standard library declarations. The python_* and stdlib/stdio .pxd files have been deprecated in favor of clib.* and cpython[.*] and may get removed in a future release.

* Pure Python mode no longer disallows non-Python keywords like 'cdef', 'include' or 'cimport'. It also no longer recognises syntax extensions like the for-from loop.

* Parsing has improved for Python 3 syntax in Python code, although not all features are correctly supported. The missing Python 3 features are being worked on for the next release.

* from __future__ import print_function is supported in Python 2.6 and later. Note that there is currently no emulation for earlier Python versions, so code that uses print() with this future import will require at least Python 2.6.

* New compiler directive language_level (valid values: 2 or 3) with corresponding command line options -2 and -3 requests source code compatibility with Python 2.x or Python 3.x respectively. Language level 3 currently enforces unicode literals for unprefixed string literals, enables the print function (requires Python 2.6 or later) and keeps loop variables in list comprehensions from leaking.

* Loop variables in set/dict comprehensions no longer leak into the surrounding scope (following Python 2.7). List comprehensions are unchanged in language level 2.

* print >> stream

Bugs fixed
----------

Other changes
-------------

* The availability of type inference by default means that Cython will also infer the type of pointers on assignments. Previously, code like this::

     cdef char* s = ...
     untyped_variable = s

  would convert the char* to a Python bytes string and assign that. This is no longer the case and no coercion will happen in the example above. The correct way of doing this is through an explicit cast or by typing the target variable, i.e.

  ::

     cdef char* s = ...
     untyped_variable1 = <bytes>s
     untyped_variable2 = <object>s

     cdef object py_object = s
     cdef bytes  bytes_string = s

* bool is no longer a valid type name by default. The problem is that it's not clear whether bool should refer to the Python type or the C++ type, and expecting one and finding the other has already led to several hard-to-find bugs. Both types are available for importing: you can use from cpython cimport bool for the Python bool type, and from libcpp cimport bool for the C++ type. bool is still a valid object by default, so one can still write bool(x).

* ``__getsegcount__`` is now correctly typed to take a ``Py_size_t*`` rather than an ``int*``.


0.12.1 (2010-02-02)
===================

Features added
--------------

* Type inference improvements.

  * There have been several bug fixes and improvements to the type inferencer.

  * Notably, there is now a "safe" mode enabled by setting the infer_types directive to None. (The None here refers to the "default" mode, which will be the default in 0.13.) This safe mode limits inference to Python object types and C doubles, which should speed up execution without affecting any semantics such as integer overflow behavior like infer_types=True might. There is also an infer_types.verbose option which allows one to see what types are inferred.

* The boundscheck directive works for lists and tuples as well as buffers.

* len(s) and s.decode("encoding") are efficiently supported for char* s.

* Cython's INLINE macro has been renamed to CYTHON_INLINE to reduce conflict and has better support for the MSVC compiler on Windows. It is no longer clobbered if externally defined.

* Revision history is now omitted from the source package, resulting in a 85% size reduction. Running make repo will download the history and turn the directory into a complete Mercurial working repository.

* Cython modules don't need to be recompiled when the size of an external type grows. (A warning, rather than an error, is produced.) This should be helpful for binary distributions relying on NumPy.

Bugs fixed
----------

* Several other bugs and minor improvements have been made. This release should be fully backwards compatible with 0.12.

Other changes
-------------


0.12 (2009-11-23)
=================

Features added
--------------

* Type inference with the infer_types directive

* Seamless C++ complex support

* Fast extension type instantiation using the normal Python meme obj = MyType.__new__(MyType)

* Improved support for Py3.1

* Cython now runs under Python 3.x using the 2to3 tool

* unittest support for doctests in Cython modules

* Optimised handling of C strings (char*): for c in cstring[2:50] and cstring.decode()

* Looping over c pointers: for i in intptr[:50].

* pyximport improvements

* cython_freeze improvements

Bugs fixed
----------

* Many bug fixes

Other changes
-------------

* Many other optimisation, e.g. enumerate() loops, parallel swap assignments (a,b = b,a), and unicode.encode()

* More complete numpy.pxd


0.11.2 (2009-05-20)
===================

Features added
--------------

* There's now native complex floating point support! C99 complex will be used if complex.h is included, otherwise explicit complex arithmetic working on all C compilers is used. [Robert Bradshaw]

  ::

      cdef double complex a = 1 + 0.3j
      cdef np.ndarray[np.complex128_t, ndim=2] arr = \
         np.zeros(10, np.complex128)

* Cython can now generate a main()-method for embedding of the Python interpreter into an executable (see :issue:`289`) [Robert Bradshaw]

* @wraparound directive (another way to disable arr[idx] for negative idx) [Dag Sverre Seljebotn]

* Correct support for NumPy record dtypes with different alignments, and "cdef packed struct" support [Dag Sverre Seljebotn]

* @callspec directive, allowing custom calling convention macros [Lisandro Dalcin]

Bugs fixed
----------

Other changes
-------------

* Bug fixes and smaller improvements. For the full list, see [1].
