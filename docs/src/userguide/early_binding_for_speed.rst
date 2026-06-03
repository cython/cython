.. highlight:: cython

.. _early-binding-for-speed:

**************************
Early Binding for Speed
**************************

.. include::
    ../two-syntax-variants-used

As a dynamic language, Python encourages a programming style of considering
classes and objects in terms of their methods and attributes, more than where
they fit into the class hierarchy.

This can make Python a very relaxed and comfortable language for rapid
development, but with a price - the 'red tape' of managing data types is
dumped onto the interpreter. At run time, the interpreter does a lot of work
searching namespaces, fetching attributes and parsing argument and keyword
tuples. This run-time 'late binding' is a major cause of Python's relative
slowness compared to 'early binding' languages such as C++.

However with Cython it is possible to gain significant speed-ups through the
use of 'early binding' programming techniques.

For example, consider the following (silly) code example:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle.pyx

In the :func:`rectArea` method, the call to :meth:`rect.area` and the
:meth:`.area` method contain a lot of Python overhead.

However, in Cython, it is possible to eliminate a lot of this overhead in cases
where calls occur within Cython code. For example:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle_cdef.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle_cdef.pyx

Here, in the Rectangle extension class, we have defined two different area
calculation methods, the efficient :meth:`_area` C method, and the
Python-callable :meth:`area` method which serves as a thin wrapper around
:meth:`_area`. Note also in the function :func:`rectArea` how we 'early bind'
by declaring the local variable ``rect`` which is explicitly given the type
Rectangle. By using this declaration, instead of just dynamically assigning to
``rect``, we gain the ability to access the much more efficient C-callable
:meth:`_area` method.

But Cython offers us more simplicity again, by allowing us to declare
dual-access methods - methods that can be efficiently called at C level, but
can also be accessed from pure Python code at the cost of the Python access
overheads. Consider this code:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle_cpdef.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/early_binding_for_speed/rectangle_cpdef.pyx

Here, we just have a single area method, declared as :keyword:`cpdef` or with ``@ccall`` decorator
to make it efficiently callable as a C function, but still accessible from pure Python
(or late-binding Cython) code.

If within Cython code, we have a variable already 'early-bound' (ie, declared
explicitly as type Rectangle, (or cast to type Rectangle), then invoking its
area method will use the efficient C code path and skip the Python overhead.
But if in Cython or regular Python code we have a regular object variable
storing a Rectangle object, then invoking the area method will require:

* an attribute lookup for the area method
* packing a tuple for arguments and a dict for keywords (both empty in this case)
* using the Python API to call the method

and within the area method itself:

* parsing the tuple and keywords
* executing the calculation code
* converting the result to a python object and returning it

So within Cython, it is possible to achieve massive optimisations by
using strong typing in declaration and casting of variables. For tight loops
which use method calls, and where these methods are pure C, the difference can
be huge.

