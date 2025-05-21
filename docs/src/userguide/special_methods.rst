.. _special-methods:

Special Methods of Extension Types
===================================

.. include::
    ../two-syntax-variants-used

This page describes the special methods currently supported by Cython extension
types. A complete list of all the special methods appears in the table at the
bottom. Some of these methods behave differently from their Python
counterparts or have no direct Python counterparts, and require special
mention.

.. Note::

    Everything said on this page applies only to extension types, defined
    with the :keyword:`cdef` class statement or decorated using ``@cclass`` decorator.
    It doesn't apply to classes defined with the
    Python :keyword:`class` statement, where the normal Python rules apply.

.. _declaration:

Declaration
------------
Special methods of extension types must be declared with :keyword:`def`, not
:keyword:`cdef`/``@cfunc``. This does not impact their performance--Python uses different
calling conventions to invoke these special methods.

.. _docstrings:

Docstrings
-----------

Currently, docstrings are not fully supported in some special methods of extension
types. You can place a docstring in the source to serve as a comment, but it
won't show up in the corresponding :attr:`__doc__` attribute at run time. (This
seems to be is a Python limitation -- there's nowhere in the :c:type:`PyTypeObject`
data structure to put such docstrings.)


.. _initialisation_methods:

Initialisation methods: :meth:`__cinit__` and :meth:`__init__`
---------------------------------------------------------------
There are two methods concerned with initialising the object, the normal Python
:meth:`__init__` method and a special :meth:`__cinit__` method where basic
C level initialisation can be performed.

The main difference between the two is when they are called.
The :meth:`__cinit__` method is guaranteed to be called as part of the object
allocation, but before the object is fully initialised.  Specifically, methods
and object attributes that belong to subclasses or that were overridden by
subclasses may not have been initialised at all yet and must not be used by
:meth:`__cinit__` in a base class.  Note that the object allocation in Python
clears all fields and sets them to zero (or ``NULL``).  Cython additionally
takes responsibility of setting all object attributes to ``None``, but again,
this may not yet have been done for the attributes defined or overridden by
subclasses.  If your object needs anything more than this basic attribute
clearing in order to get into a correct and safe state, :meth:`__cinit__`
may be a good place to do it.

