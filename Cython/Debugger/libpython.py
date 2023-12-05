#!/usr/bin/python

import sys

if sys.version_info[0] == 3:
    if sys.version_info[1] == 4:
        from .vendored.libpython34 import *
    elif sys.version_info[1] == 5:
        from .vendored.libpython35 import *
    elif sys.version_info[1] == 6:
        from .vendored.libpython36 import *
    elif sys.version_info[1] == 7:
        from .vendored.libpython37 import *
    elif sys.version_info[1] == 8:
        from .vendored.libpython38 import *
    elif sys.version_info[1] == 9:
        from .vendored.libpython39 import *
    elif sys.version_info[1] == 10:
        from .vendored.libpython310 import *
    elif sys.version_info[1] == 1:
        from .vendored.libpython311 import *
    elif sys.version_info[1] >= 12:
        from .vendored.libpython312 import *
else:
    raise RuntimeError("cython debugger only works in 3.x series")


##################################################################
## added, not in CPython
##################################################################

import re
import warnings
import tempfile
import functools
import textwrap
import itertools
import traceback


def dont_suppress_errors(function):
    "*sigh*, readline"
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise

    return wrapper

class PyGlobals(gdb.Command):
    'List all the globals in the currently select Python frame'
    def __init__(self):
        gdb.Command.__init__ (self,
                              "py-globals",
                              gdb.COMMAND_DATA,
                              gdb.COMPLETE_NONE)

    @dont_suppress_errors
    def invoke(self, args, from_tty):
        name = str(args)

        frame = Frame.get_selected_python_frame()
        if not frame:
            print('Unable to locate python frame')
            return

        pyop_frame = frame.get_pyop()
        if not pyop_frame:
            print(UNABLE_READ_INFO_PYTHON_FRAME)
            return

        for pyop_name, pyop_value in pyop_frame.iter_locals():
            print('%s = %s'
                   % (pyop_name.proxyval(set()),
                      pyop_value.get_truncated_repr(MAX_OUTPUT_LEN)))

    def get_namespace(self, pyop_frame):
        return pyop_frame.iter_globals()


PyGlobals()

# This function used to be a part of CPython's libpython.py (as a member function of frame).
# It isn't anymore, so I copied it.
def is_evalframeex(frame):
    '''Is this a PyEval_EvalFrameEx frame?'''
    if frame._gdbframe.name() == 'PyEval_EvalFrameEx':
        '''
        I believe we also need to filter on the inline
        struct frame_id.inline_depth, only regarding frames with
        an inline depth of 0 as actually being this function

        So we reject those with type gdb.INLINE_FRAME
        '''
        if frame._gdbframe.type() == gdb.NORMAL_FRAME:
            # We have a PyEval_EvalFrameEx frame:
            return True

    return False

class PyNameEquals(gdb.Function):

    def _get_pycurframe_attr(self, attr):
        frame = Frame(gdb.selected_frame())
        if is_evalframeex(frame):
            pyframe = frame.get_pyop()
            if pyframe is None:
                warnings.warn("Use a Python debug build, Python breakpoints "
                              "won't work otherwise.")
                return None

            return getattr(pyframe, attr).proxyval(set())

        return None

    @dont_suppress_errors
    def invoke(self, funcname):
        attr = self._get_pycurframe_attr('co_name')
        return attr is not None and attr == funcname.string()

PyNameEquals("pyname_equals")


class PyModEquals(PyNameEquals):

    @dont_suppress_errors
    def invoke(self, modname):
        attr = self._get_pycurframe_attr('co_filename')
        if attr is not None:
            filename, ext = os.path.splitext(os.path.basename(attr))
            return filename == modname.string()
        return False

PyModEquals("pymod_equals")


class PyBreak(gdb.Command):
    """
    Set a Python breakpoint. Examples:

    Break on any function or method named 'func' in module 'modname'

        py-break modname.func

    Break on any function or method named 'func'

        py-break func
    """

    @dont_suppress_errors
    def invoke(self, funcname, from_tty):
        if '.' in funcname:
            modname, dot, funcname = funcname.rpartition('.')
            cond = '$pyname_equals("%s") && $pymod_equals("%s")' % (funcname,
                                                                    modname)
        else:
            cond = '$pyname_equals("%s")' % funcname

        gdb.execute('break PyEval_EvalFrameEx if ' + cond)

