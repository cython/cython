.. _The Test Suite:

The Test Suite
==============

A very good place to start understanding Cython is the `test suite <https://github.com/cython/cython/tree/master/tests/>`_, 
which lives in the "tests" directory of the source repository. The tests (collected and run by
`runtests.py <https://github.com/cython/cython/blob/master/runtests.py>`_)
mostly use the `doctest module <https://docs.python.org/3/library/doctest.html>`_ of Python.
They contain lots of little examples that Cython can compile, so if you want to understand a specific part of 
Cython or make a new feature work, it is a very good idea to look out for a related test case or to
write one yourself, and then run Cython in a code coverage tool or debugger to see what happens.
You run the test suite with this command:

.. code-block:: bash

    python runtests.py -vv

As before, there's no need to compile or install Cython; just run this from the checked-out Git
repository.  To select a specific test (or a set of tests), just pass the name(s) as parameters.
You can also pass regular expressions or tags in the form ``tag:value``.
The testrunner takes many options, see ``python runtests.py --help``.
To enable only C++ tests (and C tests in C++ mode), for example, pass ``--backends=cpp``.

Another useful thing to know is that setting CFLAGS to ``-O0`` or ``-Og``
can nearly half the runtime of the tests, as it disables all costly optimisations done by the C compiler.

Tags
----

Tests can be tagged for easy filtering and running. A tag is simply a comment,
which must occur before any other non-whitespace non-comment lines, of the 
form ``#tag: value``. Some tags have special meaning, for example ``tag:cpp`` tests are only compiled in C++.
Multiple values for a single tag can be separated by commas or given in repeated tag lines.

Tests
-----

There are three different kinds of tests:

* compile: tests that are only compiled, not run
* errors: tests that check for compile errors
* run: tests that are compiled and run using doctest

These are distinguished by a ``mode`` tag comment at the top of the file, which defaults to run if not given.

A test consists of a .pyx file that Cython compiles, possibly accompanied by a couple of .pxd or
header files in the same directory.  More complicated cases use a ``.srctree`` file which is broken by the
test runner into a set of files, and the commands at the top are run as the test.  We don't recommend
``.srctree`` tests unless necessary because they are less well integrated into the test system and are
slower to run.
Error tests additionally contain an error description, as in this example:

.. code-block:: cython

    # mode: error

    cdef extern from *:
        void foo(void)

    _ERRORS = u"""
    4:13:Use spam() rather than spam(void) to declare a function with no arguments.
    """

This is regular Cython code, so you can compile this file yourself to see the error.
However, the test runner splits the source file at the line starting with "_ERRORS" and parses the
rest of the file for error output. That includes all lines that follow a "LINE:COLUMN:error message" scheme.
The error lines are then compared against the actual output of the compiler run.

Runnable tests in the "tests/run/" directory use doctests, as in the following example:

.. code-block:: cython

    # mode: run

    def f():
        """
        This doctest runs in plain Python:

        >>> 1 + 2
        3
        >>> f()
        3
        >>> b
        3
        """
        # this is code that Cython executes when the doctest calls the function:

        a = 1 + 2
        return a

    # this is code that Cython executes at module initialisation time:

    b = 1 + 2

The important thing to know here is that the doctest will be executed by Python,
while the rest of the file will be compiled to C code by Cython and only called by the doctest
when run by the test runner. So you can directly compare results that Python delivers with results that you get from Cython.

If you are trying to match Python behaviour, it's often a good idea to write the test as a ``.py``
file rather than a ``.pyx`` file.  These will get run uncompiled in Python too so serve as a
useful cross-check.

Parse tree assertions
---------------------

A useful feature for testing optimisations that only impact the performance and do not change the 
behaviour is to add parse tree assertions.
Otherwise, it would be impossible to tell if an optimisation strikes or not,
thus rendering the test useless if the optimisation ever fails to apply for some reason.

You can express assertions using a simple ``XPath``-like language called ``TreePath`` that traverses the parse tree.
Nodes are referred to by their type name (inheritance is not considered). 
For example, to make sure that a Python function call "``foo()``" gets replaced by a C-API call to "``c_foo()``",
you can write a test as follows:

.. code-block:: cython

    # mode: run

    cimport cython

    @cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'foo']")
    @cython.test_assert_path_exists("//SimpleCallNode//NameNode[@name = 'c_foo']")
    def f():
        foo()

As known from XPath, you can use