The :meth:`__init__` method, on the other hand, works exactly like in Python.
It is called after allocation and basic initialisation of the object, including
the complete inheritance chain.
By the time :meth:`__init__` is called, the object is a fully valid Python object
and all operations are safe.  Any initialisation which cannot safely be done in
the :meth:`__cinit__` method should be done in the :meth:`__init__` method.
However, as in Python, it is the responsibility of the subclasses to call up the
hierarchy and make sure that the :meth:`__init__` methods in the base class are
called correctly.  If a subclass forgets (or refuses) to call the :meth:`__init__`
method of one of its base classes, that method will not be called.
Also, if the object gets created by calling directly its :meth:`__new__` method [#]_
(as opposed to calling the class itself), then none of the :meth:`__init__`
methods will be called.

The :meth:`__cinit__` method is where you should perform basic safety C-level
initialisation of the object, possibly including allocation of any C data
structures that your object will own.  In contrast to :meth:`__init__`,
your :meth:`__cinit__` method is guaranteed to be called exactly once.

If your extension type has a base type, any existing :meth:`__cinit__` methods in
the base type hierarchy are automatically called before your :meth:`__cinit__`
method.  You cannot explicitly call the inherited :meth:`__cinit__` methods, and the
base types are free to choose whether they implement :meth:`__cinit__` at all.
If you need to pass a modified argument list to the base type, you will have to do
the relevant part of the initialisation in the :meth:`__init__` method instead,
where the normal rules for calling inherited methods apply.

Any arguments passed to the constructor will be passed to both the
:meth:`__cinit__` method and the :meth:`__init__` method.  If you anticipate
subclassing your extension type, you may find it useful to give the
:meth:`__cinit__` method ``*`` and ``**`` arguments so that it can accept and
ignore arbitrary extra arguments, since the arguments that are passed through
the hierarchy during allocation cannot be changed by subclasses.
Alternatively, as a convenience, if you declare your :meth:`__cinit__` method
to take no arguments (other than self) it will simply ignore any extra arguments
passed to the constructor without complaining about the signature mismatch.

..  Note::

    All constructor arguments will be passed as Python objects.
    This implies that non-convertible C types such as pointers or C++ objects
    cannot be passed into the constructor, neither from Python nor from Cython code.
    If this is needed, use a factory function or method instead that handles the
    object initialisation.
    It often helps to directly call the :meth:`__new__` method in this function to
    explicitly bypass the call to the :meth:`__init__` constructor.

    See :ref:`existing-pointers-instantiation` for an example.

..  Note::

    Implementing a :meth:`__cinit__` method currently excludes the type from
    :ref:`auto-pickling <auto_pickle>`.

.. [#] https://docs.python.org/reference/datamodel.html#object.__new__


.. _finalization_method:

Finalization methods: :meth:`__dealloc__` and :meth:`__del__`
-------------------------------------------------------------

The counterpart to the :meth:`__cinit__` method is the :meth:`__dealloc__`
method, which should perform the inverse of the :meth:`__cinit__` method. Any
C data that you explicitly allocated (e.g. via malloc) in your
:meth:`__cinit__` method should be freed in your :meth:`__dealloc__` method.

You need to be careful what you do in a :meth:`__dealloc__` method. By the time your
:meth:`__dealloc__` method is called, the object may already have been partially
destroyed and may not be in a valid state as far as Python is concerned, so
you should avoid invoking any Python operations which might touch the object.
In particular, don't call any other methods of the object or do anything which
might cause the object to be resurrected. It's best if you stick to just
deallocating C data.

You don't need to worry about deallocating Python attributes of your object,
because that will be done for you by Cython after your :meth:`__dealloc__` method
returns.

When subclassing extension types, be aware that the :meth:`__dealloc__` method
of the superclass will always be called, even if it is overridden.  This is in
contrast to typical Python behavior where superclass methods will not be
executed unless they are explicitly called by the subclass.

Python 3.4 made it possible for extension types to safely define
finalizers for objects. When running a Cython module on Python 3.4 and
higher you can add a :meth:`__del__` method to extension types in
order to perform Python cleanup operations. When the :meth:`__del__`
is called the object is still in a valid state (unlike in the case of
:meth:`__dealloc__`), permitting the use of Python operations
on its class members. On Python <3.4 :meth:`__del__` will not be called.

.. _arithmetic_methods:

Arithmetic methods
-------------------

Arithmetic operator methods, such as :meth:`__add__`, used to behave differently
from their Python counterparts in Cython 0.x, following the low-level semantics
of the C-API slot functions.  Since Cython 3.0, they are called in the same way
as in Python, including the separate "reversed" versions of these methods
(:meth:`__radd__`, etc.).

Previously, if the first operand could not perform the operation, the same method
of the second operand was called, with the operands in the same order.
This means that you could not rely on the first parameter of these methods being
"self" or being the right type, and you needed to test the types of both operands
before deciding what to do.

If backwards compatibility is needed, the normal operator method (``__add__``, etc.)
can still be implemented to support both variants, applying a type check to the
arguments.  The reversed method (``__radd__``, etc.) can always be implemented
with ``self`` as first argument and will be ignored by older Cython versions, whereas
Cython 3.x and later will only call the normal method with the expected argument order,
and otherwise call the reversed method instead.

Alternatively, the old Cython 0.x (or native C-API) behaviour is still available with
the directive ``c_api_binop_methods=True``.

If you can't handle the combination of types you've been given, you should return
``NotImplemented``.  This will let Python's operator implementation first try to apply
the reversed operator to the second operand, and failing that as well, report an
appropriate error to the user.

This change in behaviour also applies to the in-place arithmetic method :meth:`__ipow__`.
It does not apply to any of the other in-place methods (:meth:`__iadd__`, etc.)
which always take ``self`` as the first argument.

.. _rich_comparisons:

Rich comparisons
-----------------

There are a few ways to implement comparison methods.
Depending on the application, one way or the other may be better:

* Use the 6 Python
  `special methods <https://docs.python.org/3/reference/datamodel.html#basic-customization>`_
  :meth:`__eq__`, :meth:`__lt__`, etc.
  This is supported since Cython 0.27 and works exactly as in plain Python classes.

* Use a single special method :meth:`__richcmp__`.
  This implements all rich comparison operations in one method.
  The signature is ``def __richcmp__(self, other, int op)``.
  The integer argument ``op`` indicates which operation is to be performed
  as shown in the table below:

  +-----+-------+
  |  <  | Py_LT |
  +-----+-------+
  | ==  | Py_EQ |
  +-----+-------+
  |  >  | Py_GT |
  +-----+-------+
  | <=  | Py_LE |
  +-----+-------+
  | !=  | Py_NE |
  +-----+-------+
  | >=  | Py_GE |
  +-----+-------+

  These constants can be cimported from the ``cpython.object`` module.

* If you use the `functools.total_ordering <https://docs.python.org/3/library/functools.html#functools.total_ordering>`_
  decorator on an extension type/``cdef`` class, Cython replaces it with a low-level reimplementation
  designed specifically for extension types.  (On a normal Python classes, the ``functools`` 
  decorator continues to work as before.)  As a shortcut you can also use ``cython.total_ordering``, which
  applies the same re-implementation but also transforms the class to an extension type if it
  isn't already.

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/special_methods/total_ordering.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/special_methods/total_ordering.pyx


.. _the__next__method:

The :meth:`__next__` method
----------------------------

Extension types wishing to implement the iterator interface should define a
method called :meth:`__next__`, not next. The Python system will automatically
supply a next method which calls your :meth:`__next__`. Do *NOT* explicitly
give your type a :meth:`next` method, or bad things could happen.

.. _special_methods_table:

Special Method Table
---------------------

This table lists all of the special methods together with their parameter and
return types. In the table below, a parameter name of self is used to indicate
that the parameter has the type that the method belongs to. Other parameters
with no type specified in the table are generic Python objects.

You don't have to declare your method as taking these parameter types. If you
declare different types, conversions will be performed as necessary.

General
^^^^^^^

https://docs.python.org/3/reference/datamodel.html#special-method-names

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __cinit__             |self, ...                              |             | Basic initialisation (no direct Python equivalent)  |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __init__              |self, ...                              |             | Further initialisation                              |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __dealloc__           |self 	                                |             | Basic deallocation (no direct Python equivalent)    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __cmp__               |x, y 	                                | int         | 3-way comparison (Python 2 only)                    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __str__               |self 	                                | object      | str(self)                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __repr__              |self 	                                | object      | repr(self)                                          |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __hash__              |self 	                                | Py_hash_t   | Hash function (returns 32/64 bit integer)           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __call__              |self, ...                              | object      | self(...)                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __iter__              |self 	                                | object      | Return iterator for sequence                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getattr__           |self, name                             | object      | Get attribute                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getattribute__      |self, name                             | object      | Get attribute, unconditionally                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __setattr__           |self, name, val                        |             | Set attribute                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __delattr__           |self, name                             |             | Delete attribute                                    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Rich comparison operators
^^^^^^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#basic-customization

You can choose to either implement the standard Python special methods
like :meth:`__eq__` or the single special method :meth:`__richcmp__`.
Depending on the application, one way or the other may be better.

+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                    |
+=======================+=======================================+=============+========================================================+
| __eq__                |self, y                                | object      | self == y                                              |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __ne__                |self, y                                | object      | self != y  (falls back to ``__eq__`` if not available) |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __lt__                |self, y                                | object      | self < y                                               |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __gt__                |self, y                                | object      | self > y                                               |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __le__                |self, y                                | object      | self <= y                                              |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __ge__                |self, y                                | object      | self >= y                                              |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+
| __richcmp__           |self, y, int op                        | object      | Joined rich comparison method for all of the above     |
|                       |                                       |             | (no direct Python equivalent)                          |
+-----------------------+---------------------------------------+-------------+--------------------------------------------------------+

Arithmetic operators
^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types

+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| Name 	                      | Parameters         | Return type | Description                                         |
+=============================+====================+=============+=====================================================+
| __add__, __radd__           | self, other        | object      | binary `+` operator                                 |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __sub__, __rsub__           | self, other        | object      | binary `-` operator                                 |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __mul__, __rmul__           | self, other        | object      | `*` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __div__, __rdiv__           | self, other        | object      | `/`  operator for old-style division                |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __floordiv__, __rfloordiv__ | self, other        | object      | `//`  operator                                      |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __truediv__, __rtruediv__   | self, other        | object      | `/`  operator for new-style division                |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __mod__, __rmod__           | self, other        | object      | `%` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __divmod__, __rdivmod__     | self, other        | object      | combined div and mod                                |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __pow__, __rpow__           | self, other, [mod] | object      | `**` operator or pow(x, y, [mod])                   |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __neg__                     | self               | object      | unary `-` operator                                  |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __pos__                     | self               | object      | unary `+` operator                                  |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __abs__                     | self               | object      | absolute value                                      |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __nonzero__ 	              | self               | int         | convert to boolean                                  |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __invert__ 	              | self               | object      | `~` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __lshift__, __rlshift__     | self, other        | object      | `<<` operator                                       |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __rshift__, __rrshift__     | self, other        | object      | `>>` operator                                       |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __and__, __rand__           | self, other        | object      | `&` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __or__, __ror__             | self, other        | object      | `|` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+
| __xor__, __rxor__           | self, other        | object      | `^` operator                                        |
+-----------------------------+--------------------+-------------+-----------------------------------------------------+

Note that Cython 0.x did not make use of the ``__r...__`` variants and instead
used the bidirectional C slot signature for the regular methods, thus making the
first argument ambiguous (not 'self' typed).
Since Cython 3.0, the operator calls are passed to the respective special methods.
See the section on :ref:`Arithmetic methods <arithmetic_methods>` above.
Cython 0.x also did not support the 2 argument version of ``__pow__`` and 
``__rpow__``, or the 3 argument version of ``__ipow__``.

Numeric conversions
^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __int__ 	        | self 	                                | object      | Convert to integer                                  |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __long__ 	        | self 	                                | object      | Convert to long integer                             |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __float__ 	        | self 	                                | object      | Convert to float                                    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __oct__ 	        | self 	                                | object      | Convert to octal                                    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __hex__ 	        | self 	                                | object      | Convert to hexadecimal                              |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __index__            	| self	                                | object      | Convert to sequence index                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

In-place arithmetic operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __iadd__ 	        | self, x 	                        | object      | `+=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __isub__ 	        | self, x 	                        | object      | `-=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __imul__ 	        | self, x 	                        | object      | `*=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __idiv__ 	        | self, x 	                        | object      | `/=` operator for old-style division                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __ifloordiv__         | self, x 	                        | object      | `//=` operator                                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __itruediv__ 	        | self, x 	                        | object      | `/=` operator for new-style division                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __imod__ 	        | self, x 	                        | object      | `%=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __ipow__ 	        | self, y, [z]                          | object      | `**=` operator (3-arg form only on Python >= 3.8)   |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __ilshift__ 	        | self, x 	                        | object      | `<<=` operator                                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __irshift__ 	        | self, x 	                        | object      | `>>=` operator                                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __iand__ 	        | self, x 	                        | object      | `&=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __ior__ 	        | self, x 	                        | object      | `|=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __ixor__ 	        | self, x 	                        | object      | `^=` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Sequences and mappings
^^^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-container-types

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __len__               | self                                  | Py_ssize_t  | len(self)                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getitem__ 	        | self, x 	                        | object      | self[x]                                             |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __setitem__ 	        | self, x, y 	  	                |             | self[x] = y                                         |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __delitem__ 	        | self, x 	  	                |             | del self[x]                                         |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getslice__ 	        | self, Py_ssize_t i, Py_ssize_t j 	| object      | self[i:j]                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __setslice__ 	        | self, Py_ssize_t i, Py_ssize_t j, x 	|  	      | self[i:j] = x                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __delslice__ 	        | self, Py_ssize_t i, Py_ssize_t j 	|  	      | del self[i:j]                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __contains__ 	        | self, x 	                        | int 	      | x in self                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Iterators
^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-container-types

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __next__ 	        | self 	                                | object      |	Get next item (called next in Python)               |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Buffer interface [:PEP:`3118`] (no Python equivalents - see note 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name                  | Parameters                            | Return type |         Description                                 |
+=======================+=======================================+=============+=====================================================+
| __getbuffer__         | self, Py_buffer `*view`, int flags    |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __releasebuffer__     | self, Py_buffer `*view`               |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Customizing class creation
^^^^^^^^^^^^^^^^^^^^^^^^^^
https://docs.python.org/3/reference/datamodel.html#customizing-class-creation

+-----------------------+---------------------------------------+-------------+----------------------------------------------------------------------+
| Name                  | Parameters                            | Return type |         Description                                                  |
+=======================+=======================================+=============+======================================================================+
| __set_name__          | self, owner, name                     |             |  Automatically called at the time the owning class owner is created. |
+-----------------------+---------------------------------------+-------------+----------------------------------------------------------------------+

Descriptor objects (see note 2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#implementing-descriptors

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __get__ 	        | self, instance, class 	        | object      | 	Get value of attribute                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __set__ 	        | self, instance, value 	        |  	      |     Set value of attribute                          |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __delete__ 	        | self, instance 	  	        |             |     Delete attribute                                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

.. note:: (1) The buffer interface was intended for use by C code and is not directly
        accessible from Python.  For a how-to guide to the new API, see :ref:`buffer`.
        The old Python 2 buffer protocol (```__getreadbuffer__``, ``__getwritebuffer__``,
        ``__getsegcount__``, ``__getcharbuffer__``) is no longer supported from Cython 3.1
        since Python 2 is no longer supported.

.. note:: (2) Descriptor objects are part of the support mechanism for new-style
        Python classes. See the discussion of descriptors in the Python documentation.
        See also :PEP:`252`, "Making Types Look More Like Classes", and :PEP:`253`,
        "Subtyping Built-In Types".
