.. _tutorial_label:

*********
Tutorial
*********

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



Cython Hello World
===================

As Cython can accept almost any valid plain python file (though see the
`exceptions`), one of the hardest things in getting started is just figuring
out how to compile your file.

So lets start with the canonical python hello world::

    print "Hello World"

So the first thing to do is rename the file to :file:`helloworld.pyx`. Now we
need to make the :file:`setup.py`, which is like a python Makefile if you are
familiar.::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("helloworld", ["helloworld.pyx"])]
    ) 

To use this to build your Cython file use the commandline options::

    $ python setup.py build_ext --inplace

Which will leave a file in your local directory called `helloworld.so`. Now to
use this file start the python interpreter and::

    >>> import helloworld
    "Hello World"

Congratulations! You know know how to build a Cython extension. But So Far
this example doesn't really show us why we would even want to use Cython, so
lets do a more realistic example.

Fibonacci Fun
==============

From the official Python tutorial a simple fibonacci function is defined as::

    def fib(n):
        """Print the Fibonacci series up to n."""
        a, b = 0, 1
        while b < n:
            print b,
            a, b = b, a + b

Now following the steps for the Hello World example we first rename the file
to have a `.pyx` extension, lets say :file:`fib.pyx`, then we create the
:file:`setup.py` file. Using the file created for the Hello World example, all
that you need to change is the name of the Cython filename, and the resulting
module name, doing this we have::

    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Distutils import build_ext

    setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("fib", ["fib.pyx"])]
    )

Build the extension with the same command used for the helloworld.pyx::

    $ python setup.py build_ext --inplace

And use the new extension with::

    >>> import fib
    >>> fib.fib(2000)
    1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

Primes
=======

Here's a small example showing some of what can be done. It's a routine for
finding prime numbers. You tell it how many primes you want, and it returns
them as a Python list.

:file:`primes.pyx`: :: 

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

