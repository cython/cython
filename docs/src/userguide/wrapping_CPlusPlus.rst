.. highlight:: cython

.. _wrapping-cplusplus:

********************************
Using C++ in Cython
********************************

Overview
=========

Cython v0.13 introduces native support for most of the C++ language. This means that the previous tricks that were used to wrap C++ classes (as described in http://wiki.cython.org/WrappingCPlusPlus_ForCython012AndLower) are no longer needed. 

Wrapping C++ classes with Cython is now much more straightforward. This document describe in details the new way of wrapping C++ code.

What's new in Cython v0.13 about C++
---------------------------------------------------

For users of previous Cython versions, here is a brief overview of the main new features of Cython v0.13 regarding C++ support:

* C++ objects can now be dynamically allocated with ``new`` and ``del`` keywords.
* C++ objects can now be stack-allocated.
* C++ classes can be declared with the new keyword ``cppclass``.
* Templated classes are supported.
* Overloaded functions are supported.
* Overloading of C++ operators (such as operator+, operator[],...) is supported.

Procedure Overview
-------------------
The general procedure for wrapping a C++ file can now be described as follow:

* Specify C++ language in :file:`setup.py` script
* Create ``cdef extern from`` blocks with the optional namespace (if exists) and the namespace name as string
* Declare classes as ``cdef cppclass`` blocks
* Declare public attributes (variables, methods and constructors) 

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
            Rectangle(int x0, int y0, int x1, int y1);
            ~Rectangle();
            int getLength();
            int getHeight();
            int getArea();
            void move(int dx, int dy);
        };
    }
    
and the implementation in the file called :file:`Rectangle.cpp`:

.. sourcecode:: c++

    #include "Rectangle.h"

    using namespace shapes;

    Rectangle::Rectangle(int X0, int Y0, int X1, int Y1)
    {
        x0 = X0;
        y0 = Y0;
        x1 = X1;
        y1 = Y1;
    }

    Rectangle::~Rectangle()
    {
    }

    int Rectangle::getLength()
    {
        return (x1 - x0);
    }

    int Rectangle::getHeight()
    {
        return (y1 - y0);
    }

    int Rectangle::getArea()
    {
        return (x1 - x0) * (y1 - y0);
    }

    void Rectangle::move(int dx, int dy)
    {
        x0 += dx;
        y0 += dy;
        x1 += dx;
        y1 += dy;
    }

This is pretty dumb, but should suffice to demonstrate the steps involved.

Specify C++ language in setup.py
---------------------------------

In Cython :file:`setup.py` scripts, one normally instantiates an Extension
object. To make Cython generate and compile a C++ source, you just need
to add the keyword ``language="c++"`` to your Extension construction statement, as in::

   from distutils.core import setup
   from distutils.extension import Extension
   from Cython.Distutils import build_ext

   setup(ext_modules=[Extension(
                      "rectangle",                 # name of extension
                      ["rectangle.pyx", "Rectangle.cpp"], #  our Cython source
                      language="c++")],  # causes Cython to create C++ source
         cmdclass={'build_ext': build_ext})

Cython will generate and compile the :file:`rectangle.cpp` file (from the
:file:`rectangle.pyx`), then it will compile :file:`Rectangle.cpp`
(implementation of the ``Rectangle`` class) and link both objects files
together into :file:`rectangle.so`, which you can then import in Python using
``import rectangle`` (if you forget to link the :file:`Rectangle.o`, you will
get missing symbols while importing the library in Python).


Alternatively, one can also use the ``cython`` command-line utility to generate a C++ ``.cpp`` file, and then compile it into a python extension. C++ mode for the ``cython`` command is turned on with the ``--cplus`` option.

Declaring a C++ class interface
--------------------------------

The procedure for wrapping a C++ class is quite similar to that for wrapping
normal C structs, with a couple of additions. Let's start here by creating the
basic ``cdef extern from`` block::

    cdef extern from "Rectangle.h" namespace "shapes":

This will make the C++ class def for Rectangle available. Note the namespace declaration.

Declare class with cdef cppclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, let's add the Rectangle class to this extern from block - just copy the class name from Rectangle.h and adjust for Cython syntax, so now it becomes::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:
    
Add public attributes
^^^^^^^^^^^^^^^^^^^^^^

We now need to declare the attributes for use on Cython::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:
            Rectangle(int, int, int, int)
            int x0, y0, x1, y1
            int getLength()
            int getHeight()
            int getArea()
            void move(int, int)

Declare a var with the wrapped C++ class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, we use cdef to declare a var of the class with the C++ ``new`` statement::

    cdef Rectangle *rec = new Rectangle(1, 2, 3, 4)
    cdef int recLength = rec.getLength()
    ...
    del rec #delete heap allocated object

It's also possible to declare a stack allocated object, but it's necessary to have a "default" constructor::

    cdef extern from "Foo.h":
        cdef cppclass Foo:
            Foo()

    cdef Foo foo

Note that, like C++, if the class has only one constructor and it is a default one, it's not necessary to declare it.

Create Cython wrapper class
----------------------------

