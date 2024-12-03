.. highlight:: cython

.. _tutorial:

**************
Basic Tutorial
**************

.. include::
    ../two-syntax-variants-used

The Basics of Cython
====================

The fundamental nature of Cython can be summed up as follows: Cython is Python
with C data types.

Cython is Python: Almost any piece of Python code is also valid Cython code.
(There are a few :ref:`cython-limitations`, but this approximation will
serve for now.) The Cython compiler will convert it into C code which makes
equivalent calls to the Python/C API.

But Cython is much more than that, because parameters and variables can be
declared to have C data types. Code which manipulates :term:`Python values<Python object>` and C
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

    print("Hello World")

Save this code in a file named :file:`helloworld.py`.  Now we need to create
the :file:`setup.py`, which is like a python Makefile (for more information
see :ref:`compilation`). Your :file:`setup.py` should look like::

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        ext_modules = cythonize("helloworld.py")
    )

To use this to build your Cython file use the commandline options:

.. code-block:: text

    $ python setup.py build_ext --inplace

Which will leave a file in your local directory called :file:`helloworld.so` in unix
or :file:`helloworld.pyd` in Windows. Now to use this file: start the python
interpreter and simply import it as if it was a regular python module::

    >>> import helloworld
    Hello World

Congratulations! You now know how to build a Cython extension. But so far
this example doesn't really give a feeling why one would ever want to use Cython, so
lets create a more realistic example.


Fibonacci Fun
==============

From the official Python tutorial a simple fibonacci function is defined as:

.. literalinclude:: ../../examples/tutorial/cython_tutorial/fibonacci.py

Now following the steps for the Hello World example we first save this code
to a Python file, let's say :file:`fibonacci.py`.  Next, we create the
:file:`setup.py` file. Using the file created for the Hello World example, all
that you need to change is the name of the Cython filename, and the resulting
module name, doing this we have::

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        ext_modules=cythonize("fibonacci.py"),
    )

Build the extension with the same command used for the "helloworld.py":

.. code-block:: text

    $ python setup.py build_ext --inplace

And use the new extension with::

    >>> import fibonacci
    >>> fibonacci.fib(2000)
    1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

.. _primes:

Primes
=======

Here's a small example showing some of what can be done. It's a routine for
finding prime numbers. You tell it how many primes you want, and it returns
them as a Python list.

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.py
            :linenos:
            :caption: primes.py

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
            :linenos:
            :caption: primes.pyx

The two syntax variants ("Pure Python" and "Cython") represent different ways
of annotating the code with C data types.  The first uses regular Python syntax
with Cython specific type hints, thus allowing the code to run as a normal
Python module.  Python type checkers will ignore most of the type details,
but on compilation, Cython interprets them as C data types and uses them
to generate tightly adapted C code.

The second variant uses a Cython specific syntax.  This syntax is mostly used
in older code bases and in Cython modules that need to make use of advanced
C or C++ features when interacting with C/C++ libraries.  The additions to
the syntax require a different file format, thus the ``.pyx`` extension:
Python code 'extended'.

For this tutorial, assuming you have a Python programming background,
it's probably best to stick to the Python syntax examples
and glimpse at the Cython specific syntax for comparison.

You can see that the example above starts out just like a normal Python function
definition, except that the parameter ``nb_primes`` is declared to be of Cython
type ``int`` (not the Python type of the same name).  This means that the Python
object passed into the function will be converted to a C integer on entry,
or a ``TypeError`` will be raised if it cannot be converted.

Now, let's dig into the core of the function:

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.py
            :lines: 2,3
            :dedent:
            :lineno-start: 2

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.py
            :lines: 11,12
            :dedent:
            :lineno-start: 11

        Lines 2, 3, 11 and 12 use the variable annotations
        to define some local C variables.
        The result is stored in the C array ``p`` during processing,
        and will be copied into a Python list at the end (line 26).

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
            :lines: 2,3
            :dedent:
            :lineno-start: 2

        Lines 2 and 3 use the ``cdef`` statement to define some local C variables.
        The result is stored in the C array ``p`` during processing,
        and will be copied into a Python list at the end (line 26).

.. NOTE:: You cannot create very large arrays in this manner, because
          they are allocated on the C function call :term:`stack<Stack allocation>`,
          which is a rather precious and scarce resource.
          To request larger arrays,
          or even arrays with a length only known at runtime,
          you can learn how to make efficient use of
          :ref:`C memory allocation <memory_allocation>`,
          :ref:`Python arrays <array-array>`
          or :ref:`NumPy arrays <memoryviews>` with Cython.

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
    :lines: 5,6
    :dedent:
    :lineno-start: 5

