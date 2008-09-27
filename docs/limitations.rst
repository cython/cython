.. _cython-limitations-label:

*************
Limitations
*************

Unsupported Python Features
============================

One of our goals is to make Cython as compatible as possible with standard
Python. This page lists the things that work in Python but not in Cython.

.. TODO: this limitation seems to be removed
.. ::

..    from module import *

.. This relies on at-runtime insertion of objects into the current namespace and
.. probably will be one of the few features never implemented (as any
.. implementation would be very slow). However, there is the --pre-import option
.. with treats all un-declared names as coming from the specified module, which
.. has the same effect as putting "from module import *" at the top-level of the
.. code. Note: the one difference is that builtins cannot be overriden in this
.. way, as the 'pre-import' scope is even higher than the builtin scope.

Nested def statements
----------------------
Function definitions (whether using ``def`` or ``cdef``) cannot be nested within
other function definitions. ::

    def make_func():
        def f(x):
            return x*x
        return f

(work in progress) This relies on functional closures

Generators
-----------

Using the yield keywords. (work in progress) This relies on functional closures


.. TODO Not really a limitation, rather an enchancement proposal

.. Support for builtin types
.. --------------------------

.. Support for statically declaring types such as list and dict and sequence
.. should be provided, and optimized code produced.

.. This needs to be well thought-out, and I think Pyrex has some plans along
.. these lines as well.

Modulo '%' operation on floats
-------------------------------
::

    a = b%c

where `b` and `c` are floats will raise the error "Invalid operand types for '%' (float; float)"

This can currently be worked around by putting::

    cdef extern from "math.h":
        double fmod(double x, double y)

somewhere is the source file and then using::

    a = fmod(b,c)


Other Current Limitations
==========================

* The :func:`globals` and :func:`locals` functions cannot be used.
* Class and function definitions cannot be placed inside control structures.
* Special methods of extension types cannot have functioning docstrings.
* The use of string literals as comments is not recommended at present,
  because Cython doesn't optimize them away, and won't even accept them in places
  where executable statements are not allowed.

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

.. rubric:: Footnotes

.. [#] The reason for the different behaviour of class scopes is that
       Cython-defined Python functions are ``PyCFunction`` objects, not
       ``PyFunction`` objects, and are not recognised by the machinery that creates a
       bound or unbound method when a function is extracted from a class. To get
       around this, Cython wraps each method in an unbound method object itself
       before storing it in the class's dictionary.
