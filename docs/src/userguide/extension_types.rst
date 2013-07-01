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
statement.  Here's an example::

    cdef class Shrubbery:

        cdef int width, height

        def __init__(self, w, h):
            self.width = w
            self.height = h

        def describe(self):
            print "This shrubbery is", self.width, \
                "by", self.height, "cubits."

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

Attributes
============

Attributes of an extension type are stored directly in the object's C struct.
The set of attributes is fixed at compile time; you can't add attributes to an
extension type instance at run time simply by assigning to them, as you could
with a Python class instance. (You can subclass the extension type in Python
and add attributes to instances of the subclass, however.)

There are two ways that attributes of an extension type can be accessed: by
Python attribute lookup, or by direct access to the C struct from Cython code.
Python code is only able to access attributes of an extension type by the
first method, but Cython code can use either method.

By default, extension type attributes are only accessible by direct access,
not Python access, which means that they are not accessible from Python code.
To make them accessible from Python code, you need to declare them as
:keyword:`public` or :keyword:`readonly`. For example::

    cdef class Shrubbery:
        cdef public int width, height
        cdef readonly float depth

makes the width and height attributes readable and writable from Python code,
and the depth attribute readable but not writable.

.. note::

    You can only expose simple C types, such as ints, floats, and
    strings, for Python access. You can also expose Python-valued attributes.

.. note::

    Also the :keyword:`public` and :keyword:`readonly` options apply only to
    Python access, not direct access. All the attributes of an extension type
    are always readable and writable by C-level access.

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
follows::

    cdef widen_shrubbery(Shrubbery sh, extra_width):
        sh.width = sh.width + extra_width

Now the Cython compiler knows that ``sh`` has a C attribute called
:attr:`width` and will generate code to access it directly and efficiently.
The same consideration applies to local variables, for example,::

    cdef Shrubbery another_shrubbery(Shrubbery sh1):
        cdef Shrubbery sh2
        sh2 = Shrubbery()
        sh2.width = sh1.width
        sh2.height = sh1.height
        return sh2


Type Testing and Casting
------------------------

Suppose I have a method :meth:`quest` which returns an object of type :class:`Shrubbery`. 
To access it's width I could write::

    cdef Shrubbery sh = quest()
    print sh.width

which requires the use of a local variable and performs a type test on assignment. 
If you *know* the return value of :meth:`quest` will be of type :class:`Shrubbery`
you can use a cast to write::

    print (<Shrubbery>quest()).width

This may be dangerous if :meth:`quest()` is not actually a :class:`Shrubbery`, as it 
will try to access width as a C struct member which may not exist. At the C level, 
rather than raising an :class:`AttributeError`, either an nonsensical result will be 
returned (interpreting whatever data is at at that address as an int) or a segfault 
may result from trying to access invalid memory. Instead, one can write::

    print (<Shrubbery?>quest()).width

which performs a type check (possibly raising a :class:`TypeError`) before making the 
cast and allowing the code to proceed. 

To explicitly test the type of an object, use the :meth:`isinstance` method. By default, 
in Python, the :meth:`isinstance` method checks the :class:`__class__` attribute of the 
first argument to determine if it is of the required type. However, this is potentially 
unsafe as the :class:`__class__` attribute can be spoofed or changed, but the C structure 
of an extension type must be correct to access its :keyword:`cdef` attributes and call its :keyword:`cdef` methods. Cython detects if the second argument is a known extension 
type and does a type check instead, analogous to Pyrex's :meth:`typecheck`.  
The old behavior is always available by passing a tuple as the second parameter::

    print isinstance(sh, Shrubbery)     # Check the type of sh
    print isinstance(sh, (Shrubbery,))  # Check sh.__class__


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

Properties
============

There is a special syntax for defining properties in an extension class::

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

        property cheese:

            def __get__(self):
                return "We don't have: %s" % self.cheeses

            def __set__(self, value):
                self.cheeses.append(value)

            def __del__(self):
                del self.cheeses[:]

    # Test input
    from cheesy import CheeseShop

    shop = CheeseShop()
    print shop.cheese

    shop.cheese = "camembert"
    print shop.cheese

    shop.cheese = "cheddar"
    print shop.cheese

    del shop.cheese
    print shop.cheese

