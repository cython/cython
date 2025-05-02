
.. _pure-mode:

Pure Python Mode
================

In some cases, it's desirable to speed up Python code without losing the
ability to run it with the Python interpreter.  While pure Python scripts
can be compiled with Cython, it usually results only in a speed gain of
about 20%-50%.

To go beyond that, Cython provides language constructs to add static typing
and cythonic functionalities to a Python module to make it run much faster
when compiled, while still allowing it to be interpreted.
This is accomplished via an augmenting ``.pxd`` file, via Python
type :ref:`pep484_type_annotations` (following
`PEP 484 <https://www.python.org/dev/peps/pep-0484/>`_ and
`PEP 526 <https://www.python.org/dev/peps/pep-0526/>`_), and/or
via special functions and decorators available after importing the magic
``cython`` module.  All three ways can be combined at need, although
projects would commonly decide on a specific way to keep the static type
information easy to manage.

Although it is not typically recommended over writing straight Cython code
in a :file:`.pyx` file, there are legitimate reasons to do this - easier
testing and debugging, collaboration with pure Python developers, etc.
In pure mode, you are more or less restricted to code that can be expressed
(or at least emulated) in Python, plus static type declarations. Anything
beyond that can only be done in .pyx files with extended language syntax,
because it depends on features of the Cython compiler.

.. _augmenting_pxd:

Augmenting .pxd
---------------

Using an augmenting :file:`.pxd` allows to let the original :file:`.py` file
completely untouched.  On the other hand, one needs to maintain both the
:file:`.pxd` and the :file:`.py` to keep them in sync.

While declarations in a :file:`.pyx` file must correspond exactly with those
of a :file:`.pxd` file with the same name (and any contradiction results in
a compile time error, see :doc:`pxd_files`), the untyped definitions in a
:file:`.py` file can be overridden and augmented with static types by the more
specific ones present in a :file:`.pxd`.

If a :file:`.pxd` file is found with the same name as the :file:`.py` file
being compiled, it will be searched for :keyword:`cdef` classes and
:keyword:`cdef`/:keyword:`cpdef` functions and methods.  The compiler will
then convert the corresponding classes/functions/methods in the :file:`.py`
file to be of the declared type.  Thus if one has a file :file:`A.py`:

.. literalinclude:: ../../examples/tutorial/pure/A.py

and adds :file:`A.pxd`:

.. literalinclude:: ../../examples/tutorial/pure/A.pxd

then Cython will compile the :file:`A.py` as if it had been written as follows:

.. literalinclude:: ../../examples/tutorial/pure/A_equivalent.pyx

Notice how in order to provide the Python wrappers to the definitions
in the :file:`.pxd`, that is, to be accessible from Python,

* Python visible function signatures must be declared as `cpdef` (with default
  arguments replaced by a `*` to avoid repetition)::

    cpdef int myfunction(int x, int y=*)

* C function signatures of internal functions can be declared as `cdef`::

    cdef double _helper(double a)

* `cdef` classes (extension types) are declared as `cdef class`;

* `cdef` class attributes must be declared as `cdef public` if read/write
  Python access is needed, `cdef readonly` for read-only Python access, or
  plain `cdef` for internal C level attributes;

* `cdef` class methods must be declared as `cpdef` for Python visible
  methods or `cdef` for internal C methods.


In the example above, the type of the local variable `a` in `myfunction()`
is not fixed and will thus be a :term:`Python object`.  To statically type it, one
can use Cython's ``@cython.locals`` decorator (see :ref:`magic_attributes`,
and :ref:`magic_attributes_pxd`).

Normal Python (:keyword:`def`) functions cannot be declared in :file:`.pxd`
files.  It is therefore currently impossible to override the types of plain
Python functions in :file:`.pxd` files, e.g. to override types of their local
variables.  In most cases, declaring them as `cpdef` will work as expected.


.. _magic_attributes:

Magic Attributes
----------------

Special decorators are available from the magic ``cython`` module that can
be used to add static typing within the Python file, while being ignored
by the interpreter.

This option adds the ``cython`` module dependency to the original code, but
does not require to maintain a supplementary :file:`.pxd` file.  Cython
provides a fake version of this module as `Cython.Shadow`, which is available
as `cython.py` when Cython is installed, but can be copied to be used by other
modules when Cython is not installed.


"Compiled" switch
^^^^^^^^^^^^^^^^^