PyBreak("py-break", gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE)


class _LoggingState:
    """
    State that helps to provide a reentrant gdb.execute() function.
    """

    def __init__(self):
        f = tempfile.NamedTemporaryFile('r+')
        self.file = f
        self.filename = f.name
        self.fd = f.fileno()
        _execute("set logging file %s" % self.filename)
        self.file_position_stack = []

    def __enter__(self):
        if not self.file_position_stack:
            _execute("set logging redirect on")
            _execute("set logging on")
            _execute("set pagination off")

        self.file_position_stack.append(os.fstat(self.fd).st_size)
        return self

    def getoutput(self):
        gdb.flush()
        self.file.seek(self.file_position_stack[-1])
        result = self.file.read()
        return result

    def __exit__(self, exc_type, exc_val, tb):
        startpos = self.file_position_stack.pop()
        self.file.seek(startpos)
        self.file.truncate()
        if not self.file_position_stack:
            _execute("set logging off")
            _execute("set logging redirect off")
            _execute("set pagination on")


def execute(command, from_tty=False, to_string=False):
    """
    Replace gdb.execute() with this function and have it accept a 'to_string'
    argument (new in 7.2). Have it properly capture stderr also. Ensure
    reentrancy.
    """
    if to_string:
        with _logging_state as state:
            _execute(command, from_tty)
            return state.getoutput()
    else:
        _execute(command, from_tty)


_execute = gdb.execute
gdb.execute = execute
_logging_state = _LoggingState()


def get_selected_inferior():
    """
    Return the selected inferior in gdb.
    """
    # Woooh, another bug in gdb! Is there an end in sight?
    # http://sourceware.org/bugzilla/show_bug.cgi?id=12212
    return gdb.inferiors()[0]

    selected_thread = gdb.selected_thread()

    for inferior in gdb.inferiors():
        for thread in inferior.threads():
            if thread == selected_thread:
                return inferior


def source_gdb_script(script_contents, to_string=False):
    """
    Source a gdb script with script_contents passed as a string. This is useful
    to provide defines for py-step and py-next to make them repeatable (this is
    not possible with gdb.execute()). See
    http://sourceware.org/bugzilla/show_bug.cgi?id=12216
    """
    fd, filename = tempfile.mkstemp()
    f = os.fdopen(fd, 'w')
    f.write(script_contents)
    f.close()
    gdb.execute("source %s" % filename, to_string=to_string)
    os.remove(filename)


def register_defines():
    source_gdb_script(textwrap.dedent("""\
        define py-step
        -py-step
        end

        define py-next
        -py-next
        end

        document py-step
        %s
        end

        document py-next
        %s
        end
    """) % (PyStep.__doc__, PyNext.__doc__))


def stackdepth(frame):
    "Tells the stackdepth of a gdb frame."
    depth = 0
    while frame:
        frame = frame.older()
        depth += 1

    return depth


