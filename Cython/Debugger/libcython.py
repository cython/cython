"""
GDB extension that adds Cython support.
"""

import sys
import textwrap
import traceback
import functools
import itertools
import collections

import gdb

try:
  from lxml import etree
  have_lxml = True
except ImportError:
    have_lxml = False
    try:
        # Python 2.5
        from xml.etree import cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            from xml.etree import ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                # normal ElementTree install
                import elementtree.ElementTree as etree

try:
    import pygments.lexers
    import pygments.formatters
except ImportError:
    pygments = None
    sys.stderr.write("Install pygments for colorized source code.\n")

if hasattr(gdb, 'string_to_argv'):
    from gdb import string_to_argv
else:
    from shlex import split as string_to_argv

from Cython.Debugger import libpython

# C or Python type
CObject = 'CObject'
PythonObject = 'PythonObject'

_data_types = dict(CObject=CObject, PythonObject=PythonObject)
_filesystemencoding = sys.getfilesystemencoding() or 'UTF-8'

# decorators

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

def default_selected_gdb_frame(err=True):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, frame=None, **kwargs):
            try:
                frame = frame or gdb.selected_frame()
            except RuntimeError:
                raise gdb.GdbError("No frame is currently selected.")
                
            if err and frame.name() is None:
                raise NoFunctionNameInFrameError()
    
            return function(self, frame, **kwargs)
        return wrapper
    return decorator

def require_cython_frame(function):
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        if not self.is_cython_function():
            raise gdb.GdbError('Selected frame does not correspond with a '
                               'Cython function we know about.')
        return function(self, *args, **kwargs)
    return wrapper 

def dispatch_on_frame(c_command, python_command=None):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            is_cy = self.is_cython_function()
            is_py = self.is_python_function()
            
            if is_cy or (is_py and not python_command):
                function(self, *args, **kwargs)
            elif is_py:
                gdb.execute(python_command)
            elif self.is_relevant_function():
                gdb.execute(c_command)
            else:
                raise gdb.GdbError("Not a function cygdb knows about. "
                                   "Use the normal GDB commands instead.")
        
        return wrapper
    return decorator


# Classes that represent the debug information
# Don't rename the parameters of these classes, they come directly from the XML

class CythonModule(object):
    def __init__(self, module_name, filename, c_filename):
        self.name = module_name
        self.filename = filename
        self.c_filename = c_filename
        self.globals = {}
        # {cython_lineno: min(c_linenos)}
        self.lineno_cy2c = {}
        # {c_lineno: cython_lineno}
        self.lineno_c2cy = {}
        self.functions = {}
        
    def qualified_name(self, varname):
        return '.'.join(self.name, varname)

class CythonVariable(object):

    def __init__(self, name, cname, qualified_name, type):
        self.name = name
        self.cname = cname
        self.qualified_name = qualified_name
        self.type = type

class CythonFunction(CythonVariable):
    def __init__(self, 
                 module, 
                 name, 
                 cname, 
                 pf_cname,
                 qualified_name, 
                 lineno, 
                 type=CObject):
        super(CythonFunction, self).__init__(name, 
                                             cname, 
                                             qualified_name, 
                                             type)
        self.module = module
        self.pf_cname = pf_cname
        self.lineno = int(lineno)
        self.locals = {}
        self.arguments = []
        self.step_into_functions = set()


# General purpose classes