* ``compiled`` is a special variable which is set to ``True`` when the compiler
  runs, and ``False`` in the interpreter. Thus, the code

  .. literalinclude:: ../../examples/tutorial/pure/compiled_switch.py

  will behave differently depending on whether or not the code is executed as a
  compiled extension (:file:`.so`/:file:`.pyd`) module or a plain :file:`.py`
  file.


Static typing
^^^^^^^^^^^^^

* ``cython.declare`` declares a typed variable in the current scope, which can be
  used in place of the :samp:`cdef type var [= value]` construct. This has two forms,
  the first as an assignment (useful as it creates a declaration in interpreted
  mode as well):

  .. literalinclude:: ../../examples/tutorial/pure/cython_declare.py

  and the second mode as a simple function call:

  .. literalinclude:: ../../examples/tutorial/pure/cython_declare2.py

  It can also be used to define extension type private, readonly and public attributes:

  .. literalinclude:: ../../examples/tutorial/pure/cclass.py

* ``@cython.locals`` is a decorator that is used to specify the types of local
  variables in the function body (including the arguments):

  .. literalinclude:: ../../examples/tutorial/pure/locals.py

* ``@cython.returns(<type>)`` specifies the function's return type.

* ``@cython.exceptval(value=None, *, check=False)`` specifies the function's exception
  return value and exception check semantics as follows::

    @exceptval(-1)               # cdef int func() except -1:
    @exceptval(-1, check=False)  # cdef int func() except -1:
    @exceptval(check=True)       # cdef int func() except *:
    @exceptval(-1, check=True)   # cdef int func() except? -1:
    @exceptval(check=False)      # no exception checking/propagation

  If exception propagation is disabled, any Python exceptions that are raised
  inside of the function will be printed and ignored.

C types
^^^^^^^

There are numerous types built into the Cython module.  It provides all the
standard C types, namely ``char``, ``short``, ``int``, ``long``, ``longlong``
as well as their unsigned versions ``uchar``, ``ushort``, ``uint``, ``ulong``,
``ulonglong``.  The special ``bint`` type is used for C boolean values and
:c:type:`Py_ssize_t` for (signed) sizes of Python containers.

For each type, there are pointer types ``p_int``, ``pp_int``, etc., up to
three levels deep in interpreted mode, and infinitely deep in compiled mode.
Further pointer types can be constructed with ``cython.pointer[cython.int]``
(or ``cython.pointer(cython.int)`` for compatibility with Cython versions before 3.1),
and arrays as ``cython.int[10]``. A limited attempt is made to emulate these
more complex types, but only so much can be done from the Python language.

The Python types int, long and bool are interpreted as C ``int``, ``long``
and ``bint`` respectively. Also, the Python builtin types ``list``, ``dict``,
``tuple``, etc. may be used, as well as any user defined types.

Typed C-tuples can be declared as a tuple of C types.


Extension types and cdef functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* The class decorator ``@cython.cclass`` creates a ``cdef class``.

* The function/method decorator ``@cython.cfunc`` creates a :keyword:`cdef` function.

* ``@cython.ccall`` creates a :keyword:`cpdef` function, i.e. one that Cython code
  can call at the C level.

* ``@cython.locals`` declares local variables (see above). It can also be used to
  declare types for arguments, i.e. the local variables that are used in the
  signature.

* ``@cython.inline`` is the equivalent of the C ``inline`` modifier.

* ``@cython.final`` terminates the inheritance chain by preventing a type from
  being used as a base class, or a method from being overridden in subtypes.
  This enables certain optimisations such as inlined method calls.

Here is an example of a :keyword:`cdef` function::

    @cython.cfunc
    @cython.returns(cython.bint)
    @cython.locals(a=cython.int, b=cython.int)
    def c_compare(a,b):
        return a == b


Managing the Global Interpreter Lock
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``cython.nogil`` can be used as a context manager or as a decorator to replace the :keyword:`nogil` keyword::

    with cython.nogil:
        # code block with the GIL released

    @cython.nogil
    @cython.cfunc
    def func_released_gil() -> cython.int:
        # function that can be run with the GIL released

  Note that the two uses differ: the context manager releases the GIL while the decorator marks that a
  function *can* be run without the GIL. See :ref:`cython_and_gil` for more details.

* ``cython.gil`` can be used as a context manager to replace the :keyword:`gil` keyword::

    with cython.gil:
        # code block with the GIL acquired

  .. Note:: Cython currently does not support the ``@cython.with_gil`` decorator.