As in C, declaring a static array requires knowing the size at compile time.
We make sure the user doesn't set a value above 1000 (or we would have a
segmentation fault, just like in C)

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.py
            :lines: 8,9
            :dedent:
            :lineno-start: 8

        When we run this code from Python, we have to initialize the items in the array.
        This is most easily done by filling it with zeros (as seen on line 8-9).
        When we compile this with Cython, on the other hand, the array will
        behave as in C.  It is allocated on the function call stack with a fixed
        length of 1000 items that contain arbitrary data from the last time that
        memory was used.  We will then overwrite those items in our calculation.

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.py
            :lines: 10-13
            :dedent:
            :lineno-start: 10

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
            :lines: 10-13
            :dedent:
            :lineno-start: 10

Lines 11-13 set up a while loop which will test numbers-candidates to primes
until the required number of primes has been found.

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
    :lines: 14-17
    :dedent:
    :lineno-start: 14

Lines 15-16, which try to divide a candidate by all the primes found so far,
are of particular interest. Because no Python objects are referred to,
the loop is translated entirely into C code, and thus runs very fast.
You will notice the way we iterate over the ``p`` C array.

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
    :lines: 15
    :dedent:
    :lineno-start: 15

The loop gets translated into a fast C loop and works just like iterating
over a Python list or NumPy array.  If you don't slice the C array with
``[:len_p]``, then Cython will loop over the 1000 elements of the array.

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
    :lines: 19-23
    :dedent:
    :lineno-start: 19

If no breaks occurred, it means that we found a prime, and the block of code
after the ``else`` line 20 will be executed. We add the prime found to ``p``.
If you find having an ``else`` after a for-loop strange, just know that it's a
lesser known features of the Python language, and that Cython executes it at
C speed for you.
If the for-else syntax confuses you, see this excellent
`blog post <https://shahriar.svbtle.com/pythons-else-clause-in-loops>`_.

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes.pyx
    :lines: 25-27
    :dedent:
    :lineno-start: 25

In line 26, before returning the result, we need to copy our C array into a
Python list, because Python can't read C arrays.  Cython can automatically
convert many C types from and to Python types, as described in the
documentation on :ref:`type conversion <type-conversion>`, so we can use
a simple list comprehension here to copy the C ``int`` values into a Python
list of Python ``int`` objects, which Cython creates automatically along the way.
You could also have iterated manually over the C array and used
``result_as_list.append(prime)``, the result would have been the same.

You'll notice we declare a Python list exactly the same way it would be in Python.
Because the variable ``result_as_list`` hasn't been explicitly declared with a type,
it is assumed to hold a Python object, and from the assignment, Cython also knows
that the exact type is a Python list.

Finally, at line 27, a normal Python return statement returns the result list.

.. tabs::
    .. group-tab:: Pure Python

        Compiling primes.py with the Cython compiler produces an extension module
        which we can try out in the interactive interpreter as follows:

    .. group-tab:: Cython

        Compiling primes.pyx with the Cython compiler produces an extension module
        which we can try out in the interactive interpreter as follows:

.. code-block:: python

    >>> import primes
    >>> primes.primes(10)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

See, it works! And if you're curious about how much work Cython has saved you,
take a look at the C code generated for this module.

Cython has a way to visualise where interaction with Python objects and
Python's C-API is taking place. For this, pass the
``annotate=True`` parameter to ``cythonize()``. It produces a HTML file. Let's see:

.. tabs::
    .. group-tab:: Pure Python

        .. figure:: htmlreport_py.png
            :scale: 90 %

    .. group-tab:: Cython

        .. figure:: htmlreport_pyx.png
            :scale: 90 %

If a line is white, it means that the code generated doesn't interact
with Python, so will run as fast as normal C code.  The darker the yellow, the more
Python interaction there is in that line.  Those yellow lines will usually operate
on Python objects, raise exceptions, or do other kinds of higher-level operations
than what can easily be translated into simple and fast C code.
The function declaration and return use the Python interpreter so it makes
sense for those lines to be yellow. Same for the list comprehension because
it involves the creation of a Python object. But the line ``if n % i == 0:``, why?
We can examine the generated C code to understand:

.. figure:: python_division.png

