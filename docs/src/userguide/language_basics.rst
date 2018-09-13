.. highlight:: cython

.. _language-basics:
.. _struct:
.. _union:
.. _enum:
.. _ctypedef:


*****************
Language Basics
*****************

.. _declaring_data_types:

Declaring Data Types
====================

As a dynamic language, Python encourages a programming style of considering
classes and objects in terms of their methods and attributes, more than where
they fit into the class hierarchy.

This can make Python a very relaxed and comfortable language for rapid
development, but with a price - the 'red tape' of managing data types is
dumped onto the interpreter. At run time, the interpreter does a lot of work
searching namespaces, fetching attributes and parsing argument and keyword tuples.
This run-time ‘late binding’ is a major cause of Python’s relative slowness
compared to ‘early binding’ languages such as C++.

However with Cython it is possible to gain significant speed-ups through
the use of ‘early binding’ programming techniques.

.. note:: Typing is not a necessity

    Providing static typing to parameters and variables is convenience to
    speed up your code, but it is not a necessity. Optimize where and when needed.
    In fact, typing can *slow down* your code in the case where the
    typing does not allow optimizations but where Cython still needs to
    check that the type of some object matches the declared type.


.. _c_variable_and_type_definitions:

C variable and type definitions
===============================

The :keyword:`cdef` statement is used to declare C variables, either local or
module-level::

    cdef int i, j, k
    cdef float f, g[42], *h

and C :keyword:`struct`, :keyword:`union` or :keyword:`enum` types:

.. literalinclude:: ../../examples/userguide/language_basics/struct_union_enum.pyx

See also :ref:`struct-union-enum-styles`

.. note::

    Structs can be declared as ``cdef packed struct``, which has
    the same effect as the C directive ``#pragma pack(1)``.

Declaring an enum as ``cpdef`` will create a :pep:`435`-style Python wrapper::

    cpdef enum CheeseState:
        hard = 1
        soft = 2
        runny = 3



There is currently no special syntax for defining a constant, but you can use
an anonymous :keyword:`enum` declaration for this purpose, for example,::

    cdef enum:
        tons_of_spam = 3

.. note::
    the words ``struct``, ``union`` and ``enum`` are used only when
    defining a type, not when referring to it. For example, to declare a variable
    pointing to a ``Grail`` you would write::

        cdef Grail *gp

    and not::

        cdef struct Grail *gp # WRONG

    There is also a ``ctypedef`` statement for giving names to types, e.g.::

        ctypedef unsigned long ULong

        ctypedef int* IntPtr


It is also possible to declare functions with :keyword:`cdef`, making them c functions.

::

    cdef int eggs(unsigned long l, float f):
        ...

You can read more about them in :ref:`python_functions_vs_c_functions`.

You can declare classes with :keyword:`cdef`, making them :ref:`extension-types`. Those will
have a behavior very close to python classes, but are faster because they use a ``struct``
internally to store attributes.

Here is a simple example:

.. literalinclude:: ../../examples/userguide/extension_types/shrubbery.pyx

You can read more about them in :ref:`extension-types`.

.. _typing_types:
.. _types:

Types
-----

Cython uses the normal C syntax for C types, including pointers.  It provides
all the standard C types, namely ``char``, ``short``, ``int``, ``long``,
``long long`` as well as their ``unsigned`` versions, e.g. ``unsigned int``.
The special ``bint`` type is used for C boolean values (``int`` with 0/non-0
values for False/True) and ``Py_ssize_t`` for (signed) sizes of Python
containers.

Pointer types are constructed as in C, by appending a ``*`` to the base type
they point to, e.g. ``int**`` for a pointer to a pointer to a C int.
Arrays use the normal C array syntax, e.g. ``int[10]``, and the size must be known
at compile time for stack allocated arrays. Cython doesn't support variable length arrays from C99.
Note that Cython uses array access for pointer dereferencing, as ``*x`` is not valid Python syntax,
whereas ``x[0]`` is.

