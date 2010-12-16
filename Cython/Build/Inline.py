import tempfile
import sys, os, re, inspect
from cython import set

try:
    import hashlib
except ImportError:
    import md5 as hashlib

from distutils.core import Distribution, Extension
from distutils.command.build_ext import build_ext

import Cython
from Cython.Compiler.Main import Context, CompilationOptions, default_options

from Cython.Compiler.ParseTreeTransforms import CythonTransform, SkipDeclarations, AnalyseDeclarationsTransform
from Cython.Compiler.TreeFragment import parse_from_strings
from Cython.Build.Dependencies import strip_string_literals, cythonize

# A utility function to convert user-supplied ASCII strings to unicode.
if sys.version_info[0] < 3:
    def to_unicode(s):
        if not isinstance(s, unicode):
            return s.decode('ascii')
        else:
            return s
else:
    to_unicode = lambda x: x

_code_cache = {}


class AllSymbols(CythonTransform, SkipDeclarations):
    def __init__(self):
        CythonTransform.__init__(self, None)
        self.names = set()
    def visit_NameNode(self, node):
        self.names.add(node.name)

def unbound_symbols(code, context=None):
    code = to_unicode(code)
    if context is None:
        context = Context([], default_options)
    from Cython.Compiler.ParseTreeTransforms import AnalyseDeclarationsTransform
    tree = parse_from_strings('(tree fragment)', code)
    for phase in context.create_pipeline(pxd=False):
        if phase is None:
            continue
        tree = phase(tree)
        if isinstance(phase, AnalyseDeclarationsTransform):
            break
    symbol_collector = AllSymbols()
    symbol_collector(tree)
    unbound = []
    try:
        import builtins
    except ImportError:
        import __builtin__ as builtins
    for name in symbol_collector.names:
        if not tree.scope.lookup(name) and not hasattr(builtins, name):
            unbound.append(name)
    return unbound

def unsafe_type(arg, context=None):
    py_type = type(arg)
    if py_type is int:
        return 'long'
    else:
        return safe_type(arg, context)

def safe_type(arg, context=None):
    py_type = type(arg)
    if py_type in [list, tuple, dict, str]:
        return py_type.__name__
    elif py_type is complex:
        return 'double complex'
    elif py_type is float:
        return 'double'
    elif py_type is bool:
        return 'bint'
    elif 'numpy' in sys.modules and isinstance(arg, sys.modules['numpy'].ndarray):
        return 'numpy.ndarray[numpy.%s_t, ndim=%s]' % (arg.dtype.name, arg.ndim)
    else:
        for base_type in py_type.mro():
            if base_type.__module__ in ('__builtin__', 'builtins'):
                return 'object'
            module = context.find_module(base_type.__module__, need_pxd=False)
            if module:
                entry = module.lookup(base_type.__name__)
                if entry.is_type:
                    return '%s.%s' % (base_type.__module__, base_type.__name__)
        return 'object'

