Porting Cython code to PyPy
===========================

Cython has basic support for cpyext, the layer in
`PyPy <http://pypy.org/>`_ that emulates CPython's C-API.  This is
achieved by making the generated C code adapt at C compile time, so
the generated code will compile in both CPython and PyPy unchanged.

However, beyond what Cython can cover and adapt internally, the cpyext
C-API emulation involves some differences to the real C-API in CPython
that have a visible impact on user code.  This page lists major
differences and ways to deal with them in order to write Cython code
that works in both CPython and PyPy.


Reference counts
----------------

A general design difference in PyPy is that the runtime does not use
reference counting internally but always a garbage collector.  Reference
counting is only emulated at the cpyext layer by counting references
being held in C space.  This implies that the reference count in PyPy
is generally different from that in CPython because it does not count
any references held in Python space.


Object lifetime
---------------

As a direct consequence of the different garbage collection characteristics,
objects may see the end of their lifetime at other points than in
CPython.  Special care therefore has to be taken when objects are expected
to have died in CPython but may not in PyPy.  Specifically, a deallocator
method of an extension type (``__dealloc__()``) may get called at a much
later point than in CPython, triggered rather by memory getting tighter
than by objects dying.

If the point in the code is known when an object is supposed to die (e.g.
when it is tied to another object or to the execution time of a function),
it is worth considering if it can be invalidated and cleaned up manually at
that point, rather than relying on a deallocator.

As a side effect, this can sometimes even lead to a better code design,
e.g. when context managers can be used together with the ``with`` statement.


Borrowed references and data pointers
-------------------------------------

The memory management in PyPy is allowed to move objects around in memory.
The C-API layer is only an indirect view on PyPy objects and often replicates
data or state into C space that is then tied to the lifetime of a C-API
object rather then the underlying PyPy object.  It is important to understand
that these two objects are separate things in cpyext.

The effect can be that when data pointers or borrowed references are used,
and the owning object is no longer directly referenced from C space, the
reference or data pointer may become invalid at some point, even if the
object itself is still alive.  As opposed to CPython, it is not enough to
keep the reference to the object alive in a list (or other Python container),
because the contents of those is only managed in Python space and thus only
references the PyPy object.  A reference in a Python container will not keep
the C-API view on it alive.  Entries in a Python class dict will obviously
not work either.

One of the more visible places where this may happen is when accessing the
:c:type:`char*` buffer of a byte string.  In PyPy, this will only work as
long as the Cython code holds a direct reference to the byte string object
itself.

Another point is when CPython C-API functions are used directly that return
borrowed references, e.g. :c:func:`PyTuple_GET_ITEM()` and similar functions,
but also some functions that return borrowed references to built-in modules or
low-level objects of the runtime environment.  The GIL in PyPy only guarantees
that the borrowed reference stays valid up to the next call into PyPy (or
its C-API), but not necessarily longer.

When accessing the internals of Python objects or using borrowed references
longer than up to the next call into PyPy, including reference counting or
anything that frees the GIL, it is therefore required to additionally keep
direct owned references to these objects alive in C space, e.g. in local
variables in a function or in the attributes of an extension type.

When in doubt, avoid using C-API functions that return borrowed references,
or surround the usage of a borrowed reference explicitly by a pair of calls
to :c:func:`Py_INCREF()` when getting the reference and :c:func:`Py_DECREF()`
when done with it to convert it into an owned reference.


Builtin types, slots and fields
-------------------------------

The following builtin types are not currently available in cpyext in
form of their C level representation: :c:type:`PyComplexObject`,
:c:type:`PyFloatObject` and :c:type:`PyBoolObject`.

Many of the type slot functions of builtin types are not initialised
in cpyext and can therefore not be used directly.

Similarly, almost none of the (implementation) specific struct fields of
builtin types is exposed at the C level, such as the ``ob_digit`` field
of :c:type:`PyLongObject` or the ``allocated`` field of the
:c:type:`PyListObject` struct etc.  Although the ``ob_size`` field of
containers (used by the :c:func:`Py_SIZE()` macro) is available, it is
not guaranteed to be accurate.

It is best not to access any of these struct fields and slots and to
use the normal Python types instead as well as the normal Python
protocols for object operations.  Cython will map them to an appropriate
usage of the C-API in both CPython and cpyext.


GIL handling
------------

Currently, the GIL handling function :c:func:`PyGILState_Ensure` is not
re-entrant in PyPy and deadlocks when called twice.  This means that
code that tries to acquire the GIL "just in case", because it might be
called with or without the GIL, will not work as expected in PyPy.
See `PyGILState_Ensure should not deadlock if GIL already held
<https://bitbucket.org/pypy/pypy/issues/1778>`_.


Efficiency
----------

Simple functions and especially macros that are used for speed in CPython
may exhibit substantially different performance characteristics in cpyext.

Functions returning borrowed references were already mentioned as requiring
special care, but they also induce substantially more runtime overhead because
they often create weak references in PyPy where they only return a plain
pointer in CPython.  A visible example is :c:func:`PyTuple_GET_ITEM()`.

Some more high-level functions may also show entirely different performance
characteristics, e.g. :c:func:`PyDict_Next()` for dict iteration.  While
being the fastest way to iterate over a dict in CPython, having linear time
complexity and a low overhead, it currently has quadratic runtime in PyPy
because it maps to normal dict iteration, which cannot keep track of the
current position between two calls and thus needs to restart the iteration
on each call.

The general advice applies here even more than in CPython, that it is always
best to rely on Cython generating appropriately adapted C-API handling code
for you than to use the C-API directly - unless you really know what you are
doing.  And if you find a better way of doing something in PyPy and cpyext
than Cython currently does, it's best to fix Cython for everyone's benefit.


Known problems
--------------

* As of PyPy 1.9, subtyping builtin types can result in infinite recursion
  on method calls in some rare cases.

* Docstrings of special methods are not propagated to Python space.

* The Python 3.x adaptations in pypy3 only slowly start to include the
  C-API, so more incompatibilities can be expected there.


Bugs and crashes
----------------

The cpyext implementation in PyPy is much younger and substantially less
mature than the well tested C-API and its underlying native implementation
in CPython.  This should be remembered when running into crashes, as the
problem may not always be in your code or in Cython.  Also, PyPy and its
cpyext implementation are less easy to debug at the C level than CPython
and Cython, simply because they were not designed for it.