* NodeName for a Node of type NodeName
* ``*`` for a Node of any type
* ``@name`` for an attribute value
* ``//`` to descend into a subtree
* `/`` to access a direct child
* ``.`` to refer to the current node
* ``[ ... ]`` to evaluate a predicate (which itself is a TreePath expression) at the current node
* ``[@name = value]`` to compare an attribute value (integer values, "string", 'string' and boolean True/False are supported)
* ``[... and ...]`` to connect two predicates with a boolean 'and'

The `TestTreePath module <https://github.com/cython/cython/blob/master/Cython/Compiler/Tests/TestTreePath.py>`_
contains some examples of accepted path expressions.

To test for more than one path, you can pass multiple path strings to each decorator.
It is good practice to add partial paths before the complete test path, as this leads to
better error messages if a subtree exists but does not fulfill the entire
expression - especially if there is overlap with a fail-if path. Example:

.. code-block:: cython

    #mode: run

    cimport cython

    @cython.test_fail_if_path_exists("//SimpleCallNode//NameNode[@name = 'foo']")
    @cython.test_assert_path_exists("//SimpleCallNode//NameNode",
                                    "//SimpleCallNode//NameNode[@name = 'c_foo']")
    def f():
        foo()

The test runner script (see below) enables the tree assertions in the test run,
but they are otherwise disabled in the normal compiler runs.

Note that the TreePath language is not a complete XPath implementation, so conditions are restricted
to node/attribute tests and simple string comparisons for attribute values.

Running the CPython test suite
------------------------------

To test the compatibility with CPython (the standard Python impleentation),
you can copy the directory ``Lib/test`` in the Python source distribution over
to the directory ``tests/pyregr`` (not into this directory, as this directory!)
in the Cython source tree. The test runner will then compile all unit test modules with Cython and run them.

To avoid doing this over and over for different CPython versions, there
is an option --sys-pyregr that you can pass to the test runner. If the installation of the
running Python version contains the regression test package (simply called 'test'),
the test runner will pick it up from the standard library automatically.
However, note that many Python distributions do not include this package.

Tip to create doctest scripts
-----------------------------

The doctest scripts have executable statements and output interleaved. It is possible to
type the test program directly into python and copy/paste the output but when the
sequence of statements is more than a few lines, it can be convenient to use a text editor to prepare them.

One useful technique to aid in this is to use the "screen" program to run a text
file with the doctest snippet to be run. Screen can be instructed to read the text file
and send it to python. The output can then be captured and placed into the doctest file. See the man page for screen on your system.

Some example steps to do this:

* Use your favorite text editor to create a file, say "t", with the code to run.
* Start screen in the same directory.
* Start an interactive python session by typing it on a line.
* To read the file into a screen buffer, type the command line: ``* <ctl-a>:readbuf t<ENTER>``
* Paste the buffer into python by typing the characters: ``* <ctl-a>]``
* Save the screen "hardcopy output" to a file named "hardcopy.0" by typing the characters: ``* <ctl-a>h``
* Exit screen
* Edit the output of hardcopy.0 and paste the appropriate script into your doctest.
* Alternatively, just turn on logging for your window to a file "screenlog.0" by typing the characters: ``* <ctl-a>H``
* By using logging, you can reuse the session iteratively and just look at the bottom of the log file for the current output.
  Further, you can rerun the readbuf command quickly from the screen window history by just typing
  the characters (if it is the last command): ``* <ctl-a>:<up-arrow><ENTER> *`` or typing: ``<ctl-a>:<ctl-p><ENTER>``

Debugging failures in the Cython test suite
-------------------------------------------

If you want to see the C code generated when running the test-suite pass 
``--no-cleanup`` to ``runtests.py``.  This leaves the generated code in
the directory ``TEST_TMP`` for inspection after the test runner finishes.
If you want to run the compiled modules yourself after the test-suite
finishes then pass ``--no-cleanup-sharedlibs`` to leave those in ``TEMP_TMP``
too.

Sometimes you may want to run the test-suite in the Python debugger
(for example, you may want to insert a breakpoint at a useful point in
Cython).  In this case pass ``--no-capture`` to ``runtests.py`` (and
don't run the test suite in parallel!).

Finally, if things are going really badly, you may want to run the
test suite in the C debugger (usually to investigate errors in the
generated code).  In this case you need to make sure the tests are
compiled in debug mode.  For gcc/gdb start Python in the C debugger
with:

.. code-block:: bash

    CFLAGS="-O0 -Og" gdb python3

and then in gdb run

.. code-block:: bash

    run runtests.py <arguments go here> test_you_are_interested_in

If you're running Python installed as part of a Linux distribution, then 
``debuginfod`` can be useful to fetch the debug symbols for Python itself making
it easier to investigate crashes that happen in Python C API calls.
