.. _special-methods:

Special Methods of Extension Types
===================================

This page describes the special methods currently supported by Cython extension
types. A complete list of all the special methods appears in the table at the
bottom. Some of these methods behave differently from their Python
counterparts or have no direct Python counterparts, and require special
mention.

.. Note::

    Everything said on this page applies only to extension types, defined
    with the :keyword:`cdef class` statement. It doesn't apply to classes defined with the
    Python :keyword:`class` statement, where the normal Python rules apply.

.. _declaration:

Declaration
------------
Special methods of extension types must be declared with :keyword:`def`, not
:keyword:`cdef`. This does not impact their performance--Python uses different
calling conventions to invoke these special methods.

.. _docstrings:

Docstrings
-----------

Currently, docstrings are not fully supported in some special methods of extension
types. You can place a docstring in the source to serve as a comment, but it
won't show up in the corresponding :attr:`__doc__` attribute at run time. (This
seems to be is a Python limitation -- there's nowhere in the `PyTypeObject`
data structure to put such docstrings.)

.. _initialisation_methods:

Initialisation methods: :meth:`__cinit__` and :meth:`__init__`
---------------------------------------------------------------
There are two methods concerned with initialising the object.

The :meth:`__cinit__` method is where you should perform basic C-level
initialisation of the object, including allocation of any C data structures
that your object will own. You need to be careful what you do in the
:meth:`__cinit__` method, because the object may not yet be fully valid Python
object when it is called. Therefore, you should be careful invoking any Python
operations which might touch the object; in particular, its methods.

