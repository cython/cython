**************
Free threading
**************

The free-threaded (sometimes known as "nogil") build of Python is an
experimental mode available from Python 3.13 onwards. It aims to
disable the "Global Interpreter Lock" and allow multiple Python threads to
run truly concurrently.

Cython 3.1 and upwards has some basic support for this build of Python.
Note that this support *is experimental* and is planned to remain experimental
for at least as long as the free-threaded build is experimental in the
CPython interpreter.

This section of documentation documents the extent of the support and the
known pitfalls.

Useful links
============

* `PEP 703 <https://peps.python.org/pep-0703/>`_ - the initial proposal that lead
  to this feature existing in Python.
* `Python documentation for free-threaded extensions <https://docs.python.org/3.13/howto/free-threading-extensions.html>`_.
* `Quansight labs' documentation of the status of free-threading <https://py-free-threading.github.io/>`_.

Status
======

.. note::

   All of this is experimental and subject to change/removal!

Cython 3.1 is able to build extension modules that are compatible with Freethreading builds
of Python.  However, by default these extension modules don't indicate their compatibility.
Therefore, importing one of these extension modules will result in the interpreter
re-enabling the GIL. The result is that the extension module will work, but you will lose
the benefits of the free-threaded interpreter!

The module-level directive ``# cython: freethreading_compatible = True`` declares that the
module is fully compatible with the free-threaded interpreter.  When you specify this
directive, importing the module will not cause the interpreter to re-enable the GIL.
The directive itself does
not do anything to ensure compatibility - it is simply a way for you to indicate that you
have tested your module and are confident that it works.

If you want to temporarily force Python not to re-enable the GIL irrespective of whether
extension modules claim to support it then you can either:

* set ``PYTHON_GIL=0`` as an environmental variable,
* run Python with ``-Xgil=0`` as a command-line argument.

These options are mainly useful for testing.

Tools for Thread-safety
=======================

Cython is gradually adding tools to help you write thread-safe code. These are
described here.

Critical Sections
-----------------

`Critical Sections <https://docs.python.org/3.13/c-api/init.html#python-critical-section-api>`_
are a feature provided by Python to generate a local lock based on some Python object.
Cython allows you to use critical sections with a convenient
syntax::

    o = object()
    ...
    with cython.critical_section(o):
      ...
      
Critical sections can take one or two Python objects as arguments.  You are required to
hold the GIL on entry to a critical section (you can release the GIL inside the critical
section but that also temporarily releases the critical section so is unlikely to be
a useful thing to do).

We suggest reading the Python documentation to understand how critical sections work.

* It is guaranteed that the lock will be held when executing code within the 
  critical section. However, there is no guarantee that the code block will be executed
  in one atomic action.  This is very similar to the guarantee provided by
  a ``with gil`` block.
* Operations on another Python object may end up temporarily releasing the
  critical section in favour of a critical section based on that object.

On non-freethreading builds ``cython.critical_section`` does nothing - you get the
same guarantees simply from the fact you hold the GIL.

As an alternative syntax, ``cython.critical_section`` can be used as a decorator
or a function taking at least one argument.  In this case the critical section
lasts the duration of the function and locks on the first argument::

    @cython.cclass
    class C:
        @cython.critical_section
        def func(self, *args):
            ...

        # equivalent to:
        def func(self, *args):
            with cython.critical_section(self):
                ...

Our expectation is that this will be most useful for locking on the ``self`` argument
of methods in C classes.

Pitfalls
========

Building on Windows
-------------------

As of the Python 3.13 beta releases, building a free-threaded Cython extension module
on Windows is tricky because Python provides a single header file shared between the
Freethreading and regular builds.  You therefore need to manually define the C
macro ``Py_GIL_DISABLED=1``.

Cython attempts to detect cases where this wasn't done correctly and will try to raise
an ``ImportError`` instead of crashing.  However - if you are seeing crashes immediately
after you import a Cython extension module, this is the most likely explanation.

Thread safety
-------------

Cython extension modules don't yet try to ensure any significant level of thread safety.
This means that if you have multiple threads both manipulating an object attribute of a
``cdef class`` (for example) then it is likely that the reference counting will end up
inconsistent and the interpreter will crash.

.. note::

   When running pure Python code directly in the Python interpreter itself, the
   interpreter should ensure that reference counting is at least consistent and
   that the interpreter does not crash.  Cython doesn't currently even go this far.
   
   By itself "not crashing" is not a useful level of thread safety for most algorithms.
   It will always be your own responsibility to use appropriate synchronization
   mechanisms so that your own algorithms work as you intend.

Running concurrent Cython functions that do not interact with the same data is
expected to be safe.

What is likely to be extremely unsafe is code like::

    for idx in cython.parallel.prange(n, nogil=True):
        with gil:
            ...

In regular non-free-threaded builds only one thread will run the ``with gil`` block
at once.  In free-threaded builds multiple threads will be able to run simultaneously.
It is extremely likely that these multiple threads will be operating on the same
data in unsafe ways.  We recommend against this kind of code in Freethreading builds
at the moment (and even with future improvements in Cython, such code is likely
to require extreme care to make it work correctly).

.. note::

   It is a common mistake to assume that a ``with gil`` block runs "atomically"
   (i.e. all in one go, without switching to another thread) on non-free-threaded builds.
   Many operations can cause the GIL to be released. Some more detail is in the section
   :ref:`gil_as_lock`.