class CythonBase(object):
    
    @default_selected_gdb_frame(err=False)
    def is_cython_function(self, frame):
        return frame.name() in self.cy.functions_by_cname

    @default_selected_gdb_frame(err=False)
    def is_python_function(self, frame):
        """
        Tells if a frame is associated with a Python function.
        If we can't read the Python frame information, don't regard it as such.
        """
        if frame.name() == 'PyEval_EvalFrameEx':
            pyframe = libpython.Frame(frame).get_pyop()
            return pyframe and not pyframe.is_optimized_out()
        return False
        
    @default_selected_gdb_frame()
    def get_c_function_name(self, frame):
        return frame.name()

    @default_selected_gdb_frame()
    def get_c_lineno(self, frame):
        return frame.find_sal().line
    
    @default_selected_gdb_frame()
    def get_cython_function(self, frame):
        result = self.cy.functions_by_cname.get(frame.name())
        if result is None:
            raise NoCythonFunctionInFrameError()
            
        return result
    
    @default_selected_gdb_frame()
    def get_cython_lineno(self, frame):
        """
        Get the current Cython line number. Returns 0 if there is no 
        correspondence between the C and Cython code.
        """
        cyfunc = self.get_cython_function(frame)
        return cyfunc.module.lineno_c2cy.get(self.get_c_lineno(frame), 0)
    
    @default_selected_gdb_frame()
    def get_source_desc(self, frame):
        filename = lineno = lexer = None
        if self.is_cython_function():
            filename = self.get_cython_function(frame).module.filename
            lineno = self.get_cython_lineno(frame)
            if pygments:
                lexer = pygments.lexers.CythonLexer()
        elif self.is_python_function():
            pyframeobject = libpython.Frame(frame).get_pyop()

            if not pyframeobject:
                raise gdb.GdbError('Unable to read information on python frame')

            filename = pyframeobject.filename()
            lineno = pyframeobject.current_line_num()
            if pygments:
                lexer = pygments.lexers.PythonLexer()

        return SourceFileDescriptor(filename, lexer), lineno

    @default_selected_gdb_frame()
    def get_source_line(self, frame):
        source_desc, lineno = self.get_source_desc()
        return source_desc.get_source(lineno)
    
    @default_selected_gdb_frame()
    def is_relevant_function(self, frame):
        """
        returns whether we care about a frame on the user-level when debugging
        Cython code
        """
        name = frame.name()
        older_frame = frame.older()
        # print 'is_relevant_function', name
        if self.is_cython_function(frame) or self.is_python_function(frame):
            return True
        elif (parameters.step_into_c_code and 
              older_frame and self.is_cython_function(older_frame)):
            # direct C function call from a Cython function
            cython_func = self.get_cython_function(older_frame)
            return name in cython_func.step_into_functions

        return False
    
    def print_cython_var_if_initialized(self, varname, max_name_length=None):
        try:
            self.cy.print_.invoke(varname, True, max_name_length)
        except gdb.GdbError:
            # variable not initialized yet
            pass

class SourceFileDescriptor(object):
    def __init__(self, filename, lexer, formatter=None):
        self.filename = filename
        self.lexer = lexer
        self.formatter = formatter

    def valid(self):
        return self.filename is not None

    def lex(self, code):
        if pygments and self.lexer and parameters.colorize_code:
            bg = parameters.terminal_background.value
            if self.formatter is None:
                formatter = pygments.formatters.TerminalFormatter(bg=bg)
            else:
                formatter = self.formatter

            return pygments.highlight(code, self.lexer, formatter)

        return code

    def _get_source(self, start, stop, lex_source, mark_line):
        with open(self.filename) as f:
            if lex_source:
                # to provide proper colouring, the entire code needs to be 
                # lexed
                lines = self.lex(f.read()).splitlines()
            else:
                lines = f
            
            for idx, line in enumerate(itertools.islice(lines, start - 1, stop - 1)):
                if start + idx == mark_line:
                    prefix = '>'
                else:
                    prefix = ' '
                
                yield '%s %4d    %s' % (prefix, start + idx, line)

    def get_source(self, start, stop=None, lex_source=True, mark_line=0):
        exc = gdb.GdbError('Unable to retrieve source code')
        
        if not self.filename:
            raise exc
            
        if stop is None:
            stop = start + 1

        try:
            return '\n'.join(
                self._get_source(start, stop, lex_source, mark_line))
        except IOError:
            raise exc


# Errors

class CyGDBError(gdb.GdbError):
    """
    Base class for Cython-command related erorrs
    """
    
    def __init__(self, *args):
        args = args or (self.msg,)
        super(CyGDBError, self).__init__(*args)
    
