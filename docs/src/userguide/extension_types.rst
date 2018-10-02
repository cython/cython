.. highlight:: cython

.. _extension-types:

******************
Extension Types
******************

Introduction
==============

As well as creating normal user-defined classes with the Python class
statement, Cython also lets you create new built-in Python types, known as
extension types. You define an extension type using the :keyword:`cdef` class
statement.  Here's an example:

.. literalinclude:: ../../examples/userguide/extension_types/shrubbery.pyx

As you can see, a Cython extension type definition looks a lot like a Python
class definition. Within it, you use the def statement to define methods that
can be called from Python code. You can even define many of the special
methods such as :meth:`__init__` as you would in Python.

The main difference is that you can use the :keyword:`cdef` statement to define
attributes. The attributes may be Python objects (either generic or of a
particular extension type), or they may be of any C data type. So you can use
extension types to wrap arbitrary C data structures and provide a Python-like
interface to them.

.. _readonly:

Static Attributes
=================

Attributes of an extension type are stored directly in the object's C struct.
The set of attributes is fixed at compile time; you can't add attributes to an
extension type instance at run time simply by assigning to them, as you could
with a Python class instance. However, you can explicitly enable support
for dynamically assigned attributes, or subclass the extension type with a normal
Python class, which then supports arbitrary attribute assignments.
See :ref:`dynamic_attributes`.

There are two ways that attributes of an extension type can be accessed: by
Python attribute lookup, or by direct access to the C struct from Cython code.
Python code is only able to access attributes of an extension type by the
first method, but Cython code can use either method.

By default, extension type attributes are only accessible by direct access,
not Python access, which means that they are not accessible from Python code.
To make them accessible from Python code, you need to declare them as
:keyword:`public` or :keyword:`readonly`. For example:

.. literalinclude:: ../../examples/userguide/extension_types/python_access.pyx

makes the width and height attributes readable and writable from Python code,
and the depth attribute readable but not writable.

.. note::

    You can only expose simple C types, such as ints, floats, and
    strings, for Python access. You can also expose Python-valued attributes.

.. note::

    Also the :keyword:`public` and :keyword:`readonly` options apply only to
    Python access, not direct access. All the attributes of an extension type
    are always readable and writable by C-level access.


.. _dynamic_attributes:

Dynamic Attributes
==================

It is not possible to add attributes to an extension type at runtime by default.
You have two ways of avoiding this limitation, both add an overhead when
a method is called from Python code. Especially when calling ``cpdef`` methods.

The first approach is to create a Python subclass.:

.. literalinclude:: ../../examples/userguide/extension_types/extendable_animal.pyx

Declaring a ``__dict__`` attribute is the second way of enabling dynamic attributes.:

.. literalinclude:: ../../examples/userguide/extension_types/dict_animal.pyx

Type declarations
===================

Before you can directly access the attributes of an extension type, the Cython
compiler must know that you have an instance of that type, and not just a
generic Python object. It knows this already in the case of the ``self``
parameter of the methods of that type, but in other cases you will have to use
a type declaration.

For example, in the following function::

    cdef widen_shrubbery(sh, extra_width): # BAD
        sh.width = sh.width + extra_width

because the ``sh`` parameter hasn't been given a type, the width attribute
will be accessed by a Python attribute lookup. If the attribute has been
declared :keyword:`public` or :keyword:`readonly` then this will work, but it
will be very inefficient. If the attribute is private, it will not work at all
-- the code will compile, but an attribute error will be raised at run time.

The solution is to declare ``sh`` as being of type :class:`Shrubbery`, as
follows:

.. literalinclude:: ../../examples/userguide/extension_types/widen_shrubbery.pyx

Now the Cython compiler knows that ``sh`` has a C attribute called
:attr:`width` and will generate code to access it directly and efficiently.
The same consideration applies to local variables, for example:

.. literalinclude:: ../../examples/userguide/extension_types/shrubbery_2.pyx

