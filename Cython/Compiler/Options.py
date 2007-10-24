#
#  Pyrex - Compilation-wide options
#

intern_names = 1    #  Intern global variable and attribute names
cache_builtins = 1  #  Perform lookups on builtin names only once

embed_pos_in_docstring = 0
gcc_branch_hints = 1

pre_import = None

# This is a SAGE-specific option that will 
# cause Cython to incref local variables before
# performing a binary operation on them, for 
# safe detection of inplace operators. 
incref_local_binop = 0