def cython_inline(code,
                  get_type=unsafe_type,
                  lib_dir=os.path.expanduser('~/.cython/inline'),
                  cython_include_dirs=['.'],
                  force=False,
                  quiet=False,
                  locals=None,
                  globals=None,
                  **kwds):
    if get_type is None:
        get_type = lambda x: 'object'
    code = to_unicode(code)
    code, literals = strip_string_literals(code)
    code = strip_common_indent(code)
    ctx = Context(cython_include_dirs, default_options)
    if locals is None:
        locals = inspect.currentframe().f_back.f_back.f_locals
    if globals is None:
        globals = inspect.currentframe().f_back.f_back.f_globals
    try:
        for symbol in unbound_symbols(code):
            if symbol in kwds:
                continue
            elif symbol in locals:
                kwds[symbol] = locals[symbol]
            elif symbol in globals:
                kwds[symbol] = globals[symbol]
            else:
                print("Couldn't find ", symbol)
    except AssertionError:
        if not quiet:
            # Parsing from strings not fully supported (e.g. cimports).
            print("Could not parse code as a string (to extract unbound symbols).")
    arg_names = kwds.keys()
    arg_names.sort()
    arg_sigs = tuple([(get_type(kwds[arg], ctx), arg) for arg in arg_names])
    key = code, arg_sigs, sys.version_info, sys.executable, Cython.__version__
    module_name = "_cython_inline_" + hashlib.md5(str(key).encode('utf-8')).hexdigest()
    try:
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        if lib_dir not in sys.path:
            sys.path.append(lib_dir)
        if force:
            raise ImportError
        else:
            __import__(module_name)
    except ImportError:
        cflags = []
        c_include_dirs = []
        cimports = []
        qualified = re.compile(r'([.\w]+)[.]')
        for type, _ in arg_sigs:
            m = qualified.match(type)
            if m:
                cimports.append('\ncimport %s' % m.groups()[0])
                # one special case
                if m.groups()[0] == 'numpy':
                    import numpy
                    c_include_dirs.append(numpy.get_include())
                    cflags.append('-Wno-unused')
        module_body, func_body = extract_func_code(code)
        params = ', '.join(['%s %s' % a for a in arg_sigs])
        module_code = """
%(module_body)s
%(cimports)s
def __invoke(%(params)s):
%(func_body)s
        """ % {'cimports': '\n'.join(cimports), 'module_body': module_body, 'params': params, 'func_body': func_body }
        for key, value in literals.items():
            module_code = module_code.replace(key, value)
        pyx_file = os.path.join(lib_dir, module_name + '.pyx')
        fh = open(pyx_file, 'w')
        try: 
            fh.write(module_code)
        finally:
            fh.close()
        extension = Extension(
            name = module_name,
            sources = [pyx_file],
            include_dirs = c_include_dirs,
            extra_compile_args = cflags)
        build_extension = build_ext(Distribution())
        build_extension.finalize_options()
        build_extension.extensions = cythonize([extension], ctx=ctx, quiet=quiet)
        build_extension.build_temp = os.path.dirname(pyx_file)
        build_extension.build_lib  = lib_dir
        build_extension.run()
        _code_cache[key] = module_name
    arg_list = [kwds[arg] for arg in arg_names]
    return __import__(module_name).__invoke(*arg_list)

non_space = re.compile('[^ ]')
def strip_common_indent(code):
    min_indent = None
    lines = code.split('\n')
    for line in lines:
        match = non_space.search(line)
        if not match:
            continue # blank
        indent = match.start()
        if line[indent] == '#':
            continue # comment
        elif min_indent is None or min_indent > indent:
            min_indent = indent
    for ix, line in enumerate(lines):
        match = non_space.search(line)
        if not match or line[indent] == '#':
            continue
        else:
            lines[ix] = line[min_indent:]
    return '\n'.join(lines)

module_statement = re.compile(r'^((cdef +(extern|class))|cimport|(from .+ cimport)|(from .+ import +[*]))')
def extract_func_code(code):
    module = []
    function = []
    current = function
    code = code.replace('\t', ' ')
    lines = code.split('\n')
    for line in lines:
        if not line.startswith(' '):
            if module_statement.match(line):
                current = module
            else:
                current = function
        current.append(line)
    return '\n'.join(module), '    ' + '\n    '.join(function)



try:
    from inspect import getcallargs
except ImportError:
    def getcallargs(func, *arg_values, **kwd_values):
        all = {}
        args, varargs, kwds, defaults = inspect.getargspec(func)
        if varargs is not None:
            all[varargs] = arg_values[len(args):]
        for name, value in zip(args, arg_values):
            all[name] = value
        for name, value in kwd_values.items():
            if name in args:
                if name in all:
                    raise TypeError, "Duplicate argument %s" % name
                all[name] = kwd_values.pop(name)
        if kwds is not None:
            all[kwds] = kwd_values
        elif kwd_values:
            raise TypeError, "Unexpected keyword arguments: %s" % kwd_values.keys()
        if defaults is None:
            defaults = ()
        first_default = len(args) - len(defaults)
        for ix, name in enumerate(args):
            if name not in all:
                if ix >= first_default:
                    all[name] = defaults[ix - first_default]
                else:
                    raise TypeError, "Missing argument: %s" % name
        return all

def get_body(source):
    ix = source.index(':')
    if source[:5] == 'lambda':
        return "return %s" % source[ix+1:]
    else:
        return source[ix+1:]

# Lots to be done here... It would be especially cool if compiled functions
# could invoke each other quickly.
class RuntimeCompiledFunction(object):

    def __init__(self, f):
        self._f = f
        self._body = get_body(inspect.getsource(f))

    def __call__(self, *args, **kwds):
        all = getcallargs(self._f, *args, **kwds)
        return cython_inline(self._body, locals=self._f.func_globals, globals=self._f.func_globals, **all)