class ExecutionControlCommandBase(gdb.Command):
    """
    Superclass for language specific execution control. Language specific
    features should be implemented by lang_info using the LanguageInfo
    interface. 'name' is the name of the command.
    """

    def __init__(self, name, lang_info):
        super().__init__(
                                name, gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE)
        self.lang_info = lang_info

    def install_breakpoints(self):
        all_locations = itertools.chain(
            self.lang_info.static_break_functions(),
            self.lang_info.runtime_break_functions())

        for location in all_locations:
            result = gdb.execute('break %s' % location, to_string=True)
            yield re.search(r'Breakpoint (\d+)', result).group(1)

    def delete_breakpoints(self, breakpoint_list):
        for bp in breakpoint_list:
            gdb.execute("delete %s" % bp)

    def filter_output(self, result):
        reflags = re.MULTILINE

        output_on_halt = [
            (r'^Program received signal .*', reflags|re.DOTALL),
            (r'.*[Ww]arning.*', 0),
            (r'^Program exited .*', reflags),
        ]

        output_always = [
            # output when halting on a watchpoint
            (r'^(Old|New) value = .*', reflags),
            # output from the 'display' command
            (r'^\d+: \w+ = .*', reflags),
        ]

        def filter_output(regexes):
            output = []
            for regex, flags in regexes:
                for match in re.finditer(regex, result, flags):
                    output.append(match.group(0))

            return '\n'.join(output)

        # Filter the return value output of the 'finish' command
        match_finish = re.search(r'^Value returned is \$\d+ = (.*)', result,
                                 re.MULTILINE)
        if match_finish:
            finish_output = 'Value returned: %s\n' % match_finish.group(1)
        else:
            finish_output = ''

        return (filter_output(output_on_halt),
                finish_output + filter_output(output_always))

    def stopped(self):
        return get_selected_inferior().pid == 0

    def finish_executing(self, result):
        """
        After doing some kind of code running in the inferior, print the line
        of source code or the result of the last executed gdb command (passed
        in as the `result` argument).
        """
        output_on_halt, output_always = self.filter_output(result)

        if self.stopped():
            print(output_always)
            print(output_on_halt)
        else:
            frame = gdb.selected_frame()
            source_line = self.lang_info.get_source_line(frame)
            if self.lang_info.is_relevant_function(frame):
                raised_exception = self.lang_info.exc_info(frame)
                if raised_exception:
                    print(raised_exception)

            if source_line:
                if output_always.rstrip():
                    print(output_always.rstrip())
                print(source_line)
            else:
                print(result)

    def _finish(self):
        """
        Execute until the function returns (or until something else makes it
        stop)
        """
        if gdb.selected_frame().older() is not None:
            return gdb.execute('finish', to_string=True)
        else:
            # outermost frame, continue
            return gdb.execute('cont', to_string=True)

    def _finish_frame(self):
        """
        Execute until the function returns to a relevant caller.
        """
        while True:
            result = self._finish()

            try:
                frame = gdb.selected_frame()
            except RuntimeError:
                break

            hitbp = re.search(r'Breakpoint (\d+)', result)
            is_relevant = self.lang_info.is_relevant_function(frame)
            if hitbp or is_relevant or self.stopped():
                break

        return result

    def finish(self, *args):
        "Implements the finish command."
        result = self._finish_frame()
        self.finish_executing(result)

    def step(self, stepinto, stepover_command='next'):
        """
        Do a single step or step-over. Returns the result of the last gdb
        command that made execution stop.

        This implementation, for stepping, sets (conditional) breakpoints for
        all functions that are deemed relevant. It then does a step over until
        either something halts execution, or until the next line is reached.

        If, however, stepover_command is given, it should be a string gdb
        command that continues execution in some way. The idea is that the
        caller has set a (conditional) breakpoint or watchpoint that can work
        more efficiently than the step-over loop. For Python this means setting
        a watchpoint for f->f_lasti, which means we can then subsequently
        "finish" frames.
        We want f->f_lasti instead of f->f_lineno, because the latter only
        works properly with local trace functions, see
        PyFrameObjectPtr.current_line_num and PyFrameObjectPtr.addr2line.
        """
        if stepinto:
            breakpoint_list = list(self.install_breakpoints())

        beginframe = gdb.selected_frame()

        if self.lang_info.is_relevant_function(beginframe):
            # If we start in a relevant frame, initialize stuff properly. If
            # we don't start in a relevant frame, the loop will halt
            # immediately. So don't call self.lang_info.lineno() as it may
            # raise for irrelevant frames.
            beginline = self.lang_info.lineno(beginframe)

            if not stepinto:
                depth = stackdepth(beginframe)

        newframe = beginframe

        while True:
            if self.lang_info.is_relevant_function(newframe):
                result = gdb.execute(stepover_command, to_string=True)
            else:
                result = self._finish_frame()

            if self.stopped():
                break

            newframe = gdb.selected_frame()
            is_relevant_function = self.lang_info.is_relevant_function(newframe)
            try:
                framename = newframe.name()
            except RuntimeError:
                framename = None

            m = re.search(r'Breakpoint (\d+)', result)
            if m:
                if is_relevant_function and m.group(1) in breakpoint_list:
                    # although we hit a breakpoint, we still need to check
                    # that the function, in case hit by a runtime breakpoint,
                    # is in the right context
                    break

            if newframe != beginframe:
                # new function

                if not stepinto:
                    # see if we returned to the caller
                    newdepth = stackdepth(newframe)
                    is_relevant_function = (newdepth < depth and
                                            is_relevant_function)

                if is_relevant_function:
                    break
            else:
                # newframe equals beginframe, check for a difference in the
                # line number
                lineno = self.lang_info.lineno(newframe)
                if lineno and lineno != beginline:
                    break

        if stepinto:
            self.delete_breakpoints(breakpoint_list)

        self.finish_executing(result)

    def run(self, args, from_tty):
        self.finish_executing(gdb.execute('run ' + args, to_string=True))

    def cont(self, *args):
        self.finish_executing(gdb.execute('cont', to_string=True))


