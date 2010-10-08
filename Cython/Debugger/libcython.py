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


# Cython module namespace
cython_namespace = {}

# C or Python type
CObject = object()
PythonObject = object()

# maps (unique) qualified function names (e.g. 
# cythonmodule.ClassName.method_name) to the CythonFunction object
functions_by_qualified_name = {}

# unique cnames of Cython functions
functions_by_cname = {}

# map function names like method_name to a list of all such CythonFunction
# objects
functions_by_name = collections.defaultdict(list)

_filesystemencoding = sys.getfilesystemencoding() or 'UTF-8'

# decorators

def dont_suppress_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise
    
    return wrapper

def default_selected_gdb_frame(function):
    @functools.wraps(function)
    def wrapper(self, frame=None, **kwargs):
        frame = frame or gdb.selected_frame()
        if frame.name() is None:
            raise NoFunctionNameInFrameError()

        return function(self, frame)
    return wrapper


# Classes that represent the debug information
# Don't rename the parameters of these classes, they come directly from the XML

class CythonModule(object):
    def __init__(self, module_name, filename):
        self.name = module_name
        self.filename = filename
        self.functions = {}
        self.globals = {}
        # {cython_lineno: min(c_linenos)}
        self.lineno_cy2c = {}
        # {c_lineno: cython_lineno}
        self.lineno_c2cy = {}

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
        self.lineno = lineno
        self.locals = {}
        self.arguments = []
        self.step_into_functions = set()

class SourceFileDescriptor(object):
    def __init__(self, filename, lineno, lexer, formatter=None):
        self.filename = filename
        self.lineno = lineno
        self.lexer = lexer
        self.formatter = formatter

    def valid(self):
        return self.filename is not None

    def lex(self, code):
        if pygments and parameter.colorize_code:
            bg = parameter.terminal_background.value
            if self.formatter is None:
                formatter = pygments.formatters.TerminalFormatter(bg=bg)
            else:
                formatter = self.formatter

            return pygments.highlight(code, self.lexer, formatter)

        return code

    def get_source(self, start=0, stop=None, lex_source=True):
        # todo: have it detect the source file's encoding
        if not self.filename:
            return 'Unable to retrieve source code'

        start = max(self.lineno + start, 0)
        if stop is None:
            stop = self.lineno + 1
        else:
            stop = self.lineno + stop
            
        with open(self.filename) as f:
            source = itertools.islice(f, start, stop)
            
            if lex_source:
                return [self.lex(line) for line in source]
            else:
                return list(source)


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
    
class Parameter(object):
    """
    Simple container class that might get more functionality in the distant
    future (mostly to remind us that we're dealing with parameters)
    """
    complete_unqualified = CompleteUnqualifiedFunctionNames(
        'cy_complete_unqualified',
        gdb.COMMAND_BREAKPOINTS,
        gdb.PARAM_BOOLEAN,
        True)
    colorize_code = ColorizeSourceCode(
        'cy_colorize_code',
        gdb.COMMAND_FILES,
        gdb.PARAM_BOOLEAN,
        True)
    terminal_background = TerminalBackground(
        'cy_terminal_background_color',
        gdb.COMMAND_FILES,
        gdb.PARAM_STRING,
        "dark")

parameter = Parameter()

# Commands