class NoCythonFunctionInFrameError(CyGDBError):
    """
    raised when the user requests the current cython function, which is 
    unavailable
    """
    msg = "Current function is a function cygdb doesn't know about"

class NoFunctionNameInFrameError(NoCythonFunctionInFrameError):
    """
    raised when the name of the C function could not be determined 
    in the current C stack frame
    """
    msg = ('C function name could not be determined in the current C stack '
           'frame')


# Parameters

class CythonParameter(gdb.Parameter):
    """
    Base class for cython parameters
    """
    
    def __init__(self, name, command_class, parameter_class, default=None):
        self.show_doc = self.set_doc = self.__class__.__doc__
        super(CythonParameter, self).__init__(name, command_class, 
                                              parameter_class)
        if default is not None:
            self.value = default
   
    def __nonzero__(self):
        return bool(self.value)
    
    __bool__ = __nonzero__ # python 3

class CompleteUnqualifiedFunctionNames(CythonParameter):
    """
    Have 'cy break' complete unqualified function or method names.
    """ 

class ColorizeSourceCode(CythonParameter):
    """
    Tell cygdb whether to colorize source code.
    """

class TerminalBackground(CythonParameter):
    """
    Tell cygdb about the user's terminal background (light or dark).
    """

class StepIntoCCode(CythonParameter):
    """
    Tells cygdb whether to step into C functions called directly from Cython
    code.
    """

class CythonParameters(object):
    """
    Simple container class that might get more functionality in the distant
    future (mostly to remind us that we're dealing with parameters).
    """
    
    def __init__(self):
        self.complete_unqualified = CompleteUnqualifiedFunctionNames(
            'cy_complete_unqualified',
            gdb.COMMAND_BREAKPOINTS,
            gdb.PARAM_BOOLEAN,
            True)
        self.colorize_code = ColorizeSourceCode(
            'cy_colorize_code',
            gdb.COMMAND_FILES,
            gdb.PARAM_BOOLEAN,
            True)
        self.terminal_background = TerminalBackground(
            'cy_terminal_background_color',
            gdb.COMMAND_FILES,
            gdb.PARAM_STRING,
            "dark")
        self.step_into_c_code = StepIntoCCode(
            'cy_step_into_c_code',
            gdb.COMMAND_RUNNING,
            gdb.PARAM_BOOLEAN,
            True)
        
parameters = CythonParameters()


# Commands

class CythonCommand(gdb.Command, CythonBase):
    """
    Base class for Cython commands
    """

    @classmethod
    def register(cls, *args, **kwargs):
        if not hasattr(cls, 'completer_class'):
            return cls(cls.name, cls.command_class, *args, **kwargs)
        else:
            return cls(cls.name, cls.command_class, cls.completer_class, 
                       *args, **kwargs)


class CyCy(CythonCommand):
    """
    Invoke a Cython command. Available commands are:
        
        cy import
        cy break
        cy step
        cy next
        cy print
        cy list
        cy locals
        cy globals
        cy backtrace
        cy up
        cy down
    """
    
    name = 'cy'
    command_class = gdb.COMMAND_NONE
    completer_class = gdb.COMPLETE_COMMAND
    
    def __init__(self, *args):
        super(CythonCommand, self).__init__(*args, prefix=True)
        
        commands = dict(
            import_ = CyImport.register(),
            break_ = CyBreak.register(),
            step = CyStep.register(),
            next = CyNext.register(),
            list = CyList.register(),
            print_ = CyPrint.register(),
            locals = CyLocals.register(),
            globals = CyGlobals.register(),
            cy_cname = CyCName('cy_cname'),
            cy_line = CyLine('cy_line'),
        )
            
        for command_name, command in commands.iteritems():
            command.cy = self
            setattr(self, command_name, command)
        
        self.cy = self
        
        # Cython module namespace
        self.cython_namespace = {}
        
        # maps (unique) qualified function names (e.g. 
        # cythonmodule.ClassName.method_name) to the CythonFunction object
        self.functions_by_qualified_name = {}
        
        # unique cnames of Cython functions
        self.functions_by_cname = {}
        
        # map function names like method_name to a list of all such 
        # CythonFunction objects
        self.functions_by_name = collections.defaultdict(list)


