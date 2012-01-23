.. highlight:: cython

.. _sharing-declarations:

********************************************
Sharing Declarations Between Cython Modules
********************************************

This section describes a new set of facilities for making C declarations,
functions and extension types in one Cython module available for use in
another Cython module. These facilities are closely modelled on the Python
import mechanism, and can be thought of as a compile-time version of it.

Definition and Implementation files
====================================

A Cython module can be split into two parts: a definition file with a ``.pxd``
suffix, containing C declarations that are to be available to other Cython
modules, and an implementation file with a ``.pyx`` suffix, containing
everything else. When a module wants to use something declared in another
module's definition file, it imports it using the :keyword:`cimport`
statement.

A ``.pxd`` file that consists solely of extern declarations does not need
to correspond to an actual ``.pyx`` file or Python module. This can make it a
convenient place to put common declarations, for example declarations of 
functions from  an :ref:`external library <external-C-code>` that one wants to use in several modules. 

What a Definition File contains
================================

A definition file can contain:

* Any kind of C type declaration.
* extern C function or variable declarations.
* Declarations of C functions defined in the module.
* The definition part of an extension type (see below).

It cannot contain any non-extern C variable declarations.

It cannot contain the implementations of any C or Python functions, or any
Python class definitions, or any executable statements. It is needed when one 
wants to  access :keyword:`cdef` attributes and methods, or to inherit from 
:keyword:`cdef` classes defined in this module. 

.. note::

    You don't need to (and shouldn't) declare anything in a declaration file
    public in order to make it available to other Cython modules; its mere
    presence in a definition file does that. You only need a public
    declaration if you want to make something available to external C code.

What an Implementation File contains
======================================

An implementation file can contain any kind of Cython statement, although there
are some restrictions on the implementation part of an extension type if the
corresponding definition file also defines that type (see below). 
If one doesn't need to :keyword:`cimport` anything from this module, then this
is the only file one needs. 

The cimport statement
=======================

The :keyword:`cimport` statement is used in a definition or
implementation file to gain access to names declared in another definition
file. Its syntax exactly parallels that of the normal Python import
statement::

    cimport module [, module...]

    from module cimport name [as name] [, name [as name] ...]

Here is an example. The file on the left is a definition file which exports a
C data type. The file on the right is an implementation file which imports and
uses it.
 
:file:`dishes.pxd`::

   cdef enum otherstuff:       
       sausage, eggs, lettuce  
                               
   cdef struct spamdish:       
       int oz_of_spam          
       otherstuff filler       
                               
:file:`restaurant.pyx`::

    cimport dishes
    from dishes cimport spamdish

    cdef void prepare(spamdish *d):
        d.oz_of_spam = 42
        d.filler = dishes.sausage

    def serve():
        cdef spamdish d
        prepare(&d)
        print "%d oz spam, filler no. %d" % (d.oz_of_spam, d.filler)
                               
It is important to understand that the :keyword:`cimport` statement can only
be used to import C data types, C functions and variables, and extension
types. It cannot be used to import any Python objects, and (with one
exception) it doesn't imply any Python import at run time. If you want to
refer to any Python names from a module that you have cimported, you will have
to include a regular import statement for it as well.

The exception is that when you use :keyword:`cimport` to import an extension type, its
type object is imported at run time and made available by the name under which
you imported it. Using :keyword:`cimport` to import extension types is covered in more
detail below.  

If a ``.pxd`` file changes, any modules that :keyword:`cimport` from it may need to be 
recompiled. 

Search paths for definition files 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you :keyword:`cimport` a module called ``modulename``, the Cython
compiler searches for a file called :file:`modulename.pxd` along the search
path for include files, as specified by ``-I`` command line options.

Also, whenever you compile a file :file:`modulename.pyx`, the corresponding
definition file :file:`modulename.pxd` is first searched for along the same
path, and if found, it is processed before processing the ``.pyx`` file.  

Using cimport to resolve naming conflicts 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :keyword:`cimport` mechanism provides a clean and simple way to solve the
problem of wrapping external C functions with Python functions of the same
name. All you need to do is put the extern C declarations into a ``.pxd`` file
for an imaginary module, and :keyword:`cimport` that module. You can then
refer to the C functions by qualifying them with the name of the module.
Here's an example:
 
:file:`c_lunch.pxd` ::

    cdef extern from "lunch.h":
        void eject_tomato(float) 	

:file:`lunch.pyx` ::

    cimport c_lunch

    def eject_tomato(float speed):
        c_lunch.eject_tomato(speed)

You don't need any :file:`c_lunch.pyx` file, because the only things defined
in :file:`c_lunch.pxd` are extern C entities. There won't be any actual
``c_lunch`` module at run time, but that doesn't matter; the
:file:`c_lunch.pxd` file has done its job of providing an additional namespace
at compile time.  

Sharing C Functions
===================

C functions defined at the top level of a module can be made available via
:keyword:`cimport` by putting headers for them in the ``.pxd`` file, for
example,:

:file:`volume.pxd`::

    cdef float cube(float)

:file:`spammery.pyx`::

    from volume cimport cube

    def menu(description, size):
        print description, ":", cube(size), \
            "cubic metres of spam"

    menu("Entree", 1)
    menu("Main course", 3)
    menu("Dessert", 2)

:file:`volume.pyx`::

    cdef float cube(float x):
        return x * x * x

.. note::

    When a module exports a C function in this way, an object appears in the
    module dictionary under the function's name. However, you can't make use of
    this object from Python, nor can you use it from Cython using a normal import
    statement; you have to use :keyword:`cimport`.  

Sharing Extension Types 
=======================

An extension type can be made available via :keyword:`cimport` by splitting
its definition into two parts, one in a definition file and the other in the
corresponding implementation file.

The definition part of the extension type can only declare C attributes and C
methods, not Python methods, and it must declare all of that type's C
attributes and C methods.

The implementation part must implement all of the C methods declared in the
definition part, and may not add any further C attributes. It may also define
Python methods.

Here is an example of a module which defines and exports an extension type,
and another module which uses it.::
 
    # Shrubbing.pxd
    cdef class Shrubbery:
        cdef int width
        cdef int length
        
    # Shrubbing.pyx
    cdef class Shrubbery:
        def __cinit__(self, int w, int l):
            self.width = w
            self.length = l

    def standard_shrubbery():
        return Shrubbery(3, 7)


    # Landscaping.pyx
    cimport Shrubbing
    import Shrubbing

    cdef Shrubbing.Shrubbery sh
    sh = Shrubbing.standard_shrubbery()
    print "Shrubbery size is %d x %d" % (sh.width, sh.length)
 
Some things to note about this example:

* There is a :keyword:`cdef` class Shrubbery declaration in both
  :file:`Shrubbing.pxd` and :file:`Shrubbing.pyx`. When the Shrubbing module
  is compiled, these two declarations are combined into one.
* In Landscaping.pyx, the :keyword:`cimport` Shrubbing declaration allows us
  to refer to the Shrubbery type as :class:`Shrubbing.Shrubbery`. But it
  doesn't bind the name Shrubbing in Landscaping's module namespace at run
  time, so to access :func:`Shrubbing.standard_shrubbery` we also need to
  ``import Shrubbing``.