We can see that some checks happen. Because Cython defaults to the
Python behavior, the language will perform division checks at runtime,
just like Python does. You can deactivate those checks by using the
:ref:`compiler directives<compiler-directives>`.

Now let's see if we get a speed increase even if there is a division check.
Let's write the same program, but in Python:

.. literalinclude:: ../../examples/tutorial/cython_tutorial/primes_python.py
    :caption: primes_python.py / primes_python_compiled.py

It is possible to take a plain (unannotated) ``.py`` file and to compile it with Cython.
Let's create a copy of ``primes_python`` and name it ``primes_python_compiled``
to be able to compare it to the (non-compiled) Python module.
Then we compile that file with Cython, without changing the code.
Now the ``setup.py`` looks like this:

.. tabs::
    .. group-tab:: Pure Python

        .. code-block:: python

            from setuptools import setup
            from Cython.Build import cythonize

            setup(
                ext_modules=cythonize(
                    ['primes.py',                   # Cython code file with primes() function
                     'primes_python_compiled.py'],  # Python code file with primes() function
                    annotate=True),                 # enables generation of the html annotation file
            )

    .. group-tab:: Cython

        .. code-block:: python

            from setuptools import setup
            from Cython.Build import cythonize

            setup(
                ext_modules=cythonize(
                    ['primes.pyx',                  # Cython code file with primes() function
                     'primes_python_compiled.py'],  # Python code file with primes() function
                    annotate=True),                 # enables generation of the html annotation file
            )

Now we can ensure that those two programs output the same values::

    >>> import primes, primes_python, primes_python_compiled
    >>> primes_python.primes(1000) == primes.primes(1000)
    True
    >>> primes_python_compiled.primes(1000) == primes.primes(1000)
    True

It's possible to compare the speed now::

    python -m timeit -s "from primes_python import primes" "primes(1000)"
    10 loops, best of 3: 23 msec per loop

    python -m timeit -s "from primes_python_compiled import primes" "primes(1000)"
    100 loops, best of 3: 11.9 msec per loop

    python -m timeit -s "from primes import primes" "primes(1000)"
    1000 loops, best of 3: 1.65 msec per loop

The cythonize version of ``primes_python`` is 2 times faster than the Python one,
without changing a single line of code.
The Cython version is 13 times faster than the Python version! What could explain this?

Multiple things:
 * In this program, very little computation happen at each line.
   So the overhead of the python interpreter is very important. It would be
   very different if you were to do a lot computation at each line. Using NumPy for
   example.
 * Data locality. It's likely that a lot more can fit in CPU cache when using C than
   when using Python. Because everything in python is an object, and every object is
   implemented as a dictionary, this is not very cache friendly.

Usually the speedups are between 2x to 1000x. It depends on how much you call
the Python interpreter. As always, remember to profile before adding types
everywhere. Adding types makes your code less readable, so use them with
moderation.


Primes with C++
===============

With Cython, it is also possible to take advantage of the C++ language, notably,
part of the C++ standard library is directly importable from Cython code.

Let's see what our code becomes when using
`vector <https://en.cppreference.com/w/cpp/container/vector>`_
from the C++ standard library.

.. note::

    Vector in C++ is a data structure which implements a list or stack based
    on a resizeable C array. It is similar to the Python ``array``
    type in the ``array`` standard library module.
    There is a method `reserve` available which will avoid copies if you know in advance
    how many elements you are going to put in the vector. For more details
    see `this page from cppreference <https://en.cppreference.com/w/cpp/container/vector>`_.

.. tabs::
    .. group-tab:: Pure Python

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes_cpp.py
            :linenos:

        .. include::
            ../cimport-warning

    .. group-tab:: Cython

        .. literalinclude:: ../../examples/tutorial/cython_tutorial/primes_cpp.pyx
            :linenos:

The first line is a compiler directive. It tells Cython to compile your code to C++.
This will enable the use of C++ language features and the C++ standard library.
Note that it isn't possible to compile Cython code to C++ with `pyximport`. You
should use a :file:`setup.py` or a notebook to run this example.

You can see that the API of a vector is similar to the API of a Python list,
and can sometimes be used as a drop-in replacement in Cython.

For more details about using C++ with Cython, see :ref:`wrapping-cplusplus`.

Language Details
================

For more about the Cython language, see :ref:`language-basics`.
To dive right in to using Cython in a numerical computation context,
see :ref:`memoryviews`.