class LanguageInfo:
    """
    This class defines the interface that ExecutionControlCommandBase needs to
    provide language-specific execution control.

    Classes that implement this interface should implement:

        lineno(frame)
            Tells the current line number (only called for a relevant frame).
            If lineno is a false value it is not checked for a difference.

        is_relevant_function(frame)
            tells whether we care about frame 'frame'

        get_source_line(frame)
            get the line of source code for the current line (only called for a
            relevant frame). If the source code cannot be retrieved this
            function should return None

        exc_info(frame) -- optional
            tells whether an exception was raised, if so, it should return a
            string representation of the exception value, None otherwise.

        static_break_functions()
            returns an iterable of function names that are considered relevant
            and should halt step-into execution. This is needed to provide a
            performing step-into

        runtime_break_functions() -- optional
            list of functions that we should break into depending on the
            context
    """

    def exc_info(self, frame):
        "See this class' docstring."

    def runtime_break_functions(self):
        """
        Implement this if the list of step-into functions depends on the
        context.
        """
        return ()


class PythonInfo(LanguageInfo):

    def pyframe(self, frame):
        pyframe = Frame(frame).get_pyop()
        if pyframe:
            return pyframe
        else:
            raise gdb.RuntimeError(
                "Unable to find the Python frame, run your code with a debug "
                "build (configure with --with-pydebug or compile with -g).")

    def lineno(self, frame):
        return self.pyframe(frame).current_line_num()

    def is_relevant_function(self, frame):
        return Frame(frame).is_evalframeex()

    def get_source_line(self, frame):
        try:
            pyframe = self.pyframe(frame)
            return '%4d    %s' % (pyframe.current_line_num(),
                                  pyframe.current_line().rstrip())
        except OSError:
            return None

    def exc_info(self, frame):
        try:
            tstate = frame.read_var('tstate').dereference()
            if gdb.parse_and_eval('tstate->frame == f'):
                # tstate local variable initialized, check for an exception
                if sys.version_info >= (3, 12, 0, 'alpha', 6):
                    inf_type = inf_value = tstate['current_exception']
                else:
                    inf_type = tstate['curexc_type']
                    inf_value = tstate['curexc_value']

                if inf_type:
                    return 'An exception was raised: %s' % (inf_value,)
        except (ValueError, RuntimeError):
            # Could not read the variable tstate or it's memory, it's ok
            pass

    def static_break_functions(self):
        yield 'PyEval_EvalFrameEx'


class PythonStepperMixin:
    """
    Make this a mixin so CyStep can also inherit from this and use a
    CythonCodeStepper at the same time.
    """

    def python_step(self, stepinto):
        """
        Set a watchpoint on the Python bytecode instruction pointer and try
        to finish the frame
        """
        output = gdb.execute('watch f->f_lasti', to_string=True)
        watchpoint = int(re.search(r'[Ww]atchpoint (\d+):', output).group(1))
        self.step(stepinto=stepinto, stepover_command='finish')
        gdb.execute('delete %s' % watchpoint)


class PyStep(ExecutionControlCommandBase, PythonStepperMixin):
    "Step through Python code."

    stepinto = True

    @dont_suppress_errors
    def invoke(self, args, from_tty):
        self.python_step(stepinto=self.stepinto)


class PyNext(PyStep):
    "Step-over Python code."

    stepinto = False


class PyFinish(ExecutionControlCommandBase):
    "Execute until function returns to a caller."

    invoke = dont_suppress_errors(ExecutionControlCommandBase.finish)


class PyRun(ExecutionControlCommandBase):
    "Run the program."

    invoke = dont_suppress_errors(ExecutionControlCommandBase.run)


class PyCont(ExecutionControlCommandBase):

    invoke = dont_suppress_errors(ExecutionControlCommandBase.cont)