Both directives accept an optional boolean parameter for conditionally
releasing or acquiring the GIL. The condition must be constant (at compile time)::

  with cython.nogil(False):
      # code block with the GIL not released

  @cython.nogil(True)
  @cython.cfunc
  def func_released_gil() -> cython.int:
      # function with the GIL released

  with cython.gil(False):
      # code block with the GIL not acquired

  with cython.gil(True):
      # code block with the GIL acquired

A common use case for conditionally acquiring and releasing the GIL are fused types
that allow different GIL handling depending on the specific type (see :ref:`gil_conditional`).


.. py:module:: cython.cimports

cimports
^^^^^^^^

The special ``cython.cimports`` package name gives access to cimports
in code that uses Python syntax.  Note that this does not mean that C
libraries become available to Python code.  It only means that you can
tell Cython what cimports you want to use, without requiring special
syntax.  Running such code in plain Python will fail.

.. literalinclude:: ../../examples/tutorial/pure/py_cimport.py

Since such code must necessarily refer to the non-existing
``cython.cimports`` 'package', the plain cimport form
``cimport cython.cimports...`` is not available.
You must use the form ``from cython.cimports...``.


Further Cython functions and declarations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``address`` is used in place of the ``&`` operator::

    cython.declare(x=cython.int, x_ptr=cython.p_int)
    x_ptr = cython.address(x)

* ``sizeof`` emulates the `sizeof` operator.  It can take both types and
  expressions.

  ::

    cython.declare(n=cython.longlong)
    print(cython.sizeof(cython.longlong))
    print(cython.sizeof(n))

* ``typeof`` returns a string representation of the argument's type for debugging purposes.  It can take expressions.

  ::

    cython.declare(n=cython.longlong)
    print(cython.typeof(n))

* ``struct`` can be used to create struct types.::

    MyStruct = cython.struct(x=cython.int, y=cython.int, data=cython.double)
    a = cython.declare(MyStruct)

  is equivalent to the code::

    cdef struct MyStruct:
        int x
        int y
        double data

    cdef MyStruct a

* ``union`` creates union types with exactly the same syntax as ``struct``.

* ``typedef`` defines a type under a given name::

    T = cython.typedef(cython.p_int)   # ctypedef int* T

* ``cast`` will (unsafely) reinterpret an expression type. ``cython.cast(T, t)``
  is equivalent to ``<T>t``. The first attribute must be a type, the second is
  the expression to cast. Specifying the optional keyword argument
  ``typecheck=True`` has the semantics of ``<T?>t``.

  ::

    t1 = cython.cast(T, t)
    t2 = cython.cast(T, t, typecheck=True)

* ``fused_type`` creates a new type definition that refers to the multiple types.
  The following example declares a new type called ``my_fused_type`` which can
  be either an ``int`` or a ``double``.::

    my_fused_type = cython.fused_type(cython.int, cython.float)

.. _magic_attributes_pxd:

Magic Attributes within the .pxd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The special `cython` module can also be imported and used within the augmenting
:file:`.pxd` file. For example, the following Python file :file:`dostuff.py`:

.. literalinclude:: ../../examples/tutorial/pure/dostuff.py

can be augmented with the following :file:`.pxd` file :file:`dostuff.pxd`:

.. literalinclude:: ../../examples/tutorial/pure/dostuff.pxd

The :func:`cython.declare()` function can be used to specify types for global
variables in the augmenting :file:`.pxd` file.

.. _pep484_type_annotations:

PEP-484 type annotations
------------------------

Python `type hints <https://www.python.org/dev/peps/pep-0484>`_
can be used to declare argument types, as shown in the
following example:

  .. literalinclude:: ../../examples/tutorial/pure/annotations.py

Note the use of ``cython.int`` rather than ``int`` - Cython does not translate
an ``int`` annotation to a C integer by default since the behaviour can be
quite different with respect to overflow and division.

Annotations on global variables are currently ignored.  This is because we expect
annotation-typed code to be in majority written for Python, and global type annotations
would turn the Python variable into an internal C variable, thus removing it from the
module dict.  To declare global variables as typed C variables, use ``@cython.declare()``.

Annotations can be combined with the ``@cython.exceptval()`` decorator for non-Python
return types:

  .. literalinclude:: ../../examples/tutorial/pure/exceptval.py

Note that the default exception handling behaviour when returning C numeric types
is to check for ``-1``, and if that was returned, check Python's error indicator
for an exception.  This means, if no ``@exceptval`` decorator is provided, and the
return type is a numeric type, then the default with type annotations is
``@exceptval(-1, check=True)``, in order to make sure that exceptions are correctly
and efficiently reported to the caller.  Exception propagation can be disabled
explicitly with ``@exceptval(check=False)``, in which case any Python exceptions
raised inside of the function will be printed and ignored.

