Pure Python Mode
================

Cython provides language constructs to let the same file be either interpreted
or compiled. This is accomplished by the same "magic" module ``cython`` that
directives use and which must be imported. This is available for both :file:`.py` and
:file:`.pyx` files.

This is accomplished via special functions and decorators and an (optional)
augmenting :file:`.pxd` file.

Magic Attributes
----------------

The currently supported attributes of the ``cython`` module are:

* ``declare`` declares a typed variable in the current scope, which can be used in
  place of the :samp:`cdef type var [= value]` construct. This has two forms, the
  first as an assignment (useful as it creates a declaration in
  interpreted mode as well)::

    x = cython.declare(cython.int)             # cdef int x
    y = cython.declare(cython.double, 0.57721) # cdef double y = 0.57721

  and the second mode as a simple function call::

    cython.declare(x=cython.int, y=cython.double) # cdef int x; cdef double y

* ``locals`` is a decorator that is used to specify the types of local variables
  in the function body (including any or all of the argument types)::

    @cython.locals(a=cython.double, b=cython.double, n=cython.p_double)
    def foo(a, b, x, y):
        ...

* ``address`` is used in place of the ``&`` operator::

    cython.declare(x=cython.int, x_ptr=cython.p_int)
    x_ptr = cython.address(x)

* ``sizeof`` emulates the `sizeof` operator. It can take both types and
  expressions.::

    cython.declare(n=cython.longlong)
    print cython.sizeof(cython.longlong), cython.sizeof(n)

* ``struct`` can be used to create struct types.::

    MyStruct = cython.struct(x=cython.int, y=cython.int, data=cython.double)
    a = cython.declare(MyStruct)

  is equivalent to the code::

    cdef struct MyStruct:
        int x
        int y
        double data

    cdef MyStruct a

* ``union`` creates union types with exactly the same syntax as ``struct``

* ``typedef`` creates a new type::

    T = cython.typedef(cython.p_int)   # ctypedef int* T

* ``compiled`` is a special variable which is set to ``True`` when the compiler
  runs, and ``False`` in the interpreter. Thus the code::

    if cython.compiled:
        print "Yep, I'm compiled."
    else:
        print "Just a lowly interpreted script."

  will behave differently depending on whether or not the code is loaded as a
  compiled :file:`.so` file or a plain :file:`.py` file.

Augmenting .pxd
---------------

If a :file:`.pxd` file is found with the same name as a :file:`.py` file, it will be
searched for :keyword:`cdef` classes and :keyword:`cdef`/:keyword:`cpdef`
functions and methods. It will then convert the corresponding
classes/functions/methods in the :file:`.py` file to be of the correct type. Thus if
one had :file:`a.pxd`::

    cdef class A:
        cpdef foo(self, int i)

the file :file:`a.py`::

    class A:
        def foo(self, i):
            print "Big" if i > 1000 else "Small"

would be interpreted as::

    cdef class A:
        cpdef foo(self, int i):
            print "Big" if i > 1000 else "Small"

The special cython module can also be imported and used within the augmenting
:file:`.pxd` file. This makes it possible to add types to a pure python file without
changing the file itself. For example, the following python file
:file:`dostuff.py`::

    def dostuff(n):
        t = 0
        for i in range(n):
            t += i
        return t

could be augmented with the following :file:`.pxd` file :file:`dostuff.pxd`::

    import cython

    @cython.locals(t = cython.int, i = cython.int)
    cpdef int dostuff(int n)

Besides the ``cython.locals`` decorator, the :func:`cython.declare` function can also be
used to add types to global variables in the augmenting :file:`.pxd` file.

Note that normal Python (:keyword:`def`) functions cannot be declared in
:file:`.pxd` files, so it is currently impossible to override the types of
Python functions in :file:`.pxd` files if they use ``*args`` or ``**kwargs`` in their
signature, for instance.

Types
-----

There are numerous types built in to the cython module. One has all the
standard C types, namely ``char``, ``short``, ``int``, ``long``, ``longlong``
as well as their unsigned versions ``uchar``, ``ushort``, ``uint``, ``ulong``,
``ulonglong``. One also has ``bint`` and ``Py_ssize_t``. For each type, one
has pointer types ``p_int``, ``pp_int``, . . ., up to three levels deep in
interpreted mode, and infinitely deep in compiled mode.  The Python types int,
long and bool are interpreted as C ``int``, ``long`` and ``bint``
respectively. Also, the python types ``list``, ``dict``, ``tuple``, . . . may
be used, as well as any user defined types.

Pointer types may be constructed with ``cython.pointer(cython.int)``, and
arrays as ``cython.int[10]``. A limited attempt is made to emulate these more
complex types, but only so much can be done from the Python language.

Decorators
--------------------------------

Use the ``@cython.cclass`` decorator to create a ``cdef class``.
Use the ``@cython.cfunc`` and ``@cython.ccall`` decorators for :keyword:`cdef`
and :keyword:`cpdef` functions (respectively).