class CyImport(CythonCommand):
    """
    Import debug information outputted by the Cython compiler
    Example: cy import FILE...
    """
    
    name = 'cy import'
    command_class = gdb.COMMAND_STATUS
    completer_class = gdb.COMPLETE_FILENAME
    
    def invoke(self, args, from_tty):
        args = args.encode(_filesystemencoding)
        for arg in string_to_argv(args):
            try:
                f = open(arg)
            except OSError, e:
                raise gdb.GdbError('Unable to open file %r: %s' % 
                                                (args, e.args[1]))
            
            t = etree.parse(f)
            
            for module in t.getroot():
                cython_module = CythonModule(**module.attrib)
                self.cy.cython_namespace[cython_module.name] = cython_module
                
                for variable in module.find('Globals'):
                    d = variable.attrib
                    cython_module.globals[d['name']] = CythonVariable(**d)
                
                for function in module.find('Functions'):
                    cython_function = CythonFunction(module=cython_module, 
                                                     **function.attrib)

                    # update the global function mappings
                    name = cython_function.name
                    qname = cython_function.qualified_name
                    
                    self.cy.functions_by_name[name].append(cython_function)
                    self.cy.functions_by_qualified_name[
                        cython_function.qualified_name] = cython_function
                    self.cy.functions_by_cname[
                        cython_function.cname] = cython_function
                    
                    d = cython_module.functions[qname] = cython_function
                    
                    for local in function.find('Locals'):
                        d = local.attrib
                        cython_function.locals[d['name']] = CythonVariable(**d)

                    for step_into_func in function.find('StepIntoFunctions'):
                        d = step_into_func.attrib
                        cython_function.step_into_functions.add(d['name'])
                    
                    cython_function.arguments.extend(
                        funcarg.tag for funcarg in function.find('Arguments'))

                for marker in module.find('LineNumberMapping'):
                    cython_lineno = int(marker.attrib['cython_lineno'])
                    c_linenos = map(int, marker.attrib['c_linenos'].split())
                    cython_module.lineno_cy2c[cython_lineno] = min(c_linenos)
                    for c_lineno in c_linenos:
                        cython_module.lineno_c2cy[c_lineno] = cython_lineno
                    

class CyBreak(CythonCommand):
    """
    Set a breakpoint for Cython code using Cython qualified name notation, e.g.:
        
        cy break cython_modulename.ClassName.method_name...
    
    or normal notation:
        
        cy break function_or_method_name...
    
    or for a line number:
    
        cy break cython_module:lineno...
    """
    
    name = 'cy break'
    command_class = gdb.COMMAND_BREAKPOINTS
    
    def _break_pyx(self, name):
        modulename, _, lineno = name.partition(':')
        lineno = int(lineno)
        cython_module = self.cy.cython_namespace[modulename]
        if lineno in cython_module.lineno_cy2c:
            c_lineno = cython_module.lineno_cy2c[lineno]
            breakpoint = '%s:%s' % (cython_module.c_filename, c_lineno)
            gdb.execute('break ' + breakpoint)
        else:
            raise GdbError("Not a valid line number. "
                           "Does it contain actual code?")
    
    def _break_funcname(self, funcname):
        func = self.cy.functions_by_qualified_name.get(funcname)
        break_funcs = [func]
        
        if not func:
            funcs = self.cy.functions_by_name.get(funcname)
            if not funcs:
                gdb.execute('break ' + funcname)
                return
                
            if len(funcs) > 1:
                # multiple functions, let the user pick one
                print 'There are multiple such functions:'
                for idx, func in enumerate(funcs):
                    print '%3d) %s' % (idx, func.qualified_name)
                
                while True:
                    try:
                        result = raw_input(
                            "Select a function, press 'a' for all "
                            "functions or press 'q' or '^D' to quit: ")
                    except EOFError:
                        return
                    else:
                        if result.lower() == 'q':
                            return
                        elif result.lower() == 'a':
                            break_funcs = funcs
                            break
                        elif (result.isdigit() and 
                            0 <= int(result) < len(funcs)):
                            break_funcs = [funcs[int(result)]]
                            break
                        else:
                            print 'Not understood...'
            else:
                break_funcs = [funcs[0]]
        
        for func in break_funcs:
            gdb.execute('break %s' % func.cname)
            if func.pf_cname:
                gdb.execute('break %s' % func.pf_cname)
    
    def invoke(self, function_names, from_tty):
        for funcname in string_to_argv(function_names.encode('UTF-8')):
            if ':' in funcname:
                self._break_pyx(funcname)
            else:
                self._break_funcname(funcname)
    
    @dont_suppress_errors
    def complete(self, text, word):
        names = self.cy.functions_by_qualified_name
        if parameters.complete_unqualified:
            names = itertools.chain(names, self.cy.functions_by_name)

        words = text.strip().split()
        if words and '.' in words[-1]:
            compl = [n for n in self.cy.functions_by_qualified_name 
                           if n.startswith(lastword)]
        else:
            seen = set(text[:-len(word)].split())
            return [n for n in names if n.startswith(word) and n not in seen]
        
        if len(lastword) > len(word):
            # readline sees something (e.g. a '.') as a word boundary, so don't
            # "recomplete" this prefix
            strip_prefix_length = len(lastword) - len(word)
            compl = [n[strip_prefix_length:] for n in compl]
            
        return compl


