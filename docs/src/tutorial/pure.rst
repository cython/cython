
.. _pure-mode:

Pure Python Mode
================

Sometimes one may want to speed up Python code without losing the possibility to run
it with the Python interpreter. While pure Python scripts can be compiled with Cython,
it usually results in a 20%-50% speed gain only.

To go beyond that, Cython provides language constructs to add static typing
and cythonic functionalities to a Python module to make it run much faster
when compiled, while still allowing it to be interpreted.

This is accomplished either via an augmenting :file:`.pxd` file, or
via special functions and decorators available after importing ``cython``.


Augmenting .pxd
---------------

Using an augmenting :file:`.pxd` allows to let the original :file:`.py` file
completely untouched. On the other hand, one needs to maintain both
the :file:`.pxd` and the :file:`.py` in parallel.

Note that this usage of the :file:`.pxd` is different of that when it is
accompanying a :file:`.pyx` file (see :doc:`pxd_files`).

If a :file:`.pxd` file is found with the same name as a :file:`.py` file,
it will be searched for :keyword:`cdef` classes and :keyword:`cdef`/:keyword:`cpdef`
functions and methods. It will then convert the corresponding
classes/functions/methods in the :file:`.py` file to be of the correct type.
Thus if one has a file :file:`A.py`::

    def myfunction(x, y=2):
        a = x-y
        return a+(x*y)

    class A:
        def __init__(self, b=0):
            self.a = 3
            self.b = b
        def foo(self, x):
            print x + 1.0

and adds :file:`A.pxd`::

    cpdef inline int myfunction(int x,int y):
        cdef int a

    cdef class A:
        cdef public int a,b
        cpdef foo(self, double x)

then at compilation time :file:`A.py` would be interpreted as::

    cdef int myfunction(int x,int y):
        cdef int a
        a = x-y
        return a+(x*y)

    cdef class A:
        cdef int a,b
        def __init__(self, int b=0):
            self.a = 3
            self.b = b
        cdef foo(self, double x):
            print x + 1.0

while still letting the possibility of running the Python interpreter
as before with `python A.py`.

Note that in order to provide the Python wrappers to the :keyword:`cdef`
definitions in the :file:`.pxd`,

* functions are declared as `cpdef inline`;
* classes are declared as `cdef class`;
* class attributes are declared as `cdef public`;
* class methods are declared as `cpdef`.

Normal Python (:keyword:`def`) functions cannot be declared in
:file:`.pxd` files, so it is currently impossible to override the types of
Python functions in :file:`.pxd` files if they use ``*args`` or ``**kwargs``
in their signature, for instance.


Magic Attributes
----------------

Special decorators are available using the ``cython`` module that can
be used to add static typing within the Python file, while being ignored
by the interpreter.

Their use is more limited than :file:`.pxd` extensions or usual Cython code,
and add the ``cython`` dependency to the original code. However they can
come in handy and do not require to maintain a supplementary file.

"Compiled" switch
^^^^^^^^^^^^^^^^^

* ``compiled`` is a special variable which is set to ``True`` when the compiler
  runs, and ``False`` in the interpreter. Thus the code::

    if cython.compiled:
        print "Yep, I'm compiled."
    else:
        print "Just a lowly interpreted script."

  will behave differently depending on whether or not the code is loaded as a
  compiled :file:`.so` file or a plain :file:`.py` file.

Static typing
^^^^^^^^^^^^^

* ``cython.declare`` declares a typed variable in the current scope, which can be used in
  place of the :samp:`cdef type var [= value]` construct. This has two forms, the
  first as an assignment (useful as it creates a declaration in
  interpreted mode as well)::

    x = cython.declare(cython.int)             # cdef int x
    y = cython.declare(cython.double, 0.57721) # cdef double y = 0.57721

  and the second mode as a simple function call::

    cython.declare(x=cython.int, y=cython.double) # cdef int x; cdef double y

* ``@cython.locals`` is a decorator that is used to specify the types of local variables
  in the function body (including any or all of the argument types)::

    @cython.locals(a=cython.double, b=cython.double, n=cython.p_double)
    def foo(a, b, x, y):
        ...

  It cannot be used to type class constructor attributes.

* ``@cython.returns(<type>)`` specifies the function's return type.

* Starting with Cython 0.21, Python signature annotations can be used to
  declare argument types.  Cython recognises three ways to do this, as
  shown in the following example::

    def func(plain_python_type: dict,
             named_python_type: 'dict',
             explicit_python_type: {'type': dict},
             explicit_c_type: {'ctype': 'int'}):
        ...

Extension types and cdef functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``@cython.cclass`` creates a ``cdef class``.
* ``@cython.cfunc`` creates a :keyword:`cdef` function.
* ``@cython.ccall`` creates a :keyword:`cpdef` function.
* ``@cython.locals`` declares the argument types (see above).
* ``@cython.inline`` is the equivalent of the C ``inline`` modifier.

Here is an example of a :keyword:`cdef` function::

    @cython.cfunc
    @cython.returns(cython.bint)
    @cython.locals(a=cython.int, b=cython.int)
    def c_compare(a,b):
        return a == b

Others attributes
^^^^^^^^^^^^^^^^^

* ``address`` is used in place of the ``&`` operator::

    cython.declare(x=cython.int, x_ptr=cython.p_int)
    x_ptr = cython.address(x)

* ``sizeof`` emulates the `sizeof` operator. It can take both types and
  expressions.::

    cython.declare(n=cython.longlong)
    print cython.sizeof(cython.longlong)
    print cython.sizeof(n)

* ``struct`` can be used to create struct types.::

    MyStruct = cython.struct(x=cython.int, y=cython.int, data=cython.double)
    a = cython.declare(MyStruct)

  is equivalent to the code::

    cdef struct MyStruct:
        int x
        int y
        double data

    cdef MyStruct a

* ``union`` creates union types with exactly the same syntax as ``struct``.

* ``typedef`` creates a new type::

    T = cython.typedef(cython.p_int)   # ctypedef int* T


Magic Attributes within the .pxd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The special Cython module can also be imported and used within the augmenting
:file:`.pxd` file. For example, the following Python file :file:`dostuff.py`::

    def dostuff(n):
        t = 0
        for i in range(n):
            t += i
        return t

could be augmented with the following :file:`.pxd` file :file:`dostuff.pxd`::

    import cython

    @cython.locals(t = cython.int, i = cython.int)
    cpdef int dostuff(int n)

which is equivalent to::

    cpdef int dostuff(int n):
        cdef int t,i

Besides the ``cython.locals`` decorator, the :func:`cython.declare` function can also be
used to add types to global variables in the augmenting :file:`.pxd` file.