Also, the Python types ``list``, ``dict``, ``tuple``, etc. may be used for
static typing, as well as any user defined :ref:`extension-types`.
For example::

    cdef list foo = []

This requires an *exact* match of the class, it does not allow
subclasses. This allows Cython to optimize code by accessing
internals of the builtin class.
For this kind of typing, Cython uses internally a C variable of type ``PyObject*``.
The Python types int, long, and float are not available for static
typing and instead interpreted as C ``int``, ``long``, and ``float``
respectively, as statically typing variables with these Python
types has zero advantages.

Cython provides an accelerated and typed equivalent of a Python tuple, the ``ctuple``.
A ``ctuple`` is assembled from any valid C types. For example::

    cdef (double, int) bar

They compile down to C-structures and can be used as efficient alternatives to
Python tuples.

While these C types can be vastly faster, they have C semantics.
Specifically, the integer types overflow
and the C ``float`` type only has 32 bits of precision
(as opposed to the 64-bit C ``double`` which Python floats wrap
and is typically what one wants).
If you want to use these numeric Python types simply omit the
type declaration and let them be objects.

It is also possible to declare :ref:`extension-types` (declared with ``cdef class``).
This does allow subclasses. This typing is mostly used to access
``cdef`` methods and attributes of the extension type.
The C code uses a variable which is a pointer to a structure of the
specific type, something like ``struct MyExtensionTypeObject*``.


Grouping multiple C declarations
--------------------------------

If you have a series of declarations that all begin with :keyword:`cdef`, you
can group them into a :keyword:`cdef` block like this:

.. literalinclude:: ../../examples/userguide/language_basics/cdef_block.pyx

.. _cpdef:
.. _cdef:
.. _python_functions_vs_c_functions:

Python functions vs. C functions
==================================

There are two kinds of function definition in Cython:

Python functions are defined using the def statement, as in Python. They take
Python objects as parameters and return Python objects.

C functions are defined using the new :keyword:`cdef` statement. They take
either Python objects or C values as parameters, and can return either Python
objects or C values.

Within a Cython module, Python functions and C functions can call each other
freely, but only Python functions can be called from outside the module by
interpreted Python code. So, any functions that you want to "export" from your
Cython module must be declared as Python functions using def.
There is also a hybrid function, called :keyword:`cpdef`. A :keyword:`cpdef`
can be called from anywhere, but uses the faster C calling conventions
when being called from other Cython code. A :keyword:`cpdef` can also be overridden
by a Python method on a subclass or an instance attribute, even when called from Cython.
If this happens, most performance gains are of course lost and even if it does not,
there is a tiny overhead in calling a :keyword:`cpdef` method from Cython compared to
calling a :keyword:`cdef` method.

Parameters of either type of function can be declared to have C data types,
using normal C declaration syntax. For example,::

    def spam(int i, char *s):
        ...

    cdef int eggs(unsigned long l, float f):
        ...

``ctuples`` may also be used::

    cdef (int, float) chips((long, long, double) t):
        ...

When a parameter of a Python function is declared to have a C data type, it is
passed in as a Python object and automatically converted to a C value, if
possible. In other words, the definition of ``spam`` above is equivalent to
writing::

    def spam(python_i, python_s):
        cdef int i = python_i
        cdef char* s = python_s
        ...

Automatic conversion is currently only possible for numeric types,
string types and structs (composed recursively of any of these types);
attempting to use any other type for the parameter of a
Python function will result in a compile-time error.
Care must be taken with strings to ensure a reference if the pointer is to be used
after the call. Structs can be obtained from Python mappings, and again care must be taken
with string attributes if they are to be used after the function returns.

C functions, on the other hand, can have parameters of any type, since they're
passed in directly using a normal C function call.

Functions declared using :keyword:`cdef` with Python object return type, like Python functions, will return a :keyword:`None`
value when execution leaves the function body without an explicit return value. This is in
contrast to C/C++, which leaves the return value undefined. 
In the case of non-Python object return types, the equivalent of zero is returned, for example, 0 for ``int``, :keyword:`False` for ``bint`` and :keyword:`NULL` for pointer types.