.. note::

    We here ``cimport`` the class :class:`Shrubbery`, and this is necessary
    to declare the type at compile time. To be able to ``cimport`` an extension type,
    we split the class definition into two parts, one in a definition file and
    the other in the corresponding implementation file. You should read
    :ref:`sharing_extension_types` to learn to do that.


Type Testing and Casting
------------------------

Suppose I have a method :meth:`quest` which returns an object of type :class:`Shrubbery`.
To access it's width I could write::

    cdef Shrubbery sh = quest()
    print(sh.width)

which requires the use of a local variable and performs a type test on assignment.
If you *know* the return value of :meth:`quest` will be of type :class:`Shrubbery`
you can use a cast to write::

    print( (<Shrubbery>quest()).width )

This may be dangerous if :meth:`quest()` is not actually a :class:`Shrubbery`, as it
will try to access width as a C struct member which may not exist. At the C level,
rather than raising an :class:`AttributeError`, either an nonsensical result will be
returned (interpreting whatever data is at that address as an int) or a segfault
may result from trying to access invalid memory. Instead, one can write::

    print( (<Shrubbery?>quest()).width )

which performs a type check (possibly raising a :class:`TypeError`) before making the
cast and allowing the code to proceed.

To explicitly test the type of an object, use the :meth:`isinstance` builtin function.
For known builtin or extension types, Cython translates these into a
fast and safe type check that ignores changes to
the object's ``__class__`` attribute etc., so that after a successful
:meth:`isinstance` test, code can rely on the expected C structure of the
extension type and its :keyword:`cdef` attributes and methods.

.. _extension_types_and_none:

Extension types and None
=========================

When you declare a parameter or C variable as being of an extension type,
Cython will allow it to take on the value ``None`` as well as values of its
declared type. This is analogous to the way a C pointer can take on the value
``NULL``, and you need to exercise the same caution because of it. There is no
problem as long as you are performing Python operations on it, because full
dynamic type checking will be applied. However, when you access C attributes
of an extension type (as in the widen_shrubbery function above), it's up to
you to make sure the reference you're using is not ``None`` -- in the
interests of efficiency, Cython does not check this.

You need to be particularly careful when exposing Python functions which take
extension types as arguments. If we wanted to make :func:`widen_shrubbery` a
Python function, for example, if we simply wrote::

    def widen_shrubbery(Shrubbery sh, extra_width): # This is
        sh.width = sh.width + extra_width           # dangerous!

then users of our module could crash it by passing ``None`` for the ``sh``
parameter.

One way to fix this would be::

    def widen_shrubbery(Shrubbery sh, extra_width):
        if sh is None:
            raise TypeError
        sh.width = sh.width + extra_width

but since this is anticipated to be such a frequent requirement, Cython
provides a more convenient way. Parameters of a Python function declared as an
extension type can have a ``not None`` clause::

    def widen_shrubbery(Shrubbery sh not None, extra_width):
        sh.width = sh.width + extra_width

Now the function will automatically check that ``sh`` is ``not None`` along
with checking that it has the right type.

.. note::

    ``not None`` clause can only be used in Python functions (defined with
    :keyword:`def`) and not C functions (defined with :keyword:`cdef`).  If
    you need to check whether a parameter to a C function is None, you will
    need to do it yourself.

.. note::

    Some more things:

    * The self parameter of a method of an extension type is guaranteed never to
      be ``None``.
    * When comparing a value with ``None``, keep in mind that, if ``x`` is a Python
      object, ``x is None`` and ``x is not None`` are very efficient because they
      translate directly to C pointer comparisons, whereas ``x == None`` and
      ``x != None``, or simply using ``x`` as a boolean value (as in ``if x: ...``)
      will invoke Python operations and therefore be much slower.

Special methods
================

Although the principles are similar, there are substantial differences between
many of the :meth:`__xxx__` special methods of extension types and their Python
counterparts. There is a :ref:`separate page <special-methods>` devoted to this subject, and you should
read it carefully before attempting to use any special methods in your
extension types.

.. _properties:

Properties
============

You can declare properties in an extension class using the same syntax as in ordinary Python code::

    cdef class Spam:

        @property
        def cheese(self):
            # This is called when the property is read.
            ...

        @cheese.setter
        def cheese(self, value):
                # This is called when the property is written.
                ...

        @cheese.deleter
        def cheese(self):
            # This is called when the property is deleted.


