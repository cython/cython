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
same guarantees simply from the fact you hold the GIL.  Our current experience is
that this provides slightly less thread-safety than you get in freethreading builds
simply because Python releases the GIL more readily than it releases a critical
section.

Locks
-----

Cython provides ``cython.pymutex`` as a more robust lock type.  Unlike
``cython.critical_section`` this will never release the lock unless you explicitly
ask it to (at the cost of losing ``critical_section``'s inbuilt protection against
deadlocks).

``cython.pymutex`` supports two operations: ``acquire`` and ``release``.
``cython.pymutex`` can also be used in a ``with`` statement::

  cdef cython.pymutex l
  with l:
      ...  # perform operations with the lock
  
  # or manually
  l.acquire()
  ...  # perform operations with the lock
  l.release()

``acquire`` will avoid deadlocks if the GIL is held (only relevant in 
non-freethreading versions of Python).  However, you are at risk of deadlock
if you attempt to acquire the GIL while holding a ``cython.pymutex`` lock.
Be aware that it is also possible for Cython to acquire the GIL implicitly
(for example by raising an exception) and this is also a deadlock risk.

On Python 3.13+, ``cython.pymutex`` is just a
`PyMutex <https://docs.python.org/3.13/c-api/init.html#synchronization-primitives>`_
and so is very low-cost.  On earlier versions of Python, it uses the
(undocumented) ``PyThread_type_lock``.

``cython.pythread_type_lock`` exposes the same interface but always
uses ``PyThread_type_lock``.  It is intended for sharing locks between
modules with the Limited API (since ``PyMutex`` is unavailable in the
Limited API).  Note that unlike the "raw" ``PyThread_type_lock`` our
wrapping will avoid deadlocks with the GIL.

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


Opinionated Suggestions
=======================

This section contains our views on how to use Cython effectively with free-threaded
Python.  It may evolve as our understanding grows.

Interaction between threads
---------------------------

Multi-threaded programs generally work best if you can minimize the interaction between
threads. It's optimal if the different threads perform completely isolated
blocks of work which are only collected at the end.  Python code is no exception -
especially since Python's reference counting means that even apparent "read-only"
operations can actually involve both reading and writing.

As an example consider a program that collects unique words from multiple files.
In this case it would probably be best to read each file to a separate ``set``
and then combine them at the end::

  def read_from_files_good(filenames):
    def read_from_file(filename):
      out = set()
      with open(filename, 'r') as f:
        for line in f:
          words = line.split()
          for word in words:
            out.add(word)
      return out

    overall_result = set()
    with concurrent.futures.ThreadPoolExecutor() as executor:
      for file_result in executor.map(read_from_file, filenames):
        overall_result.update(file_result)
    return overall_result

rather than updating one ``set`` from all threads::

  def read_from_files_bad(filenames):
    overall_result = set()

    def read_from_file(filename):
      with open(filename, 'r') as f:
        for line in f:
          words = line.split()
          for word in words:
            overall_result.add(word)

    with concurrent.futures.ThreadPoolExecutor() as executor:
      for _ in executor.map(read_from_file, filenames):
        pass
    return overall_result

The less your threads interact, the less chance there is for bugs, the less
need there is for locking to control their interaction, and the less likely
they are to slow each other down by invaliding the CPU cache for other
threads.

Should you use ``prange``?
--------------------------

Although ``prange`` is the parallelization mechanism *built in* to Cython, it
is not the only option, and probably should not be your default option.

``prange`` is a fairly thin wrapper over OpenMP's "parallel for".  This means
it is ideal for problems where you have a big loop, every iteration is basically
the same, and the result of each iteration is independent of any other iteration.
If this does *not* describe your problem then ``prange`` is probably not the solution.

Remember that all the threading options available in Python are also available
in Cython.  For example, you can start threads with ``threading.Thread`` or
``concurrent.futures.ThreadPoolExecutor``. They are much more flexible than
``prange``.  Similarly, the synchronization tools in ``threading.Thread``
are also available in Cython.

Try to avoid Python code in ``prange``
--------------------------------------

``prange`` has some slightly unintuitive behaviour about which data is
shared and which isn't.  Typically C variables (e.g. ``int``, ``double``) are
treated as "thread-local" and so each thread has its own copy. However,
Python object variables are treated as shared between all the threads.

This means that::

  cdef int i
  cdef int total = 0
  for i in cython.parallel.prange(10, nogil=True):
    tmp = i**2
    total += tmp

should work fine - each thread has its own ``tmp`` and ``total`` is
a "reduction" (so treated in an efficient thread-safe way).  However::

  cdef int i
  cdef int total = 0
  cdef object tmp
  for i in cython.parallel.prange(10, nogil=True):
    with gil:
      tmp = i**2
      total += tmp

In this case, there is only a single value of ``tmp`` shared between all the threads.
They are continuously overwriting each other's values.  Additionally, Cython does not
currently ensure that ``tmp`` is even reference-counted in a thread-safe way,
so you are at risk of crashes or memory-leaks in addition to getting a nonsense answer.

If you do want to work with Python objects, then it is best to move them into
a function and just have the loop call the function::

  cdef int square(int x):
    cdef object tmp = x**2
    cdef int result = tmp
    return result

  # ...

  cdef int i
  cdef int total = 0
  for i in cython.parallel.prange(10, nogil=True):
    with gil:
      total += square(i)

Since ``tmp`` is now local to the function scope, each function call has its own copy
and thus there is no conflict of Python objects between threads.

Use C++ for low-level synchronization primitives
------------------------------------------------

When you must have threads interact with each other, you usually need to use
special data types to control the access to shared data.  Python provides many of these in the
``threading`` module.  However, sometimes it is useful to either:

* avoid the Python-call overhead of the threading module,
* use atomic variables to update numeric types in a controlled way without locking.

For this our recommendation is to use the C++ standard library.  Most of these
are available simply by "cimporting" from ``libcpp``.  In the event that Cython
hasn't already wrapped what you want to use then you can do it yourself - our
``libcpp`` is provided for convenience but it does nothing that can't be done
with regular Cython code.

The C standard library also provides some of these features (e.g. atomic variables
and mutexes).  However, compiler support for the C++ standard library is better
(in particular for MSVC) and the C++ standard library is more fully featured,
so we recommend this first.

One difficulty is with types that are not default constructable or moveable
(e.g. ``latch``, ``semaphore``, ``barrier``).  These are difficult to
stack-allocate because of how Cython's code-genertion works, so you
need to heap-allocate them::

  from libcpp.latch cimport latch

  l = new latch(2)
  try:
    ...  # use the latch
  finally:
    del l

It is also possible to use C++ to create new threads (for example, using the ``std::jthread``
class).  This works, but we generally recommend creating threads through Python
instead.  For a C++-created thread it's necessary to register them with the interpreter
by calling ``with gil:`` before using any Python objects and this will not work reliably
with multiple subinterpreters - this recommendation is therefore mainly to future-proof
your code and not restrict where it can be used from.  It is a fairly soft suggestion though,
so feel free to ignore it if you have good reason to.

``cython.critical_section`` vs GIL
----------------------------------

Understanding what protection a ``critical_section`` provides is
important to being able to use it safely,  and it's also worth comparing
it to the guarantees that the GIL provides.  Unfortunately some of
this is very much an implementation detail of Python at the moment, so
may be subject to change.

What is guaranteed to be safe for both of ``critical_section`` and
the GIL (on non-freethreading builds) is reading and writing to
``cdef`` attributes of extension types::

  cdef class C:
    cdef object attr

  ...
  
  cdef C c_instance = C()
  with cython.critical_section(c_instance):
    c_instance.attr = something

  with cython.critical_section(c_instance):
    something = c_instance.attr

The first and most obvious place that both a ``critical_section`` and
the GIL can be interrupted is a ``with nogil:`` block.  This is hopefully
absolutely obvious for the GIL but it's worth noting that a critical
section only applies when the Python thread state is held.

In principle, both a ``critical_section`` and the GIL can be interrupted
by executing arbitrary Python code.  Arbitrary Python code can notably
include the finalizers of any objects being destroyed.  This means that
reassigning a Python attribute can trigger arbitrary code (but typically
only after the new value has been put in place).  Additionally, triggering
the GC can result in arbitrary code being executed. On Python <3.12 any
Python memory allocation can trigger the GC so be wary of this if you
aim to support multithreading in those versions (the first free-threaded
interpreters were in Python 3.13 so the GC is harder to trigger from
Cython code in them).

For example, in the following code (which uses the definition of ``C`` from
the previous example)::

  with cython.critical_section(c_instance):
    c_instance.attr = c_instance.attr + 1

the addition gets expanded to something like

.. code-block:: C

  temp1 = c_instance->attr;

  // May trigger arbitrary Python code:
  // 1. If ``temp1`` is a class with an "__add__" method
  // 2. If the allocation of the result triggers the GC on Python <3.12
  temp2 = PyNumber_Add(temp1, const_1);

  // this section is hidden inside a ``Py_SETREF`` or similar
  {
    temp3 = c_instance->attr; 
    c_instance->attr = temp2;
    // May trigger arbitrary Python code through finalizers
    Py_DECREF(temp3);
  }

(we show normal addition rather than in-place addition for ease
of explanation, but the result is similar).

Practically there are some differences between ``critical_section`` 
and the GIL:

* Releasing the GIL happens at fairly regular intervals after
  a certail number of bytecode instructions.
* Interrupting a ``critical_section`` only happens if the interpreter
  hits a deadlock (i.e. some other operation tries to get a critical
  section on the same object).

The upshot is the if you're sure that no other code will have a
reference to ``c_instance`` the example above is safe in a free-threaded
interpreter (although arbitrary code may run, it won't interact with
``c_instance``) but unsafe in a GIL-enabled interpreter.

As an example of some practical results:

* if ``c_instance`` is a Python integer the the code above *seems* to
  execute correctly (i.e. gives the expected answer consistently)
  in both free-threaded and GIL builds
  (although this was in a simplified test where no garbage was
  available to collect).
* if ``c_instance`` was a ``fractions.Fraction`` object the code above
  consistently gives the expected answer in freethreaded builds
  build not in GIL builds. ``fractions.Fraction.__add__`` will
  execute arbitrary code, but not code that interferes with the
  ``critical_section``.  Again, beware the caveat that our
  simplified test had no garbage to collect.

However, be wary of code like::

  cdef class C:
    cdef object attr

    cdef void add_one(self):
      with cython.critical_section(self):
        self.attr += 1
  
  ...

  c_instance = C()
  with cython.critical_section(c_instance):
    ...
    c_instance.add_one()
    ...

The nested ``critical_section`` blocks represent a potential
deadlock so may interrupt the outer ``critical_section``.

Avoid ``cython.critical_section`` on non-extension types
--------------------------------------------------------

Python-attribute access does hit a deadlock and will interrupt
the ``critical_section``. The code below will return incorrect
results on both free-threading and GIL builds::

  # regular class
  class C:
    def __init__(self):
      self.attr = 1

  ...
  
  c_instance = C()
  with cython.critical_section(c_instance):
    c_instance.attr += 1