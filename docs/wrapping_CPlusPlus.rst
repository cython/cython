.. _wrapping-cplusplus-label:

Wrapping C++ Classes in Cython
====================================

Overview
--------

This page aims to get you quickly up to speed so you can wrap C++ interfaces
with a minimum of pain and 'surprises'.

In the past, Pyrex only supported wrapping of C APIs, and not C++. To wrap
C++, one had to write a pure-C shim, containing functions for
constructors/destructors and method invocations. Object pointers were passed
around as opaque void pointers, and cast to/from object pointers as needed.
This approach did work, but it got awfully messy and error-prone when trying
to wrap APIs with large class hierarchies and lots of inheritance.

These days, though, Pyrex offers an adequate bare minimum of C++ support,
which Cython has inherited. The approach described in this document will help
you wrap a lot of C++ code with only moderate effort. There are some
limitations, which we will discuss at the end of the document.

Procedure Overview
------------------

* Specify C++ language in :file:`setup.py` script
* Create ``cdef extern from`` blocks and declare classes as 
  ``ctypedef struct`` blocks
* Create constructors and destructors
* Add class methods as function pointers
* Create Cython wrapper class 

An example C++ API
------------------

Here is a tiny C++ API which we will use as an example throughout this
document. Let's assume it will be in a header file called
:file:`Rectangle.h`::

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

This is pretty dumb, but should suffice to demonstrate the steps involved.

Specify C++ language in setup.py
--------------------------------

In Cython :file:`setup.py` scripts, one normally instantiates an Extension
object. To make Cython generate and compile a C++ source, you just need
to add a keyword to your Extension construction statement, as in::

    ext = Extension(
        "rectangle",                 # name of extension
        ["rectangle.pyx"],           # filename of our Cython source
        language="c++",              # this causes Cython to create C++ source
        include_dirs=[...],          # usual stuff
        libraries=[...],             # ditto
        extra_link_args=[...],       # if needed
        cmdclass = {'build_ext': build_ext}
        )

With the language="c++" keyword, Cython distutils will generate a C++ file.

Create cdef extern from block
-----------------------------

The procedure for wrapping a C++ class is quite similar to that for wrapping
normal C structs, with a couple of additions. Let's start here by creating the
basic ``cdef extern from`` block::

    cdef extern from "Rectangle.h":

This will make the C++ class def for Rectangle available.

Declare class as a ctypedef struct
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, let's add the Rectangle class to this extern from block -- just copy the
class def from :file:`Rectangle.h` and adjust for Cython syntax, so now it
becomes::

    cdef extern from "Rectangle.h":
        # known in Cython namespace as 'c_Rectangle' but in C++ as 'Rectangle'
        ctypedef struct c_Rectangle "Rectangle":
            int x0, y0, x1, y1

We don't have any way of accessing the constructor/destructor or methods, but
we'll cover this now.

Add constructors and destructors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We now need to expose a constructor and destructor into the Cython
namespace. Again, we'll be using C name specifications::

    cdef extern from "Rectangle.h":
        ctypedef struct c_Rectangle "Rectangle":
            int x0, y0, x1, y1
        c_Rectangle *new_Rectangle "new Rectangle" (int x0, int y0, int x1, int y1)
        void del_Rectangle "delete" (c_Rectangle *rect)

Add class methods
^^^^^^^^^^^^^^^^^

Now, let's add the class methods. You can circumvent Cython syntax
limitations by declaring these as function pointers. Recall that in the C++
class we have::

  int getLength();
  int getHeight();
  int getArea();
  void move(int dx, int dy);

So if we convert each of these to function pointers and stick them in our
extern block, we now get::

    cdef extern from "Rectangle.h":
        ctypedef struct c_Rectangle "Rectangle":
            int x0, y0, x1, y1
            int getLength()
            int getHeight()
            int getArea()
            void move(int dx, int dy)
        c_Rectangle *new_Rectangle "new Rectangle" (int x0, int y0, int x1, int y1)
        void del_Rectangle "delete" (c_Rectangle *rect)

This will fool Cython into generating C++ method calls even though
Cython is mostly oblivious to C++.

