.. highlight:: cython

************************
Performance Optimization
************************



.. include::
    ../two-syntax-variants-used


.. _early-binding-for-speed:

Early Binding for Speed
=======================

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

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle.pyx

In the :func:`rectArea` method, the call to :meth:`rect.area` and the
:meth:`.area` method contain a lot of Python overhead.

However, in Cython, it is possible to eliminate a lot of this overhead in cases
where calls occur within Cython code. For example:

.. tabs::

    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle_cdef.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle_cdef.pyx

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

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle_cpdef.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/userguide/performance_optimization/rectangle_cpdef.pyx

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

.. _branch_hints:

Branch Hints
============

.. currentmodule:: cython

Cython provides compiler hints to help guide the C compiler's branch prediction optimization.
These hints use GCC and Clang's ``__builtin_expect()`` intrinsic to mark branches as likely
or unlikely to execute.

.. versionadded:: 3.3.0

Overview
--------

Branch hints tell the compiler which path of a conditional branch is more commonly taken.
This information helps the compiler and CPU generate better machine code:

- ``cython.likely()`` - Marks a condition as expected to be true
- ``cython.unlikely()`` - Marks a condition as expected to be false

The compiler uses these hints to optimize instruction layout and branch prediction, potentially
improving cache hit rates and reducing pipeline flushes.

.. warning::

   Branch hints are for **rare and very clear use cases**, not for guessing. Only use them when:

   - You have concrete profiling data showing the actual branch frequency
   - You have domain knowledge that makes the prediction obvious

   Incorrect hints can make code slower, not faster. The compiler's own heuristics (e.g.
   `PGO <https://en.wikipedia.org/wiki/Profile-guided_optimization>`_) are often
   better than manual guessing.


Basic Usage
-----------

If Statements
^^^^^^^^^^^^^

Use ``cython.likely()`` to mark the condition that is expected to be true:

.. code-block:: python

    if cython.likely(x > threshold):
        # This branch is expected to execute frequently
        process_common_case(x)
    else:
        process_rare_case(x)

Use ``cython.unlikely()`` to mark the condition that is expected to be false:

.. code-block:: python

    if cython.unlikely(error_flag):
        # This branch is expected to execute rarely
        raise RuntimeError("Unexpected error")

    # Normal processing continues here


Conditional Expressions (Ternary)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Branch hints also work with conditional expressions:

.. code-block:: python

    # Likely case
    result = value if cython.likely(condition) else default

    # Unlikely case
    result = value if cython.unlikely(error_condition) else default


Comprehensions
^^^^^^^^^^^^^^

You can use branch hints within list, set, and dict comprehensions:

.. code-block:: python

    # Skip rare cases
    [x for x in data if cython.likely(x > 0)]

    # Keep only error items (rare)
    errors = [item for item in results if cython.unlikely(item.has_error())]


Automatic Branch Hints
----------------------

Cython automatically injects branch hints into exception-handling code, so you typically
don't need to annotate these patterns manually.

**Exception-Raising Branches**

When a branch contains only a ``raise`` statement, it is automatically marked as ``unlikely()``:

.. code-block:: cython

    if x > threshold:
        # Branch is automatically marked as unlikely()
        raise ValueError("Threshold exceeded")

This makes sense because exceptions represent error conditions that should occur rarely
during normal execution.

**Error Branches in If-Else**

When the ``else`` branch contains only a ``raise`` statement, the ``if`` branch is
automatically marked as ``likely()``:

.. code-block:: cython

    if x < threshold:
        # This branch is automatically marked as likely()
        process_normally()
    else:
        raise ValueError("Invalid value")

.. important::

   Cython only injects automatic branch hints if a branch contains **solely** a ``raise``
   statement. If the branch contains any other statements in addition to the raise,
   automatic hints are not applied
