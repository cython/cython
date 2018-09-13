.. highlight:: cython

.. _debugging:

**********************************
Debugging your Cython program
**********************************

Cython comes with an extension for the GNU Debugger that helps users debug
Cython code. To use this functionality, you will need to install gdb 7.2 or
higher, built with Python support (linked to Python 2.6 or higher).
The debugger supports debuggees with versions 2.6 and higher. For Python 3,
code should be built with Python 3 and the debugger should be run with
Python 2 (or at least it should be able to find the Python 2 Cython
installation). Note that in recent versions of Ubuntu, for instance, ``gdb``
installed with ``apt-get`` is configured with Python 3. On such systems, the
proper configuration of ``gdb`` can be obtained by downloading the ``gdb``
source, and then running::

    ./configure --with-python=python2
    make
    sudo make install

The debugger will need debug information that the Cython compiler can export.
This can be achieved from within the setup script by passing ``gdb_debug=True``
to ``cythonize()``::

    from distutils.core import setup
    from distutils.extension import Extension

    extensions = [Extension('source', ['source.pyx'])]

    setup(..., ext_modules=cythonize(extensions, gdb_debug=True))

For development it's often helpful to pass the ``--inplace`` flag to
the ``setup.py`` script, which makes distutils build your project
"in place", i.e., not in a separate `build` directory.

When invoking Cython from the command line directly you can have it write
debug information using the ``--gdb`` flag::

    cython --gdb myfile.pyx

Running the Debugger
=====================
.. highlight:: bash

To run the Cython debugger and have it import the debug information exported
by Cython, run ``cygdb`` in the build directory::

    $ python setup.py build_ext --inplace
    $ cygdb
    GNU gdb (GDB) 7.2
    ...
    (gdb)

When using the Cython debugger, it's preferable that you build and run your code
with an interpreter that is compiled with debugging symbols (i.e. configured
with ``--with-pydebug`` or compiled with the ``-g`` CFLAG). If your Python is
installed and managed by your package manager you probably need to install debug
support separately. If using NumPy then you also need to install numpy debugging, or you'll
see an `import error for multiarray <https://bugzilla.redhat.com/show_bug.cgi?id=1030830>`_.
E.G. for ubuntu::

    $ sudo apt-get install python-dbg python-numpy-dbg
    $ python-dbg setup.py build_ext --inplace

Then you need to run your script with ``python-dbg`` also. Ensure that when
building your package with debug symbols that cython extensions are re-compiled
if they had been previously compiled. If your package is version controlled, you
might want to perform ``git clean -fxd`` or ``hg purge --all`` before building.

You can also pass additional arguments to gdb::

    $ cygdb /path/to/build/directory/ GDBARGS

i.e.::

    $ cygdb . -- --args python-dbg mainscript.py

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
        (gdb) cy break packagename.cython_module.cython_function
        (gdb) cy break packagename.cython_module.ClassName.cython_method
        (gdb) cy break c_function

    You can also break on Cython line numbers::

        (gdb) cy break :14
        (gdb) cy break cython_module:14
        (gdb) cy break packagename.cython_module:14

    Python breakpoints currently support names of the module (not the entire
    package path) and the function or method::

        (gdb) cy break -p python_module.python_function_or_method
        (gdb) cy break -p python_function_or_method

.. note:: Python breakpoints only work in Python builds where the Python frame
          information can be read from the debugger. To ensure this, use a
          Python debug build or a non-stripped build compiled with debug
          support.

.. function:: cy step

    Step through Python, Cython or C code. Python, Cython and C functions
    called directly from Cython code are considered relevant and will be
    stepped into.

.. function:: cy next

    Step over Python, Cython or C code.

.. function:: cy run

    Run the program. The default interpreter is the interpreter that was used
    to build your extensions with, or the interpreter ``cygdb`` is run with
    in case the "don't import debug information" option was in effect.
    The interpreter can be overridden using gdb's ``file`` command.

