# mode: compile

cdef int spam() except -1:
    eggs = 42

spam()
