#
#  Cython - Compilation-wide options and pragma declarations
#

cache_builtins = 1  #  Perform lookups on builtin names only once

embed_pos_in_docstring = 0
gcc_branch_hints = 1

pre_import = None
docstrings = True

# This is a SAGE-specific option that will 
# cause Cython to incref local variables before
# performing a binary operation on them, for 
# safe detection of inplace operators. 
incref_local_binop = 0

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

# Optimize no argument and one argument methods by using the METH_O and METH_NOARGS
# calling conventions. These are faster calling conventions, but disallow the use of 
# keywords (which, admittedly, are of little use in these cases). 
optimize_simple_methods = 1

# Append the c file and line number to the traceback for exceptions. 
c_line_in_traceback = 1


# Declare pragmas
option_types = {
    'boundscheck' : bool,
    'nonecheck' : bool,
    'embedsignature' : bool,
    'locals' : dict,
}

option_defaults = {
    'boundscheck' : True,
    'nonecheck' : False,
    'embedsignature' : False,
    'locals' : {}
}

def parse_option_value(name, value):
    """
    Parses value as an option value for the given name and returns
    the interpreted value. None is returned if the option does not exist.    

    >>> print parse_option_value('nonexisting', 'asdf asdfd')
    None
    >>> parse_option_value('boundscheck', 'True')
    True
    >>> parse_option_value('boundscheck', 'true')
    Traceback (most recent call last):
       ...
    ValueError: boundscheck directive must be set to True or False
    
    """
    type = option_types.get(name)
    if not type: return None
    if type is bool:
        if value == "True": return True
        elif value == "False": return False
        else: raise ValueError("%s directive must be set to True or False" % name)
    else:
        assert False

def parse_option_list(s):
    """
    Parses a comma-seperated list of pragma options. Whitespace
    is not considered.

    >>> parse_option_list('      ')
    {}
    >>> (parse_option_list('boundscheck=True') ==
    ... {'boundscheck': True})
    True
    >>> parse_option_list('  asdf')
    Traceback (most recent call last):
       ...
    ValueError: Expected "=" in option "asdf"
    >>> parse_option_list('boundscheck=hey')
    Traceback (most recent call last):
       ...
    ValueError: Must pass a boolean value for option "boundscheck"
    >>> parse_option_list('unknown=True')
    Traceback (most recent call last):
       ...
    ValueError: Unknown option: "unknown"
    """
    result = {}
    for item in s.split(','):
        item = item.strip()
        if not item: continue
        if not '=' in item: raise ValueError('Expected "=" in option "%s"' % item)
        name, value = item.strip().split('=')
        try:
            type = option_types[name]
        except KeyError:
            raise ValueError('Unknown option: "%s"' % name)
        if type is bool:
            value = value.lower()
            if value in ('true', 'yes'):
                value = True
            elif value in ('false', 'no'):
                value = False
            else: raise ValueError('Must pass a boolean value for option "%s"' % name)
            result[name] = value
        else:
            assert False
    return result