By the time your :meth:`__cinit__` method is called, memory has been allocated for the
object and any C attributes it has have been initialised to 0 or null. (Any
Python attributes have also been initialised to None, but you probably
shouldn't rely on that.) Your :meth:`__cinit__` method is guaranteed to be called
exactly once.

If your extension type has a base type, the :meth:`__cinit__` method of the base type
is automatically called before your :meth:`__cinit__` method is called; you cannot
explicitly call the inherited :meth:`__cinit__` method. If you need to pass a modified
argument list to the base type, you will have to do the relevant part of the
initialisation in the :meth:`__init__` method instead (where the normal rules for
calling inherited methods apply).

Any initialisation which cannot safely be done in the :meth:`__cinit__` method should
be done in the :meth:`__init__` method. By the time :meth:`__init__` is called, the object is
a fully valid Python object and all operations are safe. Under some
circumstances it is possible for :meth:`__init__` to be called more than once or not
to be called at all, so your other methods should be designed to be robust in
such situations.

Any arguments passed to the constructor will be passed to both the
:meth:`__cinit__` method and the :meth:`__init__` method. If you anticipate
subclassing your extension type in Python, you may find it useful to give the
:meth:`__cinit__` method `*` and `**` arguments so that it can accept and
ignore extra arguments. Otherwise, any Python subclass which has an
:meth:`__init__` with a different signature will have to override
:meth:`__new__` [#]_ as well as :meth:`__init__`, which the writer of a Python
class wouldn't expect to have to do.  Alternatively, as a convenience, if you declare
your :meth:`__cinit__`` method to take no arguments (other than self) it
will simply ignore any extra arguments passed to the constructor without
complaining about the signature mismatch.

..  Note::

    All constructor arguments will be passed as Python objects.
    This implies that non-convertible C types such as pointers or C++ objects
    cannot be passed into the constructor from Cython code.  If this is needed,
    use a factory function instead that handles the object initialisation.
    It often helps to directly call ``__new__()`` in this function to bypass the
    call to the ``__init__()`` constructor.

    See :ref:`existing-pointers-instantiation` for an example.

.. [#] https://docs.python.org/reference/datamodel.html#object.__new__

.. _finalization_method:

Finalization method: :meth:`__dealloc__`
----------------------------------------

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

.. Note:: There is no :meth:`__del__` method for extension types.

.. _arithmetic_methods:

Arithmetic methods
-------------------

Arithmetic operator methods, such as :meth:`__add__`, behave differently from their
Python counterparts. There are no separate "reversed" versions of these
methods (:meth:`__radd__`, etc.) Instead, if the first operand cannot perform the
operation, the same method of the second operand is called, with the operands
in the same order.

This means that you can't rely on the first parameter of these methods being
"self" or being the right type, and you should test the types of both operands
before deciding what to do. If you can't handle the combination of types you've
been given, you should return `NotImplemented`.

This also applies to the in-place arithmetic method :meth:`__ipow__`. It doesn't apply
to any of the other in-place methods (:meth:`__iadd__`, etc.) which always
take `self` as the first argument.

.. _righ_comparisons:

Rich comparisons
-----------------

There are two ways to implement comparison methods.
Depending on the application, one way or the other may be better:

* The first way uses the 6 Python
  `special methods <https://docs.python.org/3/reference/datamodel.html#basic-customization>`_
  :meth:`__eq__`, :meth:`__lt__`, etc.
  This is new since Cython 0.27 and works exactly as in plain Python classes.
* The second way uses a single special method :meth:`__richcmp__`.
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
| __cmp__               |x, y 	                                | int         | 3-way comparison                                    |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __str__               |self 	                                | object      | str(self)                                           |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __repr__              |self 	                                | object      | repr(self)                                          |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __hash__              |self 	                                | int         | Hash function                                       |
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

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name 	                | Parameters                            | Return type | 	Description                                 |
+=======================+=======================================+=============+=====================================================+
| __add__               | x, y 	                                | object      | binary `+` operator                                 |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __sub__ 	        | x, y 	                                | object      | binary `-` operator                                 |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __mul__ 	        | x, y 	                                | object      | `*` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __div__ 	        | x, y 	                                | object      | `/`  operator for old-style division                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __floordiv__ 	        | x, y 	                                | object      | `//`  operator                                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __truediv__ 	        | x, y 	                                | object      | `/`  operator for new-style division                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __mod__ 	        | x, y 	                                | object      | `%` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __divmod__ 	        | x, y 	                                | object      | combined div and mod                                |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __pow__ 	        | x, y, z 	                        | object      | `**` operator or pow(x, y, z)                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __neg__ 	        | self 	                                | object      | unary `-` operator                                  |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __pos__ 	        | self 	                                | object      | unary `+` operator                                  |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __abs__ 	        | self 	                                | object      | absolute value                                      |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __nonzero__ 	        | self 	                                | int 	      | convert to boolean                                  |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __invert__ 	        | self 	                                | object      | `~` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __lshift__ 	        | x, y 	                                | object      | `<<` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __rshift__ 	        | x, y 	                                | object      | `>>` operator                                       |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __and__ 	        | x, y 	                                | object      | `&` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __or__ 	        | x, y 	                                | object      | `|` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __xor__ 	        | x, y 	                                | object      | `^` operator                                        |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

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
| __index__ (2.5+ only)	| self	                                | object      | Convert to sequence index                           |
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
| __ipow__ 	        | x, y, z 	                        | object      | `**=` operator                                      |
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
| __len__ 	        | self 	int 	                        |             | len(self)                                           |
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

Buffer interface [legacy] (no Python equivalents - see note 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| Name                  | Parameters                            | Return type |         Description                                 |
+=======================+=======================================+=============+=====================================================+
| __getreadbuffer__     | self, Py_ssize_t i, void `**p`        |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getwritebuffer__    | self, Py_ssize_t i, void `**p`        |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getsegcount__       | self, Py_ssize_t `*p`                 |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+
| __getcharbuffer__     | self, Py_ssize_t i, char `**p`        |             |                                                     |
+-----------------------+---------------------------------------+-------------+-----------------------------------------------------+

Descriptor objects (see note 2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://docs.python.org/3/reference/datamodel.html#emulating-container-types

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
        accessible from Python. It is described in the Python/C API Reference Manual
        of Python 2.x under sections 6.6 and 10.6. It was superseded by the new
        :PEP:`3118` buffer protocol in Python 2.6 and is no longer available in Python 3.
        For a how-to guide to the new API, see :ref:`buffer`.

.. note:: (2) Descriptor objects are part of the support mechanism for new-style
        Python classes. See the discussion of descriptors in the Python documentation.
        See also :PEP:`252`, "Making Types Look More Like Classes", and :PEP:`253`,
        "Subtyping Built-In Types".
