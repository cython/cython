***********************************
Extension types (aka. cdef classes)
***********************************

.. include::
    ../two-syntax-variants-used

To support object-oriented programming, Cython supports writing normal
Python classes exactly as in Python:

.. literalinclude:: ../../examples/tutorial/cdef_classes/math_function.py

Based on what Python calls a "built-in type", however, Cython supports
a second kind of class: *extension types*, sometimes referred to as
"cdef classes" due to the Cython language keywords used for their declaration.
They are somewhat restricted compared to Python classes, but are generally
more memory efficient and faster than generic Python classes.  The
main difference is that they use a C struct to store their fields and methods
instead of a Python dict.  This allows them to store arbitrary C types
in their fields without requiring a Python wrapper for them, and to
access fields and methods directly at the C level without passing
through a Python dictionary lookup.

Normal Python classes can inherit from cdef classes, but not the other
way around.  Cython requires to know the complete inheritance
hierarchy in order to lay out their C structs, and restricts it to
single inheritance.  Normal Python classes, on the other hand, can
inherit from any number of Python classes and extension types, both in
Cython code and pure Python code.

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cdef_classes/math_function_2.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cdef_classes/math_function_2.pyx

The ``cpdef`` command (or ``@cython.ccall`` in Python syntax) makes two versions
of the method available; one fast for use from Cython and one slower for use
from Python.

Now we can add subclasses of the ``Function`` class that implement different
math functions in the same ``evaluate()`` method.

Then:

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cdef_classes/sin_of_square.py
            :caption: sin_of_square.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cdef_classes/sin_of_square.pyx
            :caption: sin_of_square.pyx

This does slightly more than providing a python wrapper for a cdef
method: unlike a cdef method, a cpdef method is fully overridable by
methods and instance attributes in Python subclasses.  This adds a
little calling overhead compared to a cdef method.

To make the class definitions visible to other modules, and thus allow for
efficient C-level usage and inheritance outside of the module that
implements them, we define them in a ``.pxd`` file with the same name
as the module.  Note that we are using Cython syntax here, not Python syntax.

.. literalinclude:: ../../examples/tutorial/cdef_classes/sin_of_square.pxd
    :caption: sin_of_square.pxd

With this way to implement different functions as subclasses with fast,
Cython callable methods, we can now pass these ``Function`` objects into
an algorithm for numeric integration, that evaluates an arbitrary user
provided function over a value interval.

Using this, we can now change our integration example:

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cdef_classes/integrate.py
            :caption: integrate.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cdef_classes/integrate.pyx
            :caption: integrate.pyx

We can even pass in a new ``Function`` defined in Python space, which overrides
the Cython implemented method of the base class::

  >>> import integrate
  >>> class MyPolynomial(integrate.Function):
  ...     def evaluate(self, x):
  ...         return 2*x*x + 3*x - 10
  ...
  >>> integrate(MyPolynomial(), 0, 1, 10000)
  -7.8335833300000077

Since ``evaluate()`` is a Python method here, which requires Python objects
as input and output, this is several times slower than the straight C call
to the Cython method, but still faster than a plain Python variant.
This shows how large the speed-ups can easily be when whole computational
loops are moved from Python code into a Cython module.

Some notes on our new implementation of ``evaluate``:

-   The fast method dispatch here only works because ``evaluate`` was
    declared in ``Function``. Had ``evaluate`` been introduced in
    ``SinOfSquareFunction``, the code would still work, but Cython
    would have used the slower Python method dispatch mechanism
    instead.

-   In the same way, had the argument ``f`` not been typed, but only
    been passed as a Python object, the slower Python dispatch would
    be used.

-   Since the argument is typed, we need to check whether it is
    ``None``. In Python, this would have resulted in an ``AttributeError``
    when the ``evaluate`` method was looked up, but Cython would instead
    try to access the (incompatible) internal structure of ``None`` as if
    it were a ``Function``, leading to a crash or data corruption.

There is a *compiler directive* ``nonecheck`` which turns on checks
for this, at the cost of decreased speed. Here's how compiler directives
are used to dynamically switch on or off ``nonecheck``:

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cdef_classes/nonecheck.py
            :caption: nonecheck.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cdef_classes/nonecheck.pyx
            :caption: nonecheck.pyx

Attributes in cdef classes behave differently from attributes in regular classes:

-   All attributes must be pre-declared at compile-time
-   Attributes are by default only accessible from Cython (typed access)
-   Properties can be declared to expose dynamic attributes to Python-space

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cdef_classes/wave_function.py
            :caption: wave_function.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cdef_classes/wave_function.pyx
            :caption: wave_function.pyx
