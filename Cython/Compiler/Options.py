#
#  Pyrex - Compilation-wide options
#

intern_names = 1    #  Intern global variable and attribute names
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
