================
Cython Changelog
================

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

* Alpha quality support for compiling and running Cython generated extension modules in PyPy (through cpyext). Note that this requires at leastPyPy 1.9 and in many cases also adaptations in user code, especially to avoid borrowed references when no owned reference is being held directly in C space (a reference in a Python list or dict is not enough, for example). See the documentation on porting Cython code to PyPy.

* "yield from" is supported (PEP 380) and a couple of minor problems with generators were fixed.

* C++ STL container classes automatically coerce from and to the equivalent Python container types on typed assignments and casts. Usage examples are here. Note that the data in the containers is copied during this conversion.

* C++ iterators can now be iterated over using for x in cpp_container whenever cpp_container has begin() and end() methods returning objects satisfying the iterator pattern (that is, it can be incremented, dereferenced, and compared (for non-equality)).

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

* Stricter constraints on the inline and final modifiers. If your code does not compile due to this change, chances are these modifiers were previously being ignored by the compiler and can be removed without any performance regression.

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
