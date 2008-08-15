
# nonexistant = True
# boundscheck = true
# boundscheck = 9

print 3

# Options should not be interpreted any longer:
# boundscheck = true

_ERRORS = u"""
3:0: boundscheck directive must be set to True or False
4:0: boundscheck directive must be set to True or False
"""

