.. highlight:: cython

.. _wrapping-cplusplus:

********************************
Using C++ in Cython
********************************

Overview
=========

Cython has native support for most of the C++ language.  Specifically:

* C++ objects can be :term:`dynamically allocated<Dynamic allocation or Heap allocation>` with ``new`` and ``del`` keywords.
* C++ objects can be :term:`stack-allocated<Stack allocation>`.
* C++ classes can be declared with the new keyword ``cppclass``.
* Templated classes and functions are supported.
* Overloaded functions are supported.
* Overloading of C++ operators (such as ``operator+``, ``operator[]``, ...) is supported.

Procedure Overview
-------------------
The general procedure for wrapping a C++ file can now be described as follows:

* Specify C++ language in a :file:`setup.py` script or locally in a source file.
* Create one or more ``.pxd`` files with ``cdef extern from`` blocks and
  (if existing) the C++ namespace name. In these blocks:

  * declare classes as ``cdef cppclass`` blocks
  * declare public names (variables, methods and constructors)

* ``cimport`` them in one or more extension modules (``.pyx`` files).

A simple Tutorial
==================

An example C++ API
-------------------

Here is a tiny C++ API which we will use as an example throughout this
document. Let's assume it will be in a header file called
:file:`Rectangle.h`:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/Rectangle.h
    :language: c++
    :tab-width: 4

and the implementation in the file called :file:`Rectangle.cpp`:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/Rectangle.cpp
    :language: c++
    :tab-width: 4

This is pretty dumb, but should suffice to demonstrate the steps involved.

Declaring a C++ class interface
--------------------------------

The procedure for wrapping a C++ class is quite similar to that for wrapping
normal C structs, with a couple of additions. Let's start here by creating the
basic ``cdef extern from`` block::

    cdef extern from "Rectangle.h" namespace "shapes":