def _pointervalue(gdbval):
    """
    Return the value of the pointer as a Python int.

    gdbval.type must be a pointer type
    """
    # don't convert with int() as it will raise a RuntimeError
    if gdbval.address is not None:
        return int(gdbval.address)
    else:
        # the address attribute is None sometimes, in which case we can
        # still convert the pointer to an int
        return int(gdbval)


def pointervalue(gdbval):
    pointer = _pointervalue(gdbval)
    try:
        if pointer < 0:
            raise gdb.GdbError("Negative pointer value, presumably a bug "
                               "in gdb, aborting.")
    except RuntimeError:
        # work around yet another bug in gdb where you get random behaviour
        # and tracebacks
        pass

    return pointer


def get_inferior_unicode_postfix():
    try:
        gdb.parse_and_eval('PyUnicode_FromEncodedObject')
    except RuntimeError:
        try:
            gdb.parse_and_eval('PyUnicodeUCS2_FromEncodedObject')
        except RuntimeError:
            return 'UCS4'
        else:
            return 'UCS2'
    else:
        return ''


class PythonCodeExecutor:

    Py_single_input = 256
    Py_file_input = 257
    Py_eval_input = 258

    def malloc(self, size):
        chunk = (gdb.parse_and_eval("(void *) malloc((size_t) %d)" % size))

        pointer = pointervalue(chunk)
        if pointer == 0:
            raise gdb.GdbError("No memory could be allocated in the inferior.")

        return pointer

    def alloc_string(self, string):
        pointer = self.malloc(len(string))
        get_selected_inferior().write_memory(pointer, string)

        return pointer

    def alloc_pystring(self, string):
        stringp = self.alloc_string(string)
        PyString_FromStringAndSize = 'PyString_FromStringAndSize'

        try:
            gdb.parse_and_eval(PyString_FromStringAndSize)
        except RuntimeError:
            # Python 3
            PyString_FromStringAndSize = ('PyUnicode%s_FromStringAndSize' %
                                               (get_inferior_unicode_postfix(),))

        try:
            result = gdb.parse_and_eval(
                '(PyObject *) %s((char *) %d, (size_t) %d)' % (
                            PyString_FromStringAndSize, stringp, len(string)))
        finally:
            self.free(stringp)

        pointer = pointervalue(result)
        if pointer == 0:
            raise gdb.GdbError("Unable to allocate Python string in "
                               "the inferior.")

        return pointer

    def free(self, pointer):
        gdb.parse_and_eval("(void) free((void *) %d)" % pointer)

    def incref(self, pointer):
        "Increment the reference count of a Python object in the inferior."
        gdb.parse_and_eval('Py_IncRef((PyObject *) %d)' % pointer)

    def xdecref(self, pointer):
        "Decrement the reference count of a Python object in the inferior."
        # Py_DecRef is like Py_XDECREF, but a function. So we don't have
        # to check for NULL. This should also decref all our allocated
        # Python strings.
        gdb.parse_and_eval('Py_DecRef((PyObject *) %d)' % pointer)

    def evalcode(self, code, input_type, global_dict=None, local_dict=None):
        """
        Evaluate python code `code` given as a string in the inferior and
        return the result as a gdb.Value. Returns a new reference in the
        inferior.

        Of course, executing any code in the inferior may be dangerous and may
        leave the debuggee in an unsafe state or terminate it altogether.
        """
        if '\0' in code:
            raise gdb.GdbError("String contains NUL byte.")

        code += '\0'

        pointer = self.alloc_string(code)

        globalsp = pointervalue(global_dict)
        localsp = pointervalue(local_dict)

        if globalsp == 0 or localsp == 0:
            raise gdb.GdbError("Unable to obtain or create locals or globals.")

        code = """
            PyRun_String(
                (char *) %(code)d,
                (int) %(start)d,
                (PyObject *) %(globals)s,
                (PyObject *) %(locals)d)
        """ % dict(code=pointer, start=input_type,
                   globals=globalsp, locals=localsp)

        with FetchAndRestoreError():
            try:
                pyobject_return_value = gdb.parse_and_eval(code)
            finally:
                self.free(pointer)

        return pyobject_return_value


