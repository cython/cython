# mode: compile

cdef extern (int *[42]) spam, grail, swallow

cdef (int (*)()) brian():
    return NULL

brian()
