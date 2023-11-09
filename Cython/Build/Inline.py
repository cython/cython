from __future__ import absolute_import

import hashlib
import inspect
import os
import re
import sys

from distutils.core import Distribution, Extension
from distutils.command.build_ext import build_ext

import Cython
from ..Compiler.Main import Context
from ..Compiler.Options import (default_options, CompilationOptions,
    get_directive_defaults)

from ..Compiler.Visitor import CythonTransform, EnvTransform
from ..Compiler.ParseTreeTransforms import SkipDeclarations
from ..Compiler.TreeFragment import parse_from_strings
from ..Compiler.StringEncoding import _unicode
from .Dependencies import strip_string_literals, cythonize, cached_function
from ..Compiler import Pipeline
from ..Utils import get_cython_cache_dir
import cython as cython_module


IS_PY3 = sys.version_info >= (3,)

# A utility function to convert user-supplied ASCII strings to unicode.
if not IS_PY3:
    def to_unicode(s):
        if isinstance(s, bytes):
            return s.decode('ascii')
        else:
            return s
else:
    to_unicode = lambda x: x


if sys.version_info < (3, 5):
    import imp
    def load_dynamic(name, module_path):
        return imp.load_dynamic(name, module_path)
else:
    import importlib.util
    from importlib.machinery import ExtensionFileLoader

    def load_dynamic(name, path):
        spec = importlib.util.spec_from_file_location(name, loader=ExtensionFileLoader(name, path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class UnboundSymbols(EnvTransform, SkipDeclarations):
    def __init__(self):
        super(EnvTransform, self).__init__(context=None)
        self.unbound = set()
    def visit_NameNode(self, node):
        if not self.current_env().lookup(node.name):
            self.unbound.add(node.name)
        return node
    def __call__(self, node):
        super(UnboundSymbols, self).__call__(node)
        return self.unbound


@cached_function
def unbound_symbols(code, context=None):
    code = to_unicode(code)
    if context is None:
        context = Context([], get_directive_defaults(),
                          options=CompilationOptions(default_options))
    from ..Compiler.ParseTreeTransforms import AnalyseDeclarationsTransform
    tree = parse_from_strings('(tree fragment)', code)
    for phase in Pipeline.create_pipeline(context, 'pyx'):
        if phase is None:
            continue
        tree = phase(tree)
        if isinstance(phase, AnalyseDeclarationsTransform):
            break
    try:
        import builtins
    except ImportError:
        import __builtin__ as builtins
    return tuple(UnboundSymbols()(tree) - set(dir(builtins)))


def unsafe_type(arg, context=None):
    py_type = type(arg)
    if py_type is int:
        return 'long'
    else:
        return safe_type(arg, context)


def safe_type(arg, context=None):
    py_type = type(arg)
    if py_type in (list, tuple, dict, str):
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
        for base_type in py_type.__mro__:
            if base_type.__module__ in ('__builtin__', 'builtins'):
                return 'object'
            module = context.find_module(base_type.__module__, need_pxd=False)
            if module:
                entry = module.lookup(base_type.__name__)
                if entry.is_type:
                    return '%s.%s' % (base_type.__module__, base_type.__name__)
        return 'object'


def _get_build_extension():
    dist = Distribution()
    # Ensure the build respects distutils configuration by parsing
    # the configuration files
    config_files = dist.find_config_files()
    dist.parse_config_files(config_files)
    build_extension = build_ext(dist)
    build_extension.finalize_options()
    return build_extension


@cached_function
def _create_context(cython_include_dirs):
    return Context(
        list(cython_include_dirs),
        get_directive_defaults(),
        options=CompilationOptions(default_options)
    )


_cython_inline_cache = {}
_cython_inline_default_context = _create_context(('.',))


def _populate_unbound(kwds, unbound_symbols, locals=None, globals=None):
    for symbol in unbound_symbols:
        if symbol not in kwds:
            if locals is None or globals is None:
                calling_frame = inspect.currentframe().f_back.f_back.f_back
                if locals is None:
                    locals = calling_frame.f_locals
                if globals is None:
                    globals = calling_frame.f_globals
            if symbol in locals:
                kwds[symbol] = locals[symbol]
            elif symbol in globals:
                kwds[symbol] = globals[symbol]
            else:
                print("Couldn't find %r" % symbol)


def _inline_key(orig_code, arg_sigs, language_level):
    key = orig_code, arg_sigs, sys.version_info, sys.executable, language_level, Cython.__version__
    return hashlib.sha1(_unicode(key).encode('utf-8')).hexdigest()


def cython_inline(code, get_type=unsafe_type,
                  lib_dir=os.path.join(get_cython_cache_dir(), 'inline'),
                  cython_include_dirs=None, cython_compiler_directives=None,
                  force=False, quiet=False, locals=None, globals=None, language_level=None, **kwds):

    if get_type is None:
        get_type = lambda x: 'object'
    ctx = _create_context(tuple(cython_include_dirs)) if cython_include_dirs else _cython_inline_default_context

    cython_compiler_directives = dict(cython_compiler_directives) if cython_compiler_directives else {}
    if language_level is None and 'language_level' not in cython_compiler_directives:
        language_level = '3'
    if language_level is not None:
        cython_compiler_directives['language_level'] = language_level

    key_hash = None

    # Fast path if this has been called in this session.
    _unbound_symbols = _cython_inline_cache.get(code)
    if _unbound_symbols is not None:
        _populate_unbound(kwds, _unbound_symbols, locals, globals)
        args = sorted(kwds.items())
        arg_sigs = tuple([(get_type(value, ctx), arg) for arg, value in args])
        key_hash = _inline_key(code, arg_sigs, language_level)
        invoke = _cython_inline_cache.get((code, arg_sigs, key_hash))
        if invoke is not None:
            arg_list = [arg[1] for arg in args]
            return invoke(*arg_list)

    orig_code = code
    code = to_unicode(code)
    code, literals = strip_string_literals(code)
    code = strip_common_indent(code)
    if locals is None:
        locals = inspect.currentframe().f_back.f_back.f_locals
    if globals is None:
        globals = inspect.currentframe().f_back.f_back.f_globals
    try:
        _cython_inline_cache[orig_code] = _unbound_symbols = unbound_symbols(code)
        _populate_unbound(kwds, _unbound_symbols, locals, globals)
    except AssertionError:
        if not quiet:
            # Parsing from strings not fully supported (e.g. cimports).
            print("Could not parse code as a string (to extract unbound symbols).")

    cimports = []
    for name, arg in list(kwds.items()):
        if arg is cython_module:
            cimports.append('\ncimport cython as %s' % name)
            del kwds[name]
    arg_names = sorted(kwds)
    arg_sigs = tuple([(get_type(kwds[arg], ctx), arg) for arg in arg_names])
    if key_hash is None:
        key_hash = _inline_key(orig_code, arg_sigs, language_level)
    module_name = "_cython_inline_" + key_hash

    if module_name in sys.modules:
        module = sys.modules[module_name]

    else:
        build_extension = None
        if cython_inline.so_ext is None:
            # Figure out and cache current extension suffix
            build_extension = _get_build_extension()
            cython_inline.so_ext = build_extension.get_ext_filename('')

        lib_dir = os.path.abspath(lib_dir)
        module_path = os.path.join(lib_dir, module_name + cython_inline.so_ext)

        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        if force or not os.path.isfile(module_path):
            cflags = []
            define_macros = []
            c_include_dirs = []
            qualified = re.compile(r'([.\w]+)[.]')
            for type, _ in arg_sigs:
                m = qualified.match(type)
                if m:
                    cimports.append('\ncimport %s' % m.groups()[0])
                    # one special case
                    if m.groups()[0] == 'numpy':
                        import numpy
                        c_include_dirs.append(numpy.get_include())
                        define_macros.append(("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"))
                        # cflags.append('-Wno-unused')
            module_body, func_body = extract_func_code(code)
            params = ', '.join(['%s %s' % a for a in arg_sigs])
            module_code = """
%(module_body)s
%(cimports)s
def __invoke(%(params)s):
%(func_body)s
    return locals()
            """ % {'cimports': '\n'.join(cimports),
                   'module_body': module_body,
                   'params': params,
                   'func_body': func_body }
            for key, value in literals.items():
                module_code = module_code.replace(key, value)
            pyx_file = os.path.join(lib_dir, module_name + '.pyx')
            fh = open(pyx_file, 'w')
            try:
                fh.write(module_code)
            finally:
                fh.close()
            extension = Extension(
                name=module_name,
                sources=[pyx_file],
                include_dirs=c_include_dirs or None,
                extra_compile_args=cflags or None,
                define_macros=define_macros or None,
            )
            if build_extension is None:
                build_extension = _get_build_extension()
            build_extension.extensions = cythonize(
                [extension],
                include_path=cython_include_dirs or ['.'],
                compiler_directives=cython_compiler_directives,
                quiet=quiet)
            build_extension.build_temp = os.path.dirname(pyx_file)
            build_extension.build_lib  = lib_dir
            build_extension.run()

        if sys.platform == 'win32' and sys.version_info >= (3, 8):
            with os.add_dll_directory(os.path.abspath(lib_dir)):
                module = load_dynamic(module_name, module_path)
        else:
            module = load_dynamic(module_name, module_path)

    _cython_inline_cache[orig_code, arg_sigs, key_hash] = module.__invoke
    arg_list = [kwds[arg] for arg in arg_names]
    return module.__invoke(*arg_list)


# Cached suffix used by cython_inline above.  None should get
# overridden with actual value upon the first cython_inline invocation
cython_inline.so_ext = None

_find_non_space = re.compile('[^ ]').search


def strip_common_indent(code):
    min_indent = None
    lines = code.splitlines()
    for line in lines:
        match = _find_non_space(line)
        if not match:
            continue  # blank
        indent = match.start()
        if line[indent] == '#':
            continue  # comment
        if min_indent is None or min_indent > indent:
            min_indent = indent
    for ix, line in enumerate(lines):
        match = _find_non_space(line)
        if not match or not line or line[indent:indent+1] == '#':
            continue
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
        all = inspect.getcallargs(self._f, *args, **kwds)
        if IS_PY3:
            return cython_inline(self._body, locals=self._f.__globals__, globals=self._f.__globals__, **all)
        else:
            return cython_inline(self._body, locals=self._f.func_globals, globals=self._f.func_globals, **all)
