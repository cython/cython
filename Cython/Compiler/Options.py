#
#  Cython - Compilation-wide options and pragma declarations
#

# Perform lookups on builtin names only once, at module initialisation
# time.  This will prevent the module from getting imported if a
# builtin name that it uses cannot be found during initialisation.
cache_builtins = True

embed_pos_in_docstring = False
gcc_branch_hints = True

pre_import = None
docstrings = True

# Decref global variables in this module on exit for garbage collection.
# 0: None, 1+: interned objects, 2+: cdef globals, 3+: types objects
# Mostly for reducing noise for Valgrind, only executes at process exit
# (when all memory will be reclaimed anyways).
generate_cleanup_code = False

annotate = False

# This will abort the compilation on the first error occured rather than trying
# to keep going and printing further error messages.
fast_fail = False

# Make all warnings into errors.
warning_errors = False

# Make unknown names an error.  Python raises a NameError when
# encountering unknown names at runtime, whereas this option makes
# them a compile time error.  If you want full Python compatibility,
# you should disable this option and also 'cache_builtins'.
error_on_unknown_names = True

# This will convert statements of the form "for i in range(...)"
# to "for i from ..." when i is a cdef'd integer type, and the direction
# (i.e. sign of step) can be determined.
# WARNING: This may change the semantics if the range causes assignment to
# i to overflow. Specifically, if this option is set, an error will be
# raised before the loop is entered, wheras without this option the loop
# will execute until an overflowing value is encountered.
convert_range = True

# Enable this to allow one to write your_module.foo = ... to overwrite the
# definition if the cpdef function foo, at the cost of an extra dictionary
# lookup on every call.
# If this is 0 it simply creates a wrapper.
lookup_module_cpdef = False

# Whether or not to embed the Python interpreter, for use in making a
# standalone executable or calling from external libraries.
# This will provide a method which initalizes the interpreter and
# executes the body of this module.
embed = None

# Disables function redefinition, allowing all functions to be declared at
# module creation time. For legacy code only, needed for some circular imports.
disable_function_redefinition = False

# In previous iterations of Cython, globals() gave the first non-Cython module
# globals in the call stack.  Sage relies on this behavior for variable injection.
old_style_globals = False

# Allows cimporting from a pyx file without a pxd file.
cimport_from_pyx = False


# max # of dims for buffers -- set lower than number of dimensions in numpy, as
# slices are passed by value and involve a lot of copying
buffer_max_dims = 8

# Declare compiler directives
directive_defaults = {
    'boundscheck' : True,
    'nonecheck' : False,
    'initializedcheck' : True,
    'embedsignature' : False,
    'locals' : {},
    'auto_cpdef': False,
    'cdivision': False, # was True before 0.12
    'cdivision_warnings': False,
    'always_allow_keywords': False,
    'allow_none_for_extension_args': True,
    'wraparound' : True,
    'ccomplex' : False, # use C99/C++ for complex types and arith
    'callspec' : "",
    'final' : False,
    'internal' : False,
    'profile': False,
    'infer_types': None,
    'infer_types.verbose': False,
    'autotestdict': True,
    'autotestdict.cdef': False,
    'autotestdict.all': False,
    'language_level': 2,
    'fast_getattr': False, # Undocumented until we come up with a better way to handle this everywhere.
    'py2_import': False, # For backward compatibility of Cython's source code in Py3 source mode

    'warn': None,
    'warn.undeclared': False,
    'warn.unreachable': True,
    'warn.maybe_uninitialized': False,
    'warn.unused': False,
    'warn.unused_arg': False,
    'warn.unused_result': False,

# optimizations
    'optimize.inline_defnode_calls': False,

# remove unreachable code
    'remove_unreachable': True,

# control flow debug directives
    'control_flow.dot_output': "", # Graphviz output filename
    'control_flow.dot_annotate_defs': False, # Annotate definitions

# test support
    'test_assert_path_exists' : [],
    'test_fail_if_path_exists' : [],

# experimental, subject to change
    'binding': False,
}

# Extra warning directives
extra_warnings = {
    'warn.maybe_uninitialized': True,
    'warn.unreachable': True,
    'warn.unused': True,
}

# Override types possibilities above, if needed
directive_types = {
    'final' : bool,  # final cdef classes and methods
    'internal' : bool,  # cdef class visibility in the module dict
    'infer_types' : bool, # values can be True/None/False
    'cfunc' : None, # decorators do not take directive value
    'ccall' : None,
    'cclass' : None,
    'returns' : type,
    }

for key, val in directive_defaults.items():
    if key not in directive_types:
        directive_types[key] = type(val)

directive_scopes = { # defaults to available everywhere
    # 'module', 'function', 'class', 'with statement'
    'final' : ('cclass', 'function'),
    'internal' : ('cclass',),
    'autotestdict' : ('module',),
    'autotestdict.all' : ('module',),
    'autotestdict.cdef' : ('module',),
    'test_assert_path_exists' : ('function', 'class', 'cclass'),
    'test_fail_if_path_exists' : ('function', 'class', 'cclass'),
}

def parse_directive_value(name, value, relaxed_bool=False):
    """
    Parses value as an option value for the given name and returns
    the interpreted value. None is returned if the option does not exist.

    >>> print parse_directive_value('nonexisting', 'asdf asdfd')
    None
    >>> parse_directive_value('boundscheck', 'True')
    True
    >>> parse_directive_value('boundscheck', 'true')
    Traceback (most recent call last):
       ...
    ValueError: boundscheck directive must be set to True or False, got 'true'

    """
    type = directive_types.get(name)
    if not type: return None
    orig_value = value
    if type is bool:
        value = str(value)
        if value == 'True': return True
        if value == 'False': return False
        if relaxed_bool:
            value = value.lower()
            if value in ("true", "yes"): return True
            elif value in ("false", "no"): return False
        raise ValueError("%s directive must be set to True or False, got '%s'" % (
            name, orig_value))
    elif type is int:
        try:
            return int(value)
        except ValueError:
            raise ValueError("%s directive must be set to an integer, got '%s'" % (
                name, orig_value))
    elif type is str:
        return str(value)
    else:
        assert False

def parse_directive_list(s, relaxed_bool=False, ignore_unknown=False,
                         current_settings=None):
    """
    Parses a comma-separated list of pragma options. Whitespace
    is not considered.

    >>> parse_directive_list('      ')
    {}
    >>> (parse_directive_list('boundscheck=True') ==
    ... {'boundscheck': True})
    True
    >>> parse_directive_list('  asdf')
    Traceback (most recent call last):
       ...
    ValueError: Expected "=" in option "asdf"
    >>> parse_directive_list('boundscheck=hey')
    Traceback (most recent call last):
       ...
    ValueError: boundscheck directive must be set to True or False, got 'hey'
    >>> parse_directive_list('unknown=True')
    Traceback (most recent call last):
       ...
    ValueError: Unknown option: "unknown"
    """
    if current_settings is None:
        result = {}
    else:
        result = current_settings
    for item in s.split(','):
        item = item.strip()
        if not item: continue
        if not '=' in item: raise ValueError('Expected "=" in option "%s"' % item)
        name, value = [ s.strip() for s in item.strip().split('=', 1) ]
        parsed_value = parse_directive_value(name, value, relaxed_bool=relaxed_bool)
        if parsed_value is None:
            if not ignore_unknown:
                raise ValueError('Unknown option: "%s"' % name)
        else:
            result[name] = parsed_value
    return result
