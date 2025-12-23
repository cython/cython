# mode: error
# tag: cpp

cdef enum class Spam:
    a

cdef enum class Spam:
    b


_ERRORS="""
7:0: 'Spam' redeclared
4:0: Previous declaration is here
"""