There is also a special (deprecated) legacy syntax for defining properties in an extension class::

    cdef class Spam:

        property cheese:

            "A doc string can go here."

            def __get__(self):
                # This is called when the property is read.
                ...

            def __set__(self, value):
                # This is called when the property is written.
                ...

            def __del__(self):
                # This is called when the property is deleted.


The :meth:`__get__`, :meth:`__set__` and :meth:`__del__` methods are all
optional; if they are omitted, an exception will be raised when the
corresponding operation is attempted.

Here's a complete example. It defines a property which adds to a list each
time it is written to, returns the list when it is read, and empties the list
when it is deleted.::

    # cheesy.pyx
    cdef class CheeseShop:

        cdef object cheeses

        def __cinit__(self):
            self.cheeses = []

        @property
        def cheese(self):
            return "We don't have: %s" % self.cheeses

        @cheese.setter
        def cheese(self, value):
            self.cheeses.append(value)

        @cheese.deleter
        def cheese(self):
            del self.cheeses[:]

    # Test input
    from cheesy import CheeseShop

    shop = CheeseShop()
    print(shop.cheese)

    shop.cheese = "camembert"
    print(shop.cheese)

    shop.cheese = "cheddar"
    print(shop.cheese)

    del shop.cheese
    print(shop.cheese)

.. sourcecode:: text

    # Test output
    We don't have: []
    We don't have: ['camembert']
    We don't have: ['camembert', 'cheddar']
    We don't have: []

.. _subclassing:

Subclassing
=============

An extension type may inherit from a built-in type or another extension type::

    cdef class Parrot:
        ...

    cdef class Norwegian(Parrot):
        ...


A complete definition of the base type must be available to Cython, so if the
base type is a built-in type, it must have been previously declared as an
extern extension type. If the base type is defined in another Cython module, it
must either be declared as an extern extension type or imported using the
:keyword:`cimport` statement.

An extension type can only have one base class (no multiple inheritance).

Cython extension types can also be subclassed in Python. A Python class can
inherit from multiple extension types provided that the usual Python rules for
multiple inheritance are followed (i.e. the C layouts of all the base classes
must be compatible).

There is a way to prevent extension types from
being subtyped in Python.  This is done via the ``final`` directive,
usually set on an extension type using a decorator::

    cimport cython

    @cython.final
    cdef class Parrot:
       def done(self): pass

Trying to create a Python subclass from this type will raise a
:class:`TypeError` at runtime.  Cython will also prevent subtyping a
final type inside of the same module, i.e. creating an extension type
that uses a final type as its base type will fail at compile time.
Note, however, that this restriction does not currently propagate to
other extension modules, so even final extension types can still be
subtyped at the C level by foreign code.


C methods
=========

Extension types can have C methods as well as Python methods. Like C
functions, C methods are declared using :keyword:`cdef` or :keyword:`cpdef` instead of
:keyword:`def`. C methods are "virtual", and may be overridden in derived
extension types. In addition, :keyword:`cpdef` methods can even be overridden by python
methods when called as C method. This adds a little to their calling overhead
compared to a :keyword:`cdef` method::

    # pets.pyx
    cdef class Parrot:

        cdef void describe(self):
            print("This parrot is resting.")

    cdef class Norwegian(Parrot):

        cdef void describe(self):
            Parrot.describe(self)
            print("Lovely plumage!")


    cdef Parrot p1, p2
    p1 = Parrot()
    p2 = Norwegian()
    print("p1:")
    p1.describe()
    print("p2:")
    p2.describe()

.. sourcecode:: text

    # Output
    p1:
    This parrot is resting.
    p2:
    This parrot is resting.
    Lovely plumage!

The above example also illustrates that a C method can call an inherited C
method using the usual Python technique, i.e.::

    Parrot.describe(self)