class CythonCodeStepper(CythonCommand, libpython.GenericCodeStepper):
    """
    Base class for CyStep and CyNext. It implements the interface dictated by
    libpython.GenericCodeStepper.
    """
    
    def lineno(self, frame):
        # Take care of the Python and Cython levels. We need to care for both
        # as we can't simply dispath to 'py-step', since that would work for
        # stepping through Python code, but it would not step back into Cython-
        # related code. The C level should be dispatched to the 'step' command.
        if self.is_cython_function(frame):
            return self.get_cython_lineno(frame)
        else:
            return libpython.py_step.lineno(frame)
    
    def get_source_line(self, frame):
        # We may have ended up in a Python, Cython, or C function
        result = None
        
        if self.is_cython_function(frame) or self.is_python_function(frame):
            try:
                line = super(CythonCodeStepper, self).get_source_line(frame)
            except gdb.GdbError:
                pass
            else:
                result = line.lstrip()

        return result
        
    @classmethod
    def register(cls):
        return cls(cls.name, stepper=cls.stepper)
    

class CyStep(CythonCodeStepper):
    "Step through Python code."
    
    name = 'cy step'
    stepper = True
    
    @dispatch_on_frame(c_command='step')
    def invoke(self, *args, **kwargs):
        super(CythonCodeStepper, self).invoke(*args, **kwargs)


class CyNext(CythonCodeStepper):
    "Step-over Python code."

    name = 'cy next'
    stepper = False

    @dispatch_on_frame(c_command='next')
    def invoke(self, *args, **kwargs):
        super(CythonCodeStepper, self).invoke(*args, **kwargs)


class CyList(CythonCommand):
    """
    List Cython source code. To disable to customize colouring see the cy_*
    parameters.
    """
    
    name = 'cy list'
    command_class = gdb.COMMAND_FILES
    completer_class = gdb.COMPLETE_NONE
    
    @dispatch_on_frame(c_command='list')
    def invoke(self, _, from_tty):
        sd, lineno = self.get_source_desc()
        source = sd.get_source(lineno - 5, lineno + 5, mark_line=lineno)
        print source


class CyPrint(CythonCommand):
    """
    Print a Cython variable using 'cy-print x' or 'cy-print module.function.x'
    """
    
    name = 'cy print'
    command_class = gdb.COMMAND_DATA
    
    @dispatch_on_frame(c_command='print', python_command='py-print')
    def invoke(self, name, from_tty, max_name_length=None):
        cname = self.cy.cy_cname.invoke(name, string=True)
        try:
             value = gdb.parse_and_eval(cname)
        except RuntimeError, e:
            raise gdb.GdbError("Variable %s is not initialized yet." % (name,))
        else:
            if max_name_length is None:
                print '%s = %s' % (name, value)
            else:
                print '%-*s = %s' % (max_name_length, name, value)
        
    def complete(self):
        if self.is_cython_function():
            f = self.get_cython_function()
            return list(itertools.chain(f.locals, f.globals))
        else:
            return []


