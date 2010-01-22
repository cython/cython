#
#  Cython - Compilation-wide options and pragma declarations
#

cache_builtins = 1  #  Perform lookups on builtin names only once

embed_pos_in_docstring = 0
gcc_branch_hints = 1

pre_import = None
docstrings = True

# Decref global variables in this module on exit for garbage collection. 
# 0: None, 1+: interned objects, 2+: cdef globals, 3+: types objects
# Mostly for reducing noise for Valgrind, only executes at process exit
# (when all memory will be reclaimed anyways). 
generate_cleanup_code = 0

annotate = 0

# This will convert statements of the form "for i in range(...)" 
# to "for i from ..." when i is a cdef'd integer type, and the direction
# (i.e. sign of step) can be determined. 
# WARNING: This may change the symantics if the range causes assignment to 
# i to overflow. Specifically, if this option is set, an error will be
# raised before the loop is entered, wheras without this option the loop
# will execute util a overflowing value is encountered. 
convert_range = 1

# Enable this to allow one to write your_module.foo = ... to overwrite the 
# definition if the cpdef function foo, at the cost of an extra dictionary 
# lookup on every call. 
# If this is 0 it simply creates a wrapper. 
lookup_module_cpdef = 0

# This will set local variables to None rather than NULL which may cause 
# surpress what would be an UnboundLocalError in pure Python but eliminates 
# checking for NULL on every use, and can decref rather than xdecref at the end. 
# WARNING: This is a work in progress, may currently segfault.
init_local_none = 1

# Append the c file and line number to the traceback for exceptions. 
c_line_in_traceback = 1

# Whether or not to embed the Python interpreter, for use in making a 
# standalone executable. This will provide a main() method which simply 
# executes the body of this module. 
embed = False


# Declare compiler directives
directive_defaults = {
    'boundscheck' : True,
    'nonecheck' : False,
    'embedsignature' : False,
    'locals' : {},
    'auto_cpdef': False,
    'cdivision': False, # was True before 0.12
    'cdivision_warnings': False,
    'always_allow_keywords': False,
    'wraparound' : True,
    'ccomplex' : False, # use C99/C++ for complex types and arith
    'callspec' : "",
    'profile': False,
    'infer_types': False,
    'infer_types.verbose': False,
    'autotestdict': True,
    
    'warn': None,
    'warn.undeclared': False,

# test support
    'test_assert_path_exists' : [],
    'test_fail_if_path_exists' : [],
}

# Override types possibilities above, if needed
directive_types = {
    'infer_types' : bool, # values can be True/None/False
    }

for key, val in directive_defaults.items():
    if key not in directive_types:
        directive_types[key] = type(val)

directive_scopes = { # defaults to available everywhere
    # 'module', 'function', 'class', 'with statement'
    'autotestdict' : ('module',),
    'test_assert_path_exists' : ('function',),
    'test_fail_if_path_exists' : ('function',),
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
    ValueError: boundscheck directive must be set to True or False
    
    """
    type = directive_types.get(name)
    if not type: return None
    if type is bool:
        value = str(value)
        if value == 'True': return True
        if value == 'False': return False
        if relaxed_bool:
            value = value.lower()
            if value in ("true", "yes"): return True
            elif value in ("false", "no"): return False
        raise ValueError("%s directive must be set to True or False" % name)
    elif type is int:
        try:
            return int(value)
        except ValueError:
            raise ValueError("%s directive must be set to an integer" % name)
    elif type is str:
        return str(value)
    else:
        assert False

def parse_directive_list(s, relaxed_bool=False, ignore_unknown=False):
    """
    Parses a comma-seperated list of pragma options. Whitespace
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
    ValueError: boundscheck directive must be set to True or False
    >>> parse_directive_list('unknown=True')
    Traceback (most recent call last):
       ...
    ValueError: Unknown option: "unknown"
    """
    result = {}
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
