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
        
# Classes that represent the debug information
# Don't rename the parameters of these classes, they come directly from the XML

class CythonModule(object):
    def __init__(self, module_name, filename):
        self.name = module_name
        self.filename = filename
        self.globals = {}
        # {cython_lineno: min(c_linenos)}
        self.lineno_cy2c = {}
        # {c_lineno: cython_lineno}
        self.lineno_c2cy = {}
    
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
        return frame.name() == 'PyEval_EvalFrameEx'

    @default_selected_gdb_frame()
    def is_python_function(self, frame):
        return libpython.Frame(frame).is_evalframeex()

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
        cyfunc = self.get_cython_function(frame)
        return cyfunc.module.lineno_c2cy.get(self.get_c_lineno(frame))

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
                raise GdbError('Unable to read information on python frame')

            filename = pyframeobject.filename()
            lineno = pyframeobject.current_line_num()
            if pygments:
                lexer = pygments.lexers.PythonLexer()

        return SourceFileDescriptor(filename, lexer), lineno

    @default_selected_gdb_frame()
    def get_source_line(self, frame):
        source_desc, lineno = self.get_source_desc()
        return source_desc.get_source(lineno)

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
        if not self.filename:
            raise GdbError('Unable to retrieve source code')

        if stop is None:
            stop = start + 1
        return '\n'.join(self._get_source(start, stop, lex_source, mark_line))
        

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
    Tell cygdb whether to colorize source code
    """

class TerminalBackground(CythonParameter):
    """
    Tell cygdb about the user's terminal background (light or dark)
    """
    
class CythonParameters(object):
    """
    Simple container class that might get more functionality in the distant
    future (mostly to remind us that we're dealing with parameters)
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

parameters = CythonParameters()


# Commands

class CythonCommand(gdb.Command, CythonBase):
    """
    Base class for Cython commands
    """


class CyCy(CythonCommand):
    """
    Invoke a Cython command. Available commands are:
        
        cy import
        cy break
        cy step
        cy print
        cy list
        cy locals
        cy globals
        cy backtrace
        cy up
        cy down
    """
    
    def __init__(self):
        super(CythonCommand, self).__init__(
            'cy', gdb.COMMAND_NONE, gdb.COMPLETE_COMMAND, prefix=True)
        
        self.import_ = CyImport(
            'cy import', gdb.COMMAND_STATUS, gdb.COMPLETE_FILENAME)
            
        self.break_ = CyBreak('cy break', gdb.COMMAND_BREAKPOINTS)
        self.step = CyStep('cy step', gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE)
        self.next = CyNext('cy next', gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE)
        self.list = CyList('cy list', gdb.COMMAND_FILES, gdb.COMPLETE_NONE)
        self.print_ = CyPrint('cy print', gdb.COMMAND_DATA)
        
        self.locals = CyLocals(
            'cy locals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
        self.globals = CyGlobals(
            'cy globals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
            
        self.cy_cname = CyCName('cy_cname')
        
        objs = (self.import_, self.break_, self.step, self.list, self.print_,
                self.locals, self.globals, self.cy_cname)

        for obj in objs:
            obj.cy = self
            
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

    def invoke(self, args, from_tty):
        args = args.encode(_filesystemencoding)
        for arg in string_to_argv(args):
            try:
                f = open(arg)
            except OSError, e:
                print('Unable to open file %r: %s' % (args, e.args[1]))
                return
            
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
                    self.cy.functions_by_name[cython_function.name].append(
                        cython_function)
                    self.cy.functions_by_qualified_name[
                        cython_function.qualified_name] = cython_function
                    self.cy.functions_by_cname[
                        cython_function.cname] = cython_function
                    
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
    
    def _break_pyx(self, name):
        modulename, _, lineno = name.partition(':')
        lineno = int(lineno)
        cython_module = self.cy.cython_namespace[modulename]
        if lineno in cython_module.lineno_cy2c:
            c_lineno = cython_module.lineno_cy2c[lineno]
            breakpoint = '%s:%s' % (cython_module.name, c_lineno)
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


class CodeStepperMixin(object):
    
    def init_stepping(self):
        self.cython_func = self.get_cython_function()
        self.beginline = self.get_cython_lineno()
        self.curframe = gdb.selected_frame() 

    def next_step(self, command):
        "returns whether to continue stepping"
        result = gdb.execute(command, to_string=True)
        newframe = gdb.selected_frame()
        
        c1 = result.startswith('Breakpoint')
        c2 = (newframe == self.curframe and 
              self.get_cython_lineno() > self.beginline)
        return not c1 and not c2
        
    def end_stepping(self):
        sys.stdout.write(self.get_source_line())


class CyStep(CythonCommand, CodeStepperMixin):

    def step(self, nsteps=1):
        for nthstep in xrange(nsteps):
            self.init_stepping()
            
            while self.next_step('step'):
                newframe = gdb.selected_frame()
                if newframe != self.curframe:
                    # we entered a function
                    funcname = self.get_c_function_name(newframe)
                    if (self.is_cython_function() or 
                        self.is_python_function() or
                        funcname in cython_function.step_into_functions):
                        break
        
        self.end_stepping()

    def invoke(self, steps, from_tty):
        if self.is_cython_function():
            if steps:
                self.step(int(steps))
            else:
                self.step()
        else:
            gdb.execute('step ' + steps, from_tty)


class CyNext(CythonCommand, CodeStepperMixin):
    
    def next(self, nsteps=1):
        for nthstep in xrange(nsteps):
            self.init_stepping()
            
            while self.next_step('next'):
                pass
            
            self.end_stepping()
    
    def invoke(self, steps, from_tty):
        if self.is_cython_function():
            if steps:
                self.next(int(steps))
            else:
                self.next()
        else:
            gdb.execute('next ' + steps, from_tty)


class CyList(CythonCommand):
    
    def invoke(self, _, from_tty):
        sd, lineno = self.get_source_desc()
        source = sd.get_source(lineno - 5, lineno + 5, mark_line=lineno)
        print source


class CyPrint(CythonCommand):
    """
    Print a Cython variable using 'cy-print x' or 'cy-print module.function.x'
    """
    
    def invoke(self, name, from_tty):
        try:
            cname = cy.cy_cname.invoke(name)
        except gdb.GdbError:
            cname = name
       
        gdb.execute('print ' + cname)
        
    
    def complete(self):
        if self.is_cython_function():
            f = self.get_cython_function()
            return list(itertools.chain(f.locals, f.globals))
        return []


class CyLocals(CythonCommand):
    def ns(self):
        return self.get_cython_function().locals
    
    @require_cython_frame
    def invoke(self, name, from_tty):
        try:
            ns = self.ns()
        except RuntimeError, e:
            print e.args[0]
            return
        
        if ns is None:
            raise gdb.GdbError(
                'Information of Cython locals could not be obtained. '
                'Is this an actual Cython function and did you '
                "'cy import' the debug information?")
        
        for var in ns.itervalues():
            val = gdb.parse_and_eval(var.cname)
            if var.type == PythonObject:
                result = libpython.PyObjectPtr.from_pyobject_ptr(val)
            else:
                result = val
                
            print '%s = %s' % (var.name, result)


class CyGlobals(CythonCommand):
    def ns(self):
        return self.get_cython_function().globals
    
    @require_cython_frame
    def invoke(self, name, from_tty):
        # include globals from the debug info XML file!
        m = gdb.parse_and_eval('__pyx_m')
        
        try:
            PyModuleObject = gdb.lookup_type('PyModuleObject')
        except RuntimeError:
            raise gdb.GdbError(textwrap.dedent("""
                Unable to lookup type PyModuleObject, did you compile python 
                with debugging support (-g)? If this installation is from your
                package manager, install python-dbg and run the debug version
                of python or compile it yourself.
                """))
            
        m = m.cast(PyModuleObject.pointer())
        d = libpython.PyObjectPtr.from_pyobject_ptr(m['md_dict'])
        print d.get_truncated_repr(1000)


# Functions

class CyCName(gdb.Function, CythonBase):
    """
    Get the C name of a Cython variable.
    """
    
    @require_cython_frame
    def invoke(self, cyname, frame=None):
        frame = frame or gdb.selected_frame()
        cname = None
        
        cyname = cyname.string()
        if self.is_cython_function(frame):
            cython_function = self.get_cython_function(frame)
            if cyname in cython_function.locals:
                cname = cython_function.locals[cyname].cname
            elif cyname in cython_function.module.globals:
                cname = cython_function.module.globals[cyname].cname
        
        if not cname:
            raise gdb.GdbError('No such Cython variable: %s' % cyname)
        
        return cname
        

cy = CyCy()