`cdef` methods can be declared static by using the @staticmethod decorator.
This can be especially useful for constructing classes that take non-Python
compatible types.::

    cdef class OwnedPointer:
        cdef void* ptr

        def __dealloc__(self):
            if self.ptr is not NULL:
                free(self.ptr)

        @staticmethod
        cdef create(void* ptr):
            p = OwnedPointer()
            p.ptr = ptr
            return p

.. _forward_declaring_extension_types:

Forward-declaring extension types
===================================

Extension types can be forward-declared, like :keyword:`struct` and
:keyword:`union` types.  This is usually not necessary and violates the
DRY principle (Don't Repeat Yourself).

If you are forward-declaring an extension type that has a base class, you must
specify the base class in both the forward declaration and its subsequent
definition, for example,::

    cdef class A(B)

    ...

    cdef class A(B):
        # attributes and methods


Fast instantiation
===================

Cython provides two ways to speed up the instantiation of extension types.
The first one is a direct call to the ``__new__()`` special static method,
as known from Python.  For an extension type ``Penguin``, you could use
the following code::

    cdef class Penguin:
        cdef object food

        def __cinit__(self, food):
            self.food = food

        def __init__(self, food):
            print("eating!")

    normal_penguin = Penguin('fish')
    fast_penguin = Penguin.__new__(Penguin, 'wheat')  # note: not calling __init__() !

Note that the path through ``__new__()`` will *not* call the type's
``__init__()`` method (again, as known from Python).  Thus, in the example
above, the first instantiation will print ``eating!``, but the second will
not.  This is only one of the reasons why the ``__cinit__()`` method is
safer and preferable over the normal ``__init__()`` method for extension
types.

The second performance improvement applies to types that are often created
and deleted in a row, so that they can benefit from a freelist.  Cython
provides the decorator ``@cython.freelist(N)`` for this, which creates a
statically sized freelist of ``N`` instances for a given type.  Example::

    cimport cython

    @cython.freelist(8)
    cdef class Penguin:
        cdef object food
        def __cinit__(self, food):
            self.food = food

    penguin = Penguin('fish 1')
    penguin = None
    penguin = Penguin('fish 2')  # does not need to allocate memory!

.. _existing-pointers-instantiation:

Instantiation from existing C/C++ pointers
===========================================

It is quite common to want to instantiate an extension class from an existing
(pointer to a) data structure, often as returned by external C/C++ functions.

As extension classes can only accept Python objects as arguments in their
contructors, this necessitates the use of factory functions. For example, ::

    from libc.stdlib cimport malloc, free

    # Example C struct
    ctypedef struct my_c_struct:
        int a
        int b


    cdef class WrapperClass:
        """A wrapper class for a C/C++ data structure"""
        cdef my_c_struct *_ptr
        cdef bint ptr_owner

        def __cinit__(self):
            self.ptr_owner = False

        def __dealloc__(self):
            # De-allocate if not null and flag is set
            if self._ptr is not NULL and self.ptr_owner is True:
                free(self._ptr)
                self._ptr = NULL

        # Extension class properties
        @property
        def a(self):
            return self._ptr.a if self._ptr is not NULL else None

        @property
        def b(self):
            return self._ptr.b if self._ptr is not NULL else None

        @staticmethod
        cdef WrapperClass from_ptr(my_c_struct *_ptr, bint owner=False):
            """Factory function to create WrapperClass objects from
            given my_c_struct pointer.

            Setting ``owner`` flag to ``True`` causes
            the extension type to ``free`` the structure pointed to by ``_ptr``
            when the wrapper object is deallocated."""
            # Call to __new__ bypasses __init__ constructor
            cdef WrapperClass wrapper = WrapperClass.__new__(WrapperClass)
            wrapper._ptr = _ptr
            wrapper.ptr_owner = owner
            return wrapper

        @staticmethod
        cdef WrapperClass new_struct():
            """Factory function to create WrapperClass objects with
            newly allocated my_c_struct"""
            cdef my_c_struct *_ptr = <my_c_struct *>malloc(sizeof(my_c_struct))
            if _ptr is NULL:
                raise MemoryError
            _ptr.a = 0
            _ptr.b = 0
            return WrapperClass.from_ptr(_ptr, owner=True)


To then create a ``WrapperClass`` object from an existing ``my_c_struct``
pointer, ``WrapperClass.from_ptr(ptr)`` can be used in Cython code. To allocate
a new structure and wrap it at the same time, ``WrapperClass.new_struct`` can be
used instead.

It is possible to create multiple Python objects all from the same pointer
which point to the same in-memory data, if that is wanted, though care must be
taken when de-allocating as can be seen above.
Additionally, the ``ptr_owner`` flag can be used to control which
``WrapperClass`` object owns the pointer and is responsible for de-allocation -
this is set to ``False`` by default in the example and can be enabled by calling
``from_ptr(ptr, owner=True)``.

The GIL must *not* be released in ``__dealloc__`` either, or another lock used
if it is, in such cases or race conditions can occur with multiple
de-allocations.

Being a part of the object constructor, the ``__cinit__`` method has a Python
signature, which makes it unable to accept a ``my_c_struct`` pointer as an
argument.

Attempts to use pointers in a Python signature will result in errors like::

  Cannot convert 'my_c_struct *' to Python object

This is because Cython cannot automatically convert a pointer to a Python
object, unlike with native types like ``int``.

Note that for native types, Cython will copy the value and create a new Python
object while in the above case, data is not copied and deallocating memory is
a responsibility of the extension class.

.. _making_extension_types_weak_referenceable:

Making extension types weak-referenceable
==========================================

By default, extension types do not support having weak references made to
them. You can enable weak referencing by declaring a C attribute of type
object called :attr:`__weakref__`. For example,::

    cdef class ExplodingAnimal:
        """This animal will self-destruct when it is
        no longer strongly referenced."""

        cdef object __weakref__


Controlling cyclic garbage collection in CPython
================================================

By default each extension type will support the cyclic garbage collector of
CPython. If any Python objects can be referenced, Cython will automatically
generate the ``tp_traverse`` and ``tp_clear`` slots. This is usually what you
want.

There is at least one reason why this might not be what you want: If you need
to cleanup some external resources in the ``__dealloc__`` special function and
your object happened to be in a reference cycle, the garbage collector may
have triggered a call to ``tp_clear`` to drop references. This is the way that
reference cycles are broken so that the garbage can actually be reclaimed.

In that case any object references have vanished by the time when
``__dealloc__`` is called. Now your cleanup code lost access to the objects it
has to clean up. In that case you can disable the cycle breaker ``tp_clear``
by using the ``no_gc_clear`` decorator ::

    @cython.no_gc_clear
    cdef class DBCursor:
        cdef DBConnection conn
        cdef DBAPI_Cursor *raw_cursor
        # ...
        def __dealloc__(self):
            DBAPI_close_cursor(self.conn.raw_conn, self.raw_cursor)

This example tries to close a cursor via a database connection when the Python
object is destroyed. The ``DBConnection`` object is kept alive by the reference
from ``DBCursor``. But if a cursor happens to be in a reference cycle, the
garbage collector may effectively "steal" the database connection reference,
which makes it impossible to clean up the cursor.

Using the ``no_gc_clear`` decorator this can not happen anymore because the
references of a cursor object will not be cleared anymore.

In rare cases, extension types can be guaranteed not to participate in cycles,
but the compiler won't be able to prove this. This would be the case if
the class can never reference itself, even indirectly.
In that case, you can manually disable cycle collection by using the
``no_gc`` decorator, but beware that doing so when in fact the extension type
can participate in cycles could cause memory leaks ::

    @cython.no_gc
    cdef class UserInfo:
        cdef str name
        cdef tuple addresses

If you can be sure addresses will contain only references to strings,
the above would be safe, and it may yield a significant speedup, depending on
your usage pattern.


Controlling pickling
====================

By default, Cython will generate a ``__reduce__()`` method to allow pickling
an extension type if and only if each of its members are convertible to Python
and it has no ``__cinit__`` method.
To require this behavior (i.e. throw an error at compile time if a class
cannot be pickled) decorate the class with ``@cython.auto_pickle(True)``.
One can also annotate with ``@cython.auto_pickle(False)`` to get the old
behavior of not generating a ``__reduce__`` method in any case.

Manually implementing a ``__reduce__`` or `__reduce_ex__`` method will also
disable this auto-generation and can be used to support pickling of more
complicated types.


Public and external extension types
====================================

Extension types can be declared extern or public. An extern extension type
declaration makes an extension type defined in external C code available to a
Cython module. A public extension type declaration makes an extension type
defined in a Cython module available to external C code.

.. _external_extension_types:

External extension types
------------------------

An extern extension type allows you to gain access to the internals of Python
objects defined in the Python core or in a non-Cython extension module.

.. note::

    In previous versions of Pyrex, extern extension types were also used to
    reference extension types defined in another Pyrex module. While you can still
    do that, Cython provides a better mechanism for this. See
    :ref:`sharing-declarations`.

Here is an example which will let you get at the C-level members of the
built-in complex object.::

    from __future__ import print_function

    cdef extern from "complexobject.h":

        struct Py_complex:
            double real
            double imag

        ctypedef class __builtin__.complex [object PyComplexObject]:
            cdef Py_complex cval

    # A function which uses the above type
    def spam(complex c):
        print("Real:", c.cval.real)
        print("Imag:", c.cval.imag)

.. note::

    Some important things:

    1. In this example, :keyword:`ctypedef` class has been used. This is
       because, in the Python header files, the ``PyComplexObject`` struct is
       declared with:

       .. sourcecode:: c

        typedef struct {
            ...
        } PyComplexObject;

       At runtime, a check will be performed when importing the Cython
       c-extension module that ``__builtin__.complex``'s ``tp_basicsize``
       matches ``sizeof(`PyComplexObject)``. This check can fail if the Cython
       c-extension module was compiled with one version of the
       ``complexobject.h`` header but imported into a Python with a changed
       header. This check can be tweaked by using ``check_size`` in the name
       specification clause.

    2. As well as the name of the extension type, the module in which its type
       object can be found is also specified. See the implicit importing section
       below.

    3. When declaring an external extension type, you don't declare any
       methods.  Declaration of methods is not required in order to call them,
       because the calls are Python method calls. Also, as with
       :keyword:`struct` and :keyword:`union`, if your extension class
       declaration is inside a :keyword:`cdef` extern from block, you only need to
       declare those C members which you wish to access.

