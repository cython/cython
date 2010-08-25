.. highlight:: cython

.. _extension_types:

***************
Extension Types
***************

* Normal Python as well as extension type classes can be defined.
* Extension types:

 * Are considered by Python as "built-in" types.
 * Can be used to wrap arbitrary C-data structures, and provide a Python-like interface to them from Python.
 * Attributes and methods can be called from Python or Cython code
 * Are defined by the ``cdef class`` statement.

::

    cdef class Shrubbery:

        cdef int width, height

        def __init__(self, w, h):
            self.width = w
            self.height = h

        def describe(self):
            print "This shrubbery is", self.width, \
                "by", self.height, "cubits."

==========
Attributes
==========

* Are stored directly in the object's C struct.
* Are fixed at compile time.

 * You can't add attributes to an extension type instance at run time like in normal Python.
 * You can sub-class the extenstion type in Python to add attributes at run-time.

* There are two ways to access extension type attributes:

 * By Python look-up.

  * Python code's only method of access.

 * By direct access to the C struct from Cython code.

  * Cython code can use either method of access, though.

* By default, extension type attributes are:

 * Only accessible by direct access.
 * Not accessible from Python code.

* To make attributes accessible to Python, they must be declared ``public`` or ``readonly``::

    cdef class Shrubbery:
        cdef public int width, height
        cdef readonly float depth

 * The ``width`` and ``height`` attributes are readable and writable from Python code.
 * The ``depth`` attribute is readable but not writable.

.. note::
    .. note::
        You can only expose simple C types, such as ints, floats, and strings, for Python access. You can also expose Python-valued attributes.

    .. note::
        The ``public`` and ``readonly`` options apply only to Python access, not direct access. All the attributes of an extension type are always readable and writable by C-level access.


=======
Methods
=======

* ``self`` is used in extension type methods just like it normally is in Python.
* See **Functions and Methods**; all of which applies here.

==========
Properties
==========

* Cython provides a special syntax::

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

* The ``__get__()``, ``__set__()``, and ``__del__()`` methods are all optional.

 * If they are ommitted, An exception is raised when an access attempt is made.

* Below, is a full example that defines a property which can..

 * Add to a list each time it is written to (``"__set__"``).
 * Return the list when it is read (``"__get__"``).
 * Empty the list when it is deleted (``"__del__"``).

::

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

::

        # Test output
        We don't have: []
        We don't have: ['camembert']
        We don't have: ['camembert', 'cheddar']
        We don't have: []


===============
Special Methods
===============

.. note::

    #. The semantics of Cython's special methods are similar in principle to that of Python's.
    #. There are substantial differences in some behavior.
    #. Some Cython special methods have no Python counter-part.

* See the :ref:`special_methods_table` for the many that are available.


Declaration
===========

* Must be declared with ``def`` and cannot be declared with ``cdef``.
* Performance is not affected by the ``def`` declaration because of special calling conventions

Docstrings
==========

* Docstrings are not supported yet for some special method types.
* They can be included in the source, but may not appear in the corresponding ``__doc__`` attribute at run-time.

 * This a Python library limitation because the ``PyTypeObject`` data structure is limited

Initialization: ``__cinit__()`` and ``__init__()``
==================================================

* Any arguments passed to the extension type's constructor, will be passed to both initialization methods.
* ``__cinit__()`` is where you should perform C-level initialization of the object

 * This includes any allocation of C data structures.
 * **Caution** is warranted as to what you do in this method.

  * The object may not be fully valid Python object when it is called.
  * Calling Python objects, including the extensions own methods, may be hazardous.

 * By the time ``__cinit__()`` is called...

  * Memory has been allocated for the object.
  * All C-level attributes have been initialized to 0 or null.
  * Python have been initialized to ``None``, but you can not rely on that for each occasion.
  * This initialization method is guaranteed to be called exactly once.

 * For Extensions types that inherit a base type:

  * The ``__cinit__()`` method of the base type is automatically called before this one.
  * The inherited ``__cinit__()`` method can not be called explicitly.
  * Passing modified argument lists to the base type must be done through ``__init__()``.
  * It may be wise to give the ``__cinit__()`` method both ``"*"`` and ``"**"`` arguments.

   * Allows the method to accept or ignore additional arguments.
   * Eliminates the need for a Python level sub-class, that changes the ``__init__()`` method's signature, to have to override both the ``__new__()`` and ``__init__()`` methods.

  * If ``__cinit__()`` is declared to take no arguments except ``self``, it will ignore any extra arguments passed to the constructor without complaining about a signature mis-match