A more complete comparison of the pros and cons of these different method
types can be found at :ref:`early-binding-for-speed`.

Python objects as parameters and return values
----------------------------------------------

If no type is specified for a parameter or return value, it is assumed to be a
Python object. (Note that this is different from the C convention, where it
would default to int.) For example, the following defines a C function that
takes two Python objects as parameters and returns a Python object::

    cdef spamobjs(x, y):
        ...

Reference counting for these objects is performed automatically according to
the standard Python/C API rules (i.e. borrowed references are taken as
parameters and a new reference is returned).

 .. warning::

    This only applies to Cython code.  Other Python packages which
    are implemented in C like NumPy may not follow these conventions.


The name object can also be used to explicitly declare something as a Python
object. This can be useful if the name being declared would otherwise be taken
as the name of a type, for example,::

    cdef ftang(object int):
        ...

declares a parameter called int which is a Python object. You can also use
object as the explicit return type of a function, e.g.::

    cdef object ftang(object int):
        ...

In the interests of clarity, it is probably a good idea to always be explicit
about object parameters in C functions.


.. _optional_arguments:

Optional Arguments
------------------

Unlike C, it is possible to use optional arguments in ``cdef`` and ``cpdef`` functions.
There are differences though whether you declare them in a ``.pyx``
file or the corresponding ``.pxd`` file.

To avoid repetition (and potential future inconsistencies), default argument values are
not visible in the declaration (in ``.pxd`` files) but only in
the implementation (in ``.pyx`` files).

When in a ``.pyx`` file, the signature is the same as it is in Python itself:

.. literalinclude:: ../../examples/userguide/language_basics/optional_subclassing.pyx

When in a ``.pxd`` file, the signature is different like this example: ``cdef foo(x=*)``.
This is because the program calling the function just needs to know what signatures are
possible in C, but doesn't need to know the value of the default arguments.:

.. literalinclude:: ../../examples/userguide/language_basics/optional_subclassing.pxd

.. note::
    The number of arguments may increase when subclassing,
    but the arg types and order must be the same, as shown in the example above.

There may be a slight performance penalty when the optional arg is overridden
with one that does not have default values.


.. _keyword_only_argument:

Keyword-only Arguments
----------------------

As in Python 3, ``def`` functions can have keyword-only arguments
listed after a ``"*"`` parameter and before a ``"**"`` parameter if any:

.. literalinclude:: ../../examples/userguide/language_basics/kwargs_1.pyx

As shown above, the ``c``, ``d`` and ``e`` arguments can not be
passed as positional arguments and must be passed as keyword arguments.
Furthermore, ``c`` and ``e`` are **required** keyword arguments
since they do not have a default value.

A single ``"*"`` without argument name can be used to
terminate the list of positional arguments:

.. literalinclude:: ../../examples/userguide/language_basics/kwargs_2.pyx

Shown above, the signature takes exactly two positional
parameters and has two required keyword parameters.

Function Pointers
-----------------

Functions declared in a ``struct`` are automatically converted to function pointers.

For using error return values with function pointers, see the note at the bottom
of :ref:`error_return_values`.

.. _error_return_values:

Error return values
-------------------

If you don't do anything special, a function declared with :keyword:`cdef` that
does not return a Python object has no way of reporting Python exceptions to
its caller. If an exception is detected in such a function, a warning message
is printed and the exception is ignored.

If you want a C function that does not return a Python object to be able to
propagate exceptions to its caller, you need to declare an exception value for
it. Here is an example::

    cdef int spam() except -1:
        ...

With this declaration, whenever an exception occurs inside spam, it will
immediately return with the value ``-1``. Furthermore, whenever a call to spam
returns ``-1``, an exception will be assumed to have occurred and will be
propagated.