.. _name_specification_clause:

Name specification clause
-------------------------

The part of the class declaration in square brackets is a special feature only
available for extern or public extension types. The full form of this clause
is::

    [object object_struct_name, type type_object_name, check_size cs_option]

Where:

- ``object_struct_name`` is the name to assume for the type's C struct.
- ``type_object_name`` is the name to assume for the type's statically
  declared type object.
- ``cs_option`` is ``warn`` (the default), ``error``, or ``ignore`` and is only
  used for external extension types.  If ``error``, the ``sizeof(object_struct)``
  that was found at compile time must match the type's runtime ``tp_basicsize``
  exactly, otherwise the module import will fail with an error.  If ``warn``
  or ``ignore``, the ``object_struct`` is allowed to be smaller than the type's
  ``tp_basicsize``, which indicates the runtime type may be part of an updated
  module, and that the external module's developers extended the object in a
  backward-compatible fashion (only adding new fields to the end of the object).
  If ``warn``, a warning will be emitted in this case.

The clauses can be written in any order.

If the extension type declaration is inside a :keyword:`cdef` extern from
block, the object clause is required, because Cython must be able to generate
code that is compatible with the declarations in the header file. Otherwise,
for extern extension types, the object clause is optional.

For public extension types, the object and type clauses are both required,
because Cython must be able to generate code that is compatible with external C
code.

