.. highlight:: cython

.. _wrapping-cplusplus:

********************************
Using C++ in Cython
********************************

Overview
=========

Cython has native support for most of the C++ language.  Specifically:

* C++ objects can now be dynamically allocated with ``new`` and ``del`` keywords.
* C++ objects can be stack-allocated.
* C++ classes can be declared with the new keyword ``cppclass``.
* Templated classes and functions are supported.
* Overloaded functions are supported.
* Overloading of C++ operators (such as operator+, operator[],...) is supported.

Procedure Overview
-------------------
The general procedure for wrapping a C++ file can now be described as follows:

* Specify C++ language in :file:`setup.py` script or locally in a source file.
* Create one or more .pxd files with ``cdef extern from`` blocks and
  (if existing) the C++ namespace name.  In these blocks,

  * declare classes as ``cdef cppclass`` blocks
  * declare public names (variables, methods and constructors)

* Write an extension modules, ``cimport`` from the .pxd file and use
  the declarations.

A simple Tutorial
==================

An example C++ API
-------------------

Here is a tiny C++ API which we will use as an example throughout this
document. Let's assume it will be in a header file called
:file:`Rectangle.h`:

.. sourcecode:: c++

    namespace shapes {
        class Rectangle {
        public:
            int x0, y0, x1, y1;
            Rectangle();
            Rectangle(int x0, int y0, int x1, int y1);
            ~Rectangle();
            int getArea();
            void getSize(int* width, int* height);
            void move(int dx, int dy);
        };
    }

and the implementation in the file called :file:`Rectangle.cpp`:

.. sourcecode:: c++

    #include "Rectangle.h"

    namespace shapes {

      Rectangle::Rectangle() { }

        Rectangle::Rectangle(int X0, int Y0, int X1, int Y1) {
            x0 = X0;
            y0 = Y0;
            x1 = X1;
            y1 = Y1;
        }

        Rectangle::~Rectangle() { }

        int Rectangle::getArea() {
            return (x1 - x0) * (y1 - y0);
        }

        void Rectangle::getSize(int *width, int *height) {
            (*width) = x1 - x0;
            (*height) = y1 - y0;
        }

        void Rectangle::move(int dx, int dy) {
            x0 += dx;
            y0 += dy;
            x1 += dx;
            y1 += dy;
        }

    }

This is pretty dumb, but should suffice to demonstrate the steps involved.

Specify C++ language in setup.py
---------------------------------

The best way to build Cython code from :file:`setup.py` scripts is the
``cythonize()`` function.  To make Cython generate and compile C++ code
with distutils, you just need to pass the option ``language="c++"``::

   from distutils.core import setup
   from Cython.Build import cythonize

   setup(ext_modules = cythonize(
              "rect.pyx",                 # our Cython source
              sources=["Rectangle.cpp"],  # additional source file(s)
              language="c++",             # generate C++ code
         ))

Cython will generate and compile the :file:`rect.cpp` file (from the
:file:`rect.pyx`), then it will compile :file:`Rectangle.cpp`
(implementation of the ``Rectangle`` class) and link both objects files
together into :file:`rect.so`, which you can then import in Python using
``import rect`` (if you forget to link the :file:`Rectangle.o`, you will
get missing symbols while importing the library in Python).

Note that the ``language`` option has no effect on user provided Extension
objects that are passed into ``cythonize()``.  It is only used for modules
found by file name (as in the example above).

The ``cythonize()`` function in Cython versions up to 0.21 does not
recognize the ``language`` option and it needs to be specified as an
option to an :class:`Extension` that describes your extension and that
is then handled by ``cythonize()`` as follows::

   from distutils.core import setup, Extension
   from Cython.Build import cythonize

   setup(ext_modules = cythonize(Extension(
              "rect",                                # the extension name
              sources=["rect.pyx", "Rectangle.cpp"], # the Cython source and
                                                     # additional C++ source files
              language="c++",                        # generate and compile C++ code
         )))