When you declare an exception value for a function, you should never
explicitly or implicitly return that value. In particular, if the exceptional return value
is a ``False`` value, then you should ensure the function will never terminate via an implicit
or empty return.

If all possible return values are legal and you
can't reserve one entirely for signalling errors, you can use an alternative
form of exception value declaration::

    cdef int spam() except? -1:
        ...

The "?" indicates that the value ``-1`` only indicates a possible error. In this
case, Cython generates a call to :c:func:`PyErr_Occurred` if the exception value is
returned, to make sure it really is an error.

There is also a third form of exception value declaration::

    cdef int spam() except *:
        ...

This form causes Cython to generate a call to :c:func:`PyErr_Occurred` after
every call to spam, regardless of what value it returns. If you have a
function returning void that needs to propagate errors, you will have to use
this form, since there isn't any return value to test.
Otherwise there is little use for this form.

An external C++ function that may raise an exception can be declared with::

    cdef int spam() except +

See :ref:`wrapping-cplusplus` for more details.

Some things to note:

* Exception values can only declared for functions returning an integer, enum,
  float or pointer type, and the value must be a constant expression.
  Void functions can only use the ``except *`` form.
* The exception value specification is part of the signature of the function.
  If you're passing a pointer to a function as a parameter or assigning it
  to a variable, the declared type of the parameter or variable must have
  the same exception value specification (or lack thereof). Here is an
  example of a pointer-to-function declaration with an exception
  value::

      int (*grail)(int, char*) except -1

* You don't need to (and shouldn't) declare exception values for functions
  which return Python objects. Remember that a function with no declared
  return type implicitly returns a Python object. (Exceptions on such functions
  are implicitly propagated by returning NULL.)


.. _checking_return_values_of_non_cython_functions:

Checking return values of non-Cython functions
----------------------------------------------

It's important to understand that the except clause does not cause an error to
be raised when the specified value is returned. For example, you can't write
something like::

    cdef extern FILE *fopen(char *filename, char *mode) except NULL # WRONG!

and expect an exception to be automatically raised if a call to :func:`fopen`
returns ``NULL``. The except clause doesn't work that way; its only purpose is
for propagating Python exceptions that have already been raised, either by a Cython
function or a C function that calls Python/C API routines. To get an exception
from a non-Python-aware function such as :func:`fopen`, you will have to check the
return value and raise it yourself, for example:

.. literalinclude:: ../../examples/userguide/language_basics/open_file.pyx

.. _overriding_in_extension_types:

Overriding in extension types
-----------------------------


``cpdef`` methods can override ``cdef`` methods:

.. literalinclude:: ../../examples/userguide/language_basics/optional_subclassing.pyx

When subclassing an extension type with a Python class,
``def`` methods can override ``cpdef`` methods but not ``cdef``
methods:

.. literalinclude:: ../../examples/userguide/language_basics/override.pyx

If ``C`` above would be an extension type (``cdef class``),
this would not work correctly.
The Cython compiler will give a warning in that case.


.. _type-conversion:

Automatic type conversions
==========================

In most situations, automatic conversions will be performed for the basic
numeric and string types when a Python object is used in a context requiring a
C value, or vice versa. The following table summarises the conversion
possibilities.

