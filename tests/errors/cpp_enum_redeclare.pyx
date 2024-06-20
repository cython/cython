# mode: error
# tag: cpp

cdef enum class Spam:
    a

cdef enum class Spam:
    b

_ERRORS="""
7:5: 'Spam' redeclared
4:5: Previous declaration is here
"""
