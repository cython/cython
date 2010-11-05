#no doctest
print "Warning: Using prototype cython.inline code..."

import tempfile
import sys, os, re, inspect

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

_code_cache = {}


class AllSymbols(CythonTransform, SkipDeclarations):
    def __init__(self):
        CythonTransform.__init__(self, None)
        self.names = set()
    def visit_NameNode(self, node):
        self.names.add(node.name)

def unbound_symbols(code, context=None):
    if context is None:
        context = Context([], default_options)
    from Cython.Compiler.ParseTreeTransforms import AnalyseDeclarationsTransform
    if isinstance(code, str):
        code = code.decode('ascii')
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
    import __builtin__
    for name in symbol_collector.names:
        if not tree.scope.lookup(name) and not hasattr(__builtin__, name):
            unbound.append(name)
    return unbound
        

def get_type(arg, context=None):
    py_type = type(arg)
    if py_type in [list, tuple, dict, str]:
        return py_type.__name__
    elif py_type is float:
        return 'double'
    elif py_type is bool:
        return 'bint'
    elif py_type is int:
        return 'long'
    elif 'numpy' in sys.modules and isinstance(arg, sys.modules['numpy'].ndarray):
        return 'numpy.ndarray[numpy.%s_t, ndim=%s]' % (arg.dtype.name, arg.ndim)
    else:
        for base_type in py_type.mro():
            if base_type.__module__ == '__builtin__':
                return 'object'
            module = context.find_module(base_type.__module__, need_pxd=False)
            if module:
                entry = module.lookup(base_type.__name__)
                if entry.is_type:
                    return '%s.%s' % (base_type.__module__, base_type.__name__)
        return 'object'

# TODO: use locals/globals for unbound variables
def cython_inline(code, 
                  types='aggressive',
                  lib_dir=os.path.expanduser('~/.cython/inline'),
                  include_dirs=['.'],
                  locals=None,
                  globals=None,
                  **kwds):
    code, literals = strip_string_literals(code)
    code = strip_common_indent(code)
    ctx = Context(include_dirs, default_options)
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
                print "Couldn't find ", symbol
    except AssertionError:
        # Parsing from strings not fully supported (e.g. cimports).
        print "Could not parse code as a string (to extract unbound symbols)."
    arg_names = kwds.keys()
    arg_names.sort()
    arg_sigs = tuple([(get_type(kwds[arg], ctx), arg) for arg in arg_names])
    key = code, arg_sigs
    module_name = _code_cache.get(key)
    if module_name is None:
        module_name = "_cython_inline_" + hashlib.md5(code + str(arg_sigs) + Cython.__version__).hexdigest()
    try:
        if lib_dir not in sys.path:
            sys.path.append(lib_dir)
        __import__(module_name)
    except ImportError:
        cimports = []
        qualified = re.compile(r'([.\w]+)[.]')
        for type, _ in arg_sigs:
            m = qualified.match(type)
            if m:
                cimports.append('\ncimport %s' % m.groups()[0])
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
        pyx_file = os.path.join(tempfile.mkdtemp(), module_name + '.pyx')
        open(pyx_file, 'w').write(module_code)
        extension = Extension(
            name = module_name,
            sources = [pyx_file],
            pyrex_include_dirs = include_dirs)
        build_extension = build_ext(Distribution())
        build_extension.finalize_options()
        build_extension.extensions = cythonize([extension])
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
    # TODO: string literals, backslash
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
