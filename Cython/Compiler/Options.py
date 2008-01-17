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
convert_range = 0
