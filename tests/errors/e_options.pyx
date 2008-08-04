
#cython: nonexistant
#cython: some=9

# The one below should NOT raise an error

#cython: boundscheck=True

# However this one should
#cython: boundscheck=sadf

print 3

#cython: boundscheck=True

_ERRORS = u"""
2:0: Expected "=" in option "nonexistant"
3:0: Unknown option: "some"
10:0: Must pass a boolean value for option "boundscheck"
14:0: #cython option comments only allowed at beginning of file
"""