In Pyrex you must explicitly declare these as function pointers, i.e. 
``(int *getArea)()``.

Create Cython wrapper class
---------------------------

At this point, we have exposed into our pyx file's namespace a struct which
gives us access to the interface of a C++ Rectangle type. Now, we need to make
this accessible from external Python code (which is our whole point).

Common programming practice is to create a Cython extension type which
holds a C++ instance pointer as an attribute ``thisptr``, and create a bunch of
forwarding methods. So we can implement the Python extension type as::

    cdef class Rectangle:
        cdef c_Rectangle *thisptr      # hold a C++ instance which we're wrapping
        def __cinit__(self, int x0, int y0, int x1, int y1):
            self.thisptr = new_Rectangle(x0, y0, x1, y1)
        def __dealloc__(self):
            del_Rectangle(self.thisptr)
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

Caveats and Limitations
-----------------------

In this document, we have discussed a relatively straightforward way of
wrapping C++ classes with Cython. However, there are some limitations in
this approach, some of which could be overcome with clever workarounds (anyone
here want to share some?), but some of which will require new features in
Cython.

The major limitations I'm most immediately aware of (and there will be many
more) include:

Overloading
^^^^^^^^^^^

Presently, it's not easy to overload methods or constructors, but there may be
a workaround if you try some creative C name specifications

Access to C-only functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^

If you have a class ``Foo`` with a child class ``Bar``, and ``Foo`` has a
method :meth:`fred`, then you'll have to cast to access this method from
``Bar`` objects.
For example::

    class MyClass:
        Bar *b
        ...
        def myfunc(self):
            ...
            b.fred()   # wrong, won't work
            (<Foo *>(self.b)).fred() # should work, Cython now thinks it's a 'Foo'

It might take some experimenting by others (you?) to find the most elegant
ways of handling this issue.

Advanced C++ features
^^^^^^^^^^^^^^^^^^^^^

Exceptions
""""""""""

Cython cannot throw C++ exceptions, or catch them with a try-except statement,
but it is possible to declare a function as potentially raising an C++
exception and converting it into a Python exception. For example, ::

    cdef extern from "some_file.h":
        cdef int foo() except +

This will translate try and the C++ error into an appropriate Python exception
(currently an IndexError on std::out_of_range and a RuntimeError otherwise
(preserving the what() message). ::

    cdef int bar() except +MemoryError

This will catch any C++ error and raise a Python MemoryError in its place.
(Any Python exception is valid here.) ::

    cdef int raise_py_error()
    cdef int something_dangerous() except +raise_py_error

If something_dangerous raises a C++ exception then raise_py_error will be
called, which allows one to do custom C++ to Python error "translations." If
raise_py_error does not actually raise an exception a RuntimeError will be
raised.

Templates
"""""""""

Cython does not natively understand C++ templates but we can put them to use
in some way. As an example consider an STL vector of C ints::

    cdef extern from "some .h file which includes <vector>":
        ctypedef struct intvec "std::vector<unsigned int>":
            void (* push_back)(int elem)
        intvec intvec_factory "std::vector<unsigned int>"(int len)

now we can use the vector like this::

    cdef intvec v = intvec_factory(2)
    v.push_back(2)

Overloading
"""""""""""

To support function overloading simply add a different alias to each
signature, so if you have e.g. ::

    int foo(int a);
    int foo(int a, int b);

in your C++ header then interface it like this in your ::

    int fooi "foo"(int)
    int fooii "foo"(int, int)

Operators
"""""""""

Some operators (e.g. +,-,...) can be accessed from Cython like this::

    ctypedef struct c_Rectangle "Rectangle":
    c_Rectangle add "operator+"(c_Rectangle right)

Declaring/Using References
""""""""""""""""""""""""""

Question: How do you declare and call a function that takes a reference as an argument?

Conclusion
----------

A great many existing C++ classes can be wrapped using these techniques, in a
way much easier than writing a large messy C shim module. There's a bit of
manual work involved, and an annoying maintenance burden if the C++ library
you're wrapping is frequently changing, but this recipe should hopefully keep
the discomfort to a minimum.

