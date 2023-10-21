# mode: error

# cython: nonexistent = true
# cython: boundscheck = yes
# cython: boundscheck = 9

print 3

# Options should not be interpreted any longer:
# cython: boundscheck = yes

_ERRORS = u"""
4:0: boundscheck directive must be set to True or False, got 'yes'
5:0: boundscheck directive must be set to True or False, got '9'
"""
