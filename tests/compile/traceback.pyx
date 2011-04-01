# mode: compile

def spam():
    raise Exception

cdef int grail() except -1:
    raise Exception

def tomato():
    spam()
    grail()
