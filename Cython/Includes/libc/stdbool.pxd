# stdbool.h added in C99.
# From C23 the type is part of the language and it's no longer required
# to include the header, but it's probably still the best way to expose it.
cdef extern from "<stdbool.h>":
    ctypedef bint bool
