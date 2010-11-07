.. highlight:: cython

.. _debugging:

**********************************
Debugging your Cython program
**********************************

Cython comes with an extension for the GNU Debugger that helps users debug 
Cython code. To use this functionality, you will need to install gdb 7.2 or
higher, build with Python support (linked to Python 2.5 or higher). 

The debugger will need debug information that the Cython compiler can export.
This can be achieved from within the setup
script by passing ``pyrex_debug=True`` to your Cython Extenion class::

    from Cython.Distutils import extension
    
    ext = extension.Extension('source', 'source.pyx', pyrex_debug=True)
    setup(..., ext_modules=[ext)]

With this approach debug information can be enabled on a per-module basis.
Another (easier) way is to simply pass the ``--pyrex-debug`` flag as a command
line argument::

    python setup.py build_ext --pyrex-debug

For development it's often easy to use the ``--inplace`` flag also, which makes
distutils build your project "in place", i.e., not in a separate `build`
directory.

When invoking Cython from the command line directly you can have it write
debug information using the ``--debug`` flag::

    cython --debug myfile.pyx

.. note:: The debugger is new in the upcoming release of Cython, 0.13.1.
          Currently, it can be cloned from hg.cython.org/cython-gdb.

Running the Debugger
=====================
.. highlight:: bash

To run the Cython debugger and have it import the debug information exported 
by Cython, run ``cygdb`` in the build directory::

    $ python setup.py build_ext --pyrex-debug --inplace
    $ cygdb
    GNU gdb (GDB) 7.2
    ...
    (gdb)

When using the Cython debugger, it's preferable that you build and run your code
with an interpreter that is compiled with debugging symbols (i.e. configured
with ``--with-pydebug`` or compiled with the ``-g`` CFLAG). If your Python is 
installed and managed by your package manager you probably need to install debug
support separately, e.g. for ubuntu::

    $ sudo apt-get install python-dbg
    $ python-dbg setup.py build_ext --pyrex-debug --inplace

Then you need to run your script with ``python-dbg`` also.

You can also pass additional arguments to gdb::

    $ cygdb /path/to/build/directory/ GDBARGS

i.e.::
    
    $ cygdb . --args python-dbg mainscript.py

To tell cygdb not to import any debug information, supply ``--`` as the first
argument::

    $ cygdb --

Using the Debugger
===================
The Cython debugger comes with a set of commands that support breakpoints,
stack inspection, source code listing, stepping, stepping over, etc. Most
of these commands are analogous to their respective gdb command.

.. function:: cy break breakpoints...
    
    Break in a Python, Cython or C function. First it will look for a Cython
    function with that name, if cygdb doesn't know about a function (or method)
    with that name, it will set a (pending) C breakpoint. The ``-p`` option can
    be used to specify a Python breakpoint.

    Breakpoints can be set for either the function or method name, or they can
    be fully "qualified", which means that the entire "path" to a function is
    given::

        (gdb) cy break cython_function_or_method
        (gdb) cy break packagename.modulename.cythonfunction
        (gdb) cy break packagename.modulename.ClassName.cythonmethod
        (gdb) cy break c_function

    You can also break on Cython line numbers::

        (gdb) cy break packagename.modulename:14
        (gdb) cy break :14

    Python breakpoints currently support names of the module (not the entire
    package path) and the function or method::

        (gdb) cy break -p pythonmodule.python_function_or_method
        (gdb) cy break -p python_function_or_method

.. function:: cy step

    Step through Python, Cython or C code. Python, Cython and C functions
    called directly from Cython code are considered relevant and will be
    stepped into.

.. function:: cy next

    Step over Python, Cython or C code.

.. function:: cy run
    
    Run the program. The default interpreter is the interpreter cygdb is run
    with (but can be overridden using gdb's ``file`` command).

.. function:: cy cont

    Continue the program.

.. function:: cy up
              cy down

    Go up and down the stack to what is considered a relevant frame.

.. function:: cy bt
              cy backtrace

    Print a traceback of all frames considered relevant. The ``-a`` option
    makes it print the full traceback (all C frames).

.. function:: cy print varname

    Print a local or global Cython, Python or C variable (depending on the 
    context).

.. function:: cy list

    List the source code surrounding the current line.

.. function:: cy locals
              cy globals

    Print all the local and global variables and their values.

.. function:: cy import FILE...

    Import debug information from files given as arguments. The easiest way to
    import debug information is to use the cygdb command line tool.

