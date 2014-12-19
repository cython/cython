.. highlight:: cython

.. _language-basics:
.. _struct:
.. _union:
.. _enum:
.. _ctypedef:


*****************
Language Basics
*****************

C variable and type definitions
===============================

The :keyword:`cdef` statement is used to declare C variables, either local or
module-level::

    cdef int i, j, k
    cdef float f, g[42], *h

and C :keyword:`struct`, :keyword:`union` or :keyword:`enum` types::

    cdef struct Grail:
        int age
        float volume

    cdef union Food:
        char *spam
        float *eggs

    cdef enum CheeseType:
        cheddar, edam, 
        camembert

    cdef enum CheeseState:
        hard = 1
        soft = 2
        runny = 3

See also :ref:`struct-union-enum-styles`

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

Grouping multiple C declarations
--------------------------------

If you have a series of declarations that all begin with :keyword:`cdef`, you
can group them into a :keyword:`cdef` block like this::

    cdef:
        struct Spam:
            int tons

        int i
        float f
        Spam *p

        void f(Spam *s):
            print s.tons, "Tons of spam"


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
explicitly return that value. If all possible return values are legal and you
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
return value and raise it yourself, for example,::

    cdef FILE* p
    p = fopen("spam.txt", "r")
    if p == NULL:
        raise SpamError("Couldn't open the spam file")

    
Automatic type conversions
==========================

In most situations, automatic conversions will be performed for the basic
numeric and string types when a Python object is used in a context requiring a
C value, or vice versa. The following table summarises the conversion
possibilities.

+----------------------------+--------------------+------------------+
| C types                    | From Python types  | To Python types  |
+============================+====================+==================+
| [unsigned] char            | int, long          | int              |
| [unsigned] short           |                    |                  |
| int, long                  |                    |                  |
+----------------------------+--------------------+------------------+
| unsigned int               | int, long          | long             |
| unsigned long              |                    |                  |
| [unsigned] long long       |                    |                  |
+----------------------------+--------------------+------------------+
| float, double, long double | int, long, float   | float            |
+----------------------------+--------------------+------------------+
| char*                      | str/bytes          | str/bytes [#]_   |
+----------------------------+--------------------+------------------+
| struct                     |                    | dict             |
+----------------------------+--------------------+------------------+

.. [#] The conversion is to/from str for Python 2.x, and bytes for Python 3.x. 

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
Python variable residing in the scope where it is assigned.

.. note::
    A consequence of these rules is that the module-level scope behaves the
    same way as a Python local scope if you refer to a variable before assigning
    to it. In particular, tricks such as the following will not work in Cython::

        try:
            x = True
        except NameError:
            True = 1

    because, due to the assignment, the True will always be looked up in the
    module-level scope. You would have to do something like this instead::

        import __builtin__
        try:
            True = __builtin__.True
        except AttributeError:
            True = 1


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


The include statement
=====================

.. warning:: 
    Historically the ``include`` statement was used for sharing declarations. 
    Use :ref:`sharing-declarations` instead.

A Cython source file can include material from other files using the include
statement, for example,::

    include "spamstuff.pxi"

The contents of the named file are textually included at that point. The
included file can contain any complete statements or declarations that are
valid in the context where the include statement appears, including other
include statements. The contents of the included file should begin at an
indentation level of zero, and will be treated as though they were indented to
the level of the include statement that is including the file.

.. note::

    There are other mechanisms available for splitting Cython code into
    separate parts that may be more appropriate in many cases. See
    :ref:`sharing-declarations`.


Conditional Compilation
=======================

Some features are available for conditional compilation and compile-time
constants within a Cython source file.

Compile-Time Definitions
------------------------

A compile-time constant can be defined using the DEF statement::

    DEF FavouriteFood = "spam"
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
    abs, bool, chr, cmp, complex, dict, divmod, enumerate,
    float, hash, hex, int, len, list, long, map, max, min,
    oct, ord, pow, range, reduce, repr, round, slice, str,
    sum, tuple, xrange, zip

A name defined using ``DEF`` can be used anywhere an identifier can appear,
and it is replaced with its compile-time value as though it were written into
the source at that point as a literal. For this to work, the compile-time
expression must evaluate to a Python value of type ``int``, ``long``,
``float`` or ``str``.::

    cdef int a1[ArraySize]
    cdef int a2[OtherArraySize]
    print "I like", FavouriteFood

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

