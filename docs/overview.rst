.. _overview-label:

********
Overview
********

A language for writing Python extension modules

What is Cython all about?
=========================

Cython is a language specially designed for writing Python extension modules.
It's designed to bridge the gap between the nice, high-level, easy-to-use
world of Python and the messy, low-level world of C.

You may be wondering why anyone would want a special language for this. Python
is really easy to extend using C or C++, isn't it? Why not just write your
extension modules in one of those languages?

Well, if you've ever written an extension module for Python, you'll know that
things are not as easy as all that. First of all, there is a fair bit of
boilerplate code to write before you can even get off the ground. Then you're
faced with the problem of converting between Python and C data types. For the
basic types such as numbers and strings this is not too bad, but anything more
elaborate and you're into picking Python objects apart using the Python/C API
calls, which requires you to be meticulous about maintaining reference counts,
checking for errors at every step and cleaning up properly if anything goes
wrong. Any mistakes and you have a nasty crash that's very difficult to debug.

Various tools have been developed to ease some of the burdens of producing
extension code, of which perhaps SWIG is the best known. SWIG takes a
definition file consisting of a mixture of C code and specialised
declarations, and produces an extension module. It writes all the boilerplate
for you, and in many cases you can use it without knowing about the Python/C
API. But you need to use API calls if any substantial restructuring of the
data is required between Python and C.

What's more, SWIG gives you no help at all if you want to create a new
built-in Python type. It will generate pure-Python classes which wrap (in a
slightly unsafe manner) pointers to C data structures, but creation of true
extension types is outside its scope.

Another notable attempt at making it easier to extend Python is PyInline ,
inspired by a similar facility for Perl. PyInline lets you embed pieces of C
code in the midst of a Python file, and automatically extracts them and
compiles them into an extension. But it only converts the basic types
automatically, and as with SWIG,  it doesn't address the creation of new
Python types.

Cython aims to go far beyond what any of these previous tools provides. Cython
deals with the basic types just as easily as SWIG, but it also lets you write
code to convert between arbitrary Python data structures and arbitrary C data
structures, in a simple and natural way, without knowing anything about the
Python/C API. That's right -- nothing at all! Nor do you have to worry about
reference counting or error checking -- it's all taken care of automatically,
behind the scenes, just as it is in interpreted Python code. And what's more,
Cython lets you define new built-in Python types just as easily as you can
define new classes in Python.

Sound too good to be true? Read on and find out how it's done.

The Basics of Cython
====================

The fundamental nature of Cython can be summed up as follows: Cython is Python
with C data types.

Cython is Python: Almost any piece of Python code is also valid Cython code.
(There are a few :ref:`cython-limitations-label`, but this approximation will
serve for now.) The Cython compiler will convert it into C code which makes
equivalent calls to the Python/C API. 

But Cython is much more than that, because parameters and variables can be
declared to have C data types. Code which manipulates Python values and C
values can be freely intermixed, with conversions occurring automatically
wherever possible. Reference count maintenance and error checking of Python
operations is also automatic, and the full power of Python's exception
handling facilities, including the try-except and try-finally statements, is
available to you -- even in the midst of manipulating C data.

Here's a small example showing some of what can be done. It's a routine for
finding prime numbers. You tell it how many primes you want, and it returns
them as a Python list.

:file:`primes.pyx`:

.. code-block:: none 
    :linenos:

    def primes(int kmax):
        cdef int n, k, i
        cdef int p[1000]
        result = []
        if kmax > 1000:
            kmax = 1000
        k = 0
        n = 2
        while k < kmax:
            i = 0
            while i < k and n % p[i] != 0:
                i = i + 1
            if i == k:
               p[k] = n
               k = k + 1
               result.append(n)
            n = n + 1
        return result

You'll see that it starts out just like a normal Python function definition,
except that the parameter ``kmax`` is declared to be of type ``int`` . This
means that the object passed will be converted to a C integer (or a
``TypeError.`` will be raised if it can't be).

Lines 2 and 3 use the ``cdef`` statement to define some local C variables.
Line 4 creates a Python list which will be used to return the result. You'll
notice that this is done exactly the same way it would be in Python. Because
the variable result hasn't been given a type, it is assumed to hold a Python
object.

Lines 7-9 set up for a loop which will test candidate numbers for primeness
until the required number of primes has been found. Lines 11-12, which try
dividing a candidate by all the primes found so far, are of particular
interest. Because no Python objects are referred to, the loop is translated
entirely into C code, and thus runs very fast.

When a prime is found, lines 14-15 add it to the p array for fast access by
the testing loop, and line 16 adds it to the result list. Again, you'll notice
that line 16 looks very much like a Python statement, and in fact it is, with
the twist that the C parameter ``n`` is automatically converted to a Python
object before being passed to the append method. Finally, at line 18, a normal
Python return statement returns the result list.

Compiling primes.pyx with the Cython compiler produces an extension module
which we can try out in the interactive interpreter as follows::

    >>> import primes
    >>> primes.primes(10)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

See, it works! And if you're curious about how much work Cython has saved you,
take a look at the C code generated for this module. 

Language Details
================

For more about the Cython language, see :ref:`language-basics-label`.

Future Plans
============
Cython is not finished. Substantial tasks remaining. See
:ref:`cython-limitations-label` for a current list. 