Since version 0.27, Cython also supports the variable annotations defined
in `PEP 526 <https://www.python.org/dev/peps/pep-0526/>`_. This allows to
declare types of variables in a Python 3.6 compatible way as follows:

.. literalinclude:: ../../examples/tutorial/pure/pep_526.py

There is currently no way to express the visibility of object attributes.

Disabling annotations
^^^^^^^^^^^^^^^^^^^^^

To avoid conflicts with other kinds of annotation
usages, Cython's use of annotations to specify types can be disabled with the
``annotation_typing`` :ref:`compiler directive<compiler-directives>`. From Cython 3
you can use this as a decorator or a with statement, as shown in the following example:

.. literalinclude:: ../../examples/tutorial/pure/disabled_annotations.py



``typing`` Module
^^^^^^^^^^^^^^^^^

Support for the full range of annotations described by PEP-484 is not yet
complete. Cython 3 currently understands the following features from the
``typing`` module:

* ``Optional[tp]``, which is interpreted as ``tp or None``;
* ``Union[tp, None]`` or ``Union[None, tp]``, which is interpreted as ``tp or None``;
* typed containers such as ``List[str]``, which is interpreted as ``list``. The
  hint that the elements are of type ``str`` is currently ignored;
* ``Tuple[...]``, which is converted into a Cython C-tuple where possible
  and a regular Python ``tuple`` otherwise.
* ``ClassVar[...]``, which is understood in the context of
  ``cdef class`` or ``@cython.cclass``.

Some of the unsupported features are likely to remain
unsupported since these type hints are not relevant for the compilation to
efficient C code. In other cases, however, where the generated C code could
benefit from these type hints but does not currently, help is welcome to
improve the type analysis in Cython.

Reference table
^^^^^^^^^^^^^^^

The following reference table documents how type annotations are currently interpreted.
Cython 0.29 behaviour is only shown where it differs from Cython 3.0 behaviour.
The current limitations will likely be lifted at some point.

.. csv-table:: Annotation typing rules
   :file: annotation_typing_table.csv
   :header-rows: 1
   :class: longtable
   :widths: 1 1 1


Tips and Tricks
---------------

Avoiding the ``cython`` runtime dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python modules that are intended to run both compiled and as plain Python
usually have the line ``ìmport cython`` in them and make use of the magic
attributes in that module. If not compiled, this creates a runtime dependency
on Cython's shadow module that provides fake implementations of types and
decorators.

Code that does not want to require Cython or its shadow module as as runtime
dependency at all can often get away with a simple, stripped-down replacement
like the following::

    try:
        import cython
    except ImportError:
        class _fake_cython:
            compiled = False
            def cfunc(self, func): return func
            def ccall(self, func): return func
            def __getattr__(self, type_name): return "object"

        cython = _fake_cython()


.. _calling-c-functions:

Calling C functions
^^^^^^^^^^^^^^^^^^^

The magic :py:mod:`cython.cimports` package provides a way to cimport external
compile time C declarations from code written in plain Python.  For convenience,
it also provides a fallback Python implementation for the ``libc.math`` module.

However, it is normally not possible to *call* C functions in pure Python
code as there is no general way to represent them in normal (uncompiled) Python.
But in cases where an equivalent Python function exists, this can be achieved
by combining C function coercion with a conditional import as follows:

.. literalinclude:: ../../examples/tutorial/pure/mymodule.pxd

.. literalinclude:: ../../examples/tutorial/pure/mymodule.py

Note that the "sin" function will show up in the module namespace of "mymodule"
here (i.e. there will be a ``mymodule.sin()`` function).  You can mark it as an
internal name according to Python conventions by renaming it to "_sin" in the
``.pxd`` file as follows::

    cdef extern from "math.h":
        cpdef double _sin "sin" (double x)

You would then also change the Python import to ``from math import sin as _sin``
to make the names match again.


Using C arrays for fixed size lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C arrays can automatically coerce to Python lists or tuples.
This can be exploited to replace fixed size Python lists in Python code by C
arrays when compiled.  An example:

.. literalinclude:: ../../examples/tutorial/pure/c_arrays.py

In normal Python, this will use a Python list to collect the counts, whereas
Cython will generate C code that uses a C array of C ints.
