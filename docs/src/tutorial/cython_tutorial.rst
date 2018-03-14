.. highlight:: cython

.. _tutorial:

**************
Basic Tutorial
**************

The Basics of Cython
====================

The fundamental nature of Cython can be summed up as follows: Cython is Python
with C data types.

Cython is Python: Almost any piece of Python code is also valid Cython code.
(There are a few :ref:`cython-limitations`, but this approximation will
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

As Cython can accept almost any valid python source file, one of the hardest
things in getting started is just figuring out how to compile your extension.

So lets start with the canonical python hello world::

    print "Hello World"

Save this code in a file named :file:`helloworld.pyx`.  Now we need to create
the :file:`setup.py`, which is like a python Makefile (for more information
see :ref:`compilation`). Your :file:`setup.py` should look like::

    from distutils.core import setup
    from Cython.Build import cythonize

    setup(
        ext_modules = cythonize("helloworld.pyx")
    )

To use this to build your Cython file use the commandline options:

.. sourcecode:: text

    $ python setup.py build_ext --inplace

Which will leave a file in your local directory called :file:`helloworld.so` in unix
or :file:`helloworld.pyd` in Windows. Now to use this file: start the python
interpreter and simply import it as if it was a regular python module::

    >>> import helloworld
    Hello World

Congratulations! You now know how to build a Cython extension. But so far
this example doesn't really give a feeling why one would ever want to use Cython, so
lets create a more realistic example.

:mod:`pyximport`: Cython Compilation for Developers
---------------------------------------------------

If your module doesn't require any extra C libraries or a special
build setup, then you can use the pyximport module, originally developed
by Paul Prescod, to load .pyx files directly on import, without having
to run your :file:`setup.py` file each time you change your code.
It is shipped and installed with Cython and can be used like this::

    >>> import pyximport; pyximport.install()
    >>> import helloworld
    Hello World

Since Cython 0.11, the :mod:`pyximport` module also has experimental
compilation support for normal Python modules.  This allows you to
automatically run Cython on every .pyx and .py module that Python
imports, including the standard library and installed packages.
Cython will still fail to compile a lot of Python modules, in which
case the import mechanism will fall back to loading the Python source
modules instead.  The .py import mechanism is installed like this::

    >>> pyximport.install(pyimport = True)

Note that it is not recommended to let :mod:`pyximport` build code
on end user side as it hooks into their import system.  The best way
to cater for end users is to provide pre-built binary packages in the
`wheel <https://wheel.readthedocs.io/>`_ packaging format.

Fibonacci Fun
==============

From the official Python tutorial a simple fibonacci function is defined as:

.. literalinclude:: ../../examples/tutorial/fib1/fib.pyx

Now following the steps for the Hello World example we first rename the file
to have a `.pyx` extension, lets say :file:`fib.pyx`, then we create the
:file:`setup.py` file. Using the file created for the Hello World example, all
that you need to change is the name of the Cython filename, and the resulting
module name, doing this we have:

.. literalinclude:: ../../examples/tutorial/fib1/setup.py

Build the extension with the same command used for the helloworld.pyx:

.. sourcecode:: text

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

:file:`primes.pyx`:

.. literalinclude:: ../../examples/tutorial/primes/primes.pyx
    :linenos:

You'll see that it starts out just like a normal Python function definition,
except that the parameter ``nb_primes`` is declared to be of type ``int`` . This
means that the object passed will be converted to a C integer (or a
``TypeError.`` will be raised if it can't be).

Now, let's dig into the core of the function::

    cdef int n, i, len_p
    cdef int p[1000]

Lines 2 and 3 use the ``cdef`` statement to define some local C variables.
The result is put in ``p``, it will be converted to a python list at the end
of the function (line 22). ::

    if nb_primes > 1000:
        nb_primes = 1000

As in C, declaring a static array requires knowing the size at compile time.
We make sure the user doesn't set a value above 1000 (or we'll have a nice
segmentation fault, just like in C). ::

    len_p = 0  # The number of elements in p
    n = 2
    while len_p < nb_primes:

Lines 7-9 set up for a loop which will test candidate numbers for primeness
until the required number of primes has been found. ::

    # Is n prime?
    for i in p[:len_p]:
        if n % i == 0:
            break

Lines 11-12, which try dividing a candidate by all the primes found so far,
are of particular interest. Because no Python objects are referred to,
the loop is translated entirely into C code, and thus runs very fast.
You will notice the way we iterate over the ``p`` C array.  ::

    for i in p[:len_p]:

The loop gets translated into C code transparently. No more ugly C for loops!
Well don't forget how to loop in C style with integers yet, you might need it someday.
If you don't use ``:len_p`` then Cython will loop over the 1000 elements of
the array (it won't go out of bounds and give a segmentation fault). ::

    # If no break occurred in the loop
    else:
        p[len_p] = n
        len_p += 1
    n += 1

If no breaks occurred, it means that we found a prime, and the block of code
after the ``else`` line 16 will be executed. We add the prime found to ``p``.
If you find having a else after a for loop strange, just know that it's a
hidden secret of the python syntax, and actually doesn't exist in C!
But since Cython is made to be written with the Python syntax, it'll
work out, as if you wrote Python code, but at C speed in this case.
If the for...else syntax still confuses you, see this excellent
`blog post <https://shahriar.svbtle.com/pythons-else-clause-in-loops>`_. ::

    # Let's put the result in a python list:
    result_as_list  = [prime for prime in p[:len_p]]
    return result_as_list

Line 22, before returning the result, we need to convert our C array into a
Python list, because Python can't read C arrays. Note that Cython handle
for you the conversion of quite some types between C and Python (you can
see exactly which :ref:`here<type-conversion>`. But not C arrays. We can trick
Cython into doing it because Cython knows how to convert a C int to a Python int.
By doing a list comprehension, we "cast" each C int prime from p into a Python int.
You could have also iterated manually over the C array and used
``result_as_list.append(prime)``, the result would have been the same.

You'll notice we declare a Python list exactly the same way it would be in Python.
Because the variable ``result_as_list`` hasn't been given a type, it is assumed to
hold a Python object.

Finally, at line 18, a normal
Python return statement returns the result list.

Compiling primes.pyx with the Cython compiler produces an extension module
which we can try out in the interactive interpreter as follows::

    >>> import primes
    >>> primes.primes(10)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

See, it works! And if you're curious about how much work Cython has saved you,
take a look at the C code generated for this module.


It is always good to check where is the Python interaction in the code with the
``annotate=True`` parameter in ``cythonize()``. Let's see:

.. figure:: htmlreport.png

The function declaration and return use the Python interpreter so it makes
sense for those lines to be yellow. Same for the list comprehension because
it involves the creation of a python object. But the line ``if n % i == 0:``, why?
We can examine the generated C code to understand:

.. figure:: python_division.png

We can see that some checks happen. Because Cython defaults to the
Python behavior, the language will perform division checks at runtime,
just like Python does. You can deactivate those checks by using the
:ref:`compiler directives<compiler-directives>`.

Now let's see if, even if we have division checks, we obtained a boost in speed.
Let's write the same program, but Python-style::

    def primes_python(nb_primes):
        p = []
        n = 2
        while len(p) < nb_primes:
            # Is n prime?
            for i in p:
                if n % i == 0:
                    break

            # If no break occurred in the loop
            else:
                p.append(n)
            n += 1
        return p

Now we can ensure that those two programs output the same values::

    >>> primes_python(500) == primes(500)
    True

It's possible to compare the speed now::

    >>> %timeit primes_python(500)
5.8 ms ± 178 µs per loop (mean ± std. dev. of 7 runs, 100 loops each) ::

    >>> %timeit primes(500)
502 µs ± 2.22 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

The Cython version is 11 550 times faster than the Python version! What could explain this?

Multiple things:
 * In this program, very little computation happen at each line.
   So the overhead of the python interpreter is very important. It would be
   very different if you were to do a lot computation at each line. Using NumPy for
   example.
 * Data locality. It's likely that a lot more can fit in CPU cache when using C than
   when using Python. Because everything in python is an object, and every object is
   implemented as a dictionary, this is not very cache friendly.

It's worth mentioning that you won't usually get speedups like this.
We very likeky touched a sweet spot with the CPU cache. Usually the speedups
are between 2x to 1000x. As always, remember to profile before adding types
everywhere.


Language Details
================

For more about the Cython language, see :ref:`language-basics`.
To dive right in to using Cython in a numerical computation context,
see :ref:`numpy_tutorial`.

