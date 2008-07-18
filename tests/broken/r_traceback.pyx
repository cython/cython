cdef int spam() except -1:
    raise Exception("Spam error")

cdef int grail() except -1:
    spam()

def tomato():
    grail()

