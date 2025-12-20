"Where does that C code come from?"
===================================

Most often, when you are new to Cython development, you have an idea about the Cython code you want to debug.
So, looking at the generated C code, your main question will be: »where is that C code generated?«.

One simple and useful feature to help you start: by default Cython injects the source
Python code into the C code as comments in the form:

.. code-block:: c

    /* "source_file.pyx":2
     * def print_hello():
     *    print("Hello world")       # <<<<<<<<<<<<<<
     */
    
    __pyx_t_1 = /* some complicated C expression */;

so searching the generated C code file for the line of Python/Cython code you're interested in can be
a good place to start.  Some lines may appear in more than one place.  For example, functions appear
in both the implementation of the function and the place where it's added to the module namespace.

To get more detail, the Cython compiler has a couple of debug features that you
can use to pin-point the relevant code sections. They can be enabled in
the module `Cython.Compiler.DebugFlags <https://github.com/cython/cython/blob/master/Cython/Compiler/DebugFlags.py>`_.
Read the comments in that file, enable the relevant debug features
(usually ``debug_trace_code_generation`` to get started), and then
read the C code that Cython generates to find out what is going on.

One trick to identify the origin of a specific line of C code is
to use the Python debugger to stop when that specific line is
written by adding a conditional breakpoint to stop on that line to the
``CCodeWriter.write`` function in Code.py.  From there you can go up
the call stack and investigate it "live".