.. function:: cy cont

    Continue the program.

.. function:: cy up
              cy down

    Go up and down the stack to what is considered a relevant frame.

.. function:: cy finish

    Execute until an upward relevant frame is met or something halts
    execution.

.. function:: cy bt
              cy backtrace

    Print a traceback of all frames considered relevant. The ``-a`` option
    makes it print the full traceback (all C frames).

.. function:: cy select

    Select a stack frame by number as listed by ``cy backtrace``. This
    command is introduced because ``cy backtrace`` prints a reversed stack
    trace, so frame numbers differ from gdb's ``bt``.

.. function:: cy print varname

    Print a local or global Cython, Python or C variable (depending on the
    context). Variables may also be dereferenced::

        (gdb) cy print x
        x = 1
        (gdb) cy print *x
        *x = (PyObject) {
            _ob_next = 0x93efd8,
            _ob_prev = 0x93ef88,
            ob_refcnt = 65,
            ob_type = 0x83a3e0
        }

.. function:: cy set cython_variable = value

    Set a Cython variable on the Cython stack to value.

.. function:: cy list

    List the source code surrounding the current line.

.. function:: cy locals
              cy globals

    Print all the local and global variables and their values.

.. function:: cy import FILE...

    Import debug information from files given as arguments. The easiest way to
    import debug information is to use the cygdb command line tool.

.. function:: cy exec code

    Execute code in the current Python or Cython frame. This works like
    Python's interactive interpreter.

    For Python frames it uses the globals and locals from the Python frame,
    for Cython frames it uses the dict of globals used on the Cython module
    and a new dict filled with the local Cython variables.

.. note:: ``cy exec`` modifies state and executes code in the debuggee and is
          therefore potentially dangerous.

Example::

    (gdb) cy exec x + 1
    2
    (gdb) cy exec import sys; print sys.version_info
    (2, 6, 5, 'final', 0)
    (gdb) cy exec
    >global foo
    >
    >foo = 'something'
    >end

Convenience functions
=====================
The following functions are gdb functions, which means they can be used in a
gdb expression.

.. function:: cy_cname(varname)

    Returns the C variable name of a Cython variable. For global
    variables this may not be actually valid.

.. function:: cy_cvalue(varname)

    Returns the value of a Cython variable.

.. function:: cy_eval(expression)

    Evaluates Python code in the nearest Python or Cython frame and returns
    the result of the expression as a gdb value. This gives a new reference
    if successful, NULL on error.

.. function:: cy_lineno()

    Returns the current line number in the selected Cython frame.

Example::

    (gdb) print $cy_cname("x")
    $1 = "__pyx_v_x"
    (gdb) watch $cy_cvalue("x")
    Hardware watchpoint 13: $cy_cvalue("x")
    (gdb) cy set my_cython_variable = $cy_eval("{'spam': 'ham'}")
    (gdb) print $cy_lineno()
    $2 = 12


Configuring the Debugger
========================
A few aspects of the debugger are configurable with gdb parameters. For
instance, colors can be disabled, the terminal background color
and breakpoint autocompletion can be configured.

.. c:macro:: cy_complete_unqualified

    Tells the Cython debugger whether ``cy break`` should also complete
    plain function names, i.e. not prefixed by their module name.
    E.g. if you have a function named ``spam``,
    in module ``M``, it tells whether to only complete ``M.spam`` or also just
    ``spam``.

    The default is true.

.. c:macro:: cy_colorize_code

    Tells the debugger whether to colorize source code. The default is true.

.. c:macro:: cy_terminal_background_color

    Tells the debugger about the terminal background color, which affects
    source code coloring. The default is "dark", another valid option is
    "light".

This is how these parameters can be used::

    (gdb) set cy_complete_unqualified off
    (gdb) set cy_terminal_background_color light
    (gdb) show cy_colorize_code