This will make the C++ class def for Rectangle available. Note the namespace declaration.
Namespaces are simply used to make the fully qualified name of the object,
and can be nested (e.g. ``"outer::inner"``) or even refer to
classes (e.g. ``"namespace::MyClass`` to declare static members on MyClass).

Declare class with cdef cppclass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, let's add the Rectangle class to this extern from block - just copy the
class name from Rectangle.h and adjust for Cython syntax, so now it becomes::

    cdef extern from "Rectangle.h" namespace "shapes":
        cdef cppclass Rectangle:

Add public attributes
^^^^^^^^^^^^^^^^^^^^^^

We now need to declare the attributes and methods for use on Cython. We put those declarations
in a file called :file:`Rectangle.pxd`. You can see it as a header file
which is readable by Cython:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/Rectangle.pxd

Note that the constructor is declared as "except +". If the C++ code or
the initial memory allocation raises an exception due to a failure, this
will let Cython safely raise an appropriate Python exception instead
(see below).  Without this declaration, C++ exceptions originating from
the constructor will not be handled by Cython.

We use the lines::

    cdef extern from "Rectangle.cpp":
        pass

to include the C++ code from :file:`Rectangle.cpp`. It is also possible to specify to
setuptools that :file:`Rectangle.cpp` is a source. To do that, you can add this directive at the
top of the ``.pyx`` (not ``.pxd``) file::

    # distutils: sources = Rectangle.cpp

Note that when you use ``cdef extern from``, the path that you specify is relative to the current
file, but if you use the distutils directive, the path is relative to the
:file:`setup.py`. If you want to discover the path of the sources when
running the :file:`setup.py`, you can use the ``aliases`` argument
of the :func:`cythonize` function.

Declare a var with the wrapped C++ class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We'll create a ``.pyx`` file named ``rect.pyx`` to build our wrapper. We're
using a name other than ``Rectangle``, but if you prefer giving the same name
to the wrapper as the C++ class, see the section on 
:ref:`resolving naming conflicts <resolve-conflicts>`.

Within, we use cdef to declare a var of the class with the C++ ``new`` statement:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/cython_usage.pyx

The line::

    # distutils: language = c++

is to indicate to Cython that this ``.pyx`` file has to be compiled to C++.

It's also possible to declare a stack allocated object, as long as it has
a "default" constructor::

    cdef extern from "Foo.h":
        cdef cppclass Foo:
            Foo()

    def func():
        cdef Foo foo
        ...
        
See the section on the :ref:`cpp_locals directive` for a way
to avoid requiring a nullary/default constructor.

Note that, like C++, if the class has only one constructor and it
is a nullary one, it's not necessary to declare it.

Create Cython wrapper class
----------------------------

At this point, we have exposed into our pyx file's namespace the interface
of the C++ Rectangle type.  Now, we need to make this accessible from
external Python code (which is our whole point).

Common programming practice is to create a Cython extension type which
holds a C++ instance as an attribute and create a bunch of
forwarding methods. So we can implement the Python extension type as:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/rect.pyx

And there we have it. From a Python perspective, this extension type will look
and feel just like a natively defined Rectangle class.
It should be noted that if you want to give
attribute access, you could just implement some properties:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/rect_with_attributes.pyx

Cython initializes C++ class attributes of a cdef class using the nullary constructor.
If the class you're wrapping does not have a nullary constructor, you must store a pointer
to the wrapped class and manually allocate and deallocate it.  Alternatively, the
:ref:`cpp_locals directive` avoids the need for the pointer and only initializes the
C++ class attribute when it is assigned to.
A convenient and safe place to do so is in the `__cinit__` and `__dealloc__` methods
which are guaranteed to be called exactly once upon creation and deletion of the Python
instance.

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/rect_ptr.pyx

Compilation and Importing
=========================

To compile a Cython module, it is necessary to have a :file:`setup.py` file:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/setup.py

Run ``$ python setup.py build_ext --inplace``

To test it, open the Python interpreter::

    >>> import rect
    >>> x0, y0, x1, y1 = 1, 2, 3, 4
    >>> rect_obj = rect.PyRectangle(x0, y0, x1, y1)
    >>> print(dir(rect_obj))
    ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
     '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
     '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
     '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 'get_area', 'get_size', 'move']


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
            int operator*(int, Foo) # allows 1*Foo()
        # nonmember operators can also be specified outside the class
        double operator/(double, Foo)


    cdef Foo foo = new Foo()

    foo2 = foo + foo
    foo2 = foo - foo

    x = foo * foo2
    x = foo / 1

    x = foo[0] * foo2
    x = foo[0] / 1
    x = 1*foo[0]

    cdef double y
    y = 2.0/foo[0]

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
nested in Cython:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/nested_class.pyx

Note that the nested class is declared with a ``cppclass`` but without a ``cdef``,
as it is already part of a ``cdef`` declaration section.

C++ operators not compatible with Python syntax
------------------------------------------------

Cython tries to keep its syntax as close as possible to standard Python.
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

Cython uses a bracket syntax for templating. A simple example for wrapping C++ vector:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/templates.pyx

Multiple template parameters can be defined as a list, such as ``[T, U, V]``
or ``[int, bool, char]``.  Optional template parameters can be indicated
by writing ``[T, U, V=*]``.  In the event that Cython needs to explicitly
reference the type of a default template parameter for an incomplete template
instantiation, it will write ``MyClass<T, U>::V``, so if the class provides
a typedef for its template parameters it is preferable to use that name here.


Template functions are defined similarly to class templates, with
the template parameter list following the function name:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/function_templates.pyx

.. _stl_types:

Standard library
-----------------

Most of the containers of the C++ Standard Library have been declared
in pxd files located
in `/Cython/Includes/libcpp <https://github.com/cython/cython/tree/master/Cython/Includes/libcpp>`_.
These containers are: deque, list, map,  pair,  queue,  set,  stack,  vector.

For example:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/vector_demo.pyx

The pxd files
in `/Cython/Includes/libcpp <https://github.com/cython/cython/tree/master/Cython/Includes/libcpp>`_
also work as good examples on how to declare C++ classes.

The STL containers coerce from and to the
corresponding Python builtin types.  The conversion is triggered
either by an assignment to a typed variable (including typed function
arguments) or by an explicit cast, e.g.:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/python_to_cpp.pyx

The following coercions are available:

+------------------+------------------------+-----------------+
| Python type =>   | *C++ type*             | => Python type  |
+==================+========================+=================+
| bytes            | std::string            | bytes           |
+------------------+------------------------+-----------------+
| iterable         | std::vector            | list            |
+------------------+------------------------+-----------------+
| iterable         | std::list              | list            |
+------------------+------------------------+-----------------+
| iterable         | std::set               | set             |
+------------------+------------------------+-----------------+
| iterable         | std::unordered_set     | set             |
+------------------+------------------------+-----------------+
| mapping          | std::map               | dict            |
+------------------+------------------------+-----------------+
| mapping          | std::unordered_map     | dict            |
+------------------+------------------------+-----------------+
| iterable (len 2) | std::pair              | tuple (len 2)   |
+------------------+------------------------+-----------------+
| complex          | std::complex           | complex         |
+------------------+------------------------+-----------------+

All conversions create a new container and copy the data into it.
The items in the containers are converted to a corresponding type
automatically, which includes recursively converting containers
inside of containers, e.g. a C++ vector of maps of strings.

Be aware that the conversions do have some pitfalls, which are
detailed in :ref:`the troubleshooting section <automatic_conversion_pitfalls>`.

Iteration over stl containers (or indeed any class with ``begin()`` and
``end()`` methods returning an object supporting incrementing, dereferencing,
and comparison) is supported via the ``for .. in`` syntax (including in list
comprehensions).  For example, one can write:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/iterate.pyx

If the loop target variable is unspecified, an assignment from type
``*container.begin()`` is used for :ref:`type inference <compiler-directives>`.

.. note::

    Slicing stl containers is supported,
    you can do ``for x in my_vector[:5]: ...`` but unlike pointers slices,
    it will create a temporary Python object and iterate over it. Thus
    making the iteration very slow. You might want to avoid slicing
    C++ containers for performance reasons.


Simplified wrapping with default constructor
--------------------------------------------

If your extension type instantiates a wrapped C++ class using the default
constructor (not passing any arguments), you may be able to simplify the
lifecycle handling by tying it directly to the lifetime of the Python wrapper
object.  Instead of a pointer attribute, you can declare an instance:

.. literalinclude:: ../../examples/userguide/wrapping_CPlusPlus/wrapper_vector.pyx

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
(Any Python exception is valid here.)

Cython also supports using a custom exception handler. This is an advanced feature
that most users won't need, but for those that do a full example follows::

    cdef int raise_py_error()
    cdef int something_dangerous() except +raise_py_error

If something_dangerous raises a C++ exception then raise_py_error will be
called, which allows one to do custom C++ to Python error "translations." If
raise_py_error does not actually raise an exception a RuntimeError will be
raised. This approach may also be used to manage custom Python exceptions
created using the Python C API. ::

    # raising.pxd
    cdef extern from "Python.h" nogil:
        ctypedef struct PyObject

    cdef extern from *:
        """
        #include <Python.h>
        #include <stdexcept>
        #include <ios>

        PyObject *CustomLogicError;

        void create_custom_exceptions() {
            CustomLogicError = PyErr_NewException("raiser.CustomLogicError", NULL, NULL);
        }

        void custom_exception_handler() {
            try {
                if (PyErr_Occurred()) {
                    ; // let the latest Python exn pass through and ignore the current one
                } else {
                    throw;
                }
            }  catch (const std::logic_error& exn) {
                // Add mapping of std::logic_error -> CustomLogicError
                PyErr_SetString(CustomLogicError, exn.what());
            } catch (...) {
                PyErr_SetString(PyExc_RuntimeError, "Unknown exception");
            }
        }

        class Raiser {
            public:
                Raiser () {}
                void raise_exception() {
                    throw std::logic_error("Failure");
                }
        };
        """
        cdef PyObject* CustomLogicError
        cdef void create_custom_exceptions()
        cdef void custom_exception_handler()

        cdef cppclass Raiser:
            Raiser() noexcept
            void raise_exception() except +custom_exception_handler


    # raising.pyx
    create_custom_exceptions()
    PyCustomLogicError = <object> CustomLogicError


    cdef class PyRaiser:
        cdef Raiser c_obj

        def raise_exception(self):
            self.c_obj.raise_exception()

The above example leverages Cython's ability to include :ref:`verbatim C code
<verbatim_c>` in pxd files to create a new Python exception type
``CustomLogicError`` and map it to the standard C++ ``std::logic_error`` using
the ``custom_exception_handler`` function. There is nothing special about using
a standard exception class here, ``std::logic_error`` could easily be replaced
with some new C++ exception type defined in this file. The
``Raiser::raise_exception`` is marked with ``+custom_exception_handler`` to
indicate that this function should be called whenever an exception is raised.
The corresponding Python function ``PyRaiser.raise_exception`` will raise a
``CustomLogicError`` whenever it is called. Defining ``PyCustomLogicError``
allows other code to catch this exception, as shown below: ::
    
    try:
        PyRaiser().raise_exception()
    except PyCustomLogicError:
        print("Caught the exception")

When defining custom exception handlers it is typically good to also include
logic to handle all the standard exceptions that Cython typically handles as
listed in the table above. The code for this standard exception handler can be
found `here
<https://github.com/cython/cython/blob/master/Cython/Utility/CppSupport.cpp>`__.

If you want to use `std::exception_ptr` then you can ``cimport`` it from
``libcpp.exception``.  That provides a special exception handler
``exception_ptr_error_handler`` allowing you to declare a function: ::

    cdef extern from "some_header":
        void some_function() except +exception_ptr_error_handler

The exception raised from ``some_function`` will always be an ``Exception``
and the underlying ``std::exception_ptr`` can be retrieved with
``wrapped_exception_ptr_from_exception``.  This is a slightly niche use,
but ``std::exception_ptr`` is a useful way to safely store arbitrary C++
exceptions for later.

There is also the special form::

    cdef int raise_py_or_cpp() except +*

for those functions that may raise either a Python or a C++ exception.


Static member method
--------------------

If the Rectangle class has a static member:

.. code-block:: c++

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

Scoped Enumerations
-------------------

Cython supports scoped enumerations (``enum class``) in C++ mode::

    cdef enum class Cheese:
        cheddar = 1
        camembert = 2

As with "plain" enums, you may access the enumerators as attributes of the type.
Unlike plain enums however, the enumerators are not visible to the
enclosing scope::

    cdef Cheese c1 = Cheese.cheddar  # OK
    cdef Cheese c2 = cheddar  # ERROR!

Optionally, you may specify the underlying type of a scoped enumeration.
This is especially important when declaring an external scoped enumeration
with an underlying type::

    cdef extern from "Foo.h":
        cdef enum class Spam(unsigned int):
            x = 10
            y = 20
            ...

Declaring an enum class as ``cpdef`` will create a :pep:`435`-style Python wrapper.

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
as a pointer rather than a reference::

    from libcpp.typeinfo cimport type_info
    cdef const type_info* info = &typeid(MyClass)

If an invalid type is passed to ``typeid``, it will throw an ``std::bad_typeid``
exception which is converted into a ``TypeError`` exception in Python.

An additional C++11-only RTTI-related class, ``std::type_index``, is available
in ``libcpp.typeindex``.


Specify C++ language in setup.py
================================

Instead of specifying the language and the sources in the source files, it is
possible to declare them in the :file:`setup.py` file::

   from setuptools import setup
   from Cython.Build import cythonize

   setup(ext_modules = cythonize(
              "rect.pyx",                 # our Cython source
              sources=["Rectangle.cpp"],  # additional source file(s)
              language="c++",             # generate C++ code
         ))

Cython will generate and compile the :file:`rect.cpp` file (from
:file:`rect.pyx`), then it will compile :file:`Rectangle.cpp`
(implementation of the ``Rectangle`` class) and link both object files
together into :file:`rect.so` on Linux, or :file:`rect.pyd` on windows,
which you can then import in Python using
``import rect`` (if you forget to link the :file:`Rectangle.o`, you will
get missing symbols while importing the library in Python).

Note that the ``language`` option has no effect on user provided Extension
objects that are passed into ``cythonize()``.  It is only used for modules
found by file name (as in the example above).

The ``cythonize()`` function in Cython versions up to 0.21 does not
recognize the ``language`` option and it needs to be specified as an
option to an :class:`Extension` that describes your extension and that
is then handled by ``cythonize()`` as follows::

   from setuptools import Extension, setup
   from Cython.Build import cythonize

   setup(ext_modules = cythonize(Extension(
              "rect",                                # the extension name
              sources=["rect.pyx", "Rectangle.cpp"], # the Cython source and
                                                     # additional C++ source files
              language="c++",                        # generate and compile C++ code
         )))

The options can also be passed directly from the source file, which is
often preferable (and overrides any global option).  Starting with
version 0.17, Cython also allows passing external source files into the
``cythonize()`` command this way.  Here is a simplified setup.py file::

   from setuptools import setup
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

.. note::

     When using distutils directives, the paths are relative to the working
     directory of the setuptools run (which is usually the project root where
     the :file:`setup.py` resides).

To compile manually (e.g. using ``make``), the ``cython`` command-line
utility can be used to generate a C++ ``.cpp`` file, and then compile it
into a python extension.  C++ mode for the ``cython`` command is turned
on with the ``--cplus`` option.

.. _cpp_locals directive:

``cpp_locals`` directive
========================

The ``cpp_locals`` compiler directive is an experimental feature that makes
C++ variables behave like normal Python object variables.  With this
directive they are only initialized at their first assignment, and thus
they no longer require a nullary constructor to be stack-allocated.  Trying to
access an uninitialized C++ variable will generate an ``UnboundLocalError``
(or similar) in the same way as a Python variable would.  For example::

    def function(dont_write):
        cdef SomeCppClass c  # not initialized
        if dont_write:
            return c.some_cpp_function()  # UnboundLocalError
        else:
            c = SomeCppClass(...)  # initialized
            return c.some_cpp_function()  # OK
            
Additionally, the directive avoids initializing temporary C++ objects before
they are assigned, for cases where Cython needs to use such objects in its
own code-generation (often for return values of functions that can throw
exceptions).

For extra speed, the ``initializedcheck`` directive disables the check for an
unbound-local.  With this directive on, accessing a variable that has not
been initialized will trigger undefined behaviour, and it is entirely the user's
responsibility to avoid such access.

The ``cpp_locals`` directive is currently implemented using ``std::optional``
and thus requires a C++17 compatible compiler. Defining
``CYTHON_USE_BOOST_OPTIONAL`` (as define for the C++ compiler) uses ``boost::optional``
instead (but is even more experimental and untested).  The directive may
come with a memory and performance cost due to the need to store and check 
a boolean that tracks if a variable is initialized, but the C++ compiler should
be able to eliminate the check in most cases.


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