class CyLocals(CythonCommand):
    """
    List the locals from the current Cython frame.
    """
    
    name = 'cy locals'
    command_class = gdb.COMMAND_STACK
    completer_class = gdb.COMPLETE_NONE
    
    @dispatch_on_frame(c_command='info locals', python_command='py-locals')
    def invoke(self, args, from_tty):
        local_cython_vars = self.get_cython_function().locals
        max_name_length = len(max(local_cython_vars, key=len))
        for varname in local_cython_vars:
            self.print_cython_var_if_initialized(varname, max_name_length)
                

class CyGlobals(CythonCommand):
    """
    List the globals from the current Cython module.
    """
    
    name = 'cy globals'
    command_class = gdb.COMMAND_STACK
    completer_class = gdb.COMPLETE_NONE
    
    @dispatch_on_frame(c_command='info variables', python_command='py-globals')
    def invoke(self, args, from_tty):
        m = gdb.parse_and_eval('__pyx_m')
        
        try:
            PyModuleObject = gdb.lookup_type('PyModuleObject')
        except RuntimeError:
            raise gdb.GdbError(textwrap.dedent("""
                Unable to lookup type PyModuleObject, did you compile python 
                with debugging support (-g)?
                """))
            
        m = m.cast(PyModuleObject.pointer())
        pyobject_dict = libpython.PyObjectPtr.from_pyobject_ptr(m['md_dict'])
        
        module_globals = self.get_cython_function().module.globals
        # - 2 for the surrounding quotes
        max_name_length = max(len(max(module_globals, key=len)),
                              len(max(pyobject_dict.iteritems())) - 2)
        
        seen = set()
        for k, v in pyobject_dict.iteritems():
            # Note: k and v are values in the inferior, they are 
            #       libpython.PyObjectPtr objects
            
            k = k.get_truncated_repr(libpython.MAX_OUTPUT_LEN)
            # make it look like an actual name (inversion of repr())
            k = k[1:-1].decode('string-escape')
            v = v.get_truncated_repr(libpython.MAX_OUTPUT_LEN)
            
            seen.add(k)
            print '%-*s = %s' % (max_name_length, k, v)
        
        for varname in seen.symmetric_difference(module_globals):
            self.print_cython_var_if_initialized(varname, max_name_length)


# Functions

class CyCName(gdb.Function, CythonBase):
    """
    Get the C name of a Cython variable in the current context.
    Examples:
        
        print $cy_cname("function")
        print $cy_cname("Class.method")
        print $cy_cname("module.function")
    """
    
    @require_cython_frame
    def invoke(self, cyname, string=False, frame=None):
        frame = frame or gdb.selected_frame()
        cname = None
        
        if isinstance(cyname, gdb.Value):
            # convert to a python string so it supports proper hashing
            cyname = cyname.string()
        
        if self.is_cython_function(frame):
            cython_function = self.get_cython_function(frame)
            if cyname in cython_function.locals:
                cname = cython_function.locals[cyname].cname
            elif cyname in cython_function.module.globals:
                cname = cython_function.module.globals[cyname].cname
            else:
                qname = '%s.%s' % (cython_function.module.name, cyname)
                if qname in cython_function.module.functions:
                    cname = cython_function.module.functions[qname].cname
            
        if not cname:
            cname = self.cy.functions_by_qualified_name.get(cyname)
            
        if not cname:
            raise gdb.GdbError('No such Cython variable: %s' % cyname)
        
        if string:
            return cname
        else:
            return gdb.parse_and_eval(cname)


class CyLine(gdb.Function, CythonBase):
    """
    Get the current Cython line.
    """
    
    @require_cython_frame
    def invoke(self):
        return self.get_cython_lineno()


cy = CyCy.register()