class FetchAndRestoreError(PythonCodeExecutor):
    """
    Context manager that fetches the error indicator in the inferior and
    restores it on exit.
    """

    def __init__(self):
        self.sizeof_PyObjectPtr = gdb.lookup_type('PyObject').pointer().sizeof
        self.pointer = self.malloc(self.sizeof_PyObjectPtr * 3)

        type = self.pointer
        value = self.pointer + self.sizeof_PyObjectPtr
        traceback = self.pointer + self.sizeof_PyObjectPtr * 2

        self.errstate = type, value, traceback

    def __enter__(self):
        gdb.parse_and_eval("PyErr_Fetch(%d, %d, %d)" % self.errstate)

    def __exit__(self, *args):
        if gdb.parse_and_eval("(int) PyErr_Occurred()"):
            gdb.parse_and_eval("PyErr_Print()")

        pyerr_restore = ("PyErr_Restore("
                            "(PyObject *) *%d,"
                            "(PyObject *) *%d,"
                            "(PyObject *) *%d)")

        try:
            gdb.parse_and_eval(pyerr_restore % self.errstate)
        finally:
            self.free(self.pointer)


class FixGdbCommand(gdb.Command):

    def __init__(self, command, actual_command):
        super().__init__(command, gdb.COMMAND_DATA,
                                            gdb.COMPLETE_NONE)
        self.actual_command = actual_command

    def fix_gdb(self):
        """
        It seems that invoking either 'cy exec' and 'py-exec' work perfectly
        fine, but after this gdb's python API is entirely broken.
        Maybe some uncleared exception value is still set?
        sys.exc_clear() didn't help. A demonstration:

        (gdb) cy exec 'hello'
        'hello'
        (gdb) python gdb.execute('cont')
        RuntimeError: Cannot convert value to int.
        Error while executing Python code.
        (gdb) python gdb.execute('cont')
        [15148 refs]

        Program exited normally.
        """
        warnings.filterwarnings('ignore', r'.*', RuntimeWarning,
                                re.escape(__name__))
        try:
            int(gdb.parse_and_eval("(void *) 0")) == 0
        except RuntimeError:
            pass
        # warnings.resetwarnings()

    @dont_suppress_errors
    def invoke(self, args, from_tty):
        self.fix_gdb()
        try:
            gdb.execute('%s %s' % (self.actual_command, args))
        except RuntimeError as e:
            raise gdb.GdbError(str(e))
        self.fix_gdb()


def _evalcode_python(executor, code, input_type):
    """
    Execute Python code in the most recent stack frame.
    """
    global_dict = gdb.parse_and_eval('PyEval_GetGlobals()')
    local_dict = gdb.parse_and_eval('PyEval_GetLocals()')

    if (pointervalue(global_dict) == 0 or pointervalue(local_dict) == 0):
        raise gdb.GdbError("Unable to find the locals or globals of the "
                           "most recent Python function (relative to the "
                           "selected frame).")

    return executor.evalcode(code, input_type, global_dict, local_dict)


class PyExec(gdb.Command):

    def readcode(self, expr):
        if expr:
            return expr, PythonCodeExecutor.Py_single_input
        else:
            lines = []
            while True:
                try:
                    line = input('>')
                except EOFError:
                    break
                else:
                    if line.rstrip() == 'end':
                        break

                    lines.append(line)

            return '\n'.join(lines), PythonCodeExecutor.Py_file_input

    @dont_suppress_errors
    def invoke(self, expr, from_tty):
        expr, input_type = self.readcode(expr)
        executor = PythonCodeExecutor()
        executor.xdecref(_evalcode_python(executor, input_type, global_dict, local_dict))


gdb.execute('set breakpoint pending on')

if hasattr(gdb, 'GdbError'):
     # Wrap py-step and py-next in gdb defines to make them repeatable.
    py_step = PyStep('-py-step', PythonInfo())
    py_next = PyNext('-py-next', PythonInfo())
    register_defines()
    py_finish = PyFinish('py-finish', PythonInfo())
    py_run = PyRun('py-run', PythonInfo())
    py_cont = PyCont('py-cont', PythonInfo())

    py_exec = FixGdbCommand('py-exec', '-py-exec')
    _py_exec = PyExec("-py-exec", gdb.COMMAND_DATA, gdb.COMPLETE_NONE)
else:
    warnings.warn("Use gdb 7.2 or higher to use the py-exec command.")    