At this point, we have exposed into our pyx file's namespace the interface of the C++ Rectangle type. Now, we need to make
this accessible from external Python code (which is our whole point).

Common programming practice is to create a Cython extension type which
holds a C++ instance pointer as an attribute ``thisptr``, and create a bunch of
forwarding methods. So we can implement the Python extension type as::

    cdef class PyRectangle:
        cdef Rectangle *thisptr      # hold a C++ instance which we're wrapping
        def __cinit__(self, int x0, int y0, int x1, int y1):
            self.thisptr = new Rectangle(x0, y0, x1, y1)
        def __dealloc__(self):
            del self.thisptr
        def getLength(self):
            return self.thisptr.getLength()
        def getHeight(self):
            return self.thisptr.getHeight()
        def getArea(self):
            return self.thisptr.getArea()
        def move(self, dx, dy):
            self.thisptr.move(dx, dy)

And there we have it. From a Python perspective, this extension type will look
and feel just like a natively defined Rectangle class. If you want to give
attribute access, you could just implement some properties::

    property x0:
        def __get__(self): return self.thisptr.x0
        def __set__(self, x0): self.thisptr.x0 = x0
    ...


Advanced C++ features
======================

We describe here all the C++ features that were not discussed in the above tutorial.

Overloading
------------

Overloading is very simple. Just declare the method with different parameters and use any of them::

    cdef extern from "Foo.h":
        cdef cppclass Foo:
            Foo(int)
            Foo(bool)
            Foo(int, bool)
            Foo(int, int)

Overloading operators
----------------------

Cython uses C++ for overloading operators::

    cdef extern from "foo.h":
        cdef cppclass Foo:
            Foo()
            Foo* operator+(Foo*)
            Foo* operator-(Foo)
            int operator*(Foo*)
            int operator/(int)

    cdef Foo* foo = new Foo()
    cdef int x

    cdef Foo* foo2 = foo[0] + foo
    foo2 = foo[0] - foo[0]

    x = foo[0] * foo2
    x = foo[0] / 1

    cdef Foo f
    foo = f + &f
    foo2 = f - f

    del foo, foo2

Nested class declarations
--------------------------
C++ allows nested class declaration. Class declarations can also be nested in Cython::


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

Cython try to keep a syntax as close as possible to standard Python. Because of this, certain C++ operators, like the preincrement ``++foo`` or the dereferencing operator ``*foo`` cannot be used with the same syntax as C++. Cython provides functions replacing these operators in a special module ``cython.operator``. The functions provided are:

* ``cython.operator.dereference`` for dereferencing. ``dereference(foo)`` will produce the C++ code ``*foo``
* ``cython.operator.preincrement`` for pre-incrementation. ``preincrement(foo)`` will produce the C++ code ``++foo``
* ...

These functions need to be cimported. Of course, one can use a ``from ... cimport ... as`` to have shorter and more readable functions. For example: ``from cython.operator cimport dereference as deref``.

Templates
----------

Cython uses a bracket syntax for templating. A simple example for wrapping C++ vector::

    from cython.operator cimport dereference as deref, preincrement as inc #dereference and increment operators

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

Multiple template parameters can be defined as a list, such as [T, U, V] or [int, bool, char]. 

Standard library
-----------------

Most of the containers of the C++ Standard Library have been declared in pxd files  located in ``/Cython/Includes/libcpp``. These containers are: deque, list, map,  pair,  queue,  set,  stack,  vector.

For example::

    from libcpp.vector cimport vector

    cdef vector[int] vect
    cdef int i
    for i in range(10):
        vect.push_back(i)
    for i in range(10):
        print vect[i]
        
The pxd files in ``/Cython/Includes/libcpp`` also work as good examples on how to declare C++ classes.

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


Caveats and Limitations
========================

Access to C-only functions
---------------------------

Whenever generating C++ code, Cython generates declarations of and calls
to functions assuming these functions are C++ (ie, not declared as extern "C"
{...} . This is ok if the C functions have C++ entry points, but if they're C
only, you will hit a roadblock. If you have a C++ Cython module needing
to make calls to pure-C functions, you will need to write a small C++ shim
module which:

* includes the needed C headers in an extern "C" block
* contains minimal forwarding functions in C++, each of which calls the
  respective pure-C function 

Inherited C++ methods
----------------------

If you have a class ``Foo`` with a child class ``Bar``, and ``Foo`` has a
method :meth:`fred`, then you'll have to cast to access this method from
``Bar`` objects.
For example::

    cdef class MyClass:
        Bar *b
        ...
        def myfunc(self):
            ...
            b.fred()   # wrong, won't work
            (<Foo *>(self.b)).fred() # should work, Cython now thinks it's a 'Foo'

It might take some experimenting by others (you?) to find the most elegant
ways of handling this issue.

Declaring/Using References
---------------------------

Question: How do you declare and call a function that takes a reference as an argument?

C++ left-values
----------------

C++ allows functions returning a reference to be left-values. This is currently not supported in Cython. ``cython.operator.dereference(foo)`` is also not considered a left-value.


