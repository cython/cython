================
Cython Changelog
================

0.24.1 (2016-07-15)
===================

Bugs fixed
----------

* IPython cell magic was lacking a good way to enable Python 3 code semantics.
  It can now be used as "%%cython -3".

* Follow a recent change in `PEP 492 <https://www.python.org/dev/peps/pep-0498/>`_
  and CPython 3.5.1 that now requires the ``__aiter__()`` method of asynchronous
  iterators to be a simple ``def`` method instead of an ``async def`` method.

* Coroutines and generators were lacking the ``__module__`` special attribute.

* C++ ``std::complex`` values failed to auto-convert from and to Python complex
  objects.

* Namespaced C++ types could not be used as memory view types due to lack of
  name mangling.  Patch by Ivan Smirnov.

* Assignments between the identical C++ types that were declared with differently
  typedefed template types could fail.

* Rebuilds could fail to evaluate dependency timestamps in C++ mode.
  Path by Ian Henriksen.

* Macros defined in the ``distutils`` compiler option do not require values
  anymore. Patch by Ian Henriksen.

* Minor fixes for MSVC, Cygwin and PyPy.


0.24 (2016-04-04)
=================

Features added
--------------

* PEP 498: Literal String Formatting (f-strings).
  Original patch by Jelle Zijlstra.
  https://www.python.org/dev/peps/pep-0498/

* PEP 515: Underscores as visual separators in number literals.
  https://www.python.org/dev/peps/pep-0515/

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

* Reference leak when "*args" argument was reassigned in closures.

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

* PEP 492 (async/await) was implemented.
  See https://www.python.org/dev/peps/pep-0492/

* PEP 448 (Additional Unpacking Generalizations) was implemented.
  See https://www.python.org/dev/peps/pep-0448/

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

* PEP 479: turn accidental StopIteration exceptions that exit generators
  into a RuntimeError, activated with future import "generator_stop".
  See https://www.python.org/dev/peps/pep-0479/

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
  (following CPython 3.5).  See http://bugs.python.org/issue21205

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
  See http://bugs.python.org/issue21420

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

* GDB support. http://docs.cython.org/src/userguide/debugging.html

* A new build system with support for inline distutils directives, correct dependency tracking, and parallel compilation. http://wiki.cython.org/enhancements/distutils_preprocessing

* Support for dynamic compilation at runtime via the new cython.inline function and cython.compile decorator. http://wiki.cython.org/enhancements/inline

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

* Cython can now generate a main()-method for embedding of the Python interpreter into an executable (see #289) [Robert Bradshaw]

* @wraparound directive (another way to disable arr[idx] for negative idx) [Dag Sverre Seljebotn]

* Correct support for NumPy record dtypes with different alignments, and "cdef packed struct" support [Dag Sverre Seljebotn]

* @callspec directive, allowing custom calling convention macros [Lisandro Dalcin]

Bugs fixed
----------

Other changes
-------------

* Bug fixes and smaller improvements. For the full list, see [1].