* ``__init__()`` is for higher-level initialization and is safer for Python access.

 * By the time this method is called, the extension type is a fully valid Python object.
 * All operations are safe.
 * This method may sometimes be called more than once, or possibly not at all.

  * Take this into consideration to make sure the design of your other methods are robust of this fact.

Finalization: ``__dealloc__()``
===============================

* This method is the counter-part to ``__cinit__()``.
* Any C-data that was explicitly allocated in the ``__cinit__()`` method should be freed here.
* Use caution in this method:

 * The Python object to which this method belongs may not be completely intact at this point.
 * Avoid invoking any Python operations that may touch the object.
 * Don't call any of this object's methods.
 * It's best to just deallocate C-data structures here.

* All Python attributes of your extension type object are deallocated by Cython after the ``__dealloc__()`` method returns.

Arithmetic Methods
==================

.. note:: Most of these methods behave differently than in Python

* There are not "reversed" versions of these methods... there is no __radd__() for instance.
* If the first operand cannot perform the operation, the same method of the second operand is called, with the operands in the same order.
* Do not rely on the first parameter of these methods, being ``"self"`` or the right type.
* The types of both operands should be tested before deciding what to do.
* Return ``NotImplemented`` for unhandled, mis-matched operand types.
* The previously mentioned points..

 * Also apply to 'in-place' method ``__ipow__()``.
 * Do not apply to other 'in-place' methods like ``__iadd__()``, in that these always take ``self`` as the first argument.


Rich Comparisons
================

.. note:: There are no separate methods for individual rich comparison operations.

* A single special method called ``__richcmp__()`` replaces all the individual rich compare, special method types.
* ``__richcmp__()`` takes an integer argument, indicating which operation is to be performed as shown in the table below.

    +-----+-----+
    |  <  |  0  |
    +-----+-----+
    | ==  |  2  |
    +-----+-----+
    |  >  |  4  |
    +-----+-----+
    | <=  |  1  |
    +-----+-----+
    | !=  |  3  |
    +-----+-----+
    | >=  |  5  |
    +-----+-----+




The ``__next__()`` Method
=========================

* Extension types used to expose an iterator interface should define a ``__next__()`` method.
* **Do not** explicitly supply a ``next()`` method, because Python does that for you automatically.


===========
Subclassing
===========

* An extension type may inherit from a built-in type or another extension type::

    cdef class Parrot:
        ...

    cdef class Norwegian(Parrot):
        ...

* A complete definition of the base type must be available to Cython

 * If the base type is a built-in type, it must have been previously declared as an ``extern`` extension type.
 * ``cimport`` can be used to import the base type, if the extern declared base type is in a ``.pxd`` definition file.

 * In Cython, multiple inheritance is not permitted.. singlular inheritance only

* Cython extenstion types can also be sub-classed in Python.

 * Here multiple inhertance is permissible as is normal for Python.
 * Even multiple extension types may be inherited, but C-layout of all the base classes must be compatible.


====================
Forward Declarations
====================

* Extension types can be "forward-declared".
* This is necessary when two extension types refer to each other::

    cdef class Shrubbery # forward declaration

    cdef class Shrubber:
        cdef Shrubbery work_in_progress

    cdef class Shrubbery:
        cdef Shrubber creator

* An extension type that has a base-class, requires that both forward-declarations be specified::

    cdef class A(B)

    ...

    cdef class A(B):
        # attributes and methods


========================
Extension Types and None
========================

* Parameters and C-variables declared as an Extension type, may take the value of ``None``.
* This is analogous to the way a C-pointer can take the value of ``NULL``.

.. note::
    #. Exercise caution when using ``None``
    #. Read this section carefully.

* There is no problem as long as you are performing Python operations on it.

 * This is because full dynamic type checking is applied

