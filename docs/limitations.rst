.. _cython-limitations-label:

Limitations
===========

Unsupported Python features
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cython is not quite a full superset of Python. The following restrictions apply:

* Function definitions (whether using ``def`` or ``cdef``) cannot be nested within
  other function definitions.  
* Class definitions can only appear at the top level of a module, 
  not inside a function.
* The ``import *`` form of import is not allowed anywhere (other forms of the
  import statement are fine, though).  
* Generators cannot be defined in Cython.
* The ``globals()`` and ``locals()`` functions cannot be used.

The above restrictions will most likely remain, since removing them would be
difficult and they're not really needed for Cython's intended applications.

There are also some temporary limitations, which may eventually be lifted, including:

* Class and function definitions cannot be placed inside control structures.
* There is no support for Unicode.
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
usual idiom for using the ``classmethod`` and ``staticmethod`` functions,
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
       Cython-defined Python functions are PyCFunction objects, not PyFunction
       objects, and are not recognised by the machinery that creates a bound
       or unbound method when a function is extracted from a class. To get
       around this, Cython wraps each method in an unbound method object itself
       before storing it in the class's dictionary.