.. sourcecode:: text

    # Test output
    We don't have: []
    We don't have: ['camembert']
    We don't have: ['camembert', 'cheddar']
    We don't have: []

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

Since Cython 0.13.1, there is a way to prevent extension types from
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
compared to a :keyword:`cdef` methd::

    # pets.pyx
    cdef class Parrot:

        cdef void describe(self):
            print "This parrot is resting."

    cdef class Norwegian(Parrot):

        cdef void describe(self):
            Parrot.describe(self)
            print "Lovely plumage!"


    cdef Parrot p1, p2
    p1 = Parrot()
    p2 = Norwegian()
    print "p1:"
    p1.describe()
    print "p2:"
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


Forward-declaring extension types
===================================

Extension types can be forward-declared, like :keyword:`struct` and
:keyword:`union` types. This will be necessary if you have two extension types
that need to refer to each other, e.g.::

    cdef class Shrubbery # forward declaration

    cdef class Shrubber:
        cdef Shrubbery work_in_progress

    cdef class Shrubbery:
        cdef Shrubber creator

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


Making extension types weak-referenceable
==========================================

By default, extension types do not support having weak references made to
them. You can enable weak referencing by declaring a C attribute of type
object called :attr:`__weakref__`. For example,::

    cdef class ExplodingAnimal:
        """This animal will self-destruct when it is
        no longer strongly referenced."""
    
        cdef object __weakref__


Public and external extension types
====================================

Extension types can be declared extern or public. An extern extension type
declaration makes an extension type defined in external C code available to a
Cython module. A public extension type declaration makes an extension type
defined in a Cython module available to external C code.

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

    cdef extern from "complexobject.h":

        struct Py_complex:
            double real
            double imag

        ctypedef class __builtin__.complex [object PyComplexObject]:
            cdef Py_complex cval

    # A function which uses the above type
    def spam(complex c):
        print "Real:", c.cval.real
        print "Imag:", c.cval.imag

.. note::

    Some important things:

    1. In this example, :keyword:`ctypedef` class has been used. This is
       because, in the Python header files, the ``PyComplexObject`` struct is
       declared with:

       .. sourcecode:: c

        typedef struct {
            ...
        } PyComplexObject;

    2. As well as the name of the extension type, the module in which its type
       object can be found is also specified. See the implicit importing section
       below. 

    3. When declaring an external extension type, you don't declare any
       methods.  Declaration of methods is not required in order to call them,
       because the calls are Python method calls. Also, as with
       :keyword:`struct` and :keyword:`union`, if your extension class
       declaration is inside a :keyword:`cdef` extern from block, you only need to
       declare those C members which you wish to access.

Name specification clause
-------------------------

The part of the class declaration in square brackets is a special feature only
available for extern or public extension types. The full form of this clause
is::

    [object object_struct_name, type type_object_name ]

where ``object_struct_name`` is the name to assume for the type's C struct,
and type_object_name is the name to assume for the type's statically declared
type object. (The object and type clauses can be written in either order.)

If the extension type declaration is inside a :keyword:`cdef` extern from
block, the object clause is required, because Cython must be able to generate
code that is compatible with the declarations in the header file. Otherwise,
for extern extension types, the object clause is optional.

For public extension types, the object and type clauses are both required,
because Cython must be able to generate code that is compatible with external C
code.

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
example, if you were to explicity import MyModule, you could use
``MyModule.Spam()`` to create a Spam instance, but you wouldn't be able to use
:class:`MyModule.Spam` as a type name.

When an as clause is used, the name specified in the as clause also takes over
both roles. So if you declare::

    cdef extern class MyModule.Spam as Yummy:
        ...

then Yummy becomes both the type name and a name for the constructor. Again,
there are other ways that you could get hold of the constructor, but only
Yummy is usable as a type name.

Public extension types
======================

An extension type can be declared public, in which case a ``.h`` file is
generated containing declarations for its object struct and type object. By
including the ``.h`` file in external C code that you write, that code can
access the attributes of the extension type.



