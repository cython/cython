Troubleshooting
===============

This section provides some general troubleshooting advice about commonly-seen
errors. If you're having a problem with Cython it may be worth reading this.
If you encounter a commonly-seen error that we haven't covered here, we'd
appreciate a PR adding it to this section!

Where the language is "messy"
-----------------------------

By necessity, Cython is a slightly odd mix of the resolved-at-run-time, dynamic
behaviour of Python, and the statically-defined, resolved at compile-time behaviour
of C. These don't always combine perfectly, and the places that often cause confusion
are often the places they meet.

As example, for a ``cdef class``, Cython is able to access ``cdef`` attributes
directly (as a simple C lookup). However, if the direct attribute lookup "misses"
then Cython doesn't produce an error message - instead it assumes that it will
be able to resolve that attribute through the standard Python "string lookup from
a dictionary" mechanism at runtime. The two mechanisms are quite different in
how they work and what they can return (the Python mechanism can only return
Python objects, while the the direct lookup can return largely any C type).

Much the same can occur when a name is imported rather "cimported" - Cython does
not know where the name comes from so treats it as a regular Python object.

This silent-fallback to Python behaviour is often a source of confusion. In the
best case it gives the same overall behaviour but slightly slower (for example
calling a ``cpdef`` function through the Python mechanism rather than directly
to C). Often it just causes an ``AttributeError`` exception at runtime. Very
occasionally it might do something quite different - invoke a Python method
with the same name as a ``cdef`` method, or cause a convert from a C++ container
to a Python one.

This kind of dual-layered behaviour probably isn't how one would design a
language from scratch, but is needed for Cython's goals for being Python compatible
and allowing C types to be used fairly seamlessly.

``AttributeErrors``
-------------------

Untyped objects
^^^^^^^^^^^^^^^

A common reason to get ``AttributeErrors`` is that Cython does not know the type of your
object::

    cdef class Counter:
        cdef int count_so_far
        
        ...

The attribute ``count_so_far`` is only accessible from Cython code, and Cython accesses
it through a direct lookup into the C struct that it defines for ``Counter`` (i.e.
it's really quick!).
Now try run the following Cython code on a pair of ``Counter`` objects::

    def bigger_count(c1, c2):
        return c1.count_so_far < c2.count_so_far
        
This will give an ``AttributeError`` because Cython does not know the types of ``c1``
and ``c2``. Typing them as ``Counter c1`` and ``Counter c2`` fixes the problem::

    def bigger_count(c1, c2):
        return c1.count_so_far < c2.count_so_far

A common variation of the same problem happens for global objects::

    def count_something():
        c = Counter()
        
        # code goes here!!!
        
        print(c.count_so_far)  # works
        
    global_count = Counter()
    print(global_count.count_so_far)  # AttributeError!
    
Within a function Cython usually manages to infer the type. So it knows that ``c`` is a ``Counter``
even though you have not told it. However the same *doesn't* apply at global/module scope. Here
there's a strong assumption that you want objects to be exposed as Python attributes of the
module (and remember that Python attributes could be modified from elsewhere...), so Cython
essentially disables all type-inference. Therefore it doesn't know the type of ``global_count``.

Writing into extension types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``AttributeError``s can also happen when writing into a ``cdef class``, commonly in ``__init__``::

    cdef class Company:
        def __init__(self, staff):
            self.staff = staff  # AttributeError!
            
Unlike a regular class, ``cdef class`` has a fixed list of attributes that you can write to and
you need to declare them explicitly. For example::

    cdef class Company:
       cdef list staff
       # ...
       
(use ``cdef staff`` or ``cdef object staff`` if you don't want to specify a type). If you do want
the ability to add arbitrary attributes then you can add a ``__dict__`` member::

    cdef class Company:
       cdef dict __dict__
       def __init__(self, staff):
           self.staff = staff
           
This gives extra flexibility, but loses some of the performance benefits of using an extension type.
It also adds restrictions to inheritance.

Extension type class attributes vs instance attributes
------------------------------------------------------

A common pattern in Python (used a lot within the Cython code-base itself) is to
use instance attributes that shadow class attributes::

    class Email:
        message = "hello"  # sensible default
        
        def actually_I_really_dislike_this_person(self):
            self.message = "go away!"

On access to ``message`` Python first looks up the instance dictionary to see if it
has a value for ``message`` and if that fails looks up the class dictionary to get
the default value. The advantages are

* it provides an easy sensible default,
* it potentially saves a bit of memory by not populating the instance dictionary if
  not necessary (although modern versions of Python are pretty good at sharing keys
  for common attributes between instances),
* it saves a bit of time reference counting (vs if you initialized the defaults in
  the constructor),
  
Cython extension types don't support this pattern. You should just set the
defaults in the constructor. If you don't set defaults for a ``cdef`` attribute then
they'll be set to an "empty" value (``None`` for Python object attributes).
