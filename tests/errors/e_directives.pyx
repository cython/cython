# mode: error

# cython: nonexistent = True
# cython: boundscheck = true
# cython: boundscheck = 9

print 3

# Options should not be interpreted any longer:
# cython: boundscheck = true

_ERRORS = u"""
4:0: boundscheck directive must be set to True or False, got 'true'
5:0: boundscheck directive must be set to True or False, got '9'
"""
