import tempfile
import sys, os, re

try:
    import hashlib
except ImportError:
    import md5 as hashlib

from distutils.dist import Distribution
from distutils.core import Extension
from Cython.Distutils import build_ext
    
code_cache = {}

def get_type(arg):
    py_type = type(arg)
    # TODO: numpy
    # TODO: extension types
    if py_type in [list, tuple, dict, str]:
        return py_type.__name__
    elif py_type is float:
        return 'double'
    elif py_type is int:
        return 'long'
    else:
        return 'object'

# TODO: use locals/globals for unbound variables
def cython_inline(code, types='aggressive', lib_dir=os.path.expanduser('~/.cython/inline'), **kwds):
    _, pyx_file = tempfile.mkstemp('.pyx')
    arg_names = kwds.keys()
    arg_names.sort()
    arg_sigs = tuple((get_type(kwds[arg]), arg) for arg in arg_names)
    key = code, arg_sigs
    module = code_cache.get(key)
    if not module:
        module_body, func_body = extract_func_code(code)
        params = ', '.join('%s %s' % a for a in arg_sigs)
        module_code = """
%(module_body)s
def __invoke(%(params)s):
%(func_body)s
        """ % locals()
        open(pyx_file, 'w').write(module_code)
        module = "_" + hashlib.md5(code + str(arg_sigs)).hexdigest()
        extension = Extension(
            name = module,
            sources=[pyx_file])
        build_extension = build_ext(Distribution())
        build_extension.finalize_options()
        build_extension.extensions = [extension]
        build_extension.build_temp = os.path.dirname(pyx_file)
        if lib_dir not in sys.path:
            sys.path.append(lib_dir)
        build_extension.build_lib  = lib_dir
        build_extension.run()
        code_cache[key] = module
    arg_list = [kwds[arg] for arg in arg_names]
    return __import__(module).__invoke(*arg_list)

non_space = re.compile('[^ ]')
def strip_common_indent(lines):
    min_indent = None
    for line in lines:
        if not line:
            continue # empty
        indent = non_space.search(line).start()
        if indent == len(line):
            continue # blank
        elif line[indent] == '#':
            continue # comment
        elif min_indent is None or min_indent > indent:
            min_indent = indent
    for line in lines:
        if not line:
            continue
        indent = non_space.search(line).start()
        if indent == len(line):
            continue
        elif line[indent] == '#':
            yield line
        else:
            yield line[min_indent:]

module_statement = re.compile(r'^((cdef +(extern|class))|cimport|(from .+ cimport)|(from .+ import +[*]))')
def extract_func_code(code):
    module = []
    function = []
    # TODO: string literals, backslash
    current = function
    code = code.replace('\t', ' ')
    lines = strip_common_indent(code.split('\n'))
    for line in lines:
        if not line.startswith(' '):
            if module_statement.match(line):
                current = module
            else:
                current = function
        current.append(line)
    return '\n'.join(module), '    ' + '\n    '.join(function)