class CythonCommand(gdb.Command):
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
        cy info line
    """
    
    def is_cython_function(self, frame=None):
        func_name = (frame or gdb.selected_frame()).name()
        return func_name is not None and func_name in functions_by_cname

    @default_selected_gdb_frame
    def is_python_function(self, frame):
        return libpython.Frame(frame).is_evalframeex()

    @default_selected_gdb_frame
    def get_c_function_name(self, frame):
        return frame.name()

    @default_selected_gdb_frame
    def get_c_lineno(self, frame):
        return frame.find_sal().line
    
    @default_selected_gdb_frame
    def get_cython_function(self, frame):
        result = functions_by_cname.get(frame.name())
        if result is None:
            raise NoCythonFunctionInFrameError()
            
        return result
    
    @default_selected_gdb_frame
    def get_cython_lineno(self, frame):
        cyfunc = self.get_cython_function(frame)
        return cyfunc.module.lineno_c2cy.get(self.get_c_lineno(frame))

    @default_selected_gdb_frame
    def get_source_desc(self, frame):
        if self.is_cython_function():
            filename = self.get_cython_function(frame).module.filename
            lineno = self.get_cython_lineno(frame)
            lexer = pygments.lexers.CythonLexer()
        else:
            filename = None
            lineno = -1
            lexer = None

        return SourceFileDescriptor(filename, lineno, lexer)

   
cy = CythonCommand('cy', gdb.COMMAND_NONE, gdb.COMPLETE_COMMAND, prefix=True)


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
                cython_namespace[cython_module.name] = cython_module
                
                for variable in module.find('Globals'):
                    d = variable.attrib
                    cython_module.globals[d['name']] = CythonVariable(**d)
                
                for function in module.find('Functions'):
                    cython_function = CythonFunction(module=cython_module, 
                                                     **function.attrib)
                    cython_module.functions[cython_function.name] = \
                        cython_function
                    
                    # update the global function mappings
                    functions_by_name[cython_function.name].append(
                        cython_function)
                    functions_by_qualified_name[
                        cython_function.qualified_name] = cython_function
                    functions_by_cname[cython_function.cname] = cython_function
                    
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
                    
                
cy.import_ = CyImport('cy import', gdb.COMMAND_STATUS, gdb.COMPLETE_FILENAME)


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
        cython_module = cython_namespace[modulename]
        if lineno in cython_module.lineno_cy2c:
            c_lineno = cython_module.lineno_cy2c[lineno]
            breakpoint = '%s:%s' % (cython_module.name, c_lineno)
            gdb.execute('break ' + breakpoint)
        else:
            sys.stderr.write("Not a valid line number (does it contain actual code?)\n")
    
    def _break_funcname(self, funcname):
        func = functions_by_qualified_name.get(funcname)
        break_funcs = [func]
        
        if not func:
            funcs = functions_by_name.get(funcname)
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
        names = functions_by_qualified_name
        if parameter.complete_unqualified:
            names = itertools.chain(names, functions_by_name)

        words = text.strip().split()
        if words and '.' in words[-1]:
            compl = [n for n in functions_by_qualified_name 
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

cy.break_ = CyBreak('cy break', gdb.COMMAND_BREAKPOINTS)


class CyStep(CythonCommand):

    def step(self, from_tty=True, nsteps=1):
        for nthstep in xrange(nsteps):
            cython_func = self.get_cython_function()
            beginline = self.get_cython_lineno()
            curframe = gdb.selected_frame() 
    
            while True:
                result = gdb.execute('step', False, True)
                if result.startswith('Breakpoint'):
                        break
                newframe = gdb.selected_frame()
                if newframe == curframe:
                    # still in the same function
                    if self.get_cython_lineno() > beginline:
                        break
                else:
                    # we entered a function
                    funcname = self.get_c_function_name(newframe)
                    if (self.is_cython_function() or 
                        self.is_python_function() or
                        funcname in cython_function.step_into_functions):
                        break
        
        line, = self.get_source_desc().get_source()
        sys.stdout.write(line)

    def invoke(self, steps, from_tty):
        if self.is_cython_function():
            if steps:
                self.step(from_tty, int(steps))
            else:
                self.step(from_tty)
        else:
            gdb.execute('step ' + steps)

cy.step = CyStep('cy step', gdb.COMMAND_RUNNING, gdb.COMPLETE_NONE)


class CyList(CythonCommand):
    
    def invoke(self, _, from_tty):
        sd = self.get_source_desc()
        it = enumerate(sd.get_source(-5, +5))
        sys.stdout.write(
            ''.join('%4d    %s' % (sd.lineno + i, line) for i, line in it))

cy.list = CyList('cy list', gdb.COMMAND_FILES, gdb.COMPLETE_NONE)


class CyPrint(CythonCommand):
    """
    Print a Cython variable using 'cy-print x' or 'cy-print module.function.x'
    """
   
    
    def invoke(self, name, from_tty):
        cname = None
        if self.is_cython_function():
            cython_function = self.get_cython_function()
            if name in cython_function.locals:
                cname = cython_function.locals[name].cname
            elif name in cython_function.module.globals:
                cname = cython_function.module.globals[name].cname

        # let the pretty printers do the work
        cname = cname or name
        gdb.execute('print ' + cname)
    
    def complete(self):
        if self.is_cython_function():
            cf = self.get_cython_function()
            return list(itertools.chain(cf.locals, cf.globals))
        return []
    
cy.print_ = CyPrint('cy print', gdb.COMMAND_DATA)


class CyLocals(CythonCommand):
    def ns(self):
        return self.get_cython_function().locals
        
    def invoke(self, name, from_tty):
        try:
            ns = self.ns()
        except RuntimeError, e:
            print e.args[0]
            return
        
        if ns is None:
            print ('Information of Cython locals could not be obtained. '
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


cy.locals = CyLocals('cy locals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
cy.globals = CyGlobals('cy globals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