+----------------------------+--------------------+------------------+
| C types                    | From Python types  | To Python types  |
+============================+====================+==================+
| [unsigned] char,           | int, long          | int              |
| [unsigned] short,          |                    |                  |
| int, long                  |                    |                  |
+----------------------------+--------------------+------------------+
| unsigned int,              | int, long          | long             |
| unsigned long,             |                    |                  |
| [unsigned] long long       |                    |                  |
+----------------------------+--------------------+------------------+
| float, double, long double | int, long, float   | float            |
+----------------------------+--------------------+------------------+
| char*                      | str/bytes          | str/bytes [#]_   |
+----------------------------+--------------------+------------------+
| C array                    | iterable           | list [#2]_       |
+----------------------------+--------------------+------------------+
| struct,                    |                    | dict [#1]_       |
| union                      |                    |                  |
+----------------------------+--------------------+------------------+

.. [#] The conversion is to/from str for Python 2.x, and bytes for Python 3.x.

.. [#1] The conversion from a C union type to a Python dict will add
   a value for each of the union fields.  Cython 0.23 and later, however,
   will refuse to automatically convert a union with unsafe type
   combinations.  An example is a union of an ``int`` and a ``char*``,
   in which case the pointer value may or may not be a valid pointer.

.. [#2] Other than signed/unsigned char[].
   The conversion will fail if the length of C array is not known at compile time,
   and when using a slice of a C array.


Caveats when using a Python string in a C context
-------------------------------------------------

You need to be careful when using a Python string in a context expecting a
``char*``. In this situation, a pointer to the contents of the Python string is
used, which is only valid as long as the Python string exists. So you need to
make sure that a reference to the original Python string is held for as long
as the C string is needed. If you can't guarantee that the Python string will
live long enough, you will need to copy the C string.

Cython detects and prevents some mistakes of this kind. For instance, if you
attempt something like::

    cdef char *s
    s = pystring1 + pystring2

then Cython will produce the error message ``Obtaining char* from temporary
Python value``. The reason is that concatenating the two Python strings
produces a new Python string object that is referenced only by a temporary
internal variable that Cython generates. As soon as the statement has finished,
the temporary variable will be decrefed and the Python string deallocated,
leaving ``s`` dangling. Since this code could not possibly work, Cython refuses to
compile it.

The solution is to assign the result of the concatenation to a Python
variable, and then obtain the ``char*`` from that, i.e.::

    cdef char *s
    p = pystring1 + pystring2
    s = p

It is then your responsibility to hold the reference p for as long as
necessary.

Keep in mind that the rules used to detect such errors are only heuristics.
Sometimes Cython will complain unnecessarily, and sometimes it will fail to
detect a problem that exists. Ultimately, you need to understand the issue and
be careful what you do.

.. _type_casting:

Type Casting
------------

Where C uses ``"("`` and ``")"``, Cython uses ``"<"`` and ``">"``. For example::

    cdef char *p
    cdef float *q
    p = <char*>q

When casting a C value to a Python object type or vice versa,
Cython will attempt a coercion. Simple examples are casts like ``<int>pyobj``,
which converts a Python number to a plain C ``int`` value, or ``<bytes>charptr``,
which copies a C ``char*`` string into a new Python bytes object.

 .. note:: Cython will not prevent a redundant cast, but emits a warning for it.

To get the address of some Python object, use a cast to a pointer type
like ``<void*>`` or ``<PyObject*>``.
You can also cast a C pointer back to a Python object reference
with ``<object>``, or a more specific builtin or extension type
(e.g. ``<MyExtType>ptr``). This will increase the reference count of
the object by one, i.e. the cast returns an owned reference.
Here is an example:

.. literalinclude:: ../../examples/userguide/language_basics/casting_python.pyx

The precedence of ``<...>`` is such that ``<type>a.b.c`` is interpreted as ``<type>(a.b.c)``.

.. _checked_type_casts:

Checked Type Casts
------------------

A cast like ``<MyExtensionType>x`` will cast x to the class
``MyExtensionType`` without any checking at all.

To have a cast checked, use the syntax like: ``<MyExtensionType?>x``.
In this case, Cython will apply a runtime check that raises a ``TypeError``
if ``x`` is not an instance of ``MyExtensionType``.
This tests for the exact class for builtin types,
but allows subclasses for :ref:`extension-types`.

.. _statements_and_expressions:

Statements and expressions
==========================

Control structures and expressions follow Python syntax for the most part.
When applied to Python objects, they have the same semantics as in Python
(unless otherwise noted). Most of the Python operators can also be applied to
C values, with the obvious semantics.

If Python objects and C values are mixed in an expression, conversions are
performed automatically between Python objects and C numeric or string types.

Reference counts are maintained automatically for all Python objects, and all
Python operations are automatically checked for errors, with appropriate
action taken.

Differences between C and Cython expressions
--------------------------------------------

There are some differences in syntax and semantics between C expressions and
Cython expressions, particularly in the area of C constructs which have no
direct equivalent in Python.

* An integer literal is treated as a C constant, and will
  be truncated to whatever size your C compiler thinks appropriate.
  To get a Python integer (of arbitrary precision) cast immediately to
  an object (e.g. ``<object>100000000000000000000``). The ``L``, ``LL``,
  and ``U`` suffixes have the same meaning as in C.
* There is no ``->`` operator in Cython. Instead of ``p->x``, use ``p.x``
* There is no unary ``*`` operator in Cython. Instead of ``*p``, use ``p[0]``
* There is an ``&`` operator, with the same semantics as in C.
* The null C pointer is called ``NULL``, not ``0`` (and ``NULL`` is a reserved word).
* Type casts are written ``<type>value`` , for example,::

        cdef char* p, float* q
        p = <char*>q

Scope rules
-----------

Cython determines whether a variable belongs to a local scope, the module
scope, or the built-in scope completely statically. As with Python, assigning
to a variable which is not otherwise declared implicitly declares it to be a
variable residing in the scope where it is assigned.  The type of the variable
depends on type inference, except for the global module scope, where it is
always a Python object.

.. _built_in_functions:

Built-in Functions
------------------

Cython compiles calls to most built-in functions into direct calls to
the corresponding Python/C API routines, making them particularly fast.

Only direct function calls using these names are optimised. If you do
something else with one of these names that assumes it's a Python object,
such as assign it to a Python variable, and later call it, the call will
be made as a Python function call.

+------------------------------+-------------+----------------------------+
| Function and arguments       | Return type | Python/C API Equivalent    |
+==============================+=============+============================+
| abs(obj)                     | object,     | PyNumber_Absolute, fabs,   |
|                              | double, ... | fabsf, ...                 |
+------------------------------+-------------+----------------------------+
| callable(obj)                | bint        | PyObject_Callable          |
+------------------------------+-------------+----------------------------+
| delattr(obj, name)           | None        | PyObject_DelAttr           |
+------------------------------+-------------+----------------------------+
| exec(code, [glob, [loc]])    | object      | -                          |
+------------------------------+-------------+----------------------------+
| dir(obj)                     | list        | PyObject_Dir               |
+------------------------------+-------------+----------------------------+
| divmod(a, b)                 | tuple       | PyNumber_Divmod            |
+------------------------------+-------------+----------------------------+
| getattr(obj, name, [default])| object      | PyObject_GetAttr           |
| (Note 1)                     |             |                            |
+------------------------------+-------------+----------------------------+
| hasattr(obj, name)           | bint        | PyObject_HasAttr           |
+------------------------------+-------------+----------------------------+
| hash(obj)                    | int / long  | PyObject_Hash              |
+------------------------------+-------------+----------------------------+
| intern(obj)                  | object      | Py*_InternFromString       |
+------------------------------+-------------+----------------------------+
| isinstance(obj, type)        | bint        | PyObject_IsInstance        |
+------------------------------+-------------+----------------------------+
| issubclass(obj, type)        | bint        | PyObject_IsSubclass        |
+------------------------------+-------------+----------------------------+
| iter(obj, [sentinel])        | object      | PyObject_GetIter           |
+------------------------------+-------------+----------------------------+
| len(obj)                     | Py_ssize_t  | PyObject_Length            |
+------------------------------+-------------+----------------------------+
| pow(x, y, [z])               | object      | PyNumber_Power             |
+------------------------------+-------------+----------------------------+
| reload(obj)                  | object      | PyImport_ReloadModule      |
+------------------------------+-------------+----------------------------+
| repr(obj)                    | object      | PyObject_Repr              |
+------------------------------+-------------+----------------------------+
| setattr(obj, name)           | void        | PyObject_SetAttr           |
+------------------------------+-------------+----------------------------+

Note 1: Pyrex originally provided a function :func:`getattr3(obj, name, default)`
corresponding to the three-argument form of the Python builtin :func:`getattr()`.
Cython still supports this function, but the usage is deprecated in favour of
the normal builtin, which Cython can optimise in both forms.


Operator Precedence
-------------------

Keep in mind that there are some differences in operator precedence between
Python and C, and that Cython uses the Python precedences, not the C ones.

Integer for-loops
------------------

Cython recognises the usual Python for-in-range integer loop pattern::

    for i in range(n):
        ...

If ``i`` is declared as a :keyword:`cdef` integer type, it will
optimise this into a pure C loop.  This restriction is required as
otherwise the generated code wouldn't be correct due to potential
integer overflows on the target architecture.  If you are worried that
the loop is not being converted correctly, use the annotate feature of
the cython commandline (``-a``) to easily see the generated C code.
See :ref:`automatic-range-conversion`

For backwards compatibility to Pyrex, Cython also supports a more verbose
form of for-loop which you might find in legacy code::

    for i from 0 <= i < n:
        ...

or::

    for i from 0 <= i < n by s:
        ...

where ``s`` is some integer step size.

.. note:: This syntax is deprecated and should not be used in new code.
          Use the normal Python for-loop instead.

Some things to note about the for-from loop:

* The target expression must be a plain variable name.
* The name between the lower and upper bounds must be the same as the target
  name.
* The direction of iteration is determined by the relations. If they are both
  from the set {``<``, ``<=``} then it is upwards; if they are both from the set
  {``>``, ``>=``} then it is downwards. (Any other combination is disallowed.)

Like other Python looping statements, break and continue may be used in the
body, and the loop may have an else clause.

.. _cython_file_types:

Cython file types
=================

There are three file types in Cython:

* The implementation files, carrying a ``.py`` or ``.pyx`` suffix.
* The definition files, carrying a ``.pxd`` suffix.
* The include files, carrying a ``.pxi`` suffix.

The implementation file
-----------------------

The implementation file, as the name suggest, contains the implementation
of your functions, classes, extension types, etc. Nearly all the
python syntax is supported in this file. Most of the time, a ``.py``
file can be renamed into a ``.pyx`` file without changing
any code, and Cython will retain the python behavior.

It is possible for Cython to compile both ``.py`` and ``.pyx`` files.
The name of the file isn't important if one wants to use only the Python syntax,
and Cython won't change the generated code depending on the suffix used.
Though, if one want to use the Cython syntax, using a ``.pyx`` file is necessary.

In addition to the Python syntax, the user can also
leverage Cython syntax (such as ``cdef``) to use C variables, can
declare functions as ``cdef`` or ``cpdef`` and can import C definitions
with :keyword:`cimport`. Many other Cython features usable in implementation files
can be found throughout this page and the rest of the Cython documentation.

There are some restrictions on the implementation part of some :ref:`extension-types`
if the corresponding definition file also defines that type.

.. note::

    When a ``.pyx`` file is compiled, Cython first checks to see if a corresponding
    ``.pxd`` file exists and processes it first. It acts like a header file for
    a Cython ``.pyx`` file. You can put inside functions that will be used by
    other Cython modules. This allows different Cython modules to use functions
    and classes from each other without the Python overhead. To read more about
    what how to do that, you can see :ref:`pxd_files`.


The definition file
-------------------

A definition file is used to declare various things.

Any C declaration can be made, and it can be also a declaration of a C variable or
function implemented in a C/C++ file. This can be done with ``cdef extern from``.
Sometimes, ``.pxd`` files are used as a translation of C/C++ header files
into a syntax that Cython can understand. This allows then the C/C++ variable and
functions to be used directly in implementation files with :keyword:`cimport`.
You can read more about it in :ref:`external-C-code` and :ref:`wrapping-cplusplus`.

It can also contain the definition part of an extension type and the declarations
of functions for an external library.

It cannot contain the implementations of any C or Python functions, or any
Python class definitions, or any executable statements. It is needed when one
wants to  access :keyword:`cdef` attributes and methods, or to inherit from
:keyword:`cdef` classes defined in this module.

.. note::

    You don't need to (and shouldn't) declare anything in a declaration file
    :keyword:`public` in order to make it available to other Cython modules; its mere
    presence in a definition file does that. You only need a public
    declaration if you want to make something available to external C code.


The include statement and include files
---------------------------------------

.. warning::
    Historically the ``include`` statement was used for sharing declarations.
    Use :ref:`sharing-declarations` instead.

A Cython source file can include material from other files using the include
statement, for example,::

    include "spamstuff.pxi"

The contents of the named file are textually included at that point.  The
included file can contain any complete statements or declarations that are
valid in the context where the include statement appears, including other
include statements.  The contents of the included file should begin at an
indentation level of zero, and will be treated as though they were indented to
the level of the include statement that is including the file.  The include
statement cannot, however, be used outside of the module scope, such as inside
of functions or class bodies.

.. note::

    There are other mechanisms available for splitting Cython code into
    separate parts that may be more appropriate in many cases. See
    :ref:`sharing-declarations`.

.. _conditional_compilation:

Conditional Compilation
=======================

Some features are available for conditional compilation and compile-time
constants within a Cython source file.

Compile-Time Definitions
------------------------

A compile-time constant can be defined using the DEF statement::

    DEF FavouriteFood = u"spam"
    DEF ArraySize = 42
    DEF OtherArraySize = 2 * ArraySize + 17

The right-hand side of the ``DEF`` must be a valid compile-time expression.
Such expressions are made up of literal values and names defined using ``DEF``
statements, combined using any of the Python expression syntax.

The following compile-time names are predefined, corresponding to the values
returned by :func:`os.uname`.

    UNAME_SYSNAME, UNAME_NODENAME, UNAME_RELEASE,
    UNAME_VERSION, UNAME_MACHINE

The following selection of builtin constants and functions are also available:

    None, True, False,
    abs, all, any, ascii, bin, bool, bytearray, bytes, chr, cmp, complex, dict,
    divmod, enumerate, filter, float, format, frozenset, hash, hex, int, len,
    list, long, map, max, min, oct, ord, pow, range, reduce, repr, reversed,
    round, set, slice, sorted, str, sum, tuple, xrange, zip

Note that some of these builtins may not be available when compiling under
Python 2.x or 3.x, or may behave differently in both.

A name defined using ``DEF`` can be used anywhere an identifier can appear,
and it is replaced with its compile-time value as though it were written into
the source at that point as a literal. For this to work, the compile-time
expression must evaluate to a Python value of type ``int``, ``long``,
``float``, ``bytes`` or ``unicode`` (``str`` in Py3).

.. literalinclude:: ../../examples/userguide/language_basics/compile_time.pyx

Conditional Statements
----------------------

The ``IF`` statement can be used to conditionally include or exclude sections
of code at compile time. It works in a similar way to the ``#if`` preprocessor
directive in C.::

    IF UNAME_SYSNAME == "Windows":
        include "icky_definitions.pxi"
    ELIF UNAME_SYSNAME == "Darwin":
        include "nice_definitions.pxi"
    ELIF UNAME_SYSNAME == "Linux":
        include "penguin_definitions.pxi"
    ELSE:
        include "other_definitions.pxi"

The ``ELIF`` and ``ELSE`` clauses are optional. An ``IF`` statement can appear
anywhere that a normal statement or declaration can appear, and it can contain
any statements or declarations that would be valid in that context, including
``DEF`` statements and other ``IF`` statements.

The expressions in the ``IF`` and ``ELIF`` clauses must be valid compile-time
expressions as for the ``DEF`` statement, although they can evaluate to any
Python value, and the truth of the result is determined in the usual Python
way.