The options can also be passed directly from the source file, which is
often preferable (and overrides any global option).  Starting with
version 0.17, Cython also allows to pass external source files into the
``cythonize()`` command this way.  Here is a simplified setup.py file::

   from distutils.core import setup
   from Cython.Build import cythonize

   setup(
       name = "rectangleapp",
       ext_modules = cythonize('*.pyx'),
   )

And in the .pyx source file, write this into the first comment block, before
any source code, to compile it in C++ mode and link it statically against the
:file:`Rectangle.cpp` code file::

   # distutils: language = c++
   # distutils: sources = Rectangle.cpp

To compile manually (e.g. using ``make``), the ``cython`` command-line
utility can be used to generate a C++ ``.cpp`` file, and then compile it
into a python extension.  C++ mode for the ``cython`` command is turned
on with the ``--cplus`` option.

Declaring a C++ class interface
--------------------------------

The procedure for wrapping a C++ class is quite similar to that for wrapping
normal C structs, with a couple of additions. Let's start here by creating the
basic ``cdef extern from`` block::

    cdef extern from "Rectangle.h" namespace "shapes":

This will make the C++ class def for Rectangle available. Note the namespace declaration.
Namespaces are simply used to make the fully qualified name of the object, and can be nested (e.g. ``"outer::inner"``) or even refer to classes (e.g. ``"namespace::MyClass`` to declare static members on MyClass).

Declare class with cdef cppclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, let's add the Rectangle class to this extern from block - just copy the
class name from Rectangle.h and adjust for Cython syntax, so now it becomes::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:

Add public attributes
^^^^^^^^^^^^^^^^^^^^^^

We now need to declare the attributes and methods for use on Cython::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:
            Rectangle() except +
            Rectangle(int, int, int, int) except +
            int x0, y0, x1, y1
            int getArea()
            void getSize(int* width, int* height)
            void move(int, int)

Note that the constructor is declared as "except +".  If the C++ code or
the initial memory allocation raises an exception due to a failure, this
will let Cython safely raise an appropriate Python exception instead
(see below).  Without this declaration, C++ exceptions originating from
the constructor will not be handled by Cython.

Declare a var with the wrapped C++ class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, we use cdef to declare a var of the class with the C++ ``new`` statement::

    rec_ptr = new Rectangle(1, 2, 3, 4)
    try:
        recArea = rec_ptr.getArea()
        ...
    finally:
        del rec_ptr     # delete heap allocated object

It's also possible to declare a stack allocated object, as long as it has
a "default" constructor::

    cdef extern from "Foo.h":
        cdef cppclass Foo:
            Foo()

    def func():
        cdef Foo foo
        ...

Note that, like C++, if the class has only one constructor and it
is a nullary one, it's not necessary to declare it.

Create Cython wrapper class
----------------------------

At this point, we have exposed into our pyx file's namespace the interface
of the C++ Rectangle type.  Now, we need to make this accessible from
external Python code (which is our whole point).

Common programming practice is to create a Cython extension type which
holds a C++ instance as an attribute and create a bunch of
forwarding methods. So we can implement the Python extension type as::

    cdef class PyRectangle:
        cdef Rectangle c_rect      # hold a C++ instance which we're wrapping
        def __cinit__(self, int x0, int y0, int x1, int y1):
            self.c_rect = Rectangle(x0, y0, x1, y1)
        def get_area(self):
            return self.c_rect.getArea()
        def get_size(self):
            cdef int width, height
            self.c_rect.getSize(&width, &height)
            return width, height
        def move(self, dx, dy):
            self.c_rect.move(dx, dy)

And there we have it. From a Python perspective, this extension type will look
and feel just like a natively defined Rectangle class.
It should be noted that

If you want to give
attribute access, you could just implement some properties::

    @property
    def x0(self):
        return self.c_rect.x0

    @x0.setter
    def x0(self):
        def __set__(self, x0): self.c_rect.x0 = x0
    ...

Cython initializes C++ class attributes of a cdef class using the nullary constructor.
If the class you're wrapping does not have a nullary constructor, you must store a pointer
to the wrapped class and manually allocate and deallocate it.
A convenient and safe place to do so is in the `__cinit__` and `__dealloc__` methods
which are guaranteed to be called exactly once upon creation and deletion of the Python
instance.

::

    cdef class PyRectangle:
        cdef Rectangle* c_rect      # hold a pointer to the C++ instance which we're wrapping
        def __cinit__(self, int x0, int y0, int x1, int y1):
            self.c_rect = new Rectangle(x0, y0, x1, y1)
        def __dealloc__(self):
            del self.c_rect
        ...

If you prefer giving the same name to the wrapper as the C++ class, see the
section on :ref:`resolving naming conflicts <resolve-conflicts>`.


Advanced C++ features
======================

We describe here all the C++ features that were not discussed in the above tutorial.

Overloading
------------

Overloading is very simple. Just declare the method with different parameters
and use any of them::

    cdef extern from "Foo.h":
        cdef cppclass Foo:
            Foo(int)
            Foo(bool)
            Foo(int, bool)
            Foo(int, int)

Overloading operators
----------------------

Cython uses C++ naming for overloading operators::

    cdef extern from "foo.h":
        cdef cppclass Foo:
            Foo()
            Foo operator+(Foo)
            Foo operator-(Foo)
            int operator*(Foo)
            int operator/(int)

    cdef Foo foo = new Foo()

    foo2 = foo + foo
    foo2 = foo - foo

    x = foo * foo2
    x = foo / 1

Note that if one has *pointers* to C++ objects, dereferencing must be done
to avoid doing pointer arithmetic rather than arithmetic on the objects
themselves::

    cdef Foo* foo_ptr = new Foo()
    foo = foo_ptr[0] + foo_ptr[0]
    x = foo_ptr[0] / 2

    del foo_ptr


Nested class declarations
--------------------------
C++ allows nested class declaration. Class declarations can also be
nested in Cython::

    cdef extern from "<vector>" namespace "std":
        cdef cppclass vector[T]:
            cppclass iterator:
                T operator*()
                iterator operator++()
                bint operator==(iterator)
                bint operator!=(iterator)
            vector()
            void push_back(T&)
            T& operator[](int)
            T& at(int)
            iterator begin()
            iterator end()

    cdef vector[int].iterator iter  #iter is declared as being of type vector<int>::iterator

Note that the nested class is declared with a ``cppclass`` but without a ``cdef``.

C++ operators not compatible with Python syntax
------------------------------------------------

Cython try to keep a syntax as close as possible to standard Python.
Because of this, certain C++ operators, like the preincrement ``++foo``
or the dereferencing operator ``*foo`` cannot be used with the same
syntax as C++. Cython provides functions replacing these operators in
a special module ``cython.operator``. The functions provided are:

* ``cython.operator.dereference`` for dereferencing. ``dereference(foo)``
  will produce the C++ code ``*(foo)``
* ``cython.operator.preincrement`` for pre-incrementation. ``preincrement(foo)``
  will produce the C++ code ``++(foo)``.
  Similarly for ``predecrement``, ``postincrement`` and ``postdecrement``.
* ``cython.operator.comma`` for the comma operator. ``comma(a, b)``
  will produce the C++ code ``((a), (b))``.

These functions need to be cimported. Of course, one can use a
``from ... cimport ... as`` to have shorter and more readable functions.
For example: ``from cython.operator cimport dereference as deref``.

For completeness, it's also worth mentioning ``cython.operator.address``
which can also be written ``&foo``.

Templates
----------

Cython uses a bracket syntax for templating. A simple example for wrapping C++ vector::

    # import dereference and increment operators
    from cython.operator cimport dereference as deref, preincrement as inc

    cdef extern from "<vector>" namespace "std":
        cdef cppclass vector[T]:
            cppclass iterator:
                T operator*()
                iterator operator++()
                bint operator==(iterator)
                bint operator!=(iterator)
            vector()
            void push_back(T&)
            T& operator[](int)
            T& at(int)
            iterator begin()
            iterator end()

    cdef vector[int] *v = new vector[int]()
    cdef int i
    for i in range(10):
        v.push_back(i)

    cdef vector[int].iterator it = v.begin()
    while it != v.end():
        print deref(it)
        inc(it)

    del v

Multiple template parameters can be defined as a list, such as ``[T, U, V]``
or ``[int, bool, char]``.  Optional template parameters can be indicated
by writing ``[T, U, V=*]``.  In the event that Cython needs to explicitly
reference the type of a default template parameter for an incomplete template
instantiation, it will write ``MyClass<T, U>::V``, so if the class provides
a typedef for its template parameters it is preferable to use that name here.


Template functions are defined similarly to class templates, with
the template parameter list following the function name::

    cdef extern from "<algorithm>" namespace "std":
        T max[T](T a, T b)

    print max[long](3, 4)
    print max(1.5, 2.5)  # simple template argument deduction


Standard library
-----------------

Most of the containers of the C++ Standard Library have been declared
in pxd files located in ``/Cython/Includes/libcpp``.  These containers
are: deque, list, map,  pair,  queue,  set,  stack,  vector.

For example::

    from libcpp.vector cimport vector

    cdef vector[int] vect
    cdef int i
    for i in range(10):
        vect.push_back(i)
    for i in range(10):
        print vect[i]

The pxd files in ``/Cython/Includes/libcpp`` also work as good examples on
how to declare C++ classes.

Since Cython 0.17, the STL containers coerce from and to the
corresponding Python builtin types.  The conversion is triggered
either by an assignment to a typed variable (including typed function
arguments) or by an explicit cast, e.g.::

    from libcpp.string cimport string
    from libcpp.vector cimport vector

    cdef string s = py_bytes_object
    print(s)
    cpp_string = <string> py_unicode_object.encode('utf-8')

    cdef vector[int] vect = xrange(1, 10, 2)
    print(vect)              # [1, 3, 5, 7, 9]

    cdef vector[string] cpp_strings = b'ab cd ef gh'.split()
    print(cpp_strings[1])   # b'cd'

The following coercions are available:

+------------------+----------------+-----------------+
| Python type =>   | *C++ type*     | => Python type  |
+==================+================+=================+
| bytes            | std::string    | bytes           |
+------------------+----------------+-----------------+
| iterable         | std::vector    | list            |
+------------------+----------------+-----------------+
| iterable         | std::list      | list            |
+------------------+----------------+-----------------+
| iterable         | std::set       | set             |
+------------------+----------------+-----------------+
| iterable (len 2) | std::pair      | tuple (len 2)   |
+------------------+----------------+-----------------+

All conversions create a new container and copy the data into it.
The items in the containers are converted to a corresponding type
automatically, which includes recursively converting containers
inside of containers, e.g. a C++ vector of maps of strings.

Iteration over stl containers (or indeed any class with ``begin()`` and
``end()`` methods returning an object supporting incrementing, dereferencing,
and comparison) is supported via the ``for .. in`` syntax (including in list
comprehensions).  For example, one can write::

    cdef vector[int] v = ...
    for value in v:
        f(value)
    return [x*x for x in v if x % 2 == 0]

If the loop target variable is unspecified, an assignment from type
``*container.begin()`` is used for :ref:`type inference <compiler-directives>`.


Simplified wrapping with default constructor
--------------------------------------------

If your extension type instantiates a wrapped C++ class using the default
constructor (not passing any arguments), you may be able to simplify the
lifecycle handling by tying it directly to the lifetime of the Python wrapper
object.  Instead of a pointer attribute, you can declare an instance::

    cdef class VectorStack:
        cdef vector[int] v

        def push(self, x):
            self.v.push_back(x)

        def pop(self):
            if self.v.empty():
                raise IndexError()
            x = self.v.back()
            self.v.pop_back()
            return x

Cython will automatically generate code that instantiates the C++ object
instance when the Python object is created and deletes it when the Python
object is garbage collected.



Exceptions
-----------

Cython cannot throw C++ exceptions, or catch them with a try-except statement,
but it is possible to declare a function as potentially raising an C++
exception and converting it into a Python exception. For example, ::

    cdef extern from "some_file.h":
        cdef int foo() except +

This will translate try and the C++ error into an appropriate Python exception.
The translation is performed according to the following table
(the ``std::`` prefix is omitted from the C++ identifiers):

+-----------------------+---------------------+
| C++                   | Python              |
+=======================+=====================+
| ``bad_alloc``         | ``MemoryError``     |
+-----------------------+---------------------+
| ``bad_cast``          | ``TypeError``       |
+-----------------------+---------------------+
| ``bad_typeid``        | ``TypeError``       |
+-----------------------+---------------------+
| ``domain_error``      | ``ValueError``      |
+-----------------------+---------------------+
| ``invalid_argument``  | ``ValueError``      |
+-----------------------+---------------------+
| ``ios_base::failure`` | ``IOError``         |
+-----------------------+---------------------+
| ``out_of_range``      | ``IndexError``      |
+-----------------------+---------------------+
| ``overflow_error``    | ``OverflowError``   |
+-----------------------+---------------------+
| ``range_error``       | ``ArithmeticError`` |
+-----------------------+---------------------+
| ``underflow_error``   | ``ArithmeticError`` |
+-----------------------+---------------------+
| (all others)          | ``RuntimeError``    |
+-----------------------+---------------------+

The ``what()`` message, if any, is preserved. Note that a C++
``ios_base_failure`` can denote EOF, but does not carry enough information
for Cython to discern that, so watch out with exception masks on IO streams. ::

    cdef int bar() except +MemoryError

This will catch any C++ error and raise a Python MemoryError in its place.
(Any Python exception is valid here.) ::

    cdef int raise_py_error()
    cdef int something_dangerous() except +raise_py_error

If something_dangerous raises a C++ exception then raise_py_error will be
called, which allows one to do custom C++ to Python error "translations." If
raise_py_error does not actually raise an exception a RuntimeError will be
raised.

Static member method
--------------------

If the Rectangle class has a static member:

.. sourcecode:: c++

    namespace shapes {
        class Rectangle {
        ...
        public:
            static void do_something();

        };
    }

you can declare it using the Python @staticmethod decorator, i.e.::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:
            ...
            @staticmethod
            void do_something()


Declaring/Using References
---------------------------

Cython supports declaring lvalue references using the standard ``Type&`` syntax.
Note, however, that it is unnecessary to declare the arguments of extern
functions as references (const or otherwise) as it has no impact on the
caller's syntax.


``auto`` Keyword
----------------

Though Cython does not have an ``auto`` keyword, Cython local variables
not explicitly typed with ``cdef`` are deduced from the types of the right hand
side of *all* their assignments (see the ``infer_types``
:ref:`compiler directive <compiler-directives>`).  This is particularly handy
when dealing with functions that return complicated, nested, templated types,
e.g.::

    cdef vector[int] v = ...
    it = v.begin()

(Though of course the ``for .. in`` syntax is preferred for objects supporting
the iteration protocol.)

RTTI and typeid()
=================

Cython has support for the ``typeid(...)`` operator.

    from cython.operator cimport typeid

The ``typeid(...)`` operator returns an object of the type ``const type_info &``.

If you want to store a type_info value in a C variable, you will need to store it
as a pointer rather than a reference:

    from libcpp.typeinfo cimport type_info
    cdef const type_info* info = &typeid(MyClass)

If an invalid type is passed to ``typeid``, it will throw an ``std::bad_typeid``
exception which is converted into a ``TypeError`` exception in Python.

An additional C++11-only RTTI-related class, ``std::type_index``, is available
in ``libcpp.typeindex``.


Caveats and Limitations
========================

Access to C-only functions
---------------------------

Whenever generating C++ code, Cython generates declarations of and calls
to functions assuming these functions are C++ (ie, not declared as ``extern "C"
{...}``. This is ok if the C functions have C++ entry points, but if they're C
only, you will hit a roadblock. If you have a C++ Cython module needing
to make calls to pure-C functions, you will need to write a small C++ shim
module which:

* includes the needed C headers in an extern "C" block
* contains minimal forwarding functions in C++, each of which calls the
  respective pure-C function

C++ left-values
----------------

C++ allows functions returning a reference to be left-values.  This is currently
not supported in Cython. ``cython.operator.dereference(foo)`` is also not
considered a left-value.