* When accessing an extension type's C-attributes, **make sure** it is not ``None``.

 * Cython does not check this for reasons of efficency.

* Be very aware of exposing Python functions that take extension types as arguments::

    def widen_shrubbery(Shrubbery sh, extra_width): # This is
    sh.width = sh.width + extra_width

    * Users could **crash** the program by passing ``None`` for the ``sh`` parameter.
    * This could be avoided by::

        def widen_shrubbery(Shrubbery sh, extra_width):
            if sh is None:
                raise TypeError
            sh.width = sh.width + extra_width

    * Cython provides a more convenient way with a ``not None`` clause::

        def widen_shrubbery(Shrubbery sh not None, extra_width):
            sh.width = sh.width + extra_width

    * Now this function automatically checks that ``sh`` is not ``None``, as well as that is the right type.

* ``not None`` can only be used in Python functions (declared with ``def`` **not** ``cdef``).
* For ``cdef`` functions, you will have to provide the check yourself.
* The ``self`` parameter of an extension type is guaranteed to **never** be ``None``.
* When comparing a value ``x`` with ``None``, and ``x`` is a Python object, note the following:

 * ``x is None`` and ``x is not None`` are very efficient.

  * They translate directly to C-pointer comparisons.

 * ``x == None`` and ``x != None`` or ``if x: ...`` (a boolean condition), will invoke Python operations and will therefore be much slower.

================
Weak Referencing
================

* By default, weak references are not supported.
* It can be enabled by declaring a C attribute of the ``object`` type called ``__weakref__()``::

    cdef class ExplodingAnimal:
        """This animal will self-destruct when it is
        no longer strongly referenced."""

        cdef object __weakref__

=========================
External and Public Types
=========================


Public
======

* When an extention type is declared ``public``, Cython will generate a C-header (".h") file.
* The header file will contain the declarations for it's **object-struct** and it's **type-object**.
* External C-code can now access the attributes of the extension type.


External
========

* An ``extern`` extension type allows you to gain access to the internals of:

 * Python objects defined in the Python core.
 * Non-Cython extension modules

* The following example lets you get at the C-level members of Python's built-in "complex" object::

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

.. note:: Some important things in the example:
    #. ``ctypedef`` has been used because because Python's header file has the struct decalared with::

        ctypedef struct {
        ...
        } PyComplexObject;

    #. The module of where this type object can be found is specified along side the name of the extension type. See **Implicit Importing**.

    #. When declaring an external extension type...

     * Don't declare any methods, because they are Python method class the are not needed.
     * Similiar to **structs** and **unions**, extension classes declared inside a ``cdef extern from`` block only need to declare the C members which you will actually need to access in your module.


Name Specification Clause
=========================

.. note:: Only available to **public** and **extern** extension types.

* Example::

    [object object_struct_name, type type_object_name ]

* ``object_struct_name`` is the name to assume for the type's C-struct.
* ``type_object_name`` is the name to assume for the type's statically declared type-object.
* The object and type clauses can be written in any order.
* For ``cdef extern from`` declarations, This clause **is required**.

 * The object clause is required because Cython must generate code that is compatible with the declarations in the header file.
 * Otherwise the object clause is optional.

* For public extension types, both the object and type clauses **are required** for Cython to generate code that is compatible with external C-code.

================================
Type Names vs. Constructor Names
================================

* In a Cython module, the name of an extension type serves two distinct purposes:

 #. When used in an expression, it refers to a "module-level" global variable holding the type's constructor (i.e. it's type-object)
 #. It can also be used as a C-type name to declare a "type" for variables, arguments, and return values.

* Example::

    cdef extern class MyModule.Spam:
        ...

 * The name "Spam" serves both of these roles.
 * Only "Spam" can be used as the type-name.
 * The constructor can be referred to by other names.
 * Upon an explicit import of "MyModule"...

  * ``MyModule.Spam()`` could be used as the constructor call.
  * ``MyModule.Spam`` could not be used as a type-name

* When an "as" clause is used, the name specified takes over both roles::

    cdef extern class MyModule.Spam as Yummy:
        ...

 * ``Yummy`` becomes both type-name and a name for the constructor.
 * There other ways of course, to get hold of the constructor, but ``Yummy`` is the only usable type-name.























