# mode: error

cdef enum class Spam:
    a

cdef enum class Spam:
    b

_ERRORS="""
6:5: 'Spam' redeclared
3:5: Previous declaration is here
"""
