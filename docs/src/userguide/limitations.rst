.. highlight:: cython

.. _cython-limitations:

*************
Limitations
*************

Unsupported Python Features
============================

One of our goals is to make Cython as compatible as possible with standard
Python. This page lists the things that work in Python but not in Cython.
As Cython matures, the items in this list should go away. 


Generators and generator expressions
-------------------------------------

The yield keyword is not yet supported.  This is work in progress.

Since Cython 0.13, some generator expressions are supported when they
can be transformed into inlined loops in combination with builtins,
e.g.  ``sum(x*2 for x in seq)``.  As of 0.14, the supported builtins
are ``list()``, ``set()``, ``dict()``, ``sum()``, ``any()``,
``all()``, ``sorted()``.


Other Current Limitations
==========================

* The :func:`globals` builtin returns the last Python callers globals, not the current function's locals. This behavior should not be relied upon, as it will probably change in the future. 
* The :func:`locals` builtin can only be used if all local variables can be converted to Python objects, and returns a dict.
* Class and function definitions cannot be placed inside control structures.

Semantic differences between Python and Cython
----------------------------------------------

Behaviour of class scopes
^^^^^^^^^^^^^^^^^^^^^^^^^

In Python, referring to a method of a class inside the class definition, i.e.
while the class is being defined, yields a plain function object, but in
Cython it yields an unbound method [#]_. A consequence of this is that the
usual idiom for using the :func:`classmethod` and :func:`staticmethod` functions,
e.g.::

    class Spam:

        def method(cls):
            ...

        method = classmethod(method)

will not work in Cython. This can be worked around by defining the function
outside the class, and then assigning the result of ``classmethod`` or
``staticmethod`` inside the class, i.e.::

    def Spam_method(cls):
        ...

    class Spam:

        method = classmethod(Spam_method)

This will change in the near future. 

.. rubric:: Footnotes

.. [#] The reason for the different behaviour of class scopes is that
       Cython-defined Python functions are ``PyCFunction`` objects, not
       ``PyFunction`` objects, and are not recognised by the machinery that creates a
       bound or unbound method when a function is extracted from a class. To get
       around this, Cython wraps each method in an unbound method object itself
       before storing it in the class's dictionary.
