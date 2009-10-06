.. highlight:: cython

.. _extension_types:

***************
Extention Types
***************

* Normal Python as well as extension type classes can be defined.
* Extension types:

 * Are considered by Python to be "built-in" types.
 * Can be used to wrap arbitrary C data structures, and provide a Python-like interface to them from Python.
 * Attributes and methods can be called from Python or Cython code
 * Are defined by the ``cdef`` class statement::

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

 * Add to a list each time it is written to.
 * Return the list when it is read.
 * Empty the list when it is deleted.

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

.. provide link to the table of special methods

===========
Subclassing
===========

====================
Forward Declarations
====================

========================
Extension Types and None
========================

================
Weak Referencing
================

======
Public
======

========
External
========





























