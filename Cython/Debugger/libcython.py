"""
GDB extension that adds Cython support.
"""

import sys
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

def dont_suppress_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            raise
    
    return wrapper

class CythonModule(object):
    def __init__(self, module_name, filename):
        self.name = module_name
        self.filename = filename
        self.functions = {}
        self.globals = {}

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
        super(CythonFunction, self).__init__(name, cname, qualified_name, type)
        self.module = module
        self.pf_cname = pf_cname
        self.lineno = lineno
        self.locals = {}
        self.arguments = []


class CythonCommand(gdb.Command):
    """
    Invoke a Cython command. Available commands are:
        
        cy import
        cy break
        cy condition
        cy step
        cy enable
        cy disable
        cy print
        cy list
        cy locals
        cy globals
        cy tb
        cy cname
    """

CythonCommand('cy', gdb.COMMAND_NONE, gdb.COMPLETE_COMMAND, prefix=True)


class CyImport(gdb.Command):
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
                    
                    cython_function.arguments.extend(
                        funcarg.tag for funcarg in function.find('Arguments'))
        
CyImport('cy import', gdb.COMMAND_STATUS, gdb.COMPLETE_FILENAME)


class CyBreak(gdb.Command):
    """
    Set a breakpoint for Cython code using Cython qualified name notation, e.g.:
        
        cy-break cython_modulename.ClassName.method_name...
    
    or normal notation:
        
        cy-break function_or_method_name...
    """
    
    def invoke(self, function_names, from_tty):
        for funcname in string_to_argv(function_names.encode('UTF-8')):
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
    
    @dont_suppress_errors
    def complete(self, text, word):
        names = itertools.chain(functions_by_qualified_name, functions_by_name)
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

CyBreak('cy break', gdb.COMMAND_BREAKPOINTS)

# This needs GDB 7.2 or the Archer branch
# class CompleteUnqualifiedFunctionNames(gdb.Parameter):
    # """
    # Indicates whether 'cy break' should complete unqualified function or 
    # method names. e.g. whether only 'modulename.functioname' should be
    # completed, or also just 'functionname'
    # """
# 
# cy_complete_unqualified = CompleteUnqualifiedFunctionNames(
    # 'cy_complete_unqualified', 
    # gdb.COMMAND_BREAKPOINTS, 
    # gdb.PARAM_BOOLEAN)


class NoCythonFunctionNameInFrameError(Exception):
    """
    raised when the name of the C function could not be determined 
    in the current C stack frame
    """

class CyPrint(gdb.Command):
    """
    Print a Cython variable using 'cy-print x' or 'cy-print module.function.x'
    """
    def _get_current_cython_function(self):
        func_name = gdb.selected_frame().name()
        if func_name is None:
            raise NoCythonFunctionNameInFrameError()
        
        return functions_by_cname.get(func_name)
    
    def _get_locals_globals(self):
        try:
            cython_function = self._get_current_cython_function()
        except NoCythonFunctionNameInFrameError:
            return (None, None)
        else:
            if cython_function is None:
                return (None, None)
                
            return cython_function.locals, cython_function.module.globals
    
    def invoke(self, name, from_tty):
        try:
            cython_function = self._get_current_cython_function()
        except NoCythonFunctionNameInFrameError:
            print('Unable to determine the name of the function in the '
                  'current frame.')
        except RuntimeError, e:
            print e.args[0]
        else:
            # a cython_function of None means we don't know about such a Cython
            # function and we fall back to GDB's print
            cname = name
            if cython_function is not None:
                if name in cython_function.locals:
                    cname = cython_function.locals[name].cname
                elif name in cython_function.module.globals:
                    cname = cython_function.module.globals[name].cname
            
            gdb.execute('print ' + cname)
    
    def complete(self):
        locals_, globals_ = self._get_locals_globals()
        if locals_ is None:
            return []
        return list(itertools.chain(locals_, globals_))
    
CyPrint('cy print', gdb.COMMAND_DATA)

class CyLocals(CyPrint):
    def ns(self):
        locals_, _ = self._get_locals_globals()
        return locals_
        
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
                result = CObject
                
            print '%s = %s' % (var.name, result)

class CyGlobals(CyLocals):
    def ns(self):
        _, globals_ = self._get_locals_globals()
        return globals_
    
    def invoke(self, name, from_tty):
        m = gdb.parse_and_eval('PyModule_GetDict(__pyx_m)')
        m = m.cast(gdb.lookup_type('PyModuleObject').pointer())
        print PyObjectPtrPrinter(libpython.PyObjectPtr.from_pyobject_ptr(m['md_dict'])).to_string()

CyLocals('cy locals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
CyGlobals('cy globals', gdb.COMMAND_STACK, gdb.COMPLETE_NONE)