Attribute name matching and aliasing
------------------------------------

Sometimes the type's C struct as specified in ``object_struct_name`` may use
different labels for the fields than those in the ``PyTypeObject``. This can
easily happen in hand-coded C extensions where the ``PyTypeObject_Foo`` has a
getter method, but the name does not match the name in the ``PyFooObject``. In
NumPy, for instance, python-level ``dtype.itemsize`` is a getter for the C
struct field ``elsize``. Cython supports aliasing field names so that one can
write ``dtype.itemsize`` in Cython code which will be compiled into direct
access of the C struct field, without going through a C-API equivalent of
``dtype.__getattr__('itemsize')``.

For example we may have an extension
module ``foo_extension``::

    cdef class Foo:
        cdef public int field0, field1, field2;

        def __init__(self, f0, f1, f2):
            self.field0 = f0
            self.field1 = f1
            self.field2 = f2

but a C struct in a file ``foo_nominal.h``::

   typedef struct {
        PyObject_HEAD
        int f0;
        int f1;
        int f2;
    } FooStructNominal;

Note that the struct uses ``f0``, ``f1``, ``f2`` but they are ``field0``,
``field1``, and ``field2`` in ``Foo``. We are given this situation, including
a header file with that struct, and we wish to write a function to sum the
values. If we write an extension module ``wrapper``::

    cdef extern from "foo_nominal.h":

        ctypedef class foo_extension.Foo [object FooStructNominal]:
            cdef:
                int field0
                int field1
                int feild2

    def sum(Foo f):
        return f.field0 + f.field1 + f.field2

then ``wrapper.sum(f)`` (where ``f = foo_extension.Foo(1, 2, 3)``) will still
use the C-API equivalent of::

    return f.__getattr__('field0') +
           f.__getattr__('field1') +
           f.__getattr__('field1')

instead of the desired C equivalent of ``return f->f0 + f->f1 + f->f2``. We can
alias the fields by using::
    cdef extern from "foo_nominal.h":

        ctypedef class foo_extension.Foo [object FooStructNominal]:
            cdef:
                int field0 "f0"
                int field1 "f1"
                int field2 "f2"

    def sum(Foo f) except -1:
        return f.field0 + f.field1 + f.field2

and now Cython will replace the slow ``__getattr__`` with direct C access to
the FooStructNominal fields. This is useful when directly processing Python
code. No changes to Python need be made to achieve significant speedups, even
though the field names in Python and C are different. Of course, one should
make sure the fields are equivalent.

Implicit importing
------------------

Cython requires you to include a module name in an extern extension class
declaration, for example,::

    cdef extern class MyModule.Spam:
        ...

The type object will be implicitly imported from the specified module and
bound to the corresponding name in this module. In other words, in this
example an implicit::

      from MyModule import Spam

statement will be executed at module load time.

The module name can be a dotted name to refer to a module inside a package
hierarchy, for example,::

    cdef extern class My.Nested.Package.Spam:
        ...

You can also specify an alternative name under which to import the type using
an as clause, for example,::

      cdef extern class My.Nested.Package.Spam as Yummy:
         ...

which corresponds to the implicit import statement::

      from My.Nested.Package import Spam as Yummy

.. _types_names_vs_constructor_names:

Type names vs. constructor names
--------------------------------

Inside a Cython module, the name of an extension type serves two distinct
purposes. When used in an expression, it refers to a module-level global
variable holding the type's constructor (i.e. its type-object). However, it
can also be used as a C type name to declare variables, arguments and return
values of that type.

When you declare::

    cdef extern class MyModule.Spam:
        ...

the name Spam serves both these roles. There may be other names by which you
can refer to the constructor, but only Spam can be used as a type name. For
example, if you were to explicitly import MyModule, you could use
``MyModule.Spam()`` to create a Spam instance, but you wouldn't be able to use
:class:`MyModule.Spam` as a type name.

When an as clause is used, the name specified in the as clause also takes over
both roles. So if you declare::

    cdef extern class MyModule.Spam as Yummy:
        ...

then Yummy becomes both the type name and a name for the constructor. Again,
there are other ways that you could get hold of the constructor, but only
Yummy is usable as a type name.

.. _public:

Public extension types
======================

An extension type can be declared public, in which case a ``.h`` file is
generated containing declarations for its object struct and type object. By
including the ``.h`` file in external C code that you write, that code can
access the attributes of the extension type.



